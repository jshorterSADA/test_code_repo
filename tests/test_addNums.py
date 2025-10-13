To validate the fix, we'll create a unittest that ensures the `add_two_numbers` function correctly handles `None` inputs (which cause a `TypeError`) by catching them alongside `ValueError` and logging the appropriate error message, rather than the generic "unexpected error".

The test will:
1.  **Be self-contained**: The `add_two_numbers` function and its associated global `correlation_ID` will be included directly in the test file.
2.  **Capture logging output**: It will temporarily redirect log messages to an `io.StringIO` buffer to inspect the output.
3.  **Simulate the error**: Call `add_two_numbers` with `None` as one of the inputs.
4.  **Verify return value**: Assert that the function returns `None`.
5.  **Verify log message**: Assert that the captured log output contains the specific "Value Error: Failed to convert one or both inputs to integers." message, prefixed with the correct correlation ID, and does *not* contain the generic "An unexpected error occurred" message.
6.  **Add additional tests**: Include tests for `ValueError` (e.g., non-numeric string), successful addition, and custom correlation IDs to ensure overall functionality is preserved.

**Test File Name**: `tests/test_add_two_numbers.py`


# tests/test_add_two_numbers.py
import unittest
import logging
import io
import sys

# --- Start of self-contained code (copied from fixed addNums.py) ---

# Global correlation ID as defined in the original file.
# This variable is part of the context for the add_two_numbers function.
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

    # The logging configuration (basicConfig) is handled by the test setUp/tearDown
    # to ensure isolation and capture.
    logging.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{info_prefix}Attempting to convert inputs to integers.')

    try:
        # Attempt to convert inputs to integers
        # int(None) raises a TypeError, not a ValueError.
        # We need to catch both ValueError (e.g., int('abc')) and TypeError (e.g., int(None))
        # to gracefully handle all cases where inputs cannot be converted to numbers.
        num1_int = int(num1)
        num2_int = int(num2)
    
        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result
    except (ValueError, TypeError): # Corrected to catch both ValueError and TypeError
        # Log the error in the specified format and return None to indicate failure
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None
    except Exception as e:
        # Catch any other truly unexpected errors during conversion or addition
        logging.error(f'{error_prefix}An unexpected error occurred: {e}')
        return None

# --- End of self-contained code ---

