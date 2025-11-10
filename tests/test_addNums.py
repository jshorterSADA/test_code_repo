
import unittest
import logging
from unittest.mock import patch, MagicMock
import io
import sys

# --- Start of the fixed add_two_numbers function (self-contained) ---

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# This basicConfig will be overridden or supplemented by the test's logging setup.
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
        # The error "ValueError: invalid literal for int() with base 10: '1e5'" occurs
        # when trying to convert a string like '1e5' directly to an int.
        # To handle scientific notation strings (e.g., '1e5') or other float-representable strings,
        # we first convert to float and then to int. This also handles direct float/int types correctly.
        num1_float = float(num1)
        num2_float = float(num2)
        
        # Then, convert the floats to integers. This will truncate any decimal part,
        # fulfilling the "convert inputs to integers" requirement.
        num1_int = int(num1_float)
        num2_int = int(num2_float)

        # Defensive check: This ensures that num1_int and num2_int are confirmed as integers
        # before addition. This check is logically redundant under normal Python behavior
        # (as int() either returns an int or raises an exception), but it directly addresses
        # the reported TypeError if, for an unexpected reason, one of these variables became None.
        # This is the specific fix being validated.
        if num1_int is None or num2_int is None:
            logging.error(f'{error_prefix}Internal conversion error: Expected integers, but one or both numbers became None after conversion. num1_int: {num1_int}, num2_int: {num2_int}')
            return None

        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result

    except (ValueError, TypeError) as e:
        logging.error(f'{error_prefix}Error converting inputs to numbers: {e}')
        return None

# --- End of the fixed add_two_numbers function ---


