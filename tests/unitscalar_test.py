import unittest
from unitscalar import UnitScalar

class UnitScalarTest(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_everything(self):
        """Basic functional tests of core module functionality"""
        # Trivial unit
        self.assertTrue(UnitScalar(3.14, "m").__str__() == "3.14 m")
        self.assertTrue(UnitScalar(3.14, "1/m").__str__() == "3.14 1/m")
        self.assertTrue(UnitScalar(3.14, "m/s").__str__() == "3.14 m/s")
        self.assertTrue(UnitScalar(3.14, "m/s2").__str__() == "3.14 m/s2")
        self.assertTrue(UnitScalar(3.14, "m2/s2").__str__() == "3.14 m2/s2")

        # Unit string parsing tests
        self.assertTrue(UnitScalar._parse_units("m") == ([UnitScalar.SimpleUnit("m", 1)], [], 1))
        self.assertTrue(UnitScalar._parse_units("s") == ([UnitScalar.SimpleUnit("s", 1)], [], 1))
        self.assertTrue(UnitScalar._parse_units("m2") == ([UnitScalar.SimpleUnit("m", 2)], [], 1))
        self.assertTrue(UnitScalar._parse_units("m3") == ([UnitScalar.SimpleUnit("m", 3)], [], 1))
        self.assertTrue(UnitScalar._parse_units("m22") == ([UnitScalar.SimpleUnit("m", 22)], [], 1))
        self.assertTrue(UnitScalar._parse_units("m2 s4") == ([UnitScalar.SimpleUnit("m", 2), UnitScalar.SimpleUnit("s", 4)], [], 1))
        self.assertTrue(UnitScalar._parse_units("m s4") == ([UnitScalar.SimpleUnit("m", 1), UnitScalar.SimpleUnit("s", 4)], [], 1))
        self.assertTrue(UnitScalar._parse_units("1/m") == ([], [UnitScalar.SimpleUnit("m", 1)], 1))
        self.assertTrue(UnitScalar._parse_units("1/mm") == ([], [UnitScalar.SimpleUnit("m", 1)], 1000))
        self.assertTrue(UnitScalar._parse_units("mm/mm") == ([UnitScalar.SimpleUnit("m", 1)], [UnitScalar.SimpleUnit("m", 1)], 1))

        # Unit fraction reduction tests
        self.assertTrue(UnitScalar._reduce_units([UnitScalar.SimpleUnit("m", 1)], [UnitScalar.SimpleUnit("m", 1)]) == ([], []))
        self.assertTrue(UnitScalar._reduce_units([UnitScalar.SimpleUnit("m", 2)], [UnitScalar.SimpleUnit("m", 1)]) == ([UnitScalar.SimpleUnit("m", 1)], []))
        self.assertTrue(UnitScalar._reduce_units([UnitScalar.SimpleUnit("m", 1)], [UnitScalar.SimpleUnit("m", 2)]) == ([], [UnitScalar.SimpleUnit("m", 1)]))

        # Equality testing
        self.assertTrue(UnitScalar(3.14, "m") != UnitScalar(3, "m"))
        self.assertTrue(UnitScalar(3.14, "m") != UnitScalar(3.14, "s"))
        self.assertTrue(UnitScalar(3.14, "m s") == UnitScalar(3.14, "s m"))

        # Basic arithmetic checkouts
        self.assertTrue(UnitScalar(3.14, "m") + UnitScalar(3.14, "m") == UnitScalar(6.28, "m"))
        self.assertTrue(UnitScalar(3.14, "m") - UnitScalar(1.14, "m") == UnitScalar(2, "m"))
        self.assertTrue(UnitScalar(3.14, "m/s") * UnitScalar(3.14, "1/s") == UnitScalar(3.14 ** 2, "m/s2"))
        self.assertTrue(UnitScalar(3.14, "m/s") / UnitScalar(3.14, "1/s") == UnitScalar(1, "m"))
        self.assertTrue(UnitScalar(3.14, "m/s") ** 2 == UnitScalar(3.14 ** 2, "m2/s2"))
        self.assertTrue(UnitScalar(3.14, "m/s2") ** 3 == UnitScalar(3.14 ** 3, "m3/s6"))
        self.assertTrue(UnitScalar(2.0, "") + 1 == UnitScalar(3, ""))
        self.assertTrue(1 + UnitScalar(2.0, "") == UnitScalar(3, ""))
        self.assertTrue(UnitScalar(2.0, "") / 3 == UnitScalar(2/3, ""))
        self.assertTrue(1 / UnitScalar(2.0, "") == UnitScalar(1/2, ""))

        # Verifying unit agreement between different units
        self.assertTrue(UnitScalar(1.0, "lbf").units_agree("kg m/s2"))
        self.assertTrue(UnitScalar(1.0, "kg m/s2").units_agree("lbf"))
        self.assertFalse(UnitScalar(1.0, "kg").units_agree("lbf"))



if __name__ == '__main__':
    unittest.main()
