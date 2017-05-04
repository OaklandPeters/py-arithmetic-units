



# Next task
* Write meets.py - do via the registry system
    - Tree.__meets__
* change generic parameters on Tree --> to be parameters for Node, and NOT Domain
* Test fold
* Unittests: more for join - Node(...).join()
* Confirm - that Node.value is also a Leaf
* Tests for callable TreeFunction
    - apply, call, __call__, map, lift
* UnitTree composition --> platform for simplify()


# Testing
* Testing to confirm however I'm supposed to use generic parameters on Tree
* I'm very confused ATM - because Leaf[A] should have one parameter - but I'm ending up with 3
* UnitTree.maybe(..., f) and UnitTree.maybe(..., _not=f)
    - Purpose: confirm that domain and codomain are correct
    - Try running it against Tree objects and UnitTree objects, and normal objects

# Clasification:
* could probabably merge the functor parts of treefunction into Tree
* Tree should be generic on two types, not one:
    - Type of the node, and type of the leafs
    - Probably should apply to Node, Leaf, and Empty as well

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

# Testing
* Unittest registry
* Unittests for tree methods:
    - join
    - bind
    - lift
    - apply
    - fold
    - traverse
    - zero
    - identity

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

# Advanced
* Switch TreeFunction to be an instanciatble class
    - Multiply, Add, etc become instances
    - Hard part: getting `__call__` to work - given that I change __call__ in metaclass
    - Easiest would be: if TreeMEta.__call__ changed
        + Leave calling __init__ up to __new__
        + Meta.__call__ --> cls.__new__
        + @classmethod __call__
