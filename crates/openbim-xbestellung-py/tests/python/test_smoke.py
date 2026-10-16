import unittest

import openbim_xbestellung


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xbestellung.STANDARD_NAME, "XBestellung")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xbestellung.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
