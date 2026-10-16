import unittest

import openbim_xrechnung


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xrechnung.STANDARD_NAME, "XRechnung")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xrechnung.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