class TestAddTwoNumbersFix(unittest.TestCase):

    def setUp(self):
        # Capture logging output during tests
        self.log_stream = io.StringIO()
        self.handler = logging.StreamHandler(self.log_stream)
        # Set formatter to match the application's simple '%(message)s' format
        self.formatter = logging.Formatter('%(message)s')
        self.handler.setFormatter(self.formatter)

        # Add our handler to the root logger and set level to INFO to capture all relevant messages
        self.root_logger = logging.getLogger()
        self.root_logger.addHandler(self.handler)
        self.root_logger.setLevel(logging.INFO)

        # Clear any existing log messages from previous tests or module loading
        self.log_stream.seek(0)
        self.log_stream.truncate(0)

    def tearDown(self):
        # Clean up logging handlers to avoid interference with other tests or the main program
        self.root_logger.removeHandler(self.handler)
        self.handler.close()

    def assertLogInOutput(self, expected_substring):
        """Helper to check if a substring is present in the captured log output."""
        log_output = self.log_stream.getvalue()
        self.assertIn(expected_substring, log_output)
    
    def clearLogOutput(self):
        """Helper to clear the captured log output for a new test case."""
        self.log_stream.seek(0)
        self.log_stream.truncate(0)

    # --- Test cases for general functionality (regression prevention) ---

    def test_valid_integer_inputs(self):
        self.clearLogOutput()
        result = add_two_numbers(10, 5)
        self.assertEqual(result, 15)
        self.assertLogInOutput(f'{correlation_ID} - Successfully added 10 and 5. Result: 15')

    def test_valid_float_string_inputs(self):
        self.clearLogOutput()
        # int(10.5) is 10, int(5.2) is 5 due to truncation
        result = add_two_numbers("10.5", "5.2")
        self.assertEqual(result, 15) 
        self.assertLogInOutput(f'{correlation_ID} - Successfully added 10 and 5. Result: 15')

    def test_valid_scientific_notation_string_inputs(self):
        self.clearLogOutput()
        # 1e1 = 10.0, 2.3e1 = 23.0; int() truncates to 10 and 23
        result = add_two_numbers("1e1", "2.3e1") 
        self.assertEqual(result, 33)
        self.assertLogInOutput(f'{correlation_ID} - Successfully added 10 and 23. Result: 33')
        
    def test_invalid_string_input(self):
        self.clearLogOutput()
        result = add_two_numbers("hello", "5")
        self.assertIsNone(result)
        self.assertLogInOutput(
            f'correlation_ID:{correlation_ID} Error converting inputs to numbers: ValueError: could not convert string to float: \'hello\''
        )

    def test_none_input_for_conversion(self):
        self.clearLogOutput()
        result = add_two_numbers(None, 5)
        self.assertIsNone(result)
        self.assertLogInOutput(
            f'correlation_ID:{correlation_ID} Error converting inputs to numbers: TypeError: float() argument must be a string or a real number, not \'NoneType\''
        )

    # --- Test cases specifically validating the fix using mocking ---

    @patch('builtins.int')
    def test_fix_num1_int_becomes_none_after_conversion(self, mock_int):
        """
        Validates the fix by mocking `builtins.int` to return None for the first conversion,
        simulating an unexpected scenario where num1_int becomes None.
        """
        self.clearLogOutput()
        # Configure mock_int to return None for the first call (num1_int = int(num1_float))
        # and a valid integer for the second call (num2_int = int(num2_float)).
        # The float() conversions will still happen normally.
        mock_int.side_effect = [
            None,      # Return value for the first call to int() (for num1_float)
            5          # Return value for the second call to int() (for num2_float)
        ]
        
        # Call the function with valid numbers; the mock will intercept the int() calls
        result = add_two_numbers(10.0, 5.0) 
        
        self.assertIsNone(result)
        
        # Check that the specific error message from the fix was logged
        expected_log_message = (
            f'correlation_ID:{correlation_ID} Internal conversion error: Expected integers, '
            f'but one or both numbers became None after conversion. num1_int: None, num2_int: 5'
        )
        self.assertLogInOutput(expected_log_message)
        
        # Verify that int() was called as expected with the float values
        self.assertEqual(mock_int.call_count, 2)
        mock_int.assert_any_call(10.0) # Called for num1_float
        mock_int.assert_any_call(5.0)  # Called for num2_float

    @patch('builtins.int')
    def test_fix_num2_int_becomes_none_after_conversion(self, mock_int):
        """
        Validates the fix by mocking `builtins.int` to return None for the second conversion.
        """
        self.clearLogOutput()
        mock_int.side_effect = [
            10,        # Return value for the first call to int() (for num1_float)
            None       # Return value for the second call to int() (for num2_float)
        ]
        
        result = add_two_numbers(10.0, 5.0)
        
        self.assertIsNone(result)
        
        expected_log_message = (
            f'correlation_ID:{correlation_ID} Internal conversion error: Expected integers, '
            f'but one or both numbers became None after conversion. num1_int: 10, num2_int: None'
        )
        self.assertLogInOutput(expected_log_message)
        
        self.assertEqual(mock_int.call_count, 2)
        mock_int.assert_any_call(10.0)
        mock_int.assert_any_call(5.0)

    @patch('builtins.int')
    def test_fix_both_ints_become_none_after_conversion(self, mock_int):
        """
        Validates the fix by mocking `builtins.int` to return None for both conversions.
        """
        self.clearLogOutput()
        mock_int.side_effect = [
            None,      # Return value for the first call to int() (for num1_float)
            None       # Return value for the second call to int() (for num2_float)
        ]
        
        result = add_two_numbers(10.0, 5.0)
        
        self.assertIsNone(result)
        
        expected_log_message = (
            f'correlation_ID:{correlation_ID} Internal conversion error: Expected integers, '
            f'but one or both numbers became None after conversion. num1_int: None, num2_int: None'
        )
        self.assertLogInOutput(expected_log_message)
        
        self.assertEqual(mock_int.call_count, 2)
        mock_int.assert_any_call(10.0)
        mock_int.assert_any_call(5.0)

# Optional: To run the tests from command line if this file is executed directly
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
