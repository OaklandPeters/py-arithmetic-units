
# Mathematics
1. Merge the syntax functor into UnitsLeaf

# Package Structure
1. Move abstracts to their module

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
