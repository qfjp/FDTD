"""
.. module:: units
   :platform: Unix, Windows
   :synopsis: An attempt to define units as they are used in Geant4,
              where we can multiply by units to 'type' certain
              scalars, and divide by  units to get the corresponding
              value.

.. moduleauthor:: Daniel Pade <djpade@gmail.com>
"""
# Defines units which we can use as types
from enum import Enum

import numpy as np

from tags.tags import deprecated

# pylint: disable=no-member
NUM_TYPES = [int, float, np.int8, np.int16, np.int32, np.int64,
             np.uint8, np.uint16, np.uint32, np.uint64, np.float16,
             np.float32, np.float64, np.complex64, np.complex128]
# pylint: enable=no-member


class UnitType(Enum):
    """ Base SI Unit Categories """

    CHARGE = 'charge'
    """ SI units of charge """

    LENGTH = 'length'
    """ SI units of length """

    MASS = 'mass'
    """ SI units of mass """

    TIME = 'time'
    """ SI units of time """

    def __lt__(self, other):
        """
        Defines less than over UnitTypes.
        This method is necessary so we can sort lists of UnitTypes,
        ultimately so we can cancel out units during multiplication or
        division.
        This function can be arbitrary, so long as it is consistent and
        gives a unique value between all pairs.

        :type  other: UnitType
        :param other: the unit on the right side of the '<' sign

        :return: True if the value of self is less than the value of other.
        """
        if isinstance(other, UnitType):
            return self.value < other.value


