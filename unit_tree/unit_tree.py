"""
Build UnitTree out of abstract Tree
"""
from numbers import Number

from .base import UnitBase, NotPassed
from .tree import (Tree, Empty, Leaf, Node)
from .syntax import TreeArithmeticSyntax, TreeFunction


class UnitTree(Tree[Number], TreeArithmeticSyntax, UnitBase):
    def __new__(cls, value=NotPassed, left=NotPassed, right=NotPassed):
        if value is NotPassed:
            return object.__new__(UnitEmpty)
        elif left is NotPassed and right is NotPassed:
            return object.__new__(UnitLeaf)
        else:
            return object.__new__(UnitNode)

    @classmethod
    def __call__(cls, *args):
        if cls is UnitTree:
            self = UnitTree.__new__(cls, *args)
        else:
            self = object.__new__(cls)
        self.__init__(*args)
        return self

    @classmethod
    def construct(cls, domain: Number = NotPassed) -> 'UnitTree':
        """Construct a Tree element out of a Domain element"""
        # Handle an edge case - where domain is 'NotPassed', but
        # we need to prevent passing 'NotPassed' into Empty.__init__
        if domain is NotPassed:
            return UnitTree()
        else:
            return UnitTree(domain)


UnitTree.codomain = UnitTree
UnitTree.domain = object


class UnitNode(Node, UnitTree):
    pass


class UnitLeaf(Leaf, UnitTree):
    pass


class UnitEmpty(Empty, UnitTree):
    pass


class UnitTreeFunction(TreeFunction):
    pass
