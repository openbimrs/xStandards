import unittest

import openbim_xtrasse


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xtrasse.STANDARD_NAME, "XTrasse")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xtrasse.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
