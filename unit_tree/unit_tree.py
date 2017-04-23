"""
Build UnitTree out of abstract Tree
"""


from .tree import (Tree, Empty, Leaf, Node, bfs, dfs)


class UnitTree(Tree):
    pass


class UnitNode(Node):
    pass


class UnitLeaf(Leaf):
    pass


class UnitEmpty(Empty):
    pass
