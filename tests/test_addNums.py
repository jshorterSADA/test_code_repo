
import unittest
import logging
import io
import sys

# --- Start of the fixed add_two_numbers function (self-contained for the test) ---

# Note: In a real test setup, you would typically import this function from its module.
# For a self-contained test as requested, we include the function definition here.

# The original logging.basicConfig call from the fix:
# logging.basicConfig(level=logging.INFO, format='%(message)s')
# We will manage logging dynamically within the test's setUp/tearDown methods
# to capture output and prevent interference with other tests or the environment.

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

    logging.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1!r}, num2={num2!r}.')
    logging.info(f'{info_prefix}Attempting to convert inputs to integers.')

    try:
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError as e:
        # Gracefully handle the conversion error by logging and returning None
        logging.error(f'{error_prefix}Failed to convert inputs to integers. Error: {e}. Received num1={num1!r}, num2={num2!r}.')
        return None
    
    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- End of the fixed add_two_numbers function ---

class TestAddTwoNumbers(unittest.TestCase):

    def setUp(self):
        """Set up logging to capture output before each test."""
        # Create a StringIO object to capture log output
        self.log_capture_stream = io.StringIO()
        
        # Create a StreamHandler that writes to our StringIO object
        self.handler = logging.StreamHandler(self.log_capture_stream)
        
        # Set the formatter to match the expected format '%(message)s'
        self.formatter = logging.Formatter('%(message)s')
        self.handler.setFormatter(self.formatter)
        
        # Get the root logger
        self.logger = logging.getLogger()
        
        # Store original handlers and remove them to isolate logging for the test
        self.original_handlers = self.logger.handlers[:]
        for h in self.original_handlers:
            self.logger.removeHandler(h)
        
        # Add our custom handler
        self.logger.addHandler(self.handler)
        
        # Set the logging level to capture INFO and ERROR messages
        self.logger.setLevel(logging.INFO)

    def tearDown(self):
        """Clean up logging configuration after each test."""
        # Clean up by removing our handler and closing the stream
        self.logger.removeHandler(self.handler)
        self.handler.close()
        
        # Restore the original handlers that were present before the test
        for h in self.original_handlers:
            self.logger.addHandler(h)
        
        # Reset logging level if necessary (though restoring handlers usually handles this)
        self.logger.setLevel(logging.NOTSET) # Reset to default level

    def test_fix_invalid_first_input_returns_none_and_logs_error(self):
        """
        Validates the fix: calling add_two_numbers with a non-convertible first input
        should return None and log an error message with the correct correlation ID format.
        """
        num1 = "one"
        num2 = 2
        custom_corr_id = "test-error-input1-123"
        
        result = add_two_numbers(num1, num2, corrID=custom_corr_id)
        
        self.assertIsNone(result, "Function should return None for invalid input.")
        
        log_output = self.log_capture_stream.getvalue()
        
        # Verify the error message format and content
        expected_error_prefix = f'correlation_ID:{custom_corr_id} '
        self.assertIn(expected_error_prefix, log_output, 
                      "Error log should contain the correct correlation ID prefix.")
        self.assertIn(
            f"Failed to convert inputs to integers. Error: invalid literal for int() with base 10: {num1!r}. Received num1={num1!r}, num2={num2!r}.",
            log_output,
            f"Error log message should accurately describe the conversion failure for '{num1}'."
        )
        
        # Verify info messages are also logged correctly before the error
        expected_info_prefix = f'{custom_corr_id} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1='one', num2=2.", log_output)
        self.assertIn(f"{expected_info_prefix}Attempting to convert inputs to integers.", log_output)

    def test_fix_invalid_second_input_returns_none_and_logs_error(self):
        """
        Validates the fix: calling add_two_numbers with a non-convertible second input
        should return None and log an error message, falling back to global ID.
        """
        num1 = 1
        num2 = "two" # This is the exact error scenario from the problem description
        
        # Test with fallback to global correlation_ID
        result = add_two_numbers(num1, num2) 
        
        self.assertIsNone(result, "Function should return None for invalid second input.")
        
        log_output = self.log_capture_stream.getvalue()
        
        expected_error_prefix = f'correlation_ID:{correlation_ID} ' # Using global ID
        self.assertIn(expected_error_prefix, log_output, 
                      "Error log should contain the correct global correlation ID prefix.")
        self.assertIn(
            f"Failed to convert inputs to integers. Error: invalid literal for int() with base 10: {num2!r}. Received num1={num1!r}, num2={num2!r}.",
            log_output,
            f"Error log message should accurately describe the conversion failure for '{num2}'."
        )
        
        # Verify info messages using global ID
        expected_info_prefix = f'{correlation_ID} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1=1, num2='two'.", log_output)
        self.assertIn(f"{expected_info_prefix}Attempting to convert inputs to integers.", log_output)

    def test_valid_integer_inputs_success(self):
        """
        Ensures existing functionality for valid integer inputs works correctly
        and logs info messages with a custom correlation ID.
        """
        custom_corr_id = "success-test-int-789"
        result = add_two_numbers(3, 4, corrID=custom_corr_id)
        
        self.assertEqual(result, 7, "Valid integer inputs should return their sum.")
        
        log_output = self.log_capture_stream.getvalue()
        expected_info_prefix = f'{custom_corr_id} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1=3, num2=4.", log_output)
        self.assertIn(f"{expected_info_prefix}Successfully added 3 and 4. Result: 7", log_output)
        
        # Ensure no error messages are logged for valid input
        self.assertNotIn("Failed to convert inputs to integers", log_output)

    def test_valid_string_inputs_success_with_global_id(self):
        """
        Ensures existing functionality for valid string-number inputs works correctly
        and logs info messages, falling back to the global correlation ID.
        """
        # Test with global correlation ID fallback (corrID is None)
        result = add_two_numbers("10", "20")
        
        self.assertEqual(result, 30, "Valid string-number inputs should return their sum.")
        
        log_output = self.log_capture_stream.getvalue()
        expected_info_prefix = f'{correlation_ID} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1='10', num2='20'.", log_output)
        self.assertIn(f"{expected_info_prefix}Successfully added 10 and 20. Result: 30", log_output)
        
        self.assertNotIn("Failed to convert inputs to integers", log_output)

    def test_mixed_valid_inputs(self):
        """
        Tests handling of mixed integer and string-number valid inputs.
        """
        custom_corr_id = "mixed-input-test"
        result = add_two_numbers("5", 15, corrID=custom_corr_id)
        
        self.assertEqual(result, 20, "Should correctly sum mixed string and integer inputs.")
        
        log_output = self.log_capture_stream.getvalue()
        expected_info_prefix = f'{custom_corr_id} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1='5', num2=15.", log_output)
        self.assertIn(f"{expected_info_prefix}Successfully added 5 and 15. Result: 20", log_output)
        self.assertNotIn("Failed to convert inputs to integers", log_output)

    def test_zero_and_negative_inputs(self):
        """
        Tests handling of zero and negative integer inputs.
        """
        result = add_two_numbers(-5, 0) # Using global ID
        
        self.assertEqual(result, -5, "Should correctly sum negative and zero inputs.")
        
        log_output = self.log_capture_stream.getvalue()
        expected_info_prefix = f'{correlation_ID} - '
        self.assertIn(f"{expected_info_prefix}Function `add_two_numbers` called with num1=-5, num2=0.", log_output)
        self.assertIn(f"{expected_info_prefix}Successfully added -5 and 0. Result: -5", log_output)
        self.assertNotIn("Failed to convert inputs to integers", log_output)

# To run the tests if this script is executed directly
if __name__ == '__main__':
    # unittest.main() might call sys.exit(), so use these arguments to prevent that
    # when running tests as part of a larger script or in an IDE.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

