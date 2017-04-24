
# Next task
* unittests for subclass stub constructors & typing
* Unittests for tree methods:
    - join
    - bind
    - lift
    - apply
    - fold
    - traverse
    - zero
    - identity


# Building UnitTree
* Subclass Tree versions:
    - UnitTree
    - UnitNode
        + UnitFunction
            * Probably needs own build step
        + Restrict type - UnitNode.value must be UnitFunction
    - UnitLeaf
        + Contains dimension
    - UnitEmpty
* Write unittests for UnitTree
    - Related - Tree methods - no directly call Empty/Leaf/Node as constructors
        + messes up inheritance
    - Unittests for UnitTree methods:
        + join
        + bind
        + lift
        + apply
        + fold
        + traverse
        + zero
        + identity

# Bugfixes
* Dimension should not inherit from TreeBase, but should have metaclass=TreeMeta
    - Then override __Call__

# Cleanup
* Remove __call__ from Tree - inherited one from UnitBase should be fine

# Mathematical correctness
* Make the Domain of Tree correct - via (,) | (A,) | (B, A, A)
    - I'm not sure how to provide type for empty tuple ~ Domain for Empty
* AFTER UnitTree unittests - try Splitting abstract functions up onto child classes
    - map
    - fold
    - traverse
    - join

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
