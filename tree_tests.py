"""
Run tests with:
cd py-arithmetic-units\
py -m unittest tree_tests
"""
import unittest
from typing import Mapping
import operator

from unit_tree import (
    Tree, Empty, Leaf, Node,
    TreeMeta,
    TreeBase, UnitBase,
    Dimension, NullUnit,
    UnitTree, UnitNode, UnitLeaf, UnitEmpty, UnitTreeFunction,
    TreeFunction, Add, Subtract, Multiply, Divide, TreeArithmeticSyntax
)

_default_type_mapping = {
    TreeBase: False,
    Tree: False,
    Node: False,
    Leaf: False,
    Empty: False,
    UnitBase: False,
    UnitTree: False,
    UnitNode: False,
    UnitLeaf: False,
    UnitEmpty: False,
}


def combine_dicts(*_dicts):
    return dict(pair for _dict in _dicts for pair in _dict.items())


def validate_types(test, subject, type_mapping: Mapping[type, bool]):
    """Helper function for extensive type checking."""
    for _type, expectation in type_mapping.items():
        if expectation:
            test.assertIsInstance(
                subject, _type,
                # str.format(
                #     "Object of type '{0}' is not an instance of {1}",
                #     subject.__class__.__name__, _type
                # )
            )
        else:
            test.assertNotIsInstance(
                subject, _type,
                # str.format(
                #     "Object of type '{0}' is incorrectly an instance of {1}",
                #     subject.__class__.__name__, _type
                # )
            )


def validate_subclasses(test, subject, type_mapping: Mapping[type, bool]):
    for _type, expectation in type_mapping.items():
        if expectation:
            test.assertTrue(
                issubclass(subject, _type),
                str.format(
                    "Type AssertionError: {0} is not a subclass of {1}",
                    subject.__name__, _type.__name__
                )
            )
        else:
            test.assertFalse(
                issubclass(subject, _type),
                str.format(
                    "Type AssertionError: {0} is incorrectly a subclass of {1}",
                    subject.__name__, _type.__name__
                )
            )

# class DimensionTests(unittest.TestCase):

#     def test_nullunit(self):
#         self.assertIsInstance(Dimension(), Dimension)
#         self.assertIsInstance(NullUnit, Dimension)
#         self.assertEqual(Dimension(), Dimension())
#         self.assertEqual(Dimension(), NullUnit)
#         self.assertNotEqual(Dimension('feet'), NullUnit)

#     def test_dimension_registry(self):
#         """Do this via checking the id() of the returned objects"""
#         self.assertTrue(Dimension is NullUnit)
#         feet = Dimension('feet')
#         self.assertTrue(Dimension('feet') is feet)