class TestAddTwoNumbersFix(unittest.TestCase):
    """
    Unit tests for the add_two_numbers function, focusing on the fix for TypeError.
    """

    def setUp(self):
        """
        Set up logging to capture output for each test method.
        """
        # Save original logging state
        self.original_handlers = logging.root.handlers[:]
        self.original_level = logging.root.level
        self.original_propagate = logging.root.propagate

        # Clear existing handlers from the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Create a StringIO object to capture log output
        self.log_stream = io.StringIO()
        
        # Create a StreamHandler that writes to our StringIO
        self.handler = logging.StreamHandler(self.log_stream)
        
        # Set the formatter to match the application's expected format ('%(message)s')
        # This ensures that the message is printed exactly as formatted by the function.
        self.handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Add our custom handler to the root logger
        logging.root.addHandler(self.handler)
        
        # Set the root logger's level to INFO to capture both INFO and ERROR messages
        logging.root.setLevel(logging.INFO)
        logging.root.propagate = True # Ensure messages are propagated to handlers

    def tearDown(self):
        """
        Restore original logging state after each test method.
        """
        # Restore original logging state
        logging.root.removeHandler(self.handler)
        for handler in self.original_handlers:
            logging.root.addHandler(handler)
        logging.root.setLevel(self.original_level)
        logging.root.propagate = self.original_propagate
        self.log_stream.close() # Clean up the StringIO object

    def test_add_two_numbers_with_none_input_handles_typeerror_gracefully(self):
        """
        Tests that add_two_numbers gracefully handles None input (TypeError)
        by logging the correct error message and returning None.
        """
        # Arrange
        num1 = None
        num2 = 5
        # Using the global correlation_ID as it would be used if corrID is not passed
        expected_correlation_id = correlation_ID 
        expected_info_prefix = f'{expected_correlation_id} - '
        expected_error_prefix = f'correlation_ID:{expected_correlation_id} '
        expected_error_message_part = 'Value Error: Failed to convert one or both inputs to integers.'
        
        # Act
        result = add_two_numbers(num1, num2)
        
        # Assert the return value
        self.assertIsNone(result, "Function should return None when conversion fails with None input.")
        
        # Assert the log output
        log_output = self.log_stream.getvalue()
        
        # Verify info messages
        self.assertIn(f'{expected_info_prefix}Function `add_two_numbers` called with num1=None, num2=5.', log_output)
        self.assertIn(f'{expected_info_prefix}Attempting to convert inputs to integers.', log_output)

        # Verify the specific error message, confirming the fix catches TypeError
        expected_log_line = f'{expected_error_prefix}{expected_error_message_part}'
        self.assertIn(expected_log_line, log_output)

        # Verify that the generic 'An unexpected error occurred' message is NOT present,
        # which would indicate the generic Exception was caught instead of ValueError/TypeError.
        self.assertNotIn('An unexpected error occurred', log_output)

    def test_add_two_numbers_with_non_numeric_string_input_handles_valueerror_gracefully(self):
        """
        Tests that add_two_numbers gracefully handles non-numeric string input (ValueError)
        by logging the correct error message and returning None.
        """
        # Arrange
        num1 = "abc"
        num2 = "10"
        expected_correlation_id = correlation_ID
        expected_info_prefix = f'{expected_correlation_id} - '
        expected_error_prefix = f'correlation_ID:{expected_correlation_id} '
        expected_error_message_part = 'Value Error: Failed to convert one or both inputs to integers.'

        # Act
        result = add_two_numbers(num1, num2)

        # Assert the return value
        self.assertIsNone(result, "Function should return None when conversion fails for non-numeric string.")

        # Assert the log output
        log_output = self.log_stream.getvalue()
        
        # Verify info messages
        self.assertIn(f'{expected_info_prefix}Function `add_two_numbers` called with num1=abc, num2=10.', log_output)
        self.assertIn(f'{expected_info_prefix}Attempting to convert inputs to integers.', log_output)

        # Verify the specific error message
        expected_log_line = f'{expected_error_prefix}{expected_error_message_part}'
        self.assertIn(expected_log_line, log_output)
        self.assertNotIn('An unexpected error occurred', log_output)
        
    def test_add_two_numbers_successful_addition(self):
        """
        Tests that add_two_numbers correctly adds two valid numbers and logs info messages.
        """
        # Arrange
        num1 = "10"
        num2 = 20
        custom_corr_id = "test-corr-id-123" # Use a custom correlation ID to ensure parameter passing works
        expected_info_prefix = f'{custom_corr_id} - '
        expected_result = 30

        # Act
        result = add_two_numbers(num1, num2, corrID=custom_corr_id)

        # Assert the return value
        self.assertEqual(result, expected_result, "Function should correctly add two valid numbers.")

        # Assert the log output
        log_output = self.log_stream.getvalue()

        # Verify info messages
        self.assertIn(f'{expected_info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.', log_output)
        self.assertIn(f'{expected_info_prefix}Attempting to convert inputs to integers.', log_output)
        self.assertIn(f'{expected_info_prefix}Successfully added 10 and 20. Result: {expected_result}', log_output)
        
        # Ensure no error messages were logged
        self.assertNotIn('Value Error', log_output)
        self.assertNotIn('An unexpected error occurred', log_output)

    def test_add_two_numbers_with_custom_corr_id_for_error(self):
        """
        Tests that add_two_numbers uses a provided custom correlation ID for error logging
        when a TypeError occurs.
        """
        # Arrange
        num1 = None
        num2 = 5
        custom_corr_id = "custom-test-id-for-error-456"
        expected_info_prefix = f'{custom_corr_id} - '
        expected_error_prefix = f'correlation_ID:{custom_corr_id} '
        expected_error_message_part = 'Value Error: Failed to convert one or both inputs to integers.'
        
        # Act
        result = add_two_numbers(num1, num2, corrID=custom_corr_id)
        
        # Assert the return value is None
        self.assertIsNone(result, "Function should return None when conversion fails.")
        
        # Assert the log output uses the custom correlation ID
        log_output = self.log_stream.getvalue()
        
        # Verify info messages
        self.assertIn(f'{expected_info_prefix}Function `add_two_numbers` called with num1=None, num2=5.', log_output)
        self.assertIn(f'{expected_info_prefix}Attempting to convert inputs to integers.', log_output)
        
        # Verify the error message with custom correlation ID
        expected_log_line = f'{expected_error_prefix}{expected_error_message_part}'
        self.assertIn(expected_log_line, log_output)
        self.assertNotIn('An unexpected error occurred', log_output)

# To allow running tests directly from the command line
if __name__ == '__main__':
    unittest.main()
