import functools
from typing import Union

from .base import UnitMeta


class NotPassed:
    """Used to distinguish between when an argument was passed as None, or
    simply wasn't passed in at all."""


@functools.total_ordering
class Dimension(metaclass=UnitMeta):
    """Fundamental value-less unit. 'feet'/'seconds'.
    Should have special handling of NullUnit in the constructor
    """
    registry = {}

    def __new__(cls, identifier: Union[None, int, NotPassed] = NotPassed):
        if identifier in cls.registry:
            return cls.registry[identifier]
        else:
            self = super(cls).__new__(cls, identifier)
            self.__init__(identifier)
            cls.registry[identifier] = self
            return self

    def __init__(self, identifier: Union[None, int, NotPassed] = NotPassed):
        """Explicitly passing in 'None' for identifier should make this the NullUnit"""
        self.identifier = identifier

    @classmethod
    def zero(cls):
        return NullUnit

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.identifier)

    def __eq__(self, other):
        if isinstance(other, Dimension):
            if self.identifier == other.identifier:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __lt__(self, other):
        """Only compares Dimensions.
        Compares as Tuple[str] except treats 'None' as less than all others
        This is used in giving a standard representation to
        compound dimensions, such as:
            feet * pounds  ~  (feet, pounds)   and not (pounds, feet)
        """
        if not isinstance(other, Dimension):
            return NotImplemented
        else:
            # Treat 'None' as less than all strings
            is_none = (self.identifier is None, other.identifier is None)
            if is_none == (False, False):
                return self.identifier < other.identifier
            elif is_none == (True, False):
                return True
            elif is_none == (False, True):
                return False
            else:
                # is_none == (True, True):
                # default - when both are None treat left as less than right
                return True


NullUnit = Dimension('NullUnit')
