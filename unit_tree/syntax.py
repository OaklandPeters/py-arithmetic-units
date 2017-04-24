"""
* Semi Hard Problem: replacing node, while maintaining child-ref in parent
    - Possibly some Traversable-related chicanary
    - Solve via: bfs/dfs iterator, and immutablity (~Traversable chicanery)

"""
import operator
from typing import Generic, TypeVar, Union

from .unit_tree import UnitTree, UnitNode, UnitLeaf, UnitEmpty

EitherDomain = Union[Number, UnitTree[Number]]


class UnitTreeFunction:
    """
    Also a Arithmetic to UnitFunction Functor
    """
    registry = {}

    @classmethod
    def register(cls, unit_tree_function: UnitTreeFunction):
        cls.registry[operation.operator] = operation

    @classmethod
    def map(cls, pair, operation):
        # unpack arguments
        left, right = pair
        # Look up the operation
        if operation in UnitTreeFunction.registry:
            unit_tree_function = UnitTreeFunction.registry[operation]
        else:
            raise KeyError(str.format(
                "operation '{0}' is not a registered UnitTreeFunction operation",
                repr(operation)
            ))
        return UnitNode(unit_tree_function, left, right)


@UnitTreeFunction.register
class Multiply(UnitTreeFunction):
    """
    operator_registry[operator.__mul__] = Multiply
    """
    short = "*"
    name = "multiply"
    operator = operator.__mul__


@UnitTreeFunction.register
class Divide(UnitTreeFunction):
    short = "/"
    name = "divide"
    operator = operator.__truediv__


@UnitTreeFunction.register
class Add(UnitTreeFunction):
    short = "+"
    name = "add"
    operator = operator.__add__


@UnitTreeFunction.register
class Subtract(UnitTreeFunction):
    short = "-"
    name = "subtract"
    operator = operator.__add__







class UnitSyntax:
    def __add__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__add__, self, a)

    def __radd__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__add__, a, self)

    def __sub__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__sub__, self, a)

    def __rsub__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__sub__, a, self)

    def __mul__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mul__, self, a)

    def __rmul__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mul__, a, self)

    def __truediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__truediv__, self, a)

    def __rtruediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__truediv__, a, self)

    def __floordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__floordiv__, self, a)

    def __rfloordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__floordiv__, a, self)

    def __mod__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mod__, self, a)

    def __rmod__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mod__, a, self)

    def __pow__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__pow__, self, a)

    def __rpow__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__pow__, a, self)

#===================================================
#  Functor splat
#===================================================
# Lifting functions in several ways
#  The eventual syntax on Tree will involve all of these

# Aside: I don't have a mathematics term for functions of the form:
#   Term[A] : Callable[[A, A], A]
#
# ... sudden realization!
#   --> functions of the form ( (a,a)->a )
#   are not morphisms
#   but they *are* functors from BinaryNumber to UnaryNumber
#   Functor[Domain=Tuple[Number, Number], Codomain=Tuple[Number]]
#

def lift_arithmetic_to_tree_operator(_operator) -> :

