import unittest

import openbim_xbau


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xbau.STANDARD_NAME, "XBau")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xbau.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
