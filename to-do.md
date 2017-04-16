
# Immediate & Mess cleanup
* Cleanup type annotations in syntax.py
* Figure out how to handle InvariantFunctor, and it's use of abstractmethod
    - ... because other classes do not inherit from ABCMeta
* Remove unneeded imports from syntax.py


# Problem:
* Can't combine 'UnitMeta' with 'Generic'


# Mathematics
* Merge the syntax functor into UnitsLeaf
* Write new functor + SyntaxMixin for:
    - UnitsVector
    - UnitsStem

# Package Structure
* Move import and `__all__` into `__init__`
    - Change tests to import from `__all__`
* Move syntax and functor into their own file
* Move abstracts to their module

# Class structure
* Make Scalar inherit from syntax mixin
* Rename NumberUnitSyntaxMixin --> ArithmeticSyntaxMixin

# Constructors
1. `Dimension` - return `NullUnit` when name/identifier is None
1. 1. handle the case of only one of name/identifier being None

# Simplification
1. Clean up `simplify` for the two functions - they still reference .units
2. `Scalar.simplify`
3. 1. which basically consists of actually doing math
3. 2. Probably best handled via the external **simplify** module



# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
