"""
* Semi Hard Problem: replacing node, while maintaining child-ref in parent
    - Possibly some Traversable-related chicanary
    - Solve via: bfs/dfs iterator, and immutablity (~Traversable chicanery)

"""
import operator


class Operations:
    registry = []

operation_registry = {}


def register(klass):
    operator_registry[klass.scalar_function] = klass


@register
class Multiply:
    """
    operator_registry[operator.__mul__] = Multiply
    """
    short = "*"
    name = "multiply"
    operator = operator.__mul__

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


class NodeSyntaxFunctor:
    def __mul__(self, tree):
        pass

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

