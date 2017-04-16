from typing import GenericMeta


class UnitsError(Exception):
    pass


class UnitsTypeError(UnitsError, TypeError):
    pass


class FunctorError(UnitsTypeError):
    pass


class UnitsType:
    pass


class UnitMeta(GenericMeta):
    """
    This inherits from GenericMeta instead of 'type' - to solve metaclass conflicts
    with classes which use metaclass=UnitMeta, but also need to inherit from 'Generic'
    """
    def __call__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
