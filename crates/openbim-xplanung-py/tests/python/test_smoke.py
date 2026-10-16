import unittest

import openbim_xplanung


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xplanung.STANDARD_NAME, "XPlanung")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xplanung.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
