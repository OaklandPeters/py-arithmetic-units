"""

Info from typing.py
# Special typing constructs Union, Optional, Generic, Callable and Tuple
# use three special attributes for internal bookkeeping of generic types:
# * __parameters__ is a tuple of unique free type parameters of a generic
#   type, for example, Dict[T, T].__parameters__ == (T,);
# * __origin__ keeps a reference to a type that was subscripted,
#   e.g., Union[T, int].__origin__ == Union;
# * __args__ is a tuple of all arguments used in subscripting,
#   e.g., Dict[T, int].__args__ == (T, int).


Deconstructible:
Abstract class for the ability to retreive concrete value of type-arguments
from the attribute/method type-hints on an instantiation class of a generic.

For example:
    class MyList(List[int]):
        # ...
    MyList.__deconstruct__()
    --> List.__deconstruct__(MyList)

    Algorithm #1:
    --> get_type_hints(MyList.__getitem__)['return']

    Algorithm #2:
    --> get_type_parameters(MyList)

    BUT - I don't know how to get type parameters off the MRO of a subclass

---------------------------
THE GOAL:
---------------------------
Make this work:
    Domain = Union[TreeFunction, Number, Dimension]
    isinstance(x, Domain)

Additional goals:
* Handling for Dict
* Handling for the misc objects in typing.py
* Handle for variadic Tuples
"""
from typing import (
    Union, Generic, Callable, Tuple, Optional,
    GenericMeta, get_type_hints, Any, Dict
)

from unit_tree import TreeMeta


SpecialTypes = [Union, Generic, Callable, Tuple, Optional]
NormalType = object
special_type_names = (_type.__name__ for _type in SpecialTypes)


def meets(instance, _type):
    """Does instance meet a type-object?
    Basically, an enhanced version of 'isinstance(instance, _type)', but
    works with some of the pieces from the typing module - Union, etc
    """
    # Simplify certain cases - specifically Union, Callable, and Generic
    # which are both instances and types
    handle = _handle_as_type(_type)
    if hasattr(handle, '__meets__'):
        return handle.__meets__(instance, _type)
    elif _type in _registry:
        return _registry[_type](instance, _type)
    else:
        return isinstance(instance, _type)


_registry = {}


def _handle_as_type(_type):
    """Handles cases of 'typing' related objects which are instances and also types.
    Such as Union[a, b], and parameterized Generics (Dict[a, b]), etc
    """
    if hasattr(_type, '__origin__'):
        if _type.__origin__ is not None:
            handle = _type.__origin__
            if isinstance(handle, GenericMeta):
                return Generic
            else:
                return handle
    return _type


def _register(klass):
    def wrapper(func):
        _registry[klass] = func
        return func
    return wrapper


@_register(Any)
def meets_any(instance, _type):
    return True


@_register(Union)
def meets_union(instance, _type_union):
    return any(
        meets(instance, component) for component in _type_union.__args__
    )
