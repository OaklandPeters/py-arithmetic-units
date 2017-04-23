"""
Run tests with:
cd py-arithmetic-units\
py -m unittest tree_tests
"""
import unittest
from typing import Mapping

from unit_tree import (
    Tree, Empty, Leaf, Node, bfs, dfs,
    UnitsError, UnitsTypeError, FunctorError, OperatorLookupError,
    UnitsType, UnitMeta, NotPassed,
    Dimension, NullUnit
)


def validate_types(test, subject, type_mapping: Mapping[type, bool]):
    """Helper function for extensive type checking."""
    for _type, expectation in type_mapping.items():
        if expectation:
            test.assertIsInstance(
                subject, _type,
                str.format(
                    "Type AssertionError: {0} is not an instance of {1}",
                    repr(subject), _type)
            )
        else:
            test.assertNotIsInstance(
                subject, _type,
                str.format(
                    "Type AssertionError: {0} is incorrectly an instance of {1}",
                    repr(subject), _type)
            )


class TreeTests(unittest.TestCase):
    """
    Methods to test:
    map, bind, construct, lift, apply, fold, traverse, zero
    """

    def _validate_empty(self, empty):
        validate_types(self, empty, {
            Tree: True,
            Node: False,
            Leaf: False,
            Empty: True
        })

    def _validate_leaf(self, leaf, expected_value):
        validate_types(self, leaf, {
            Tree: True,
            Node: False,
            Leaf: True,
            Empty: False
        })
        self.assertEqual(leaf.value, expected_value)

    def _validate_node(self, node, expected_value, expected_left, expected_right):
        validate_types(self, node, {
            Tree: True,
            Node: True,
            Leaf: False,
            Empty: False
        })
        self.assertEqual(node.value, expected_value)
        self.assertEqual(node.left, expected_left)
        self.assertEqual(node.right, expected_right)

    def test_empty(self):
        self._validate_empty(Empty())

    def test_leaf(self):
        self._validate_leaf(Leaf('x'), 'x')

    def test_node(self):
        self._validate_node(Node(1, 2, 3), Leaf(1), Leaf(2), Leaf(3))

    def test_maybe(self):
        """ Confirm that the isinstance(x, cls.codomain) actually works"""
        self.assertEqual(
            Tree.maybe(Leaf('x'), lambda x: x.value),
            'x'
        )

    def test_empty_equality(self):
        self.assertEqual(Empty(), Empty())
        self.assertNotEqual(Empty(), None)
        self.assertNotEqual(Empty(), Empty)

    def test_leaf_equality(self):
        self.assertEqual(Leaf(5), Leaf(5))
        self.assertNotEqual(Leaf(5), Leaf('5'))
        self.assertNotEqual(Leaf(5), Empty())
        self.assertEqual(Leaf(None), Leaf(None))
        self.assertNotEqual(Leaf(None), Empty)

    def test_leaf_inheritance(self):
        class WeirdLeaf(Leaf):
            def __new__(cls, value, more):
                self = object.__new__(cls)
                self.__init__(value, more)
                return self

            def __init__(self, value, more):
                self.value = value
                self.more = more

        self._validate_leaf(WeirdLeaf('x', 'y'), 'x')
        self.assertEqual(WeirdLeaf('x', 'y'), Leaf('x'))

    def test_node_equality(self):
        self.assertEqual(Node(1, 2, 3), Node(1, 2, 3))
        self.assertEqual(
            Node(1, 2, 3),
            Node(1, Leaf(2), Leaf(3))
        )
        self.assertEqual(Node(1, 2, None), Node(1, Leaf(2), Leaf(None)))
        self.assertNotEqual(Node('x', 'y'), ('x', 'y'))
        self.assertNotEqual(Node(3, None, None), Leaf(3))
        self.assertEqual(Node(None, None, None), Node(None, None, None))

    def test_map(self):
        self.assertEqual(
            Tree.map(Node(1, 2, 3), lambda x: x + 3),
            Node(4, 5, 6)
        )

    def test_join_leaf(self):
        pile = Leaf(Leaf(Leaf(Leaf('x'))))
        out = Tree.join(pile)
        self.assertEqual(out, Leaf('x'))

        thing = Leaf(Leaf(Leaf(Empty())))
        nothing = Tree.join(thing)
        self.assertEqual(nothing, None)

        node = Node(1, 2, 3)
        noddy = Leaf(Leaf(Leaf(node)))
        after = Tree.join(noddy)
        self.assertEqual(after, node)

    def test_type_dispatching(self):
        # Node(Node(Node('x')))
        self._validate_node(Node('x'), Leaf('x'), Empty(), Empty())
        self._validate_leaf(Tree('x'), 'x')


class UnitTreeTests(unittest.TestCase):

    # def test_multiplication_syntax_chaining(self):
    #     # Also - test that the nodes are Multiplication <: UnitFunction <: TreeFunction
    #     chained = UnitTree(5) * 4 * 3
    #     self._validate_node(chained)

    # def test_scalar_simplification(self):
    #     pass
    pass