class Unit:
    # pylint: disable=too-few-public-methods
    """
    Defines a Unit in order to make physics calculations 'typesafe'.

    Units should be used to make physics calculations that are
    checked by the program for sensibility. In order to retrieve the
    scalar value, one can simply divide by the units used. For example,
    if we have the following values:

    >>> meter  = Unit("meter", "m", {(1, UnitType.LENGTH)})
    >>> foot   = .305 * meter
    >>> height = 1.6 * meter

    We can use the following code to get the result in meters:

    >>> print(height / meter)
    1.6

    Or if we want it in feet:

    >>> print(height / foot)
    5.245901639244163

    We can also define compound units like so:

    >>> kilogram = Unit("kilogram", "kg", {(1, UnitType.MASS)})
    >>> second   = Unit("second", "s", {(1,UnitType.TIME)})
    >>> newton   = kilogram * meter / second ** 2

    and still convert between compound units:

    >>> pound = 4.448222 * newton
    >>> print(100 * pound / newton)
    444.822

    If you want to keep values type safe, you don't have to divide by
    any units:

    >>> print(100 * pound)
    444.822 * kg * m * s^-2
    """

    def __eq__(self, other):
        """
        Defines equality of units by the category and value.

        :param other: the other unit to test equality with self.
        :type  other: Unit

        :return: True if the categories and values of self and other
                match, False otherwise
        """
        if not isinstance(other, Unit):
            return False
        return self.category == other.category and \
            self.value == other.value

    def __init__(self, name, symbol, category, value=1):
        """
        Constructs a new unit type.

        :param name:     The name of the unit, as a string
        :type  name:     String

        :param symbol:   The SI unit symbol, as a string
        :type  symbol:   String

        :param category: A set of tuples of the form (int, UnitType),
                         where int is the power of the base unit, and
                         UnitType is a base unit. For example, a meter
                         would have a category of (1, UnitType.LENGTH)
        :type category: {(int,UnitType)}

        :param value:    This is how the unit is internally stored as a
                         number.
        :type  value:    Number
        """
        self.name = name
        self.symbol = symbol
        self.category = category
        self.value = value

    @staticmethod
    def _is_number(obj):
        """
        Checks whether a given object is a number as defined in the
        NUM_TYPES array
        :param obj: a generic object
        :type obj: object

        :returns: True if the object is a number
        """
        is_number = False
        for tpe in NUM_TYPES:
            if isinstance(obj, tpe):
                is_number = True
                break
        return is_number

    def __mul__(self, other):
        """
        Defines multiplication of units with other units or scalars.

        Only applies to left-multiplication, where self is on the left.

        :param other: The object to multiply by
        :type  other: Unit | Number | np.ndarray
        :returns: A scalar if all the units cancel, otherwise a new
                  unit type
        """
        # pylint: disable=no-member
        is_number = self._is_number(other)
        if is_number:
            if other == 0:
                return 0
            return Unit(self.name, self.symbol, self.category,
                        self.value * other)
        elif isinstance(other, np.ndarray):
            new_arr = np.empty(other.shape, dtype=object)
            if other.dtype.kind in ['i', 'f', 'c']:
                for i, item in enumerate(other.flat):
                    new_arr.flat[i] = Unit(self.name, self.symbol,
                                           self.category,
                                           self.value * item)
            else:
                for i, item in enumerate(other.flat):
                    new_arr.flat[i] = self * item

            return new_arr
        elif isinstance(other, Unit):
            new_cat = Unit._merge_categories(self.category, other.category)

            new_val = self.value * other.value
            new_unit = Unit(None, None, new_cat, new_val)

            # If everything cancels, return a scalar
            if new_unit.category == set():
                return new_unit.value

            # Otherwise, return a new unit
            return new_unit
        else:
            raise ArithmeticError("({0}) and ({1}) cannot be multiplied"
                                  .format(type(self), type(other)))
        # pylint: enable=no-member

    def __pow__(self, other):
        """
        Defines raising a unit to an integral power.

        :param other: The exponent
        :type other: integer
        """
        if isinstance(other, int):
            new_unit = self
            for _ in range(0, other - 1):
                new_unit = new_unit * self
            return new_unit
        else:
            raise ArithmeticError('Can only raise units to integral powers')

    def __rmul__(self, other):
        """
        Defines multiplication of units with other units or scalars.

        Only applies to right-multiplication, where self is on the right

        :param other: The object to multiply by
        :type  other: Unit | number
        :return: A scalar if all the units cancel, otherwise a new unit
                type
        """
        return self * other

    def __str__(self):
        """
        Gives a string representation of the unit as 'value * symbol'.

        :return: the string 'self.value * self.symbol'
        """
        self._set_name_and_symbol()
        return "{0} * {1}".format(self.value, self.symbol)

    def __truediv__(self, other):
        """
        Defines division of units in terms of multiplying
        reciprocal units.

        :param other: The unit to divide self by
        :type  other: Unit | number

        :return: A scalar if all the units cancel, otherwise a new unit
                 type
        """
        if isinstance(other, int) or isinstance(other, float):
            return self * (1 / other)
        elif isinstance(other, Unit):
            new_cat = set()
            new_val = 1 / other.value
            for (power, unit_type) in other.category:
                new_cat = new_cat.union({(-power, unit_type)})
            div_unit = Unit(other.name, other.symbol, new_cat, new_val)
            return self * div_unit

    @staticmethod
    def _format_name(unit, power):
        """
        Quick formatting of a unit,power pair into a string.

        Mainly used to get rid of (^1) in name and symbol strings

        :param unit:  Either the name or symbol of a unit
        :type  unit:  String
        :param power: A power of a unit
        :type  power: Integer
        :return: The unit name if the power is 1, otherwise 'unit^power'
        """
        if power == 1:
            return unit
        else:
            return '{0}^{1}'.format(unit, power)

    @staticmethod
    def _name_list_to_string(elems):
        """
        Formats a list of units into a human readable string, separated
        by spaces.

        :param elems: The list of units
        :type  elems: [Unit]
        :return: A human readable string of units raised to powers
        """
        elem_string = ""
        for (i, elem) in enumerate(elems):
            if i == 0:
                elem_string = elem
                continue
            elem_string += " * {0}".format(elem)
        return elem_string

    @staticmethod
    def _merge_categories(category1, category2):
        """
        Merge two unit categories.

        :param category1: A set of tuples of the form (int, UnitType),
                          where int is the power of the base unit,
                          and UnitType is a base unit.
        :type  category1: {(int,UnitType)}
        :param category2: A set of tuples to merge with category1
        :type  category2: {(int,UnitType)}
        :return: If all unittypes are distinct, this is just the union of
                the two categories. If a tuple in each shares a unittype,
                then the merged category contains (pow1 + pow2, UnitType),
                where powI is the exponent of the i'th tuple
        """
        category_list = []
        for tpl in category1:
            category_list.append(tpl)
        for tpl in category2:
            category_list.append(tpl)

        category_list = sorted(category_list, key=lambda tpl: tpl[1])

        prv_powr = 0
        prv_unit = None
        new_cat = set()
        for (i, cur_cat) in enumerate(category_list):
            cur_powr = cur_cat[0]
            cur_unit = cur_cat[1]
            new_powr = cur_powr
            if i == 0:
                prv_powr = cur_powr
                prv_unit = cur_unit
                new_cat.add((new_powr, cur_unit))
                continue

            if cur_unit == prv_unit:
                new_powr = prv_powr + cur_powr
                new_cat.remove((prv_powr, prv_unit))

            if new_powr != 0:
                new_cat.add((new_powr, cur_unit))

            prv_powr = cur_powr
            prv_unit = cur_unit

        return new_cat

    def _set_name_and_symbol(self):
        """
        Constructs the name and symbol based on the tuples in category.
        """
        names = []
        symbs = []
        for (power, unit_type) in self.category:
            # if power == 0:
            #     # remove items with a power of 0
            #     self.category.remove((power,unit_type))
            #     continue
            # Construct the name and symbol strings
            if unit_type == UnitType.CHARGE:
                names.append(Unit._format_name('coulomb', power))
                symbs.append(Unit._format_name('C', power))
            if unit_type == UnitType.LENGTH:
                names.append(Unit._format_name('meter', power))
                symbs.append(Unit._format_name('m', power))
            if unit_type == UnitType.MASS:
                names.append(Unit._format_name('kilogram', power))
                symbs.append(Unit._format_name('kg', power))
            if unit_type == UnitType.TIME:
                names.append(Unit._format_name('second', power))
                symbs.append(Unit._format_name('s', power))
        names = sorted(names)
        symbs = sorted(symbs)
        self.name = Unit._name_list_to_string(names)
        self.symbol = Unit._name_list_to_string(symbs)

    @deprecated
    def _remove_cancellations(self):
        """
        Removes entries from self.category that have a power of 0.
        """
        categories = set()
        for cat in self.category:
            categories.add(cat)
        for (power, unit_type) in categories:
            if power == 0:
                # remove items with a power of 0
                self.category.remove((power, unit_type))
                continue

    def __add__(self, other):
        """
        Defines Addition of units with other units

        :param other: The object to add
        :type  other: Unit
        :return: A unit of the same type, or 0 if both sum to 0
        """
        if isinstance(other, Unit) and other.category == self.category:
            if self.value + other.value == 0:
                return 0
            return Unit(self.name, self.symbol, self.category,
                        self.value + other.value)
        else:
            raise ArithmeticError("({0}) and ({1}) don't match units"
                                  .format(self, other))

    def __neg__(self):
        """
        Defines negation of a unit
        """
        return Unit(self.name, self.symbol, self.category, -self.value)

    def __sub__(self, other):
        """
        Defines Subtraction of units with other units

        A simple wrapper around addition

        :param other: The object to add
        :type  other: Unit
        :return: A unit of the same type, or 0 if both sum to 0
        """
        if isinstance(other, Unit) and other.category == self.category:
            return self + (-other)
        else:
            raise ArithmeticError("({0}) and ({1}) don't match units"
                                  .format(self, other))


