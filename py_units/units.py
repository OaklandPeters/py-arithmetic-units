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
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Callable, Sequence, Tuple, Union, Optional
from numbers import Number
import operator
import itertools
import functools

from .dimension import Dimension, NullUnit

# __all__ = (
#     UnitsType,
#     UnitsNode,
#     UnitsLeaf,
#     Scalar,
#     UnitsFunction,
#     Multiply,
#     Divide,
#     UnitsStem
# )
__all__ = (
    'UnitsType',
    'UnitsNode',
    'UnitsLeaf',
    'Scalar',
    'UnitsFunction',
    'Multiply',
    'Divide',
    'UnitsStem',
    'UnitVector',
    'Unit'
)



class UnitsTypeError(TypeError):
    pass


class UnitsType:
    pass
    # def __new__(cls, value: Union[str, Number]):


def Unit(value: Union[str, Number]):
    if isinstance(value, Number):
        return Scalar(value)
    elif isinstance(value, str):
        return UnitVector(Dimension(value, value))
    else:
        raise UnitsTypeError("Attempted to construct unit for: {0}".format(value))



class UnitsNode(UnitsType):
    pass
    # units = property(lambda self: NotImplemented) # type: UnitsType
    # simplify = property(lambda self: NotImplemented) # type: Callable[[], UnitsNode]
    # short = property(lambda self: NotImplemented) # type: str
    # name = property(lambda self: NotImplemented) # type: str
    # parent = property(lambda self: NotImplemented) # type: Union[UnitsNode, None]


class UnitsLeaf(UnitsNode):
    """
    Terminal unit: Unit = Dimension x Exponent
    """
    def __new__(cls, dimension: Dimension, value: Number = 1, parent: Union['UnitsStem', None] = None):
        if dimension == NullUnit:
            return Scalar.__new__(Scalar, parent, value)
        else:
            return UnitVector.__new__(UnitVector, parent, dimension, value)

    def __init__(self, dimension: Dimension, value: Number = 1, parent: Union['UnitsStem', None] = None):
        self.dimension = dimension
        self.value = value
        self.parent = parent


class UnitVector(UnitsLeaf):

    def __new__(cls, dimension: Dimension, value: Number = 1, parent: Union['UnitsStem', None] = None):
        """Override __new__, so that dispatching in UnitsLeaf.__new__ correctly proxies
        to UnitVector.__new__
        """
        self = object.__new__(cls)
        self.__init__(dimension, value, parent)
        return self

    def __str__(self):
        if self.value == 1:
            return str(self.dimension)
        else:
            return "{0}^{1}".format(self.dimension, self.value)

    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(
            self.__class__.__name__, self.dimension, self.value, self.parent
        )


class Scalar(UnitsLeaf):
    """Might need to synthesize this with UnitLeaf"""

    def __new__(cls, value: Number, parent: Union['UnitsStem', None] = None):
        """Override __new__, so that dispatching in UnitsLeaf.__new__ correctly proxies
        to UnitVector.__new__
        """
        self = object.__new__(cls)
        self.__init__(NullUnit, value, parent)
        return self

    def simplify(self):
        # (1) Check if this can be merged with an adjacent scalar node
        if simplify.children_match(self.parent):
            simplify.merge_child_scalars(parent)


        # (2) Migrate Scalar to the leftmost position
        return self

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.value, self.parent
        )


class UnitsFunction(UnitsNode):
    """Binary function."""
    # units = property(lambda self: NotImplemented) # type: UnitsType
    # simplify = property(lambda self: NotImplemented) # type: Callable[[], UnitsNode]
    # short = property(lambda self: NotImplemented) # type: str
    # name = property(lambda self: NotImplemented) # type: str
    # function = property(lambda self: NotImplemented) # type: Callable[[UnitsNode, UnitsNode], UnitsNode]
    # left = property(lambda self: NotImplemented) # type: UnitsNode
    # right = property(lambda self: NotImplemented) # type: UnitsNode
    # parent = property(lambda self: NotImplemented) # type: Union[UnitsNode, None]

    def __init__(self, parent, left, right):
        self.parent = parent
        self.left = left
        self.right = right



class Multiply(UnitsFunction):
    function = operator.__mul__
    short = "*"
    name = "multiply"

    @classmethod
    def simplify(cls, node):
        if node.left.unit == node.right.unit:
            # Create new with unit of left, and add exponents
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


class UnitsStem(UnitsNode):
    """
    represents a function over the units
    You don't actually execute it

    Needs to pick up the simplification rules for multiplying and dividing
    """
    def __init__(self, parent: Union[UnitsNode, None], astfunction: UnitsFunction, left: UnitsLeaf, right: UnitsLeaf):
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






