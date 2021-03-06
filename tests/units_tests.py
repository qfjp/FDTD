"""
Unit tests for units.py module
"""
# pylint: disable=pointless-statement

import fdtd.units

import unittest

import numpy as np

U = fdtd.units
Unit = fdtd.units.Unit


class TestUnitOperators(unittest.TestCase):
    """
    Unit tests for operator overloading in Unit class
    """

    def setUp(self):

        self.meter = U.Unit('meter', 'm', {(1, U.UnitType.LENGTH)})
        self.meter2 = Unit('meter^2', 'm^2', {(2, U.UnitType.LENGTH)})
        self.second = U.Unit('second', 's', {(1, U.UnitType.TIME)})
        self.kgram = U.Unit('kilogram', 'kg', {(1, U.UnitType.MASS)})

        self.imeter = U.Unit('meter', 'm', {(-1, U.UnitType.LENGTH)})
        self.isecond = U.Unit('second', 's', {(-1, U.UnitType.TIME)})
        self.ikgram = U.Unit('kilogram', 'kg', {(-1, U.UnitType.MASS)})

    def test_add(self):
        """
        + and - operations
        """
        self.assertEqual(self.meter + self.meter, 2 * self.meter)
        with self.assertRaises(ArithmeticError):
            self.meter + self.second
        with self.assertRaises(ArithmeticError):
            self.meter + 2

        self.assertEqual(self.meter - self.meter, 0)
        self.assertEqual(2 * self.meter - self.meter, self.meter)

        with self.assertRaises(ArithmeticError):
            self.meter - self.second

        with self.assertRaises(ArithmeticError):
            self.second - 1

    def test_eq(self):
        """
        == and !=
        """
        # UnitType tests
        self.assertFalse(self.meter == self.second)
        self.assertTrue(self.meter != self.second)

        self.assertFalse(self.meter2 == self.meter)
        self.assertTrue(self.meter2 != self.meter)

        # Python types match?
        self.assertFalse(self.meter == 1)

        # Equal
        self.assertTrue(U.second == U.second)
        self.assertFalse(U.second == U.foot)

        # Not equal
        self.assertTrue(U.second != U.foot)
        self.assertFalse(U.second != U.second)

    def test_mul(self):
        """
        * operator
        """
        met_sec = Unit('meter * second', 'm * s', {(1, U.UnitType.LENGTH),
                                                   (1, U.UnitType.TIME)})
        self.assertEqual(self.meter * self.meter, self.meter2)
        self.assertEqual(self.meter * self.second, met_sec)

        self.assertNotEqual(self.meter * self.meter, self.meter)

        self.assertEqual(1 * self.meter, self.meter)
        self.assertNotEqual(2 * self.meter, self.meter)

        self.assertEqual(self.meter * 1, self.meter)
        self.assertNotEqual(self.meter * 2, self.meter)

        self.assertEqual(1.0 * self.meter, self.meter)
        self.assertNotEqual(1.1 * self.meter, self.meter)

        self.assertEqual(self.meter * 1.0, self.meter)
        self.assertNotEqual(self.meter * 1.1, self.meter)

        self.assertEqual(self.meter * 0, 0)
        self.assertEqual(self.meter * 0.0, 0)

        with self.assertRaises(ArithmeticError):
            self.meter * "hey"

    def test_pow(self):
        """
        ** operator
        """
        self.assertEqual(self.meter ** 2, self.meter2)
        self.assertNotEqual(self.meter ** 2, self.meter)

        with self.assertRaises(ArithmeticError):
            self.meter ** 2.2

    def test_str(self):
        """
        Test str() on units
        """
        self.assertEqual(str(self.meter), "1 * m")

        newton = self.kgram * self.meter / (self.second ** 2)

        self.assertEqual(str(newton), "1.0 * kg * m * s^-2")

    def test_div(self):
        """
        / operator
        """
        self.assertEqual(2.2 * self.meter / self.meter, 2.2)
        self.assertNotEqual(2.2 * self.meter / self.second, 2.2)

        newton = self.kgram * self.meter / (self.second ** 2)
        self.assertEqual(newton / self.kgram,
                         self.meter / (self.second ** 2))
        self.assertNotEqual(newton / self.kgram,
                            self.meter / (self.second ** 1))

        self.assertEqual(self.meter / 1, self.meter)
        self.assertEqual(self.meter / 1.0, self.meter)

        self.assertNotEqual(self.meter / 2, self.meter)
        self.assertNotEqual(self.meter / 2.0, self.meter)

        self.assertEqual(self.meter / 2, self.meter * (1 / 2))

        with self.assertRaises(ZeroDivisionError):
            self.meter / 0

    def test_cancellations(self):
        """
        Make sure units cancel properly
        """
        self.assertEqual(self.meter * self.imeter, 1)
        self.assertEqual(self.second * self.isecond, 1)
        self.assertEqual(self.kgram * self.ikgram, 1)

    def test_convert(self):
        """
        Test physical conversions between units
        """
        height = 1.6 * self.meter
        foot = .305 * self.meter
        inch = 1 / 12 * foot

        self.assertTrue(abs(height / foot - 5.246) < .001)
        self.assertTrue(abs(height / inch - 62.951) < .001)

        newton = self.kgram * self.meter / (self.second ** 2)
        pound = 4.448222 * newton
        accel = 9.8 * self.meter / (self.second ** 2)

        weight = 150 * pound
        mass = weight / accel
        self.assertTrue(abs(mass / self.kgram - 68.085) < .001)

    def test_array_mult(self):
        """
        test multiplying arrays, units, and arrays of units
        """
        # pylint: disable=no-member
        ident_2_2 = np.array([[1, 1], [1, 1]])

        # Unit times a 2D array
        meter_ident_2_2 = self.meter * ident_2_2
        self.assertEqual(meter_ident_2_2[0][0], self.meter)
        self.assertEqual(meter_ident_2_2[0][1], self.meter)
        self.assertEqual(meter_ident_2_2[1][0], self.meter)
        self.assertEqual(meter_ident_2_2[1][1], self.meter)

        # 2D arrays multiplying each other (arrays multiply point by
        # point)
        matr_2_2 = np.array([[1, 2], [3, 4]])
        matr_mult = meter_ident_2_2 * matr_2_2
        self.assertEqual(matr_mult[0][0], self.meter)
        self.assertEqual(matr_mult[0][1], 2 * self.meter)
        self.assertEqual(matr_mult[1][0], 3 * self.meter)
        self.assertEqual(matr_mult[1][1], 4 * self.meter)


if __name__ == '__main__':
    unittest.main()
