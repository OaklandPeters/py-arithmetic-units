import functools
import operator
from typing import (
    Callable, Tuple, Union, Optional, Callable,
    Type, TypeVar, Generic, Any, ClassVar
)
from abc import ABCMeta, abstractmethod, abstractproperty

from .base import UnitMeta


# Domain & Codomain: typecheckable Type objects.
# For all actual concrete instances in the domain and codomain:
#       assert(isintance(domain_element, Domain) == True)
#       assert(isinstance(codomain_element), Codomain) == True)
# Note - this is simplest & easiest when Domain and Codomain are
#   concrete classes (such as Scalar) - but they can be abstract types,
#   unions, or interfaces as well (such as numbers.Number).
Domain = TypeVar('Domain')
Codomain = TypeVar('Codomain')
EitherDomain = Union[Domain, Codomain]
# These two function signatures should be variant on number of arguments. IE
#       DomainFunction = Callable[Tuple[Domain, ...], Domain]
# But Python 3.5 cannot handle this
# So we do the best we can, which is:
DomainFunction = Callable[[Domain], Domain]
CodomainFunction = Callable[[Codomain], Codomain]


class Functor(Generic[Domain, Codomain], metaclass=ABCMeta):
    """
    Takes two objects in the domain, and a function on those, and applies it.

    Note - this is *not* a monad - because it is not a container.
    It is intended for Scalar and other UnitsLeaf objects - which cannot
    contain other Scalar or UnitsLeaf objects.

    Note - technically this is an Invariant Functor - since it has the
    ability to construct and destruct.

    Abstracts:
        construct
        map
    """
    Domain: ClassVar[Type[Domain]]
    Codomain: ClassVar[Type[Codomain]]

    def __init__(self, domain: Type[Domain], codomain: Type[Domain]):
        self.Domain = domain
        self.Codomain = codomain

    @abstractmethod
    def construct(self, domain: Domain) -> Codomain:
        return NotImplemented

    @abstractmethod
    def map(self, func: DomainFunction,
            *codomains: Tuple[Codomain, ...]) -> Codomain:
        return NotImplemented

    def lift(self, func: DomainFunction) -> CodomainFunction:
        @functools.wraps(func)
        def wrapper(*scalars: Tuple[Scalar, ...]) -> Scalar:
            return self.map(func, *scalars)
        return wrapper


class InvariantFunctor(Functor, Generic[Domain, Codomain], metaclass=ABCMeta):
    """
    An InvariantFunctor is a Functor which can map in both directions,
    forward (Domain --> Codomain) and reverse (Codomain --> Domain).

    This allows us to implement map in terms of self.destruct.
    Note - this doesn't work in general - but it *does* work for our
    use-case (Scalar wrapping Number).

    This Functor presumes that it's Domain and Codomain are non-overlapping.
    If not, the 'apply' function may have incorrect behavior.

    Abstracts:
        destruct
        construct
    """
    @abstractmethod
    def destruct(self, codomain: Codomain) -> Domain:
        """Inverse of 'construct'. Translates codomain elements into domain."""
        return NotImplemented

    def delift(self, func: CodomainFunction) -> DomainFunction:
        @functools.wraps(func)
        def wrapper(*domains: Tuple[Domain, ...]) -> Domain:
            return func(
                *tuple(self.destruct(elm) for elm in domains)
            )
        return wrapper

    def map(self, func: DomainFunction,
            *codomains: Tuple[Codomain, ...]) -> Codomain:
        return self.construct(
            func(
                *tuple(self.destruct(arg) for arg in codomains)
            )
        )

    def demap(self, func: CodomainFunction,
              *domains: Tuple[Domain, ...]) -> Domain:
        return self.destruct(
            func(
                *tuple(self.construct(arg) for arg in domains)
            )
        )

    def apply(self, func: DomainFunction,
              *values: Tuple[EitherDomain, ...]) -> Codomain:
        """
        The .map function, but dispatches on category, so elements of codomain are
        destructed into the domain before mapping.

        Warning - 'apply' depends on Domain and Codomain to be non-overlapping.

        Allows functions to take either domain or codomain elements.
        Thus, statements like this can work:
            Unit(5) + 4
            Unit(5) + Unit(4)
        """
        _domains = tuple(
            value if isinstance(value, self.Domain)
            else self.destruct(value)
            for value in values
        )
        # _values = tuple(value if not isinstance(value, self.Codomain)
        #                     else self.destruct(value)
        #                 for value in values)
        return self.construct(func(*_domains))


class ArithmeticSyntaxMixin(Generic[Domain, Codomain], metaclass=UnitMeta):
    """Provides arithmetic operators for a class.

    The 'functor' property should be over-ridden to provide
    a class-specific functor version based
    on the concrete class at run-time.

    Abstracts:
        functor
    """
    functor: InvariantFunctor[Domain, Codomain]

    def __add__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__add__, self, a)

    def __radd__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__add__, a, self)

    def __sub__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__sub__, self, a)

    def __rsub__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__sub__, a, self)

    def __mul__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__mul__, self, a)

    def __rmul__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__mul__, a, self)

    def __truediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__truediv__, self, a)

    def __rtruediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__truediv__, a, self)

    def __floordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__floordiv__, self, a)

    def __rfloordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__floordiv__, a, self)

    def __mod__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__mod__, self, a)

    def __rmod__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__mod__, a, self)

    def __pow__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__pow__, self, a)

    def __rpow__(self, a: EitherDomain) -> Codomain:
        return self.functor.apply(operator.__pow__, a, self)
