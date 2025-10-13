To validate the fix, we will create a self-contained Python unittest named `tests/test_addNums.py`. This test will include the *fixed* version of the `add_two_numbers` function directly within the test file to ensure self-containment.

The test will cover:
1.  **Successful conversion of scientific notation strings**: This is the primary fix.
2.  **Successful conversion of standard integers and integer-like strings**.
3.  **Successful conversion of floats and float-like strings (with truncation to integer)**.
4.  **Graceful handling of invalid string inputs (e.g., 'abc')**.
5.  **Graceful handling of `None` inputs**.
6.  **Verification of logging messages**, including the correct correlation ID prefixes for both info and error messages, and the absence of error logs in successful cases.
7.  **Verification of global correlation ID fallback** when `corrID` is not provided.
8.  **Verification of behavior with an empty `corrID` string**.


# File: tests/test_addNums.py

import unittest
import logging
import io
import sys

# --- START: Copied and fixed add_two_numbers function ---
# The original code includes a logging.basicConfig call at the module level.
# In a unit test, it's crucial to manage logging carefully to avoid interference
# between tests or with the test runner's logging.
# unittest.assertLogs handles this by temporarily setting up a capture handler.
# However, if basicConfig runs before assertLogs, it might set a default stream handler.
# To ensure clean state, we will remove any default handlers added by basicConfig.

# Global correlation ID (as in original code, but can be temporarily changed in tests)
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
    
        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result
    except (ValueError, TypeError): # This block will now correctly catch issues from float() conversion
        # Log the error in the specified format and return None to indicate failure
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None
    except Exception as e:
        # Catch any other truly unexpected errors during conversion or addition
        logging.error(f'{error_prefix}An unexpected error occurred: {e}')
        return None
# --- END: Copied and fixed add_two_numbers function ---

# Configure logging for the test environment.
# This ensures that default handlers (e.g., from a module-level basicConfig call)
# don't interfere with unittest.assertLogs, which adds its own temporary handler.
def setup_logging_for_test():
    root_logger = logging.getLogger()
    # Remove any existing handlers from the root logger
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    # Set level to INFO to capture all expected messages. assertLogs will manage its own level.
    root_logger.setLevel(logging.INFO)

# Call this once when the module is loaded to clean up the logging state
setup_logging_for_test()


