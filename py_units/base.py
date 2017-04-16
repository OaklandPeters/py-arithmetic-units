
class UnitsError(Exception):
    pass


class UnitsTypeError(UnitsError, TypeError):
    pass


class FunctorError(UnitsTypeError):
    pass


class UnitsType:
    pass


class UnitMeta(type):
    def __call__(cls, *args, **kwargs):
        return cls.__call__(*args, **kwargs)
