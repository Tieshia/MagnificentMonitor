from unittest import TestCase
from monitor import error_threshold_logic

error_threshold = 0.25


class TestErrorThresholds(TestCase):
    """Test various levels of the error threshold."""

    def test_positive_status(self):
        self.assertTrue(error_threshold_logic(True, 0.20, error_threshold))

    def test_negative_status(self):
        self.assertFalse(error_threshold_logic(True, 0.30, error_threshold))

    def test_positive_to_negative_status(self):
        self.assertFalse(error_threshold_logic(True, 0.30, error_threshold))

    def test_negative_to_positive_switch(self):
        self.assertTrue(error_threshold_logic(False, 0.20, error_threshold))


###############################################################################

if __name__ == "__main__":
    import unittest
    unittest.main()
