"""
* Semi Hard Problem: replacing node, while maintaining child-ref in parent
    - Possibly some Traversable-related chicanary
    - Solve via: bfs/dfs iterator, and immutablity (~Traversable chicanery)

"""
import operator
from typing import Tuple

from .base import TreeMeta
from .tree import Node, Tree, EitherDomain


class TreeFunction(metaclass=TreeMeta):
    """
    Also a Arithmetic to UnitFunction Functor
    """
    registry = {}
    domain: Tuple[Tree, EitherDomain]
    codomain: Node

    @classmethod
    def register(cls, tree_function: 'TreeFunction'):
        cls.registry[tree_function.operator] = tree_function

    @classmethod
    def lift(cls, operation):
        if operation in TreeFunction.registry:
            return TreeFunction.registry[operation]
        else:
            raise KeyError(str.format(
                "operation '{0}' is not a registered TreeFunction operation",
                repr(operation)
            ))

    @classmethod
    def map(cls, pair, operation):
        return cls.apply(pair, cls.lift(operation))

    @classmethod
    def apply(cls, pair: 'Tuple[Tree, EitherDomain]', tree_function: 'TreeFunction') -> Node:
        # unpack arguments
        left, right = pair
        # Look up the operation
        return Node(tree_function, left, right)

    @classmethod
    def call(cls, tree_function, pair):
        return cls.apply(pair, tree_function)

    @classmethod
    def __call__(cls, left, right):
        return cls.apply((left, right), cls)

    # @classmethod
    # def __call__(cls, pair):
    #     return cls.apply(pair, self)



@TreeFunction.register
class Multiply(TreeFunction):
    """
    operator_registry[operator.__mul__] = Multiply
    """
    short = "*"
    name = "multiply"
    operator = operator.__mul__


@TreeFunction.register
class Divide(TreeFunction):
    short = "/"
    name = "divide"
    operator = operator.__truediv__


@TreeFunction.register
class Add(TreeFunction):
    short = "+"
    name = "add"
    operator = operator.__add__


@TreeFunction.register
class Subtract(TreeFunction):
    short = "-"
    name = "subtract"
    operator = operator.__add__


class TreeArithmeticSyntax:

    def __add__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__add__, (self, a))

    def __radd__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__add__, (a, self))

    def __sub__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__sub__, (self, a))

    def __rsub__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__sub__, (a, self))

    def __mul__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__mul__, (self, a))

    def __rmul__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__mul__, (a, self))

    def __truediv__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__truediv__, (self, a))

    def __rtruediv__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__truediv__, (a, self))

    def __floordiv__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__floordiv__, (self, a))

    def __rfloordiv__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__floordiv__, (a, self))

    def __mod__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__mod__, (self, a))

    def __rmod__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__mod__, (a, self))

    def __pow__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__pow__, (self, a))

    def __rpow__(self, a: EitherDomain) -> Node:
        return TreeFunction.map(operator.__pow__, (a, self))


# ===================================================
#  Functor splat
# ===================================================
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
