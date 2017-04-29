"""
Rewriting rules for the UnitTree


"""
from typing import Generic, TypeVar, Callable, Optional
from numbers import Number

from .tree import Tree, Node, Leaf
from .unit_tree import UnitTree, UnitTreeNode, UnitTreeFunction


# Temporary names... need better ones, but names are hard
LawIn = TypeVar('LawIn')
LawOut = TypeVar('LawOut')
TreeMorphism = Callable[[Tree], Tree]


class TreeLaw(AbstractTreeLaw):
    """
    This should probably be generic on something.
    Perhaps treated like Callable
    """
    predicate: Callable[[Tree], bool]
    replace: Callable[[Tree], Tree]
    execute: Callable[[Tree], Tree]


class UnitTreeLaw:
    predicate: Callable


class Scalar:
    pass


def is_scalar(tree: Leaf[Number]) -> bool:
    if isinstance(tree, Leaf):
        if isinstance(tree.value, Number):
            return True
    return False


class ScalarApplication(Law):
    """
    This needs some way to know what class the tree is
    """
    @classmethod
    def predicate(cls, tree: Tree):
        """Checks if tree is a Node with Scalars on right and left"""
        if isinstance(tree, Node):
            if is_scalar(tree.left) and is_scalar(tree.right):
                return True
        return False

    @classmethod
    def replace(cls, tree: Node):
        """
        I would like to say this, but don't have the Type Parameters set for it:
            Node[TreeFunction[[Number, Number], Number], Leaf[Number]]

        @todo - Find a more elegant expression of this
        * this is a terribly contorted and non-natural expression
        * this pokes extensively into the internals of the Tree class, and should allow Tree to handle that
        * It really needs a Functor
        * ... I think this is: tree.construct(tree.fold(tree.value.call, tree.left, tree.right.value))
           - .... which is even weirder
        * The succinct expression of this would be: tree.bifold(tree.value)
        """
        return tree.construct(tree.value.operator(tree.left.value, tree.right.value))
