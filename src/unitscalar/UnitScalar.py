from __future__ import annotations
from dataclasses import dataclass
import copy

class UnitScalar:
    VALID_UNITS = {
        # Unit (SI unit numerator, SI unit denominator, multiple)
        "m": ("m", "", 1.0),
        "s": ("s", "", 1.0),
        "kg": ("kg", "", 1.0),
        "C": ("C", "", 1.0),
        "K": ("K", "", 1.0),
        "in": ("m", "", 0.0254),
        "L": ("m3", "", 1e-3),
        "Hz": ("1", "s", 1.0),
        "rpm": ("1", "s", 1/60),
        "g": ("kg", "", 1e-3),
        "lbm": ("kg", "", 0.45359237),
        "J": ("kg m2", "s2", 1.0),
        "Wh": ("J", "", 3600.0),
        # "mol": ("", "", 6.02214076e23),
        # Molarity is *technically* not an SI unit, but it messes with
        # FP-precision to be multiplying/dividing by 6.02214076e23
        "mol": ("mol", "", 1.0),
        "N": ("kg m", "s2", 1.0),
        "lbf": ("kg m", "s2", 9.80665*0.45359237),
        "Pa": ("N", "m2", 1.0),
        "hPa": ("N", "m2", 1e2),    # Hectopascal
        "bar": ("N", "m2", 1e5),
        "atm": ("N", "m2", 101325.0),   # Atmosphere
        "psi": ("N", "m2", 9.80665*0.45359237/(0.0254**2)),
        "W": ("J", "s", 1.0),
        "Ah": ("C", "", 3600.0),    # Amp-Hour
        "A": ("C", "s", 1.0),
        "V": ("J", "C", 1.0),
        "ohm": ("V", "A", 1.0),
        "T": ("V s", "m2", 1.0),    # Tesla
        "F": ("C", "V", 1.0),       # Farad
        "H": ("m2 kg", "C2", 1.0),  # Henry
    }

    VALID_PREFIXES = {
        "f": 1e-15, # femto
        "p": 1e-12, # pico
        "n": 1e-9, # nano
        "u": 1e-6, # micro
        "m": 1e-3, # milli
        "k": 1e3, # kilo
        "M": 1e6, # mega
        "G": 1e9, # giga
        "T": 1e12, # tera
    }

    @dataclass
    class SimpleUnit: # Fundamental data type stored in the num_unit, den_unit lists
        unit: str # Must be a member of UnitScalar.VALID_UNITS
        exp: int

    @staticmethod
    def reduce_units(num_units: list[UnitScalar.SimpleUnit], den_units: list[UnitScalar.SimpleUnit]) -> tuple[list[UnitScalar.SimpleUnit], list[UnitScalar.SimpleUnit]]:
      i=0
      while i < len(num_units):
          j=0
          while j < len(den_units):
              if num_units[i].unit == den_units[j].unit:
                  if num_units[i].exp > den_units[j].exp:
                      num_units[i].exp = num_units[i].exp - den_units[j].exp
                      del den_units[j]
                  elif num_units[i].exp == den_units[j].exp:
                      del den_units[j]
                      del num_units[i]
                      i -= 1
                  else:
                      den_units[j].exp = den_units[j].exp - num_units[i].exp
                      del num_units[i]
                      i -= 1
              j += 1
          i += 1
      return num_units, den_units

    # Merge lists of SimpleUnit, taking care to not duplicate entries
    @staticmethod
    def merge_lists(la: list[UnitScalar.SimpleUnit], lb: list[UnitScalar.SimpleUnit]) -> list[UnitScalar.SimpleUnit]:
        out = copy.deepcopy(la)
        for x in lb:
            located = False
            for y in out:
                if y.unit == x.unit:
                    y.exp += x.exp
                    located = True
                    break
            if not located:
                out.append(copy.deepcopy(x))
        return out

    # Parse complicated unit string, e.g. "kg mm / ms2", into a list of base SI units
    # for the numerator and denominator, and a multiplication factor combining all
    # unit prefixes together
    def parse_units(unit_str: str) -> tuple[list[UnitScalar.SimpleUnit], list[UnitScalar.SimpleUnit], float]:
        split = unit_str.split("/")
        num_str = split[0] if len(split) > 0 else ""
        den_str = split[1] if len(split) > 1 else ""
        num_unit_strs = num_str.split(" ")
        den_unit_strs = den_str.split(" ")
        units_mult = 1.0

        num_unit_list = []
        den_unit_list = []

        # Parse (potentially complex) unit string, e.g. "uJ3", into a list of
        # SimpleUnits for the numerator and denominator, and a multiple to describe
        # the prefix and conversion to SI base units
        def identify_unit(unit_str: str) -> tuple[list[UnitScalar.SimpleUnit], list[UnitScalar.SimpleUnit], float]:
            # Steps:
            # 1. Break str into prefix, unit (member of VALID_UNITS), and an exponent
            # 2. Decide whether unit is a base unit (one of SI base units)
            #   a. If so, add this to the numerator units
            #   b. If not, break this into base SI units
            # 3. Return with the aformentioned numerator and denominator units, and a multiple
            # print("identify_unit (:) unit_str:", unit_str)
            num_units = []
            den_units = []
            mult = 1.0

            # Find first number in the string (exponent). Mark None if does not exist
            # https://stackoverflow.com/a/22446407/3339274
            for (idx_first_num, c) in enumerate(unit_str):
                if c.isdigit():
                    break
            else:
                idx_first_num = len(unit_str)

            # Decompose the string into a prefix, unit, and exponent
            unit = None
            # Unit is a base unit and maybe an exponent
            if unit_str[:idx_first_num] in UnitScalar.VALID_UNITS:
                unit = UnitScalar.VALID_UNITS[unit_str[:idx_first_num]]
            # Unit is a prefix, base unit, and maybe an exponent
            elif unit_str[0] in UnitScalar.VALID_PREFIXES:
                mult = UnitScalar.VALID_PREFIXES[unit_str[0]]
                unit = UnitScalar.VALID_UNITS[unit_str[1:idx_first_num]]
            else:
                raise Exception(f'Unit "{unit_str}" is not valid')

            # Apply unit multiple
            mult *= unit[2]

            # Break out the exponent as an integer
            exp = None
            if idx_first_num != len(unit_str):
                exp = int(unit_str[idx_first_num:])
            else:
                exp = 1

            # Is the unit already a single SI unit? (i.e. not composed of multiple units)
            # print(f"\"{unit[0]}\", \"{unit[1]}\"")
            if (unit[0] == "" or unit[1] == "") and ((not " " in unit[0]) and (not " " in unit[1])):
                if unit[1] == "":
                    num_units.append(UnitScalar.SimpleUnit(unit[0], exp))
                else:
                    den_units.append(UnitScalar.SimpleUnit(unit[1], exp))
            # Recurse on the numerator and denominator until the unit string is a single SI unit
            else:
                # Feed the unit back into parse_units to have it broken down into SI units
                num_units, den_units, mult_inner = UnitScalar.parse_units(f"{unit[0]} / {unit[1]}")
                # Apply outer exponent to all inner terms
                for unit in num_units:
                    unit.exp *= exp
                for unit in den_units:
                    unit.exp *= exp
                mult *= mult_inner# ** exp

            mult = mult ** exp
            # print("unit_str:", unit_str, "exp:", exp, "mult:", mult)
            # print("unit_str:", unit_str, "num_units:", num_units, "den_units:", den_units)

            return num_units, den_units, mult

        for unit_str in num_unit_strs:
            # e.g. 1/m
            if unit_str == "1":
                continue
            if unit_str == "":
                continue

            # Lists are empty, just assign to them
            num_units, den_units, mult = identify_unit(unit_str)
            # Merge into lists
            # print(f"parse_units (:) unit_str: \"{unit_str}\" merging")
            # print(f"\t{num_unit_list} <== {num_units}")
            # print(f"\t{den_unit_list} <== {den_units}")
            num_unit_list = UnitScalar.merge_lists(num_unit_list, num_units)
            den_unit_list = UnitScalar.merge_lists(den_unit_list, den_units)
            units_mult *= mult

        for unit_str in den_unit_strs:
            if unit_str == "":
                continue

            num_units, den_units, mult = identify_unit(unit_str)
            # Merge into lists
            # print(f"parse_units (:) unit_str: \"{unit_str}\" merging")
            # print(f"\t{num_unit_list} <== {den_units}")
            # print(f"\t{den_unit_list} <== {num_units}")
            num_unit_list = UnitScalar.merge_lists(num_unit_list, den_units)
            den_unit_list = UnitScalar.merge_lists(den_unit_list, num_units)
            # print(f"\t==>{num_unit_list}")
            # print(f"\t==>{den_unit_list}")
            units_mult /= mult

        # num_unit_list, den_unit_list = UnitScalar.reduce_units(num_unit_list, den_unit_list)
        return num_unit_list, den_unit_list, units_mult

    def __init__(self, num: float, unit: str):
        self.num_unit, self.den_unit, units_mult = UnitScalar.parse_units(unit)
        self.num_unit, self.den_unit = UnitScalar.reduce_units(self.num_unit, self.den_unit)
        self.num = num * units_mult

    def __str__(self):
        unit_str = ""
        for unit in self.num_unit:
            unit_str += f"{unit.unit}{unit.exp if unit.exp > 1 else ""} "
        if len(self.den_unit) > 0:
            if len(self.num_unit) > 0:
                unit_str += "/ "
            else:
                unit_str += "1 / "
        for unit in self.den_unit:
            unit_str += f"{unit.unit}{unit.exp if unit.exp > 1 else ""} "

        return f"{(self.num):.2f} {unit_str}" if abs(self.num) > 1e-2 else f"{(self.num):.2E} {unit_str}"

    # Returns in base (mKgs) units
    def __float__(self):
        return self.num

    def units_agree(self, other: UnitScalar) -> bool:
        # Substitute and reduce
        self_num_unit, self_den_unit = UnitScalar.reduce_units(self.num_unit, self.den_unit)
        oth_num_unit, oth_den_unit = UnitScalar.reduce_units(other.num_unit, other.den_unit)

        # Sort by unit string
        self_num_sort = sorted(self_num_unit, key=lambda x: x.unit)
        self_den_sort = sorted(self_den_unit, key=lambda x: x.unit)
        oth_num_sort = sorted(oth_num_unit, key=lambda x: x.unit)
        oth_den_sort = sorted(oth_den_unit, key=lambda x: x.unit)
        return self_num_sort == oth_num_sort and self_den_sort == oth_den_sort

    def __eq__(self, other):
        if not isinstance(other, UnitScalar):
            return False

        return self.units_agree(other) and self.num == other.num

    # https://docs.python.org/3/library/numbers.html#implementing-the-arithmetic-operations
    def __add__(self, other) -> UnitScalar:
        if isinstance(other, UnitScalar):
            if self.units_agree(other):
                new = UnitScalar(self.num + other.num, "")
                # https://stackoverflow.com/a/17873397/3339274
                new.num_unit = copy.deepcopy(self.num_unit)
                new.den_unit = copy.deepcopy(self.den_unit)
                return new
            else:
                raise Exception("LHS and RHS units don't agree")
        else:
            return NotImplemented

    def __sub__(self, other) -> UnitScalar:
        if isinstance(other, UnitScalar):
            if self.units_agree(other):
                new = UnitScalar(self.num - other.num, "")
                new.num_unit = copy.deepcopy(self.num_unit)
                new.den_unit = copy.deepcopy(self.den_unit)
                return new
            else:
                raise Exception("LHS and RHS units don't agree")
        else:
            return NotImplemented

    def __mul__(self, other) -> UnitScalar:
        if isinstance(other, UnitScalar):
            new = UnitScalar(self.num * other.num, "")
            new.num_unit = UnitScalar.merge_lists(self.num_unit, other.num_unit)
            new.den_unit = UnitScalar.merge_lists(self.den_unit, other.den_unit)
            new.num_unit, new.den_unit = UnitScalar.reduce_units(new.num_unit, new.den_unit)
            return new
        else:
            return NotImplemented

    def __truediv__(self, other) -> UnitScalar:
        if isinstance(other, UnitScalar):
            new = UnitScalar(self.num / other.num, "")
            new.num_unit = UnitScalar.merge_lists(self.num_unit, other.den_unit)
            new.den_unit = UnitScalar.merge_lists(self.den_unit, other.num_unit)
            new.num_unit, new.den_unit = UnitScalar.reduce_units(new.num_unit, new.den_unit)
            return new
        else:
            return NotImplemented

    def __pow__(self, power) -> UnitScalar:
        new = UnitScalar(self.num ** power, "")
        new.num_unit = copy.deepcopy(self.num_unit)
        new.den_unit = copy.deepcopy(self.den_unit)
        for i in range(len(new.num_unit)):
            new.num_unit[i].exp *= power
        for i in range(len(new.den_unit)):
            new.den_unit[i].exp *= power
        return new


# TODO: Use custom literals for common units
# TODO: Implement is_eqivalent_to to compare units to a unit descriptor string
# TODO: Implement convert_to_units for output in another format (e.g. A to uA or N to lbf)
# TODO: Vectorized artithmetic?
