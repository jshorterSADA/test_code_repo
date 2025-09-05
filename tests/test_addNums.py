To validate the fix, we'll create a new Python unittest file named `tests/test_addNums.py`. This test will include the fixed `add_two_numbers` function directly within it to ensure it is self-contained and explicitly tests the corrected logic.

The test will cover:
1.  Successful addition with various valid number inputs (integers, strings representing integers).
2.  Ensuring that a `ValueError` is raised when inputs cannot be converted to integers (e.g., non-numeric strings), and that the error message matches the expected output from the fix.
3.  Demonstrating that `TypeError` is still raised for inputs like `None`, as the provided fix specifically catches `ValueError` but not `TypeError` (highlighting a potential area for further improvement if all non-numeric types were intended to raise the custom `ValueError`).

**File Name:** `tests/test_addNums.py`


import unittest
import logging
import sys
import os

# --- Fixed Code (Copied for self-containment) ---
# This ensures the test directly uses the fixed version of the function
# and is entirely self-contained without needing to manage module imports
# from potentially different directory structures.

correlation_ID ="41131d34-334c-488a-bce2-a7642b27cf35"

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers.
    It gracefully handles cases where inputs cannot be converted to numbers.
    """
    # Determine the correlation ID to use for this function call
    # If corrID is provided as an argument, use it; otherwise, fall back to the global correlation_ID.
    current_corr_id = corrID if corrID is not None else correlation_ID
    corr_id_prefix = f'{current_corr_id} - ' if current_corr_id else ''

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')

    try:
        # Attempt to convert inputs to integers.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError:
        # Gracefully handle cases where conversion to integer fails.
        logging.error(f'{corr_id_prefix}Input conversion failed. num1={num1}, num2={num2} are not valid numbers.')
        raise ValueError("Invalid input. Please provide numbers.")

    # Calculate the sum using the successfully converted integer values.
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Calculation successful. Result: {result}.')

    # Return the result.
    return result

# --- End Fixed Code ---

class TestAddTwoNumbers(unittest.TestCase):
    """
    Test suite for the `add_two_numbers` function to validate its fix.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class-level configurations before any tests run.
        Disable logging to prevent test output from being cluttered by INFO/ERROR messages.
        """
        logging.disable(logging.CRITICAL) # Suppress logging output during tests

    @classmethod
    def tearDownClass(cls):
        """
        Clean up class-level configurations after all tests have run.
        Re-enable logging.
        """
        logging.disable(logging.NOTSET) # Re-enable logging after tests

    def test_add_positive_integers(self):
        """Test adding two positive integers."""
        self.assertEqual(add_two_numbers(2, 3), 5)
        self.assertEqual(add_two_numbers(100, 200), 300)

    def test_add_negative_integers(self):
        """Test adding two negative integers."""
        self.assertEqual(add_two_numbers(-2, -3), -5)
        self.assertEqual(add_two_numbers(-10, -5), -15)

    def test_add_mixed_integers(self):
        """Test adding a positive and a negative integer."""
        self.assertEqual(add_two_numbers(5, -3), 2)
        self.assertEqual(add_two_numbers(-5, 3), -2)

    def test_add_zero(self):
        """Test adding with zero."""
        self.assertEqual(add_two_numbers(0, 5), 5)
        self.assertEqual(add_two_numbers(5, 0), 5)
        self.assertEqual(add_two_numbers(0, 0), 0)

    def test_add_string_integers(self):
        """Test adding two string-represented integers."""
        self.assertEqual(add_two_numbers("2", "3"), 5)
        self.assertEqual(add_two_numbers("10", "-5"), 5)
        self.assertEqual(add_two_numbers("0", "0"), 0)

    def test_add_float_inputs(self):
        """
        Test that float inputs are handled by truncating to integers,
        as int() conversion works for floats and does not raise ValueError.
        """
        self.assertEqual(add_two_numbers(3.14, 2.86), 5) # int(3.14)=3, int(2.86)=2 => 3+2=5
        self.assertEqual(add_two_numbers(1.9, 2.1), 3)   # int(1.9)=1, int(2.1)=2 => 1+2=3

    def test_raise_value_error_with_non_numeric_string(self):
        """
        Test that ValueError is raised for non-numeric string inputs,
        and verify the specific error message. This directly validates the fix.
        """
        expected_message = "Invalid input. Please provide numbers."

        with self.assertRaisesRegex(ValueError, expected_message):
            add_two_numbers("hello", 5)
        with self.assertRaisesRegex(ValueError, expected_message):
            add_two_numbers(5, "world")
        with self.assertRaisesRegex(ValueError, expected_message):
            add_two_numbers("abc", "xyz")
        with self.assertRaisesRegex(ValueError, expected_message):
            add_two_numbers("10a", "20")
        with self.assertRaisesRegex(ValueError, expected_message):
            add_two_numbers("30", "5b")

    def test_raise_type_error_with_none_input(self):
        """
        Test that TypeError is raised for None inputs.
        The current fix specifically catches ValueError but not TypeError,
        meaning `int(None)` will still raise a TypeError not caught by the block.
        """
        with self.assertRaises(TypeError):
            add_two_numbers(None, 5)
        with self.assertRaises(TypeError):
            add_two_numbers(5, None)
        with self.assertRaises(TypeError):
            add_two_numbers(None, None)

    def test_correlation_id_parameter(self):
        """
        Test that the function can be called with a custom correlation ID
        without issues. (Does not test logging output directly, but parameter usage).
        """
        self.assertEqual(add_two_numbers(1, 2, corrID="my_test_id"), 3)
        self.assertEqual(add_two_numbers(10, 20), 30) # Test with default global ID


# This block allows running the tests directly from the command line
if __name__ == '__main__':
    # To run this test:
    # 1. Save the code above as `tests/test_addNums.py`
    # 2. Navigate to the directory containing the `tests` folder in your terminal.
    # 3. Run: `python -m unittest tests/test_addNums.py`
    #    Or for discovery: `python -m unittest discover`
    unittest.main()

