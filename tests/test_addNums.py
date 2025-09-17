To validate the fix, we will create a unit test file named `tests/test_add_nums.py`. This test will include the fixed `add_two_numbers` function and will verify the following:

1.  The function still correctly sums valid integer inputs.
2.  The function still correctly sums valid string-integer inputs.
3.  When invalid (non-numeric) inputs are provided, the function returns `None`.
4.  When invalid inputs are provided, a specific error message is logged, including the correlation ID, as defined in the fix.
5.  The logging behavior is correctly captured and asserted within the tests.


# tests/test_add_nums.py

import unittest
import logging
import io
import sys
from unittest.mock import patch

# --- Start of the fixed add_two_numbers function (copied directly for self-containment) ---

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# NOTE: basicConfig sets up the root logger. For testing, we'll manage handlers
#       within the TestAddTwoNumbers class to capture output reliably.
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
    corr_id_prefix = f'{current_corr_id} - ' if current_corr_id else ''

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')

    try:
        # Attempt to convert inputs to integers.
        # This is where the ValueError can occur if inputs are not valid.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError:
        # The problem statement indicates a ValueError occurs when converting inputs.
        # The function's docstring also states it should "gracefully handles cases where inputs cannot be converted".
        # The required error output format is: "correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers."
        # This implies that "correlation_ID:" is a literal prefix in the error message.
        error_message_for_log = f'correlation_ID:{current_corr_id} Value Error: Failed to convert one or both inputs to integers.'
        logging.error(error_message_for_log)
        return None # Return None to indicate that the operation failed gracefully

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result
# --- End of the fixed add_two_numbers function ---


class TestAddTwoNumbers(unittest.TestCase):

    def setUp(self):
        """Set up logging capture for each test."""
        # Get the root logger
        self.root_logger = logging.getLogger()
        # Save original handlers and level
        self.original_handlers = self.root_logger.handlers[:]
        self.original_level = self.root_logger.level
        
        # Clear existing handlers to prevent interfering with test output capture
        self.root_logger.handlers = []

        # Create a StringIO object to capture log output
        self.log_capture_stream = io.StringIO()
        # Create a StreamHandler that writes to our StringIO object
        self.handler = logging.StreamHandler(self.log_capture_stream)
        # Set the formatter to match the application's basicConfig format
        self.handler.setFormatter(logging.Formatter('%(message)s'))
        # Add the handler to the root logger
        self.root_logger.addHandler(self.handler)
        # Set the logger level to capture INFO and ERROR messages
        self.root_logger.setLevel(logging.INFO)

    def tearDown(self):
        """Clean up logging after each test."""
        # Remove the custom handler
        self.root_logger.removeHandler(self.handler)
        self.handler.close()
        # Restore original handlers and level
        self.root_logger.handlers = self.original_handlers
        self.root_logger.setLevel(self.original_level)

    def get_log_output(self):
        """Helper to get the captured log output."""
        return self.log_capture_stream.getvalue()

    def test_add_valid_integers(self):
        """Test with valid integer inputs, ensuring correct sum and info logs."""
        result = add_two_numbers(5, 3)
        self.assertEqual(result, 8)
        
        log_output = self.get_log_output()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=5, num2=3.', log_output)
        self.assertIn(f'{correlation_ID} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(f'{correlation_ID} - Successfully added 5 and 3. Result: 8', log_output)

    def test_add_valid_string_integers(self):
        """Test with valid string representations of integers, ensuring correct sum and info logs."""
        result = add_two_numbers("10", "20")
        self.assertEqual(result, 30)
        
        log_output = self.get_log_output()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=10, num2=20.', log_output)
        self.assertIn(f'{correlation_ID} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(f'{correlation_ID} - Successfully added 10 and 20. Result: 30', log_output)

    def test_add_invalid_input_returns_none_and_logs_error(self):
        """Test with one invalid input, expecting None and a specific error log."""
        expected_log_message = f'correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers.'

        result = add_two_numbers("abc", 5)

        self.assertIsNone(result)
        
        log_output = self.get_log_output()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=abc, num2=5.', log_output)
        self.assertIn(f'{correlation_ID} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(expected_log_message, log_output)
        # Ensure no success message is logged when an error occurs
        self.assertNotIn("Successfully added", log_output)

    def test_add_invalid_input_with_custom_corrid_returns_none_and_logs_error(self):
        """Test with invalid input and a custom correlation ID."""
        custom_corr_id = "custom-test-id-123"
        expected_log_message = f'correlation_ID:{custom_corr_id} Value Error: Failed to convert one or both inputs to integers.'

        result = add_two_numbers(10, "xyz", corrID=custom_corr_id)

        self.assertIsNone(result)
        
        log_output = self.get_log_output()
        self.assertIn(f'{custom_corr_id} - Function `add_two_numbers` called with num1=10, num2=xyz.', log_output)
        self.assertIn(f'{custom_corr_id} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(expected_log_message, log_output)
        self.assertNotIn("Successfully added", log_output)

    def test_add_both_invalid_inputs_returns_none_and_logs_error(self):
        """Test with both inputs being invalid, expecting None and specific error log."""
        expected_log_message = f'correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers.'

        result = add_two_numbers("hello", "world")

        self.assertIsNone(result)
        
        log_output = self.get_log_output()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=hello, num2=world.', log_output)
        self.assertIn(f'{correlation_ID} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(expected_log_message, log_output)
        self.assertNotIn("Successfully added", log_output)

    def test_add_float_inputs_gracefully_converted(self):
        """Test with float inputs that can be converted to int (truncation occurs)."""
        result = add_two_numbers(5.7, 3.2) # int(5.7) -> 5, int(3.2) -> 3
        self.assertEqual(result, 8)
        
        log_output = self.get_log_output()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=5.7, num2=3.2.', log_output)
        self.assertIn(f'{correlation_ID} - Attempting to convert inputs to integers.', log_output)
        self.assertIn(f'{correlation_ID} - Successfully added 5 and 3. Result: 8', log_output)


if __name__ == '__main__':
    unittest.main()

