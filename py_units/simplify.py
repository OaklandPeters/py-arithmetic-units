"""
SEMI HARD PROBLEM:
Replacing a node, while keeping the reference to it in the parent correct



Weird syntax choices:
  Primary motivation is for functional immutable style
 (~ to avoid mutation)
Tree(node).root -> Node
Tree(node).left_most -> Node

And this problem....
node = Unit('feet') * Unit('feet')
"""
from .typing import Iterator

from .units import Unit, UnitsStem, Scalar, DimensionNode
from .base import UnitsError


def ancestry_iterator(node: Unit) -> Iterator[Unit]:
    lense = node
    while (lense.parent is not None):
        yield lense
        lense = lense.parent


def find_root(node: Unit) -> Unit:
    """Recursive hunt for ancestor without a parent.
    We do not actually use function recursion, because
    Python does not handle recursion very well.
    """
    for last in ancestry_iterator(node):
        pass
    return last



#
# Partial completion
#
def simplify_tree(node: Unit) -> Unit:
    """
    Generally we will want to simplify from the root.
    """
    root = find_root(node)

    if isinstance(root, UnitsLeaf):
        # Sanity check that node == root
        if root != node:
            raise UnitsError("Sanity check failed")
        else:
            # No further simplifications can be done
            return root
    else:
        # isinstance(root, UnitsStem) == True

        # Sort the tree
        normalized_root = normalize_tree(root)

        # Note - handling iterator while also mutating... makes life hard
        for node in depth_first_iterator(normalized_root):
            if isinstance(node, UnitsLeaf):
                pass
            else:
                # Stem




def _simplify(node: Unit) -> Unit:
    pass


def simplify_scalar_nodes(stem: UnitsStem) -> Unit:
    """Check if scalar simplification can be applied"""
    if (isinstance(stem.left, Scalar) and isinstance(stem.right, Scalar)):
        return ScalarFunctor.map(
            stem.function,
            stem.left,
            stem.right
        )
    return stem


def simplify_dimension_nodes(stem: UnitsStem) -> Unit:
    """Check if dimensional simplification can be applied to a stem."""
    if isinstance(stem.left, DimensionNode) and isinstance(stem.right, DimensionNode):
        if stem.left.dimension == stem.right.dimension:
            # Create new with unit of left, and add exponents
            return DimensionFunctor.map(
                stem.function,
                stem.left,
                stem.right
            )
    return stem


def normalize_tree(stem: UnitsStem):
    """Places the tree is a normalized and standardized form,
    via applying a tree sorting algorithm.
    The goal of this is to make it easier to combine
    (Scalar, Scalar) stems and (DimensionNode, DimensionNode) stems.

    In sorted form - Scalars (~dimension == NullUnit) should be in
    the left-most position.
    """


#
# Functors
#

class DispatchingFunctor(Functor):
    """This is a bit of a hack-job, categorically speaking.
    But the idea is to shove all of the 'dispatch on left/right type', into
    it's own functor.

    ... this may be better located inside simplify.py

     Handle which operators are displayed on which node types via syntax mixins
    """


class ScalarFunctor(InvariantFunctor[Number, Scalar]):
    """For combining two Scalars

    Handle which operators are displayed on which node types via syntax mixins
    """


class DimFunctor(InvariantFunctor[Dimension, DimensionNode]):
    """For combining two DimensionNodes."""


class CompoundUnitsFunctor(InvariantFunctor[Unit, UnitsStem]):
    """For combining two UnitStem nodes."""
