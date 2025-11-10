
import unittest
import logging
from unittest.mock import patch, MagicMock
import io

# --- Start of the fixed add_two_numbers function (copied directly from the "Proposed Fix") ---
# Configure logging (re-copied from the fix description to ensure self-contained nature)
# For the purpose of the test, we'll temporarily reconfigure it in setUp/tearDown
# to capture logs. The format='%(message)s' is crucial for testing log content.
# logging.basicConfig(level=logging.INFO, format='%(message)s') # This will be overridden by the test's setUp

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
        # The error "ValueError: invalid literal for int() with base 10: '1e5'" occurs
        # when trying to convert a string like '1e5' directly to an int.
        # To handle scientific notation strings (e.g., '1e5') or other float-representable strings,
        # we first convert to float and then to int. This also handles direct float/int types correctly.
        num1_float = float(num1)
        num2_float = float(num2)

        # Then, convert the floats to integers. This will truncate any decimal parts,
        # fulfilling the "convert inputs to integers" requirement.
        num1_int = int(num1_float)
        num2_int = int(num2_float)

        # Added explicit checks to handle the reported TypeError: 'NoneType' and 'int'.
        # This handles an unexpected scenario where int() might hypothetically result in None,
        # or if num1_int/num2_int were somehow corrupted to None without raising a direct exception
        # during their assignment. This explicit check ensures the '+' operator always receives
        # valid integer types if execution proceeds.
        if num1_int is None or num2_int is None:
            raise TypeError("One of the numeric inputs was unexpectedly converted to None.")

        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result

    except (ValueError, TypeError) as e:
        # Log an error if conversion fails
        logging.error(f'{error_prefix}ERROR - correlation_ID:\'{current_corr_id}\' Failed to convert inputs to numbers: {e}. '
                      f'num1={num1} (type:{type(num1).__name__}), num2={num2} (type:{type(num2).__name__})')
        # The function's docstring says "It gracefully handles cases where inputs cannot be converted to numbers."
        # This implies it should return something other than raising an exception.
        # Returning None is a common way to signal failure for functions that are expected to return a value.
        return None
# --- End of the fixed add_two_numbers function ---


