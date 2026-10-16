import unittest

import openbim_xvergabe


class Smoke(unittest.TestCase):
    def test_names_the_standard(self):
        self.assertEqual(openbim_xvergabe.STANDARD_NAME, "XVergabe")

    def test_reports_a_version(self):
        self.assertRegex(openbim_xvergabe.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
