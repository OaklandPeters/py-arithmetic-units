from .typing import Iterator

from .units import Unit, UnitsStem, Scalar


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
def scalar_simplifications(scalar: Scalar):
    # (1) Check if this can be merged with an adjacent scalar node
    parent = scalar.parent
    if (isinstance(parent.left, Scalar) and isinstance(parent.right, Scalar)):
        merge_child_scalars(scalar.parent)

    # (2) Migrate Scalar to the leftmost position
    return scalar


#
#   Stubs
#


def merge_child_scalars(parent):
    pass


def migrate_scalar_to_left_most(node: Node):
    pass


# Weird syntax choices:
#   Primary motivation is for functional immutable style
#  (~ to avoid mutation)
# Tree(node).root -> Node
# Tree(node).left_most -> Node

# And this problem....
# node = Unit('feet') * Unit('feet')
