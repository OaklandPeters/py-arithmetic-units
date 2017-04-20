import operator

from .base import OperatorLookupError
from .units import Unit, UnitsStem, DimensionNode, Scalar


class UnitsFunction:
    """Binary function to operate on a Unit tree.
    Each UnitStem has one function UnitsFunction contained in it.
    UnitsFunction is primary used structuring simplification steps.
    """


class UnitsFunctionStem(UnitsStem):
    """
    represents a function over the units
    You don't actually execute it

    Needs to pick up the simplification rules for multiplying and dividing
    """
    parent: UnitsStem
    units_function: UnitsFunction
    left: Unit
    right: Unit

    def __init__(self, parent: Union[Unit, None],
                 units_function: UnitsFunction, left: Unit, right: Unit):
        self.parent = parent
        self.units_function = units_function
        self.left = left
        self.right = right

    def __str__(self):
        return "({0} {1} {2})".format(
            self.left, self.units_function.short, self.right
        )

    def __repr__(self):
        return "{0}({1}, {2}, {3}, {4})".format(
            self.__class__.__name__, self.parent, self.units_function,
            self.left, self.right
        )


operator_registry = {}


def register(klass):
    operator_registry[klass.scalar_function] = klass


@register
class Multiply(UnitsFunction):
    """
    operator_registry[operator.__mul__] = Multiply
    """
    short = "*"
    name = "multiply"
    scalar_function = operator.__mul__

    @classmethod
    def dimension_function(cls, left, right):
        pass


@register
class Divide(UnitsFunction):
    short = "/"
    name = "divide"
    scalar_function = operator.__truediv__


@register
class Add(UnitsFunction):
    short = "+"
    name = "add"
    scalar_function = operator.__add__


@register
class Subtract(UnitsFunction):
    short = "-"
    name = "subtract"
    scalar_function = operator.__add__


class StemFunctor:
    def construct(self, units_function, left, right):
        parent = UnitsFunctionStem(None, Add, self, right)
        parent.left.parent = parent
        parent.right.parent = parent

    def apply(self, operator, left, right) -> UnitsStem:
        try:
            units_function = operator_registry[operator]
        except LookupError as exc:
            raise OperatorLookupError(
                "No UnitsFunction identifier for operator '{0}'".format(
                    operator
                )
            )
        return self.construct(units_function, left, right)


class UnitOperators(metaclass=UnitMeta):
    """Provides operator syntax for standard arithmetic
    (+, -, *, ^, etc).
    These operations return UnitsStem instances of the correct
    UnitsFunction.


    ... how do we get the value for parent?

    """
    # functor: InvariantFunctor[Domain, Codomain]

    def __add__(self: Unit, right: Unit) -> UnitsStem:
        return UnitsFunctionStem(None, Add, self, right)

    def __radd__(self: Unit, left: Unit) -> UnitStem:
        return UnitsFunctionStem(None, Add, left, self)

    def __sub__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Subtract, self, right)

    def __rsub__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Subtract, left, self)

    def __mul__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Multiply, self, right)

    def __rmul__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Multiply, left, self)

    def __truediv__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Divide, self, right)

    def __rtruediv__(self, a: EitherDomain) -> Codomain:
        return UnitsFunctionStem(None, Divide, left, self)

    # def __floordiv__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__floordiv__, self, a)

    # def __rfloordiv__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__floordiv__, a, self)

    # def __mod__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__mod__, self, a)

    # def __rmod__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__mod__, a, self)

    # def __pow__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__pow__, self, a)

    # def __rpow__(self, a: EitherDomain) -> Codomain:
    #     return self.functor.apply(operator.__pow__, a, self)


class DimensionalOperators:
    def __mul__(left: DimensionNode, right: DimensionNode) -> DimensionNode:
        return DimensionalFunctor.construct(
            left.dimension,
            left.value + right.value
        )