def parse_dimensions(string):
    """
    Convert a String representing a value with units into the
    corresponding python object. Currently only handles units of length
    """
    string = string.split()
    value = float(string[0])
    units_str = string[1]

    if 'meter' in units_str:
        prefix = units_str.split('meter')[0]
        mult = convert_metric_prefix(prefix)
        return value * meter * mult
    elif 'inch' in units_str:
        return value * inch


def convert_metric_prefix(string):
    """
    Takes a string that represents a metric prefix and converts it
    into the equivalent multiplier
    """
    def test_upper(string):
        """
        Test the metric prefixes above 1
        """
        factor = 1
        if string == 'yotta':
            factor = int(1e24)
        elif string == 'zetta':
            factor = int(1e21)
        elif string == 'exa':
            factor = int(1e18)
        elif string == 'peta':
            factor = int(1e15)
        elif string == 'tera':
            factor = int(1e12)
        elif string == 'giga':
            factor = int(1e9)
        elif string == 'mega':
            factor = int(1e6)
        elif string == 'kilo':
            factor = int(1e3)
        elif string == 'hecto':
            factor = int(1e2)
        elif string == 'deca':
            factor = int(1e1)
        return factor

    def test_lower(string):
        """
        Test the metric prefixes below 1
        """
        factor = 1
        if string == 'deci':
            factor = 1e-1
        elif string == 'centi':
            factor = 1e-2
        elif string == 'milli':
            factor = 1e-3
        elif string == 'micro':
            factor = 1e-6
        elif string == 'nano':
            factor = 1e-9
        elif string == 'pico':
            factor = 1e-12
        elif string == 'femto':
            factor = 1e-15
        elif string == 'atto':
            factor = 1e-18
        elif string == 'zepto':
            factor = 1e-21
        elif string == 'yocto':
            factor = 1e-24
        return factor

    string = string.lower()
    factor = 1
    factor = test_upper(string)
    if factor > 1:
        return factor
    factor = test_lower(string)
    if factor < 1:
        return factor
    return factor


# pylint: disable=invalid-name
meter = Unit('meter', 'm', {(1, UnitType.LENGTH)})
""" SI Unit of length """

coul = Unit('coulomb', 'C', {(1, UnitType.CHARGE)})
""" SI Unit of charge """

kilogram = Unit('kilogram', 'kg', {(1, UnitType.MASS)})
""" SI Unit of mass """

second = Unit('second', 's', {(1, UnitType.TIME)})
""" SI Unit of time """

newton = 1 * kilogram * meter / second ** 2
""" SI Unit of force """

farad = 1 * coul ** 2 / (newton * meter)
""" SI Unit of capacitance """

ampere = 1 * coul / second
""" SI Unit of current """

henry = 1 * kilogram * meter * meter / (coul * coul)
""" SI Unit of inductance """

foot = .305 * meter
""" Standard imperial unit of length """

inch = 1 / 12 * foot
""" Imperial unit of length roughly equivalent to the centimeter """

pound = 4.448222 * newton
""" Imperial unit of force """
