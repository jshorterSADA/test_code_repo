
# tests/test_addNums.py

import unittest
import logging
from io import StringIO

# --- Start of Self-Contained Code Under Test ---
# This is the "Proposed Fix" version of the code.

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# We will capture the logs in our tests instead of printing to the console.
logging.basicConfig(level=logging.INFO, format='%(message)s')

correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers.
    It gracefully handles cases where inputs cannot be converted to numbers.
    """
    # Determine the correlation ID to use for this function call
    current_corr_id = corrID if corrID is not None else correlation_ID
    # For info messages, we'll use a prefix like "ID - "
    info_prefix = f'{current_corr_id} - ' if current_corr_id else ''
    # For error messages, we need a prefix like "correlation_ID:ID " to match the error format
    error_prefix = f'correlation_ID:{current_corr_id} ' if current_corr_id else ''

    logging.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{info_prefix}Attempting to convert inputs to integers.')

    try:
        # The original file had these lines incorrectly indented and lacked error handling.
        # They are now correctly indented within a try block to catch conversion errors.
        num1_int = int(num1)
        num2_int = int(num2)

        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result
    except ValueError:
        # Handle the case where one or both inputs cannot be converted to an integer.
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None

# --- End of Self-Contained Code Under Test ---


class TestAddNumbersFix(unittest.TestCase):
    """
    Tests the add_two_numbers function, specifically validating the fix
    for handling non-numeric inputs.
    """

    def setUp(self):
        """Set up a stream to capture log output for each test."""
        self.log_stream = StringIO()
        self.log_handler = logging.StreamHandler(self.log_stream)
        # Use the root logger to capture all logs from the function
        logging.getLogger().addHandler(self.log_handler)
        # Set the level high enough to capture ERROR messages
        logging.getLogger().setLevel(logging.ERROR)

    def tearDown(self):
        """Clean up by removing the log handler."""
        logging.getLogger().removeHandler(self.log_handler)

    def test_add_valid_numbers(self):
        """Test that the function correctly adds valid integer and string-integer inputs."""
        self.assertEqual(add_two_numbers(5, 10), 15, "Should correctly add two integers.")
        self.assertEqual(add_two_numbers("20", "-5"), 15, "Should correctly add two string-integers.")

    def test_handle_invalid_string_input(self):
        """
        Test that the function returns None when an input cannot be converted to an integer.
        This directly validates the implemented fix.
        """
        # The original code would raise a ValueError here. The fix should return None.
        result = add_two_numbers("hello", 5)
        self.assertIsNone(result, "Function should return None for non-numeric string input.")

    def test_handle_float_string_input(self):
        """
        Test that a string representation of a float also triggers the error handling,
        as int() cannot parse it directly.
        """
        # The original code would raise a ValueError here as well. The fix should return None.
        result = add_two_numbers("3.14", 10)
        self.assertIsNone(result, "Function should return None for float string input.")

    def test_error_log_on_invalid_input(self):
        """
        Test that the function logs the correct error message when conversion fails.
        This validates the `except` block's logging behavior.
        """
        # Call the function with invalid input to trigger the error log
        add_two_numbers("abc", "123")

        # Get the content of our log stream
        log_output = self.log_stream.getvalue().strip()

        # Construct the expected error message using the global correlation ID
        expected_log = (
            f'correlation_ID:{correlation_ID} Value Error: '
            'Failed to convert one or both inputs to integers.'
        )

        self.assertEqual(log_output, expected_log, "The error log message does not match the expected format.")
    
    def test_error_log_with_custom_correlation_id(self):
        """
        Test that a custom correlation ID is correctly used in the error log.
        """
        custom_id = "test-id-9876"
        add_two_numbers("invalid", "input", corrID=custom_id)
        
        log_output = self.log_stream.getvalue().strip()

        expected_log = (
            f'correlation_ID:{custom_id} Value Error: '
            'Failed to convert one or both inputs to integers.'
        )
        self.assertEqual(log_output, expected_log, "The error log message should use the custom correlation ID.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
