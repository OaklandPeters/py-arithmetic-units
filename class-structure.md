

# Unit-Tree Hierarchy

| Class name        | Parent    | Info                               |
|:------------------|:----------|:-----------------------------------|
| UnitMeta          | --        | Metaclass: override initialization |
| UnitsType         | --        | Abstract base for typing           |
| Unit              | --        | Concrete base for implementation   |
| UnitsStem         | Unit      |                                    |
| UnitsFunctionStem | UnitsStem |                                    |
| UnitsLeaf         | Unit      |                                    |
| Scalar            | UnitsLeaf |                                    |
| UnitsVector       | UnitsLeaf |                                    |


# Units-Function Hierarchy
Functions inside nodes are not directly part of the tree-hierarchy.
But, we want them to have slightly more structure

| Class name    | Parent        | Info                           |
|:--------------|:--------------|:-------------------------------|
| UnitsFunction | --            | Base class for these functions |
| Multiply      | UnitsFunction |                                |
| Divide        | UnitsFunction |                                |

# Functor & Syntax Hierarchy
Functors are used as a utility for structuring mathematics syntax.

| Class name            | Parent  | Info                                                 |
|:----------------------|:--------|:-----------------------------------------------------|
| Functor               |         |                                                      |
| InvariantFunctor      | Functor |                                                      |
| ArithmeticSyntaxMixin | --      | Implements syntax. Receives Functor via composition. |
