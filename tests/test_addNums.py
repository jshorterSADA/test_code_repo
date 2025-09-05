
# tests/test_addNums.py
import unittest
import sys
import os
import logging
from unittest.mock import patch

# Add the directory containing addNums.py to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the fixed function
from addNums import add_two_numbers, correlation_ID

class TestAddTwoNumbers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure logging for the tests to capture logs if needed, but primarily to prevent console spam
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

    def test_add_two_numbers_successful_strings(self):
        """
        Test that two valid numeric strings are correctly converted and added.
        """
        self.assertEqual(add_two_numbers("5", "7"), 12)
        self.assertEqual(add_two_numbers("-10", "20"), 10)
        self.assertEqual(add_two_numbers("0", "0"), 0)

    def test_add_two_numbers_successful_integers(self):
        """
        Test that two valid integers are correctly added.
        """
        self.assertEqual(add_two_numbers(5, 7), 12)
        self.assertEqual(add_two_numbers(-10, 20), 10)
        self.assertEqual(add_two_numbers(0, 0), 0)

    def test_add_two_numbers_successful_mixed_types(self):
        """
        Test that a mix of integer and numeric string inputs are correctly handled.
        """
        self.assertEqual(add_two_numbers(5, "7"), 12)
        self.assertEqual(add_two_numbers("-10", 20), 10)

    def test_add_two_numbers_invalid_num1_raises_value_error(self):
        """
        Test that a non-numeric string for num1 raises a ValueError.
        """
        with self.assertRaisesRegex(ValueError, "Failed to convert one or both inputs to integers."):
            add_two_numbers("abc", "7")

    def test_add_two_numbers_invalid_num2_raises_value_error(self):
        """
        Test that a non-numeric string for num2 raises a ValueError.
        """
        with self.assertRaisesRegex(ValueError, "Failed to convert one or both inputs to integers."):
            add_two_numbers("5", "xyz")

    def test_add_two_numbers_invalid_both_raises_value_error(self):
        """
        Test that non-numeric strings for both inputs raise a ValueError.
        """
        with self.assertRaisesRegex(ValueError, "Failed to convert one or both inputs to integers."):
            add_two_numbers("abc", "xyz")

    def test_add_two_numbers_logging_on_error(self):
        """
        Test that an error message is logged when conversion fails.
        """
        with self.assertLogs('root', level='ERROR') as cm:
            with self.assertRaises(ValueError):
                add_two_numbers("invalid", "2")
            self.assertIn("Conversion to integer failed for input(s): num1=\"invalid\" and/or num2=\"2\"", cm.output[0])
            self.assertIn(correlation_ID, cm.output[0]) # Check if global correlation ID is in log

    def test_add_two_numbers_with_custom_corrID(self):
        """
        Test that the function uses the provided corrID argument if present.
        """
        custom_corr_id = "custom-123"
        with self.assertLogs('root', level='INFO') as cm:
            add_two_numbers(1, 2, corrID=custom_corr_id)
            self.assertIn(f'{custom_corr_id} - Function `add_two_numbers` called with num1=1, num2=2.', cm.output[0])
            self.assertNotIn(correlation_ID, cm.output[0]) # Ensure global ID is not used

    def test_add_two_numbers_with_none_corrID_uses_global(self):
        """
        Test that the function falls back to the global correlation_ID when corrID is None.
        """
        with self.assertLogs('root', level='INFO') as cm:
            add_two_numbers(1, 2, corrID=None)
            self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=1, num2=2.', cm.output[0])


if __name__ == '__main__':
    unittest.main()