class TreeTests(unittest.TestCase):
    """
    Methods to test:
    map, bind, construct, lift, apply, fold, traverse, zero
    """

    construct = Tree.construct()

    def _validate_empty(self, empty):
        validate_types(self, empty, {
            TreeBase: True,
            Tree: True,
            Node: False,
            Leaf: False,
            Empty: True
        })

    def _validate_leaf(self, leaf, expected_value):
        validate_types(self, leaf, {
            TreeBase: True,
            Tree: True,
            Node: False,
            Leaf: True,
            Empty: False
        })
        self.assertEqual(leaf.value, expected_value)

    def _validate_node(self, node, expected_value, expected_left, expected_right):
        validate_types(self, node, {
            TreeBase: True,
            Tree: True,
            Node: True,
            Leaf: False,
            Empty: False
        })
        self.assertEqual(node.value, expected_value)
        self.assertEqual(node.left, expected_left)
        self.assertEqual(node.right, expected_right)

    def _validate_subclass(self, subject, type_mapping):
        self.assertIsInstance(subject, TreeMeta)
        validate_subclasses(
            self, subject,
            combine_dicts(_default_type_mapping, type_mapping, {subject: True})
        )

    def test_subclass_relationships(self):
        self._validate_subclass(TreeBase, {})
        self._validate_subclass(Tree, {TreeBase: True})
        self._validate_subclass(Node, {TreeBase: True, Tree: True})
        self._validate_subclass(Leaf, {TreeBase: True, Tree: True})
        self._validate_subclass(Empty, {TreeBase: True, Tree: True})

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

    construct = UnitTree.construct

    def _validate_empty(self, empty):
        validate_types(self, empty, {
            TreeBase: True,
            Tree: True,
            Node: False,
            Leaf: False,
            Empty: True,
            UnitBase: True,
            UnitTree: True,
            UnitNode: False,
            UnitLeaf: False,
            UnitEmpty: True,
        })
        self.assertEqual(empty, self.construct())

    def _validate_leaf(self, leaf, expected_value):
        validate_types(self, leaf, {
            TreeBase: True,
            Tree: True,
            Node: False,
            Leaf: True,
            Empty: False,
            UnitBase: True,
            UnitTree: True,
            UnitNode: False,
            UnitLeaf: True,
            UnitEmpty: False,
        })
        self.assertEqual(leaf.value, expected_value)

    def _validate_node(self, node, expected_value, expected_left, expected_right):
        validate_types(self, node, {
            TreeBase: True,
            Tree: True,
            Node: True,
            Leaf: False,
            Empty: False,
            UnitBase: True,
            UnitTree: True,
            UnitNode: False,
            UnitLeaf: False,
            UnitEmpty: True,
        })
        self.assertEqual(node.value, expected_value)
        self.assertEqual(node.left, expected_left)
        self.assertEqual(node.right, expected_right)

    def test_unit_empty(self):
        self._validate_empty(UnitEmpty())
        self._validate_empty(self.construct())

    # def test_basic_operator_syntax(self):
    #     # Leaf(5) * Leaf(3)
    #     # -> Leaf(5).__mul__(Leaf(3))
    #     # -> TreeFunction.map(
    #     #
    #     node = UnitLeaf(5) * UnitLeaf(3)

    def test_tree_function_call(self):
        tree_function = TreeFunction.lift(operator.__mul__)
        result = tree_function(UnitLeaf(5), UnitLeaf(3))
        self.assertEqual(
            result,
            Node(tree_function, UnitLeaf(5), UnitLeaf(3))
        )

    # def test_multiplication_syntax_chaining(self):
    #     # Also - test that the nodes are Multiplication <: UnitFunction <: TreeFunction
    #     chained = UnitTree(5) * 4 * 3
    #     self._validate_node(chained)

    # def test_scalar_simplification(self):
    #     pass

    # def test_basic_dimension_merge(self):
    #     compound = Unit('feet') * Unit('feet')
    #     import pdb
    #     print("\n(compound::{0}) = {1}\n".format(compound.__class__.__name__, repr(compound)))
    #     pdb.set_trace()

    # def test_basic_scalar_to_dimension_merge(self):
    #     compound = Unit('feet') * Unit(32)
    #     import pdb
    #     print("\n(compound::{0}) = {1}\n".format(compound.__class__.__name__, repr(compound)))
    #     pdb.set_trace()

    # def test_real_world_syntax_usage(self):
    #     Dollars = Unit('Dollars')
    #     Threads = Unit('Threads')
    #     # This step requires stems to work
    #     PpR = (44 * Dollars) / Threads
    #     RpB = (23 * Threads)
    #     # This step requires simplification to work
    #     CtB = PpR * RpB
    #     self.assertEqual(CtB, Dollars(44 * 23))
    #
    # (feet * seconds / feet * (pounds / (feet * feet)))


# class UnitTreeOperatorTests(unittest.TestCase):
#     def test_syntax_mixin_map(self):
#         pairs = [(1, 5), (3, 7), (9, -2), (0, 11.5)]
#         for a, b in pairs:
#             self.assertEqual(Scalar(a) + Scalar(b), Scalar(a + b))
#             self.assertEqual(Scalar(a) - Scalar(b), Scalar(a - b))
#             self.assertEqual(Scalar(a) * Scalar(b), Scalar(a * b))
#             self.assertEqual(Scalar(a) / Scalar(b), Scalar(a / b))
#             self.assertEqual(Scalar(a) ** Scalar(b), Scalar(a ** b))
#             self.assertEqual(Scalar(a) % Scalar(b), Scalar(a % b))

#     def test_syntax_mixin_apply(self):
#         # Confirm type
#         self.assertIsInstance(Scalar(5) + 3, Scalar)

#         # Check mathematics and composition
#         pairs = [(1, 5), (3, 7), (9, -2), (0, 11.5)]
#         for a, b in pairs:
#             self.assertEqual(Scalar(a) + b, Scalar(a + b))
#             self.assertEqual(Scalar(a) - b, Scalar(a - b))
#             self.assertEqual(Scalar(a) * b, Scalar(a * b))
#             self.assertEqual(Scalar(a) / b, Scalar(a / b))
#             self.assertEqual(Scalar(a) ** b, Scalar(a ** b))
#             self.assertEqual(Scalar(a) % b, Scalar(a % b))

#             # Test reversed operators
#             self.assertEqual(a + Scalar(b), Scalar(a + b))
#             self.assertEqual(a - Scalar(b), Scalar(a - b))
#             self.assertEqual(a * Scalar(b), Scalar(a * b))
#             self.assertEqual(a / Scalar(b), Scalar(a / b))
#             self.assertEqual(a ** Scalar(b), Scalar(a ** b))
#             self.assertEqual(a % Scalar(b), Scalar(a % b))

#     def test_long_chaining(self):
#         waaaat = Scalar(2) + 3 + 4 + 5
#         self.assertIsInstance(waaaat, Scalar)
#         self.assertEqual(waaaat, Scalar(2 + 3 + 4 + 5))


