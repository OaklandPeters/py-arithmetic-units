from typing import Iterator, TypeVar

from .base import UnitsTypeError
from .tree import Tree, Empty, Leaf, Node


A = TypeVar('A')


def dfs(tree: Tree[A]) -> Iterator[A]:
    if isinstance(tree, Empty):
        pass
    elif isinstance(tree, Leaf):
        yield tree.value
    elif isinstance(tree, Node):
        yield from dfs(tree.left)
        yield from dfs(tree.right)
        yield tree.value
    else:
        raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
            tree.__class__.__name__
        ))


def bfs(tree: Tree[A]) -> Iterator[A]:
    tree_list = [tree]
    while tree_list:
        new_tree_list = []
        for tree in tree_list:
            if isinstance(tree, Empty):
                pass
            elif isinstance(tree, Leaf):
                yield tree.value
            elif isinstance(tree, Node):
                yield tree.value
                new_tree_list.append(tree.left)
                new_tree_list.append(tree.right)
            else:
                raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                    tree.__class__.__name__
                ))
        tree_list = new_tree_list
