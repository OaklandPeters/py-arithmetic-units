"""
Run tests with:
cd SubtypeUnits\
py -m unittest units_test
"""
import unittest
import pdb
from typing import Mapping
from numbers import Number
from py_units.dimension import Dimension, NullUnit
from py_units.units import (
    UnitsType,
    Unit,
    UnitsLeaf,
    Scalar,
    UnitsFunction,
    Multiply,
    Divide,
    UnitsStem,
    UnitVector
)




def validate_types(test, subject, type_mapping: Mapping[type, bool]):
    """Helper function for extensive type checking."""
    for _type, expectation in type_mapping.items():
        if expectation:
            test.assertIsInstance(subject, _type,
                str.format(
                    "Type AssertionError: {0} is not an instance of {1}",
                    repr(subject), _type)
            )
        else:
            test.assertNotIsInstance(subject, _type,
                str.format(
                    "Type AssertionError: {0} is incorrectly an instance of {1}",
                    repr(subject), _type)
            )


class UnitsTests(unittest.TestCase):
    def _validate_scalar(self, scalar, expected_value):
        # Checking type hierarchy
        validate_types(self, scalar, {
            Scalar: True,
            UnitVector: False,
            UnitsLeaf: True,
            Unit: True,
            UnitsType: True,
            UnitsStem: False,
            Dimension: False,
            Number: False
        })
        # Checking the internals
        # try:
        self.assertIsInstance(scalar.dimension, Dimension)
        self.assertEqual(scalar.dimension, NullUnit)
        self.assertIsInstance(scalar.value, Number)
        self.assertEqual(scalar.value, expected_value)
        # except AssertionError as exc:
        #     print()
        #     print("exception: ", exc)
        #     print("scalar: ", repr(scalar))
        #     pdb.set_trace()
        # String representation
        self.assertEqual(str(scalar), str(expected_value))

    def _validate_unit_vector(self, unit_vector, expected_dimension, expected_value):
        # Checking type hierarchy
        validate_types(self, unit_vector, {
            Scalar: False,
            UnitVector: True,
            UnitsLeaf: True,
            Unit: True,
            UnitsType: True,
            UnitsStem: False,
            Dimension: False,
            Number: False
        })
        # Checking the internals
        self.assertIsInstance(unit_vector.dimension, Dimension)
        self.assertEqual(unit_vector.dimension, expected_dimension)
        self.assertIsInstance(unit_vector.value, Number)
        self.assertEqual(unit_vector.value, expected_value)
        # String representation
        if expected_value == 1:
            expected_string = str(expected_dimension)
        else:
            expected_string = "{0}^{1}".format(expected_dimension, expected_value)
        self.assertEqual(str(unit_vector), expected_string)

    def test_scalar_from_unit_function(self):
        self._validate_scalar(Unit(5), 5)

    def test_scalar_from_unitsleaf(self):
        self._validate_scalar(UnitsLeaf(21), 21)

    def test_scalar_from_direct_construction(self):
        self._validate_scalar(Scalar(17), 17)

    def test_unit_vector_from_unit_function(self):
        self._validate_unit_vector(Unit('seconds'), Dimension('seconds', 'seconds'), 1)

    def test_unit_vector_From_unitsleaf(self):
        self._validate_unit_vector(UnitsLeaf('seconds'), Dimension('seconds', 'seconds'), 1)

    def test_unit_vector_from_direct_construction(self):
        dim = Dimension('pounds')
        self._validate_unit_vector(UnitVector(dim), dim, 1)
        self._validate_unit_vector(UnitVector(dim, 3), dim, 3)






    # def test_scalar_arithmetic(self):
    #     actual = Unit(5) * Unit(4)
    #     expected = Unit(20)
    #     print(actual)
    #     pdb.set_trace()
    #     print()

    def test_dimension_registry(self):
        """Do this via checking the id() of the returned objects"""
        pass

    #---- Test ideas:
    # Unit(5) * Unit(4) == Unit(20)
    # (feet * seconds / feet * (pounds / (feet * feet)))


