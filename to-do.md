
# Next task
* Build UnitTree
* Write unittests for UnitTree - match existing ones closely

# Abstract Tree
* Split abstract functions up onto component classes:
    - map
    - fold
    - traverse
    - join
* Make abstract on Foldable and Functor
* Split fold function onto the component classes

# Mathematics
* Change mixin to be more generic across Leaf & Stem
    - Take current arithmetic mixin --> Graveyard
    - In all cases --> form UnitsStem, based on UnitsFunction
    - Requires writing one UnitsFunction per operator
        + Initially do this inside `units.py`, then move to new `arithmetic.py`
* Write new functor + SyntaxMixin for UnitsVector
    - Do it on UnitsVector class for now
    - Chart this out on paper first, for each operator
    - Pay close attention to how these should interact with exponent
* Migrate syntax methods out of UnitsVector, and into supporting classes in syntax.py
* THINK THROUGH: UnitsCompound 'new' -all possible pairs of arguments
    - what functions will be needed
* AFTER: DimensionNode has syntax - merge the syntax functor into UnitsLeaf
* Syntax mixin for UnitsStem - note this is actually hard
* Add handling for mixing mathematics arguments of types (Scalar, UnitsVector, UnitsStem)
    - Rethink from a class-structure & proxying standpoint.

# Simplification
* Integrate simplification and syntax.
* Handle which operators are displayed on which node types via syntax mixins
* Semi Hard Problem: replacing node, while maintaining child-ref in parent
    - Possibly some Traversable-related chicanary



# Class structure
* Make Scalar inherit from syntax mixin
* Rename NumberUnitSyntaxMixin --> ArithmeticSyntaxMixin

# Simplification
* Clean up `simplify` for the two functions - they still reference .units
* `Scalar.simplify`
    - which basically consists of actually doing math
    - Probably best handled via the external **simplify** module
* Edge case - simplifying Scalar == 0, but for exponentiation
    - Ex. (3 * feet) ^ 0 --> ~ Scalar(1)

# Constructors
* `Dimension` - return `NullUnit` when name/identifier is None
* handle the case of only one of name/identifier being None

# Edge

# Package Structure

# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
