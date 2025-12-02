
import unittest
import logging
import io
import sys

# --- Start of the relevant code from the proposed fix ---
# The correlation_ID is a module-level global in the original script.
# It is included here to make the test self-contained and reflect the original dependency.
correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# This basicConfig will set up the root logger, which assertLogs will then use.
logging.basicConfig(level=logging.INFO, format='%(message)s')

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers.
    It gracefully handles cases where inputs cannot be converted to numbers.
    """
    # Determine the correlation ID to use for this function call
    # If corrID is provided as an argument, use it; otherwise, fall back to the global correlation_ID.
    # The 'global correlation_ID' statement is not strictly necessary for reading, but reflects common practice.
    global correlation_ID
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
    except ValueError as e:
        # Log an error message and return None if conversion fails.
        # This addresses the 'ValueError: invalid literal for int() with base 10: "two"'
        # and fulfills the docstring's promise to "gracefully handle cases".
        logging.error(f'{error_prefix}Failed to convert one or both inputs to integers. num1="{num1}", num2="{num2}". Error: {e}')
        return None

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result
# --- End of the relevant code from the proposed fix ---


class TestAddTwoNumbersFix(unittest.TestCase):

    def test_invalid_string_input_returns_none_and_logs_error(self):
        """
        Test that `add_two_numbers` returns None for invalid string inputs
        and logs an error message matching the specified format.
        This specifically validates the fix for the original error.
        """
        num1 = 5
        num2 = "two" # This was the input causing the original ValueError
        expected_corr_id = correlation_ID # Using the default global correlation ID

        with self.assertLogs(level='ERROR') as cm:
            result = add_two_numbers(num1, num2)

            self.assertIsNone(result, "Function should return None for invalid input.")

            # Check for the expected error log message content
            self.assertEqual(len(cm.output), 1, "Expected exactly one error log message.")
            log_message = cm.output[0]
            expected_log_content = (
                f'correlation_ID:{expected_corr_id} '
                f'Failed to convert one or both inputs to integers. num1="{num1}", num2="{num2}". '
                f'Error: invalid literal for int() with base 10: \'{num2}\''
            )
            self.assertEqual(log_message, expected_log_content, "Error log message content mismatch.")

    def test_valid_inputs_return_correct_sum_and_logs_info(self):
        """
        Test that `add_two_numbers` returns the correct sum for valid inputs
        and logs info messages with the correct correlation ID prefix.
        """
        num1 = 10
        num2 = "20"
        expected_corr_id = correlation_ID
        expected_sum = 30

        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(num1, num2)

            self.assertEqual(result, expected_sum, f"Expected sum {expected_sum}, got {result}")

            # Check for info log messages
            self.assertEqual(len(cm.output), 3, "Expected three info log messages.")
            
            # Message 1: function called
            expected_msg_1 = f'{expected_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.'
            self.assertEqual(cm.output[0], expected_msg_1, "First info log message mismatch.")
            
            # Message 2: attempting conversion
            expected_msg_2 = f'{expected_corr_id} - Attempting to convert inputs to integers.'
            self.assertEqual(cm.output[1], expected_msg_2, "Second info log message mismatch.")
            
            # Message 3: success
            expected_msg_3 = f'{expected_corr_id} - Successfully added {num1} and {int(num2)}. Result: {expected_sum}'
            self.assertEqual(cm.output[2], expected_msg_3, "Third info log message mismatch.")

    def test_one_invalid_input_returns_none_and_logs_error(self):
        """
        Test that `add_two_numbers` returns None when only one input is invalid
        and logs an error message.
        """
        num1 = "one"
        num2 = 2
        expected_corr_id = correlation_ID

        with self.assertLogs(level='ERROR') as cm:
            result = add_two_numbers(num1, num2)
            self.assertIsNone(result, "Function should return None for one invalid input.")
            self.assertEqual(len(cm.output), 1, "Expected exactly one error log message.")
            log_message = cm.output[0]
            expected_log_content = (
                f'correlation_ID:{expected_corr_id} '
                f'Failed to convert one or both inputs to integers. num1="{num1}", num2="{num2}". '
                f'Error: invalid literal for int() with base 10: \'{num1}\''
            )
            self.assertEqual(log_message, expected_log_content, "Error log message content mismatch for one invalid input.")

    def test_custom_correlation_id_in_error_logs(self):
        """
        Test that a custom correlation ID is used correctly in error log messages.
        """
        custom_id = "test-corr-id-123"
        num1 = "invalid"
        num2 = 10

        with self.assertLogs(level='ERROR') as cm:
            result = add_two_numbers(num1, num2, corrID=custom_id)
            self.assertIsNone(result, "Function should return None for invalid input with custom corrID.")
            self.assertEqual(len(cm.output), 1, "Expected exactly one error log message with custom corrID.")
            log_message = cm.output[0]
            expected_log_content = (
                f'correlation_ID:{custom_id} '
                f'Failed to convert one or both inputs to integers. num1="{num1}", num2="{num2}". '
                f'Error: invalid literal for int() with base 10: \'{num1}\''
            )
            self.assertEqual(log_message, expected_log_content, "Error log message content mismatch with custom corrID.")

    def test_custom_correlation_id_in_info_logs(self):
        """
        Test that a custom correlation ID is used correctly in info log messages.
        """
        custom_id = "another-corr-id-789"
        num1 = 1
        num2 = 2
        expected_sum = 3

        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(num1, num2, corrID=custom_id)
            self.assertEqual(result, expected_sum, "Expected correct sum with custom corrID.")
            self.assertEqual(len(cm.output), 3, "Expected three info log messages with custom corrID.")
            
            expected_msg_1 = f'{custom_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.'
            self.assertEqual(cm.output[0], expected_msg_1, "First info log message mismatch with custom corrID.")
            
            expected_msg_2 = f'{custom_id} - Attempting to convert inputs to integers.'
            self.assertEqual(cm.output[1], expected_msg_2, "Second info log message mismatch with custom corrID.")
            
            expected_msg_3 = f'{custom_id} - Successfully added {num1} and {num2}. Result: {expected_sum}'
            self.assertEqual(cm.output[2], expected_msg_3, "Third info log message mismatch with custom corrID.")

    def test_zero_and_negative_numbers(self):
        """
        Test `add_two_numbers` with zero and negative numbers.
        """
        self.assertEqual(add_two_numbers(0, 0), 0)
        self.assertEqual(add_two_numbers(-5, 10), 5)
        self.assertEqual(add_two_numbers("-10", "-20"), -30)
        self.assertEqual(add_two_numbers(100, -50), 50)


if __name__ == '__main__':
    unittest.main()
