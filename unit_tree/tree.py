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

from .base import UnitMeta, UnitBase, NotPassed, UnitsTypeError, identity

Domain = TypeVar('Domain')
A = TypeVar('A', bound=Domain)
B = TypeVar('B', bound=Domain)
C = TypeVar('C', bound=Domain)
D = TypeVar('D', bound=Domain)
DomainFunction = Callable[[Domain], Domain]
TreeFunction = Callable[['Tree[Domain]'], 'Tree[Domain]']


class Tree(Generic[Domain], UnitBase):
    """
    Binary abstract tree.
    Allows for the possibility of the center of a Node having a different
    type than Leafs.
    """
    # Child classes need to override Domain
    domain: Domain
    codomain: 'Tree'

    def __new__(cls, value=NotPassed, left=NotPassed, right=NotPassed):
        if value is NotPassed:
            return object.__new__(Empty)
        elif left is NotPassed and right is NotPassed:
            return object.__new__(Leaf)
        else:
            return object.__new__(Node)

    @classmethod
    def __call__(cls, *args):
        self = object.__new__(cls)
        self.__init__(*args)
        return self

    @classmethod
    def map(cls, tree: 'Tree[Domain]', f: DomainFunction) -> 'Tree[Domain]':
        """Note - I dont like having map on the parent class Tree dispatch
        on the type of the children -
        because it require that class to know about the internals.
        """
        if isinstance(tree, Empty):
            return Empty
        elif isinstance(tree, Leaf):
            return Leaf(f(tree.value))
        elif isinstance(tree, Node):
            return Node(
                cls.map(tree.value, f),
                cls.map(tree.left, f),
                cls.map(tree.right, f)
            )
        else:
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    @classmethod
    def maybe(cls,
              x: Union['Tree', Domain],
              _do: Callable[['Tree'], Any]=identity,
              _not: Callable[[Domain], Any]=identity):
        """Sugar meta-function. Conditionally apply a function to the input
        when it is and/or is-not a type of Tree.
        Note - this is very different than the Maybe Monad
        """
        if isinstance(x, cls.codomain):
            return _do(x)
        elif isinstance(x, cls.domain):
            return _not(x)
        else:
            raise UnitsTypeError(str.format(
                "{0} is not a subtype of tree, nor in the domain '{1}'",
                x.__class__.__name__, Domain
            ))

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
                return cls.join(tree.value)
            else:
                # Leaf (non-Tree) --> no change
                return Leaf(tree.value)
            # More succicent expression:
            # return cls.maybe(tree.value, cls.join, construct)
        elif isinstance(tree, Node):
            # Structure of Node is not changed - even when one child is empty
            # Child classes may want to override and expand this behavior
            return Node(
                cls.maybe(tree.value, cls.join),
                cls.maybe(tree.left, cls.join),
                cls.maybe(tree.right, cls.join)
            )
        else:
            raise UnitsTypeError("{0} is unrecognized subtype of tree".format(
                tree.__class__.__name__
            ))

    def bind(cls, value: Union[Domain, 'Tree[Domain]'],
             f: Callable[[Domain], 'Tree[Domain]'],
             ) -> 'Tree[Domain]':
        """The point of this is that it supports having either domain or Tree
        as the argument. Especially valuable when you generalize it to *values varargs.

        Bind needs to map the internals of 'value', put it into a tree object

        Key differences with Tree.map:
        * Possibility of a f(Leaf(...)) --> Node or Empty
        """
        return cls.join(cls.map(value, f))

    @classmethod
    def construct(cls, domain: Domain) -> 'Tree[Domain]':
        """Construct a Tree element out of a Domain element"""
        # Handle an edge case - where domain is 'NotPassed', but
        # we need to prevent passing 'NotPassed' into Empty.__init__
        if domain is NotPassed:
            return Tree()
        else:
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
    def apply(cls, tree: 'Tree[Domain]', tfunc: TreeFunction):
        return tfunc(tree)

    @classmethod
    def fold(cls, tree: 'Tree[A]', f: Callable[[A, B], B], accumulator: B):
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
    def traverse(cls, tree: 'Tree[A]', f: TreeFunction):
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
    def zero(cls) -> 'Tree[A]':
        return Empty()

    @classmethod
    def identity(cls, tree: 'Tree[A]'):
        return cls.map(tree, identity)


# Tree.domain should be overridden by child-classes
Tree.domain = object
Tree.codomain = Tree


class Empty(Tree):

    def __new__(cls):
        self = object.__new__(cls)
        self.__init__()
        return self

    def __init__(self):
        pass

    def __repr__(self):
        return str.format(
            "{0}()", self.__class__.__name__
        )

    def __eq__(self, other):
        return True if isinstance(other, Empty) else False


class Leaf(Generic[D, Domain], Tree[Domain]):

    value: Union[Domain, Tree[Domain]]

    def __new__(cls, value):
        self = object.__new__(cls)
        self.__init__(value)
        return self

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str.format(
            "{0}({1})", self.__class__.__name__, repr(self.value)
        )

    def __eq__(self, other):
        if isinstance(other, Leaf):
            return self.value == other.value
        else:
            return False


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

    def __new__(cls, value,
                left: Union[D, Type[NotPassed]] = NotPassed,
                right: Union[D, Type[NotPassed]] = NotPassed):
        self = object.__new__(cls)
        self.__init__(value, left, right)
        return self

    def __init__(self, value,
                 left: Union[D, Type[NotPassed]] = NotPassed,
                 right: Union[D, Type[NotPassed]] = NotPassed):
        # If inputs are not Tree type - wrap them in one
        #   Generally results in putting things in a Leaf
        self.value = self.maybe(value, _not=self.construct)
        self.left = self.maybe(left, _not=self.construct)
        self.right = self.maybe(right, _not=self.construct)

    def __repr__(self):
        return str.format(
            "{0}({1}, {2}, {3})", self.__class__.__name__,
            repr(self.value), repr(self.left), repr(self.right)
        )

    def __eq__(self, other):
        if isinstance(other, Node):
            return all((
                self.value == other.value,
                self.left == other.left,
                self.right == other.right
            ))
        else:
            return False
