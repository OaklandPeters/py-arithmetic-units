"""
Build UnitTree out of abstract Tree
"""

from .base import UnitBase, NotPassed
from .tree import (Tree, Empty, Leaf, Node)


class UnitTree(Tree, UnitBase):
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


class UnitNode(Node, UnitTree):
    pass


class UnitLeaf(Leaf, UnitTree):
    pass


class UnitEmpty(Empty, UnitTree):
    pass
