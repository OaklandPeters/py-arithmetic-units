import functools
from typing import Callable, Sequence, Tuple, Union, Optional


class NotPassed:
    pass

@functools.total_ordering
class Dimension:
    """Fundamental value-less unit. 'feet'/'seconds'.
    Should have special handling of NullUnit in the constructor
    """
    # def __new__(cls, name: Union[None, str], identifier: Union[None, int]):
    #     if identifier in cls.registry:
    #         return cls.registry[identifier]
    #     else:
    #         self = super(cls).__new__(cls, name, identifier)
    #         cls.registry[identifier] = self
    #         return self


    def __init__(self, name: Union[None, str], identifier: Union[None, int, NotPassed] = NotPassed):
        """Explicitly passing in 'None' for identifier should make this the NullUnit"""
        self.name = name
        if identifier is NotPassed:
            identifier = name
        self.identifier = identifier

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.name)

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
        Compares as Tuple[str] except treats 'None' as less than
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

    @classmethod
    def zero(cls):
        return NullUnit

    registry = []

NullUnit = Dimension('NullUnit', None)
