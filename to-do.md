# Unittests
1. Just... in general

# Mathematics
1. Core mathematics for `UnitsLeaf` - provide a `cls.lift(f)` function
2. `Scalar.lift` should proxy to the equivalent method on `self.value`
3. ``

# Package Structure
1. Move abstracts to their module

# Class Architecture
* Change order of arguments on UnitLeaf, UnitVector, and Scalar - (dimension, value=1, parent=None)
* * make parent optional - and default to None
* Provide `__str__` and `__repr__` for classes in `units.py`
* Merge role of `exponent` into 'value' for standard `UnitsLeaf`

# Constructors
* `UnitsLeaf` - constructor to return Scalar when appropriate
1. add specialized handling in constructor for dimension
2. `Unit` needs to be a distinct/unique representation - to compare
3. registration of units based on identifier - so if one already exists, it is returned
4. `Dimension` - return `NullUnit` when name/identifier is None
4. 1. handle the case of only one of name/identifier being None

# Simplification
1. Clean up `simplify` for the two functions - they still reference .units
2. `Scalar.simplify`
3. 1. which basically consists of actually doing math
3. 2. Probably best handled via the external **simplify** module



# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
