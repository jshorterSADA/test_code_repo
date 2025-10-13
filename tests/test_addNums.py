
# tests/test_addNums.py

import unittest
import logging
from io import StringIO

# The following code is a self-contained representation of the fixed 'addNums.py' file.
# In a real project structure, this would be in `addNums.py` and imported.
# ---- START: Fixed Code to be Tested ----

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# We will reconfigure the handler in the test to capture output.
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

    # Use a try-except block to handle potential ValueError during type conversion.
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
        # If conversion to integer fails, log an error with the specific format.
        logging.error(f'{error_prefix}Value Error: Failed to convert one or both inputs to integers.')
        return None

# ---- END: Fixed Code to be Tested ----


class TestAddNumbersFix(unittest.TestCase):
    """
    Test suite for the `add_two_numbers` function, specifically validating the fix
    for handling non-numeric inputs.
    """

    def test_invalid_input_returns_none_and_logs_error(self):
        """
        Validates the fix by providing a non-numeric string as input.
        This test confirms that a ValueError is caught, the correct error is logged,
        and the function returns None instead of crashing.
        """
        test_corr_id = "test-fix-validation-12345"
        
        # The `assertLogs` context manager captures logs from the specified logger.
        # We target the root logger as no specific logger was defined in the original code.
        with self.assertLogs('root', level='ERROR') as cm:
            # Call the function with an input that would cause a ValueError
            result = add_two_numbers("not_a_number", "5", corrID=test_corr_id)

        # 1. Assert that the function returns None on failure, as per the fix.
        self.assertIsNone(result, "Function should return None when conversion fails.")

        # 2. Construct the expected error message.
        expected_log_message = (
            f'correlation_ID:{test_corr_id} '
            'Value Error: Failed to convert one or both inputs to integers.'
        )

        # 3. Assert that the captured log output matches the expected message.
        # `cm.output` is a list of logged messages. We expect exactly one.
        self.assertEqual(len(cm.output), 1)
        self.assertEqual(cm.output[0], expected_log_message)

    def test_uses_global_correlation_id_on_error(self):
        """
        Validates that the global correlation_ID is used in the error log
        when no specific `corrID` is passed to the function.
        """
        with self.assertLogs('root', level='ERROR') as cm:
            # Call with an invalid input but no `corrID` argument
            add_two_numbers("abc", "123") 
        
        # The log should use the global `correlation_ID` from the module
        expected_log = (
            f'correlation_ID:{correlation_ID} ' # Using the global variable from the module
            'Value Error: Failed to convert one or both inputs to integers.'
        )
        self.assertEqual(len(cm.output), 1)
        self.assertEqual(cm.output[0], expected_log)

    def test_valid_inputs_still_work_correctly(self):
        """
        Ensures that the "happy path" (valid inputs) was not broken by the fix.
        This is a regression test.
        """
        # Using a StringIO stream to capture INFO logs without printing them to the console
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)
        logging.getLogger('root').addHandler(handler)
        
        # Test with valid string numbers
        result_str = add_two_numbers("100", "50")
        self.assertEqual(result_str, 150, "Should correctly sum valid string inputs.")
        
        # Test with valid integers
        result_int = add_two_numbers(25, 75)
        self.assertEqual(result_int, 100, "Should correctly sum valid integer inputs.")

        # Clean up the handler to avoid affecting other tests
        logging.getLogger('root').removeHandler(handler)


# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
