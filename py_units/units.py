"""
Notes
* This is intended to handle the non-scalar value portions.
** Symbolic: (Value, Units)

@todo: Clean up .simplification for the two functions - they still reference .units
@todo: Add simplification for Scalar - which basically consists of actually doing math

@todo: UnitsStem - needs .unit property
* Problem: unit needs to be a distinct/unique representation - to compare
@todo: unittests
@todo: Move abstracts to their module
@todo: Merge role of 'exponent' into 'value' for standard UnitsLeaf
@todo: add specialized handling in constructor for dimension
* registration of units based on identifier - so if one already exists, it is returned
* return NullUnit when name/identifier is None
* handle the case of only one of name/identifier being None


Advanced - and unnecessary for now:
* operators on Dimension, that promotes it to a Leaf
"""
from typing import Union
from numbers import Number
import operator

from .dimension import Dimension, NullUnit
from .base import UnitsTypeError, UnitsType, UnitMeta
from .syntax import Functor, InvariantFunctor, ArithmeticSyntaxMixin


class Unit(UnitsType, metaclass=UnitMeta):
    """Base conrete type for all nodes of a unit-tree.
    All children must be one of:
        UnitsLeaf
        UnitsStem
    """
    @classmethod
    def __call__(cls, value: Union[str, Number]):
        return cls.simple_constructor(value)

    @classmethod
    def simple_constructor(cls, value: Union[str, Number]):
        if isinstance(value, Number):
            return Scalar(value)
        elif isinstance(value, str):
            return DimensionNode(Dimension(value, value))
        else:
            raise UnitsTypeError("Attempted to construct unit for: {0}".format(value))

    @classmethod
    def explicit_constructor(cls, dimension: Dimension, value: Number = 1, parent: Union['UnitsStem', None] = None):
        if (dimension is NullUnit):
            return Scalar(value, parent)
        else:
            return DimensionNode(dimension, value, parent)


class UnitsLeaf(Unit):
    """Base class for leaf-nodes
    Terminal unit: Unit = Dimension x Exponent
    """
    pass


class UnitsStem(Unit):
    """Base class for stem nodes."""
    pass


class DimensionNode(UnitsLeaf):
    """Leaf node representing a single unit, with an exponent.
    For example, both `feet` and `seconds^2` would be
    Compound units (such as `feet-)
    """

    @classmethod
    def __call__(cls, *args):
        self = object.__new__(cls)
        self.__init__(*args)
        return self

    def __init__(self, dimension: Dimension, value: Number = 1, parent: Union['UnitsStem', None] = None):
        self.dimension = dimension
        self.value = value
        self.parent = parent

    def __str__(self):
        if self.value == 1:
            return str(self.dimension)
        else:
            return "{0}^{1}".format(self.dimension, self.value)

    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(
            self.__class__.__name__, self.dimension, self.value, self.parent
        )

    # Mathematics syntax
    # def __add__(self, a):
    #   pass
    # def __mul__(self, a):
    #   pass
    # def __rmul__(self, a):
    #   pass


class NumberScalarInvariantFunctor(InvariantFunctor['Scalar', Number]):
    def construct(self, domain: Number) -> 'Scalar':
        return self.Codomain(domain)

    def destruct(self, codomain: 'Scalar') -> Number:
        return codomain.value


class Scalar(UnitsLeaf, ArithmeticSyntaxMixin['Scalar', Number]):
    """Leaf node representing a pure number with no units."""
    @property
    def functor(self) -> NumberScalarInvariantFunctor:
        """
        Provides a class-specific functor version based
        on the concrete class at run-time.
        """
        cls = self.__class__
        if not hasattr(self, '_functor'):
            self._functor = NumberScalarInvariantFunctor(Number, cls)
        return self._functor

    @classmethod
    def __call__(cls, *args):
        self = object.__new__(cls)
        self.__init__(*args)
        return self

    def __init__(self, value: Number, parent: Union['UnitsStem', None] = None):
        self.dimension = NullUnit
        self.value = value
        self.parent = parent

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.value, self.parent
        )

    def __eq__(self, other):
        if isinstance(other, Scalar):
            return self.value == other.value
        else:
            return False


class UnitsFunction:
    """Binary function to operate on the tree.
    Each UnitStem has one function contained in it.
    UnitsFunction is primary used structuring simplification steps.
    """



class Multiply(UnitsFunction):
    function = operator.__mul__
    short = "*"
    name = "multiply"

    @classmethod
    def simplify(cls, node):
        if node.left.unit == node.right.unit:

            return UnitsLeaf(node.left.units, node.left.exponent + node.right.exponents)
        return node






class Divide(UnitsFunction):
    function = operator.__truediv__
    short = "/"
    name = "divide"

    @classmethod
    def simplify(cls, node):
        if node.left.unit == node.right.unit:
            return UnitsLeaf(node.left.units, node.left.exponent - node.right.exponents).simplify()
        else:
            return node


class UnitsFunctionStem(UnitsStem):
    """
    represents a function over the units
    You don't actually execute it

    Needs to pick up the simplification rules for multiplying and dividing
    """

    def __init__(self, parent: Union[Unit, None],
                 astfunction: UnitsFunction, left: UnitsLeaf, right: UnitsLeaf):
        self.parent = parent
        self.astfunction = astfunction
        self.left = left
        self.right = right

    def __str__(self):
        "{0} {1} {2}".format(
            self.left, self.astfunction.short, self.right
        )

    def simplify(self):
        return self.astfunction.simplify(self)
