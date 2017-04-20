import functools
import operator
from typing import (
    Callable, Tuple, Union, Optional, Callable,
    Type, TypeVar, Generic, Any, ClassVar
)
from abc import ABCMeta, abstractmethod, abstractproperty

from .base import UnitMeta
from .functor import Functor, InvariantFunctor


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
        return self.functor.bind(operator.__add__, self, a)

    def __radd__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__add__, a, self)

    def __sub__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__sub__, self, a)

    def __rsub__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__sub__, a, self)

    def __mul__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mul__, self, a)

    def __rmul__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mul__, a, self)

    def __truediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__truediv__, self, a)

    def __rtruediv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__truediv__, a, self)

    def __floordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__floordiv__, self, a)

    def __rfloordiv__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__floordiv__, a, self)

    def __mod__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mod__, self, a)

    def __rmod__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__mod__, a, self)

    def __pow__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__pow__, self, a)

    def __rpow__(self, a: EitherDomain) -> Codomain:
        return self.functor.bind(operator.__pow__, a, self)
