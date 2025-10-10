
# tests/test_addNums.py

import unittest
import io
import logging

# --- Start of code to be tested ---
# This is the fixed version of the code from 'addNums.py'.
# Including it here makes the test self-contained.

# This global variable is used by the function.
correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers.
    It gracefully handles cases where inputs cannot be converted to numbers.
    """
    # The original file's logging was configured globally. For testing, we will manage
    # the logger within the test case setup to capture output reliably.
    logger = logging.getLogger()

    # Determine the correlation ID to use for this function call
    current_corr_id = corrID if corrID is not None else correlation_ID
    # For info messages, we'll use a prefix like "ID - "
    info_prefix = f'{current_corr_id} - ' if current_corr_id else ''
    # For error messages, we need a prefix like "correlation_ID:ID " to match the error format
    error_prefix = f'correlation_ID:{current_corr_id} ' if current_corr_id else ''

    logger.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logger.info(f'{info_prefix}Attempting to convert inputs to integers.')

    try:
        # The original file had these lines incorrectly indented and lacked error handling.
        # They are now correctly indented within a try block to catch conversion errors.
        num1_int = int(num1)
        num2_int = int(num2)

        # Calculate the sum
        result = num1_int + num2_int
        logger.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result
    except ValueError:
        # If conversion to int fails, log the specified error and return None.
        logger.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None

# --- End of code to be tested ---


class TestAddNumbersFix(unittest.TestCase):
    """
    Test suite for the add_two_numbers function, specifically validating the fix
    for handling non-integer inputs.
    """

    def setUp(self):
        """
        Set up a logger and a stream to capture log output for each test.
        This ensures tests are isolated and don't interfere with each other.
        """
        self.log_stream = io.StringIO()
        self.logger = logging.getLogger()
        
        # The original code uses basicConfig, which adds a handler. We clear it
        # to ensure only our stream handler is active during the test.
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
            
        self.stream_handler = logging.StreamHandler(self.log_stream)
        # The format is specified as just the message in the original code's basicConfig.
        formatter = logging.Formatter('%(message)s')
        self.stream_handler.setFormatter(formatter)
        
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.INFO)

    def tearDown(self):
        """
        Clean up after each test by removing the stream handler and closing the stream.
        """
        self.logger.removeHandler(self.stream_handler)
        self.log_stream.close()

    def test_handles_non_integer_input_gracefully(self):
        """
        Validates the fix by providing a non-integer string as input.
        
        This test checks that the function:
        1. Returns None instead of raising a ValueError.
        2. Logs the appropriate error message.
        """
        # Call the function with an input that would cause a ValueError in the original code
        result = add_two_numbers("5", "not a number")

        # 1. Assert that the function returns None as per the fix
        self.assertIsNone(result, "Function should return None for invalid string input.")

        # 2. Assert that the correct error message was logged
        log_output = self.log_stream.getvalue()
        expected_error_message = (
            f"correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers."
        )
        
        self.assertIn(expected_error_message, log_output, "The specific error message was not found in the logs.")

    def test_adds_valid_numbers_correctly(self):
        """
        Ensures the function still works for valid inputs (happy path).
        This acts as a regression test to ensure the fix didn't break existing functionality.
        """
        # Test with two valid integer strings
        result = add_two_numbers("10", "20")
        self.assertEqual(result, 30, "Function should correctly sum two valid string numbers.")

        # Test with two integers
        result_int = add_two_numbers(7, 8)
        self.assertEqual(result_int, 15, "Function should correctly sum two integers.")
        
        # Verify no error message was logged
        log_output = self.log_stream.getvalue()
        self.assertNotIn("Value Error", log_output, "An error message was logged for valid inputs.")
        self.assertIn("Successfully added 7 and 8. Result: 15", log_output)

    def test_uses_custom_correlation_id(self):
        """
        Tests that a custom correlation ID provided as an argument is used in logging.
        """
        custom_id = "test-id-12345"
        add_two_numbers("1", "abc", corrID=custom_id)
        
        log_output = self.log_stream.getvalue()
        expected_error_message = (
            f"correlation_ID:{custom_id} Value Error: Failed to convert one or both inputs to integers."
        )
        self.assertIn(expected_error_message, log_output, "Custom correlation ID was not used in the error log.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
