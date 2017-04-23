
# Next task
* Build UnitTree
* Write unittests for UnitTree - match existing ones closely
* AFTER unittests - try moving methods onto child classes for clarity

# Bugfixes
* In Tree - should not directly call Empty/Leaf/Node as constructors - messes up inheritance

# Cleanup
* Remove __call__ from Tree - inherited one from UnitBase should be fine

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

# Simplification
* Copy usable portions of py_units/simplfy.py --> unit_tree/simplify.py
* Write scalar pair application simplify
    - Unittests for it, without simplification runner
* Write simplification runner, to be triggered inside Tree.simplify(rules)
    - New class Rule ~ (Pattern, ArgSpec, ArgGetter, Replacer)
        + simple structure, avoid monadic strangeness
        + class Pattern ~ Predicate[Tree] -> bool
    - class Rules ~ List[Rule]
* INITIALLY - avoid pattern-recognition problem, by only specifying purely local patterns
    - LocalPattern - only looks at Tree elm its given, and that elm's immediate children

# Advanced - and unnecessary for now:
* operators on `Dimension`, that promotes it to a Leaf
