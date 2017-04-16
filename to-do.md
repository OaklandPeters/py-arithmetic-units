
# Next task
* Multiplication on UnitsVector to yield stems

# Mathematics
* Write new functor + SyntaxMixin for UnitsVector
    - Do it on UnitsVector class for now
    - Chart this out on paper first, for each operator
    - Pay close attention to how these should interact with exponent
* Migrate syntax methods out of UnitsVector, and into supporting classes in syntax.py
* THINK THROUGH: UnitsCompound 'new' -all possible pairs of arguments
    - what functions will be needed
*
* AFTER: UnitVector has syntax - merge the syntax functor into UnitsLeaf
* Syntax mixin for UnitsStem - note this is actually hard
* Add handling for mixing mathematics arguments of types (Scalar, UnitsVector, UnitsStem)
    - Rethink from a class-structure & proxying standpoint.



# Class structure
* Make Scalar inherit from syntax mixin
* Rename NumberUnitSyntaxMixin --> ArithmeticSyntaxMixin

# Simplification
* Clean up `simplify` for the two functions - they still reference .units
* `Scalar.simplify`
    - which basically consists of actually doing math
    - Probably best handled via the external **simplify** module

# Constructors
* `Dimension` - return `NullUnit` when name/identifier is None
* handle the case of only one of name/identifier being None


# Package Structure

# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
