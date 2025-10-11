
# tests/test_addNums.py

import unittest
import logging
import io

# --- Original (Fixed) Code to be Tested ---
# This code is included here to make the test self-contained.
# It is the "Proposed Fix" version of the code.

# Configure logging to be captured during tests.
# The 'message' format ensures that correlation IDs are printed directly as specified.
logging.basicConfig(level=logging.INFO, format='%(message)s')

correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

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
        # Handle the case where one or both inputs cannot be converted to an integer.
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None

# --- New Unit Test ---

class TestAddTwoNumbers(unittest.TestCase):
    """
    Test suite for the add_two_numbers function.
    """

    def test_valid_inputs_return_sum(self):
        """
        Tests that the function correctly adds valid integer and string-numeric inputs.
        """
        self.assertEqual(add_two_numbers(5, 10), 15)
        self.assertEqual(add_two_numbers('7', '3'), 10)
        self.assertEqual(add_two_numbers(-5, 5), 0)
        self.assertEqual(add_two_numbers(0, 0), 0)

    def test_invalid_input_returns_none(self):
        """
        Validates the fix: tests that non-numeric string inputs, which cause a ValueError,
        result in the function returning None instead of crashing.
        """
        # Test case where one input is a non-numeric string
        result1 = add_two_numbers('five', 5)
        self.assertIsNone(result1, "Function should return None for non-numeric string input 'five'.")
        
        # Test case where the other input is a non-numeric string
        result2 = add_two_numbers(10, 'ten')
        self.assertIsNone(result2, "Function should return None for non-numeric string input 'ten'.")
        
        # Test case where both inputs are non-numeric strings
        result3 = add_two_numbers('alpha', 'beta')
        self.assertIsNone(result3, "Function should return None when both inputs are non-numeric.")

    def test_invalid_input_logs_error(self):
        """
        Validates the fix: tests that when a ValueError occurs, an appropriate
        error message is logged.
        """
        # Create an in-memory stream to capture log output
        log_stream = io.StringIO()
        
        # Create a handler that directs logs to our stream
        handler = logging.StreamHandler(log_stream)
        
        # Get the root logger and add our handler
        logger = logging.getLogger()
        logger.addHandler(handler)

        try:
            # Call the function that is expected to log an error
            add_two_numbers('invalid', 123)

            # Get the content of the log stream
            log_output = log_stream.getvalue()

            # Check if the expected error message is in the log output
            expected_error_msg = f"correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers."
            self.assertIn(expected_error_msg, log_output)
        
        finally:
            # Important: Remove the handler to avoid interfering with other tests
            logger.removeHandler(handler)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