class TestAddTwoNumbers(unittest.TestCase):

    def setUp(self):
        # Store original global correlation_ID to restore it after each test
        self._original_correlation_ID = globals()['correlation_ID']

    def tearDown(self):
        # Restore original global correlation_ID
        globals()['correlation_ID'] = self._original_correlation_ID

    def test_scientific_notation_strings_fixed(self):
        """
        Validate that scientific notation strings (e.g., '1e5') are now correctly handled.
        """
        test_corr_id = "test-scientific-fix-id"
        num1_str = "1e5"  # Represents 100000.0
        num2_str = "2e3"  # Represents 2000.0
        
        expected_result = 100000 + 2000 # Expected sum after conversion and truncation
        
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(num1_str, num2_str, corrID=test_corr_id)
            
            self.assertEqual(result, expected_result)
            
            log_messages = [record.getMessage() for record in cm.records]
            
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1={num1_str}, num2={num2_str}.', log_messages)
            self.assertIn(f'{test_corr_id} - Attempting to convert inputs to integers.', log_messages)
            self.assertIn(f'{test_corr_id} - Successfully added 100000 and 2000. Result: 102000', log_messages)
            # Ensure no error logs were produced
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

    def test_standard_integer_strings(self):
        """
        Test with standard integer strings to ensure existing functionality is preserved.
        """
        test_corr_id = "test-int-string-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers('10', '20', corrID=test_corr_id)
            self.assertEqual(result, 30)
            log_messages = [record.getMessage() for record in cm.records]
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10, num2=20.', log_messages)
            self.assertIn(f'{test_corr_id} - Successfully added 10 and 20. Result: 30', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")


    def test_standard_integers(self):
        """
        Test with actual integer types.
        """
        test_corr_id = "test-int-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(10, 20, corrID=test_corr_id)
            self.assertEqual(result, 30)
            log_messages = [record.getMessage() for record in cm.records]
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10, num2=20.', log_messages)
            self.assertIn(f'{test_corr_id} - Successfully added 10 and 20. Result: 30', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

    def test_float_strings_truncation(self):
        """
        Test with float-representing strings; conversion to int should truncate decimals.
        """
        test_corr_id = "test-float-string-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers('10.5', '20.9', corrID=test_corr_id)
            self.assertEqual(result, 30) # 10 + 20 due to int(float_val) truncation
            log_messages = [record.getMessage() for record in cm.records]
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10.5, num2=20.9.', log_messages)
            self.assertIn(f'{test_corr_id} - Successfully added 10 and 20. Result: 30', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

    def test_direct_floats_truncation(self):
        """
        Test with direct float types; conversion to int should truncate decimals.
        """
        test_corr_id = "test-direct-float-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(10.5, 20.9, corrID=test_corr_id)
            self.assertEqual(result, 30) # 10 + 20 due to int(float_val) truncation
            log_messages = [record.getMessage() for record in cm.records]
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10.5, num2=20.9.', log_messages)
            self.assertIn(f'{test_corr_id} - Successfully added 10 and 20. Result: 30', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

    def test_invalid_string_input(self):
        """
        Test handling of strings that cannot be converted to numbers (e.g., 'abc').
        """
        test_corr_id = "test-invalid-string-id"
        with self.assertLogs(level='INFO') as cm: # Capture INFO and ERROR messages
            result = add_two_numbers('abc', 'def', corrID=test_corr_id)
            self.assertIsNone(result)
            
            info_messages = [record.getMessage() for record in cm.records if record.levelno == logging.INFO]
            error_messages = [record.getMessage() for record in cm.records if record.levelno >= logging.ERROR]
            
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=abc, num2=def.', info_messages)
            self.assertIn(f'{test_corr_id} - Attempting to convert inputs to integers.', info_messages)
            
            self.assertEqual(len(error_messages), 1)
            self.assertIn(f'correlation_ID:{test_corr_id} Value Error: Failed to convert one or both inputs to integers.', error_messages[0])

    def test_none_input_for_num1(self):
        """
        Test handling of None as the first input.
        """
        test_corr_id = "test-none-input-num1-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(None, 10, corrID=test_corr_id)
            self.assertIsNone(result)
            
            info_messages = [record.getMessage() for record in cm.records if record.levelno == logging.INFO]
            error_messages = [record.getMessage() for record in cm.records if record.levelno >= logging.ERROR]
            
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=None, num2=10.', info_messages)
            self.assertIn(f'{test_corr_id} - Attempting to convert inputs to integers.', info_messages)
            
            self.assertEqual(len(error_messages), 1)
            self.assertIn(f'correlation_ID:{test_corr_id} Value Error: Failed to convert one or both inputs to integers.', error_messages[0])

    def test_none_input_for_num2(self):
        """
        Test handling of None as the second input.
        """
        test_corr_id = "test-none-input-num2-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(10, None, corrID=test_corr_id)
            self.assertIsNone(result)
            
            info_messages = [record.getMessage() for record in cm.records if record.levelno == logging.INFO]
            error_messages = [record.getMessage() for record in cm.records if record.levelno >= logging.ERROR]
            
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10, num2=None.', info_messages)
            self.assertIn(f'{test_corr_id} - Attempting to convert inputs to integers.', info_messages)
            
            self.assertEqual(len(error_messages), 1)
            self.assertIn(f'correlation_ID:{test_corr_id} Value Error: Failed to convert one or both inputs to integers.', error_messages[0])

    def test_mix_valid_and_invalid_input(self):
        """
        Test with one valid and one invalid input.
        """
        test_corr_id = "test-mix-input-id"
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers('10', 'xyz', corrID=test_corr_id)
            self.assertIsNone(result)
            
            info_messages = [record.getMessage() for record in cm.records if record.levelno == logging.INFO]
            error_messages = [record.getMessage() for record in cm.records if record.levelno >= logging.ERROR]
            
            self.assertIn(f'{test_corr_id} - Function `add_two_numbers` called with num1=10, num2=xyz.', info_messages)
            self.assertIn(f'{test_corr_id} - Attempting to convert inputs to integers.', info_messages)
            
            self.assertEqual(len(error_messages), 1)
            self.assertIn(f'correlation_ID:{test_corr_id} Value Error: Failed to convert one or both inputs to integers.', error_messages[0])

    def test_global_correlation_id_fallback(self):
        """
        Verify that the global correlation_ID is used when corrID is not provided.
        """
        # Temporarily change the global ID to ensure fallback works as expected
        globals()['correlation_ID'] = "global-test-id-fallback"
        
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(1, 2) # No corrID provided, should use global
            self.assertEqual(result, 3)
            log_messages = [record.getMessage() for record in cm.records]
            self.assertIn(f'global-test-id-fallback - Function `add_two_numbers` called with num1=1, num2=2.', log_messages)
            self.assertIn(f'global-test-id-fallback - Successfully added 1 and 2. Result: 3', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

    def test_empty_corr_id(self):
        """
        Test behavior when an empty string is provided as corrID.
        Prefixes should be empty in this case.
        """
        test_corr_id = ""
        # Test success case with empty corrID
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(1, 2, corrID=test_corr_id)
            self.assertEqual(result, 3)
            log_messages = [record.getMessage() for record in cm.records]
            # When corrID is empty, prefixes should also be empty
            self.assertIn(f'Function `add_two_numbers` called with num1=1, num2=2.', log_messages)
            self.assertIn(f'Attempting to convert inputs to integers.', log_messages)
            self.assertIn(f'Successfully added 1 and 2. Result: 3', log_messages)
            self.assertFalse(any(record.levelno >= logging.ERROR for record in cm.records), "No error logs expected")

        # Test error case with empty corrID
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers('a', 'b', corrID=test_corr_id)
            self.assertIsNone(result)
            
            info_messages = [record.getMessage() for record in cm.records if record.levelno == logging.INFO]
            error_messages = [record.getMessage() for record in cm.records if record.levelno >= logging.ERROR]
            
            self.assertIn(f'Function `add_two_numbers` called with num1=a, num2=b.', info_messages)
            self.assertIn(f'Attempting to convert inputs to integers.', info_messages)
            
            self.assertEqual(len(error_messages), 1)
            # No prefix for error message when corrID is an empty string
            self.assertIn(f'Value Error: Failed to convert one or both inputs to integers.', error_messages[0])


# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()

