
# tests/test_addNums.py

import unittest
import logging
import io

# --- Code to be tested (from the "Proposed Fix") ---
# This is included here to make the unittest self-contained.

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# In a real application, this would likely be configured once at startup.
logging.basicConfig(level=logging.INFO, format='%(message)s')

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
        # Log an error message if conversion fails, using the specified error format.
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None # Return None to indicate failure as per the graceful handling requirement.

# --- New Unit Test ---

class TestAddTwoNumbers(unittest.TestCase):
    """
    Test suite for the add_two_numbers function.
    """

    def setUp(self):
        """
        Set up a stream to capture log output for each test.
        This prevents logs from printing to the console during tests and allows
        us to assert their content.
        """
        self.log_stream = io.StringIO()
        self.stream_handler = logging.StreamHandler(self.log_stream)
        # We get the root logger and add our handler to it.
        # It's important to remove it in tearDown to avoid side effects.
        logging.getLogger().addHandler(self.stream_handler)

    def tearDown(self):
        """
        Clean up by removing the custom log handler.
        """
        logging.getLogger().removeHandler(self.stream_handler)

    def test_handles_non_numeric_input_gracefully(self):
        """
        Validates the fix: ensures that when a non-numeric string is passed,
        the function returns None and logs the appropriate ValueError.
        This test directly targets the scenario that caused the original error.
        """
        # Call the function with one invalid input
        result = add_two_numbers("5", "abc")

        # 1. Assert that the function returns None as per the graceful handling
        self.assertIsNone(result, "Function should return None for non-numeric input.")

        # 2. Assert that the correct error was logged
        log_output = self.log_stream.getvalue()
        expected_error_log = (
            f'correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers.'
        )
        self.assertIn(expected_error_log, log_output, "Expected ValueError log message was not found.")

    def test_adds_valid_string_numbers_correctly(self):
        """
        Test the "happy path" to ensure the function still works for valid inputs.
        """
        result = add_two_numbers("10", "20")
        self.assertEqual(result, 30, "Function should correctly add two valid number strings.")
        
        # Verify no error was logged
        log_output = self.log_stream.getvalue()
        self.assertNotIn("Value Error", log_output, "Error should not be logged for valid inputs.")

    def test_adds_valid_integer_numbers_correctly(self):
        """
        Test the function with integer inputs instead of strings.
        """
        result = add_two_numbers(7, 8)
        self.assertEqual(result, 15, "Function should correctly add two integers.")

        # Verify no error was logged
        log_output = self.log_stream.getvalue()
        self.assertNotIn("Value Error", log_output, "Error should not be logged for valid inputs.")

    def test_uses_custom_correlation_id_in_error_log(self):
        """
        Test that a custom correlation ID, when provided, is used in the error log.
        """
        custom_id = "test-id-98765"
        result = add_two_numbers("one", "two", corrID=custom_id)

        # Assert the function returns None
        self.assertIsNone(result)

        # Assert the error log uses the custom ID
        log_output = self.log_stream.getvalue()
        expected_error_log = (
            f'correlation_ID:{custom_id} Value Error: Failed to convert one or both inputs to integers.'
        )
        self.assertIn(expected_error_log, log_output, "Error log should use the custom correlation ID.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
