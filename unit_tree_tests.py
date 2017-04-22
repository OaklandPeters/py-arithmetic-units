"""
Run tests with:
cd py-arithmetic-units\
py -m unittest unit_tree_tests
"""
import unittest
from typing import Mapping
# from numbers import Number

# from unit_tree.dimension import Dimension, NullUnit
from unit_tree import (
    Tree, Empty, Leaf, Node, bfs, dfs,
    UnitsError, UnitsTypeError, FunctorError, OperatorLookupError,
    UnitsType, UnitMeta, NotPassed
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


    def _validate_node(self, node, expected_value, expected_left, expected_right):
        validate_types(self, node, {
            Tree: True,
            Node: False,
            Leaf: True,
            Empty: False
        })

    def test_empty(self):
        self._validate_empty(Empty())

    def test_leaf(self):
        self._validate_leaf(Leaf('x'), 'x')

    def test_node(self):
        self._validate_node(Node(1, 2, 3), 1, 2, 3)

    def test_maybe(self):
        """ Confirm that the isinstance(x, cls.codomain) actually works"""
        pass




class UnitTreeTests(unittest.TestCase):

    # def test_multiplication_syntax_chaining(self):
    #     # Also - test that the nodes are Multiplication <: UnitFunction <: TreeFunction
    #     chained = UnitTree(5) * 4 * 3
    #     self._validate_node(chained)

    # def test_scalar_simplification(self):
    #     pass
    pass
