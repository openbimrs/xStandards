import unittest

import openbim_xbreitband


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xbreitband.STANDARD_NAME, "XBreitband")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xbreitband.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
