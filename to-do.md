
# Next task
* Build UnitTree
* Write unittests for UnitTree - match existing ones closely
* AFTER unittests - try moving methods onto child classes for clarity

# Bugfixes
* In Tree - should not directly call Empty/Leaf/Node as constructors - messes up inheritance

# Abstract Tree
* Add repr and str functions
* Add equality comparisons for Empty, Leaf, Node
    - Add unittests
* Split abstract functions up onto component classes:
    - map
    - fold
    - traverse
    - join
* Make abstract on Foldable and Functor
* Split fold function onto the component classes

# Mathematics

# Simplification
* Integrate simplification
* Handle which operators are displayed on which node types via syntax mixins
* Semi Hard Problem: replacing node, while maintaining child-ref in parent
    - Possibly some Traversable-related chicanary
    - Solve via: bfs/dfs iterator, and immutablity (~Traversable chicanery)


# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
