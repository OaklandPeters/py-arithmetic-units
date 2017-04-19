from .typing import Callable, Generic, TypeVar

from .base import UnitMeta, NotPassed, UnitsTypeError

A = TypeVar('A')
B = TypeVar('A')

class Tree(typing.Generic[A], metaclass=UnitMeta):
    """
    Binary abstract tree.
    """
    def __new__(cls, value=NotPassed, left=NotPassed, right=NotPassed):
        if value is NotPassed:
            return Empty()
        elif left is NotPassed and right is NotPassed:
            return Leaf(value)
        else:
            return Node(value, left, right)

    @classmethod
    def map(cls, f: Callable[[A], A], tree: Tree[A]):
        """Note - I dont like having map on the parent class Tree -
        because it require that class to know about the internals"""
        if isinstance(tree, Empty):
            return Empty
        elif isinstance(tree, Leaf):
            return Leaf(f(tree.value))
        elif isinstance(tree, Node):
            return Node(f(tree.value), cls.map(f, tree.left), cls.map(f, tree.right))
        else:
            UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    @classmethod
    def fold(cls, f: Callable[[A, B], B], accumulator: B, tree: Tree[A]):
        if isinstance(tree, Empty):
            return accumulator
        elif isinstance(tree, Leaf):
            return f(tree.value, accumulator)
        elif isinstance(tree, Node):
            return cls.fold(
                f,
                f(
                    tree.value,
                    cls.fold(f, accumulator, tree.right)
                ),
                tree.left
            )
        else:
            UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))



class Empty(Tree):
    def __init__(self):
        pass


class Leaf(Tree):
    def __init__(self, value):
        self.value = value


class Node(Tree):
    def __init__(self, value, left=NotPassed, right=NotPassed):
        if left is NotPassed:
            left = Empty()
        if right is NotPassed:
            right = Empty()
        self.value = value
        self.left = left
        self.right = right