class TestAddTwoNumbersFix(unittest.TestCase):

    def setUp(self):
        # Create a StringIO object to capture logs
        self.log_stream = io.StringIO()
        # Set up a new StreamHandler for our StringIO object
        self.handler = logging.StreamHandler(self.log_stream)
        # Ensure the log format matches the application's basicConfig
        self.handler.setFormatter(logging.Formatter('%(message)s'))

        # Get the root logger
        self.logger = logging.getLogger()
        self.original_level = self.logger.level
        self.original_handlers = self.logger.handlers[:] # Keep a copy of original handlers

        # Clear existing handlers and set our custom handler
        for h in self.logger.handlers:
            self.logger.removeHandler(h)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO) # Set level to INFO to capture all expected logs
        self.logger.propagate = False # Prevent logs from propagating to the console during test

    def tearDown(self):
        # Clean up logging: remove our handler, restore original level and handlers
        self.logger.removeHandler(self.handler)
        self.logger.setLevel(self.original_level)
        for h in self.original_handlers:
            self.logger.addHandler(h)
        self.logger.propagate = True # Restore propagation
        self.handler.close()
        self.log_stream.close()

    @patch('builtins.int')
    def test_fix_handles_unexpected_none_from_int_conversion(self, mock_int):
        """
        Tests the fix: if the built-in int() *unexpectedly* returns None for one operand
        (simulated via mocking), the explicit 'is None' check should catch it, raise
        TypeError, and result in the function returning None while logging the specific error.
        This validates the defensive check added by the fix.
        """
        # Configure mock_int to return a normal integer for the first call (num1_int)
        # and None for the second call (num2_int).
        # This simulates the very specific, hypothetical scenario the fix addresses.
        mock_int.side_effect = [
            10,  # First call to int() (for num1_float) returns 10
            None # Second call to int() (for num2_float) returns None
        ]

        num1_input = 10.5 # These will be converted to float(10.5) then int(10.5) -> 10 by mock
        num2_input = 20.3 # These will be converted to float(20.3) then int(20.3) -> None by mock

        test_corr_id = "test-corr-id-mock-none"
        result = add_two_numbers(num1_input, num2_input, corrID=test_corr_id)

        # Assert that the function returned None, indicating graceful error handling
        self.assertIsNone(result)

        # Retrieve logged output
        log_output = self.log_stream.getvalue()

        # Assert that the specific TypeError message raised by the fix was logged
        # (it gets caught by the outer try-except block in add_two_numbers).
        expected_error_message_part = "Failed to convert inputs to numbers: One of the numeric inputs was unexpectedly converted to None."
        self.assertIn(expected_error_message_part, log_output)

        # Also check for the specific correlation ID in the error log
        self.assertIn(f"correlation_ID:{test_corr_id} ERROR - correlation_ID:'{test_corr_id}'", log_output)
        
        # Verify the types logged for num1 and num2
        self.assertIn(f"num1={num1_input} (type:float), num2={num2_input} (type:float)", log_output)

        # Verify that int() was called twice with the correct float values
        self.assertEqual(mock_int.call_count, 2)
        mock_int.assert_any_call(float(num1_input))
        mock_int.assert_any_call(float(num2_input))


    def test_normal_integer_addition(self):
        """Tests normal integer addition to ensure basic functionality is not broken."""
        test_corr_id = "test-normal-int"
        result = add_two_numbers(5, 7, corrID=test_corr_id)
        self.assertEqual(result, 12)
        log_output = self.log_stream.getvalue()
        self.assertIn(f"{test_corr_id} - Successfully added 5 and 7. Result: 12", log_output)
        self.assertIn(f"{test_corr_id} - Function `add_two_numbers` called with num1=5, num2=7.", log_output)

    def test_float_string_addition_truncation(self):
        """Tests addition with float-like string inputs, verifying truncation to int."""
        test_corr_id = "test-float-string"
        result = add_two_numbers("5.5", "7.9", corrID=test_corr_id)
        # Expected: float("5.5") -> 5.5 -> int(5.5) -> 5
        #           float("7.9") -> 7.9 -> int(7.9) -> 7
        self.assertEqual(result, 12)
        log_output = self.log_stream.getvalue()
        self.assertIn(f"{test_corr_id} - Successfully added 5 and 7. Result: 12", log_output)
        self.assertIn(f"{test_corr_id} - Attempting to convert inputs to integers.", log_output)

    def test_scientific_notation_string_addition(self):
        """Tests addition with scientific notation string inputs, verifying correct conversion."""
        test_corr_id = "test-scientific"
        result = add_two_numbers("1e1", "2e0", corrID=test_corr_id) # 1e1 = 10, 2e0 = 2
        self.assertEqual(result, 12)
        log_output = self.log_stream.getvalue()
        self.assertIn(f"{test_corr_id} - Successfully added 10 and 2. Result: 12", log_output)

    def test_invalid_string_input_returns_none_and_logs_error(self):
        """Tests that a non-numeric string input returns None and logs an appropriate error."""
        test_corr_id = "test-invalid-string"
        result = add_two_numbers("abc", 5, corrID=test_corr_id)
        self.assertIsNone(result)
        log_output = self.log_stream.getvalue()
        self.assertIn(f"correlation_ID:{test_corr_id} ERROR - correlation_ID:'{test_corr_id}' Failed to convert inputs to numbers:", log_output)
        self.assertIn("ValueError: could not convert string to float: 'abc'", log_output)
        self.assertIn(f"num1=abc (type:str), num2=5 (type:int)", log_output)

    def test_none_input_returns_none_and_logs_error(self):
        """Tests that None as an input returns None and logs a TypeError."""
        test_corr_id = "test-none-input"
        result = add_two_numbers(None, 5, corrID=test_corr_id)
        self.assertIsNone(result)
        log_output = self.log_stream.getvalue()
        self.assertIn(f"correlation_ID:{test_corr_id} ERROR - correlation_ID:'{test_corr_id}' Failed to convert inputs to numbers:", log_output)
        self.assertIn("TypeError: float() argument must be a string or a real number, not 'NoneType'", log_output)
        self.assertIn(f"num1=None (type:NoneType), num2=5 (type:int)", log_output)


# This allows running the test directly from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
