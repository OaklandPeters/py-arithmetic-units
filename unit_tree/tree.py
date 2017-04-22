"""
Important category-theory realization:

TreeFunction != Function on Trees

I *think* that lift is supposed to generate a tagged function,
that operates differently.

"""
from typing import (
    Callable, Generic, TypeVar, NewType, Any, Union, Type,
    Iterator
)

from .base import UnitMeta, NotPassed, UnitsTypeError, identity

Domain = TypeVar('Domain')
A = TypeVar('A', bound=Domain)
B = TypeVar('B', bound=Domain)
C = TypeVar('C', bound=Domain)
D = TypeVar('D', bound=Domain)
DomainFunction = Callable[[Domain], Domain]
TreeFunction = Callable[['Tree[Domain]'], 'Tree[Domain]']
# I need: TreeFunction[A] = Callable[[Tree[A]], Tree[A]]
# Actually, TreeFunction[int] works just fine


class Tree(Generic[Domain], metaclass=UnitMeta):
    """
    Binary abstract tree.
    Allows for the possibility of the center of a Node having a different
    type than Leafs.
    """
    domain: Domain
    codomain: 'Tree'

    def __new__(cls, value=NotPassed, left=NotPassed, right=NotPassed):
        if value is NotPassed:
            return Empty()
        elif left is NotPassed and right is NotPassed:
            return Leaf(value)
        else:
            return Node(value, left, right)

    @classmethod
    def map(cls, f: DomainFunction, tree: 'Tree[Domain]') -> 'Tree[Domain]':
        """Note - I dont like having map on the parent class Tree dispatch
        on the type of the children -
        because it require that class to know about the internals.
        """
        if isinstance(tree, Empty):
            return Empty
        elif isinstance(tree, Leaf):
            return Leaf(f(tree.value))
        elif isinstance(tree, Node):
            return Node(f(tree.value), cls.map(f, tree.left), cls.map(f, tree.right))
        else:
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    @classmethod
    def maybe(cls,
              f: Callable[['Tree'], Any],
              x: Union['Tree', Domain],
              _else: Callable[[Domain], Any]=identity):
        if isinstance(x, Tree):
            return f(x)
        else:
            return _else(x)

    @classmethod
    def join(cls, tree: 'Tree[Domain]'):
        """
        I think the key here is that it depends on what the children are
        """
        if isinstance(tree, Empty):
            return None
        elif isinstance(tree, Leaf):
            if isinstance(tree.value, Tree):
                # Leaf (Empty()|Leaf(x)|Node(x,l,r)) --> Empty()|Leaf(x)|Node(x,l,r)
                return tree.value.join()
            else:
                # Leaf (non-Tree) --> no change
                return Leaf(tree.value)
        elif isinstance(tree, Node):
            # Hard case - not sure what should be done here
            # Perhaps... nothing?
            # Child classes may want to have something go here
            # And they can override it
            return Node(
                cls.maybe(tree.value),
                cls.maybe(tree.left),
                cls.maybe(tree.right)
            )
            # return Node(
            #     tree.value,
            #     tree.left,
            #     tree.right
            # )
        else:
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    def bind(cls, f: Callable[[Domain], 'Tree[Domain]'],
             value: Union[Domain, 'Tree[Domain]']) -> 'Tree[Domain]':
        """The point of this is that it supports having either domain or Tree
        as the argument. Especially valuable when you generalize it to *values varargs.

        Bind needs to map the internals of 'value', put it into a tree object

        Key differences with Tree.map:
        * Possibility of a f(Leaf(...)) --> Node or Empty
        """
        pass

    @classmethod
    def construct(cls, domain: Domain) -> 'Tree[Domain]':
        return Tree(domain)

    @classmethod
    def lift(cls, dfunc: DomainFunction) -> TreeFunction:
        """To follow most in the tradition of Haskell Applicative,
        this would return an entirely different type of object
        M[A->B] :: M[A] -> M[B]
        Instead, I'm return an unembelished function:
        M[A] -> M[B]
        """
        @functools.wraps(func)
        def wrapper(tree: 'Tree[Domain]') -> 'Tree[Domain]':
            return cls.map(dfunc, tree)
        return wrapper

    @classmethod
    def apply(cls, tfunc: TreeFunction, tree: 'Tree[Domain]'):
        return tfunc(tree)

    @classmethod
    def fold(cls, f: Callable[[A, B], B], accumulator: B, tree: 'Tree[A]'):
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
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    @classmethod
    def traverse(cls, f, tree):
        if isinstance(tree, Empty):
            # traverse f Empty = pure Empty
            #  which looks like it would be: return cls.construct(tree)
            #  but that seems wrong, so I'm going with: return tree
            # ...
            # perhaps: cls.bind(tree) ???
            #  so it takes care of the flattening,
            return tree
        elif isinstance(tree, Leaf):
            return cls.map(Tree, f(tree.value))
        elif isinstance(tree, Node):
            return Node(
                f(tree.value),
                cls.traverse(f, tree.left),
                cls.traverse(f, tree.right)
            )
        else:
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    @classmethod
    def zero(cls):
        return Empty()


class Empty(Tree):
    def __init__(self):
        pass


class Leaf(Generic[D, Domain], Tree[Domain]):

    def __init__(self, value):
        self.value = value


class Node(Generic[C, D, Domain], Tree[Domain]):
    """
    The types of value and left/right are left very vague, because
    particular tree types may have very different notions of what
    can go there.

    For example - in the UnitTree - value: UnitFunction <: TreeFunction
    class UnitTree(Node[])
    and left/right: Node
    """

    value: C
    left: Union[D, Empty]
    right: Union[D, Empty]

    def __init__(self, value,
                 left: Union[D, Type[NotPassed]] = NotPassed,
                 right: Union[D, Type[NotPassed]] = NotPassed):
        if left is NotPassed:
            left = Empty()
        if right is NotPassed:
            right = Empty()
        self.value = value
        self.left = left
        self.right = right


# ================================================
#           Supporting functions
# ================================================

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
