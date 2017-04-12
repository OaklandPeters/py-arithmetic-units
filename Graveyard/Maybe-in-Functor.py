"""
Intersting -- look at the maybe, and maybe_not on this functor

Suggests defining 'Maybe' in a functor-agnostic way
"""

class ScalarFunctor:
    """
    Takes two Scalar objects (Unit<Number>, and a function on numbers,
    and applies it.

    Note - this is *not* a monad - because it is not a container, nor
    can Scalar's contain other Scalars.

    The extension to this would handle the Stems as well
    """
    domain = Number
    codomain = Scalar

    @classmethod
    def construct(cls, number: Number) -> Scalar:
        return Scalar(number)

    @classmethod
    def maybe_construct(cls, value: Union[Number, Scalar]) -> Scalar:
        return cls.maybe(cls.construct)(value)

    @classmethod
    def destruct(cls, scalar: Scalar) -> Number:
        return scalar.value

    @classmethod
    def maybe_destruct(cls, value: Union[Number, Scalar]) -> Number:
        return cls.maybe_not(cls.destruct)(value)

    @classmethod
    def map(cls, func: NumberFunction, *scalars: Tuple[Scalar, ...]) -> Scalar:
        return cls.construct(func(*tuple(arg.value for arg in args)))

    @classmethod
    def lift(cls, func: NumberFunction, Number]) -> ScalarFunction:
        def wrapper(*scalars: Tuple[Scalar, ...]) -> Scalar:
            return cls.map(func, *scalars)
        return wrapper


    @classmethod
    def maybe(cls, f_domain: NumberFunction, f_codomain: ScalarFunction = identity) -> Union[NumberFunction, ScalarFunction]:
        def maybe_wrapper(value: Union[Number, Scalar]):
            if isinstance(value, cls.domain):
                return f_domain(value)
            elif isinstance(value, cls.codomain):
                return f_codomain(value)
            else:
                raise FunctorError(str.format(
                    ("value of type '{0}' is in neither of domain '{1}'"
                    " nor codomain '{2}' of functor '{3}'"
                    ), value.__class__, cls.domain.__name__,
                    cls.codomain.__name__, cls.__name__
                ))
        return maybe_wrapper

    @classmethod
    def maybe_not(cls, f_codomain: ScalarFunction, f_domain: NumberFunction = identity) -> Union[NumberFunction, ScalarFunction]:
        def maybe_not_wrapper(value: Union[Number, Scalar]):
            if isinstance(value, cls.codomain):
                return f_codomain(value)
            elif isinstance(value, cls.domain):
                return f_domain(value)
            else:
                raise FunctorError(str.format(
                    ("value of type '{0}' is in neither of domain '{1}'"
                    " nor codomain '{2}' of functor '{3}'"
                    ), value.__class__, cls.domain.__name__,
                    cls.codomain.__name__, cls.__name__
                ))
        return maybe_func



    @classmethod
    def apply(cls, func: NumberFunction, *values: Tuple[Union[Number, Scalar], ...]) -> Scalar:
        return cls.construct(
            func(*tuple(
                value.value if isinstance(value, Scalar) else value
                for value in values
            ))
        )
