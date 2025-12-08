
import unittest
import logging
from unittest.mock import patch, MagicMock

# --- Start of self-contained code including the fixed function ---

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# For this self-contained test, we will mock logging calls directly,
# so the basicConfig is mainly for context if this file were run standalone without mocks.
logging.basicConfig(level=logging.INFO, format='%(message)s')

correlation_ID ="41131d34-334c-488a-bce2-a7642b27cf35"

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers.
    It gracefully handles cases where inputs cannot be converted to numbers.
    """
    current_corr_id = corrID if corrID is not None else correlation_ID
    info_prefix = f'{current_corr_id} - ' if current_corr_id else ''
    error_prefix = f'correlation_ID:{current_corr_id} ' if current_corr_id else ''

    logging.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{info_prefix}Attempting to convert inputs to integers.')

    try:
        num1_int = int(num1)
        num2_int = int(num2)
    except (ValueError, TypeError) as e:
        logging.error(f'{error_prefix}Failed to convert inputs to integers. Input num1="{num1}", num2="{num2}". Error: {e}')
        return None

    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- End of self-contained code including the fixed function ---


class TestAddTwoNumbers(unittest.TestCase):

    @patch('logging.info')
    @patch('logging.error')
    def test_add_valid_numbers_default_corr_id(self, mock_log_error, mock_log_info):
        """
        Test that two valid numbers are added correctly and info logs are generated
        with the default correlation ID.
        """
        num1 = "10"
        num2 = 5
        expected_result = 15
        default_corr_id = correlation_ID

        result = add_two_numbers(num1, num2)

        self.assertEqual(result, expected_result)
        mock_log_error.assert_not_called()
        self.assertEqual(mock_log_info.call_count, 3)

        # Verify info log calls
        mock_log_info.assert_any_call(f'{default_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.')
        mock_log_info.assert_any_call(f'{default_corr_id} - Attempting to convert inputs to integers.')
        mock_log_info.assert_any_call(f'{default_corr_id} - Successfully added {int(num1)} and {num2}. Result: {expected_result}')

    @patch('logging.info')
    @patch('logging.error')
    def test_add_valid_numbers_custom_corr_id(self, mock_log_error, mock_log_info):
        """
        Test that two valid numbers are added correctly and info logs are generated
        with a custom correlation ID.
        """
        num1 = -3
        num2 = "7"
        custom_corr_id = "abc-123-xyz"
        expected_result = 4

        result = add_two_numbers(num1, num2, corrID=custom_corr_id)

        self.assertEqual(result, expected_result)
        mock_log_error.assert_not_called()
        self.assertEqual(mock_log_info.call_count, 3)

        # Verify info log calls
        mock_log_info.assert_any_call(f'{custom_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.')
        mock_log_info.assert_any_call(f'{custom_corr_id} - Attempting to convert inputs to integers.')
        mock_log_info.assert_any_call(f'{custom_corr_id} - Successfully added {num1} and {int(num2)}. Result: {expected_result}')

    @patch('logging.info')
    @patch('logging.error')
    def test_add_invalid_number_value_error(self, mock_log_error, mock_log_info):
        """
        Test handling of a ValueError during conversion (e.g., 'hello'),
        ensuring None is returned and an error is logged with the correct format.
        """
        num1 = "hello"
        num2 = 10
        default_corr_id = correlation_ID

        result = add_two_numbers(num1, num2)

        self.assertIsNone(result)
        self.assertEqual(mock_log_info.call_count, 2) # Only initial info logs, no success log

        # Verify initial info logs
        mock_log_info.assert_any_call(f'{default_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.')
        mock_log_info.assert_any_call(f'{default_corr_id} - Attempting to convert inputs to integers.')

        # Verify error log
        mock_log_error.assert_called_once()
        expected_error_message_pattern = (
            f"correlation_ID:{default_corr_id} Failed to convert inputs to integers. "
            f"Input num1=\"{num1}\", num2=\"{num2}\". Error: invalid literal for int() with base 10: '{num1}'"
        )
        mock_log_error.assert_called_with(expected_error_message_pattern)

    @patch('logging.info')
    @patch('logging.error')
    def test_add_invalid_number_type_error(self, mock_log_error, mock_log_info):
        """
        Test handling of a TypeError during conversion (e.g., a list),
        ensuring None is returned and an error is logged with the correct format.
        """
        num1 = [1, 2] # Non-numeric type
        num2 = 10
        custom_corr_id = "type-err-id"

        result = add_two_numbers(num1, num2, corrID=custom_corr_id)

        self.assertIsNone(result)
        self.assertEqual(mock_log_info.call_count, 2) # Only initial info logs

        # Verify initial info logs
        mock_log_info.assert_any_call(f'{custom_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.')
        mock_log_info.assert_any_call(f'{custom_corr_id} - Attempting to convert inputs to integers.')

        # Verify error log
        mock_log_error.assert_called_once()
        # The error message from Python's int() for a list might differ slightly across versions.
        # We'll assert for the most common pattern.
        expected_error_message_pattern = (
            f"correlation_ID:{custom_corr_id} Failed to convert inputs to integers. "
            f"Input num1=\"{num1}\", num2=\"{num2}\". Error: int() argument must be a string, a bytes-like object or a real number, not 'list'"
        )
        mock_log_error.assert_called_with(expected_error_message_pattern)

    @patch('logging.info')
    @patch('logging.error')
    def test_empty_corr_id_handling(self, mock_log_error, mock_log_info):
        """
        Test behavior when an empty string is passed as corrID,
        ensuring no prefix for info logs and only 'correlation_ID:' for error logs.
        """
        num1 = "100"
        num2 = "200"
        empty_corr_id = ''
        expected_result = 300

        # Test successful case with empty corrID
        result_success = add_two_numbers(num1, num2, corrID=empty_corr_id)
        self.assertEqual(result_success, expected_result)
        mock_log_error.assert_not_called()
        self.assertEqual(mock_log_info.call_count, 3)
        
        # Verify info logs have no ID prefix
        self.assertEqual(mock_log_info.call_args_list[0].args[0], f'Function `add_two_numbers` called with num1={num1}, num2={num2}.')
        self.assertEqual(mock_log_info.call_args_list[1].args[0], f'Attempting to convert inputs to integers.')
        self.assertEqual(mock_log_info.call_args_list[2].args[0], f'Successfully added {int(num1)} and {int(num2)}. Result: {expected_result}')
        
        mock_log_info.reset_mock()
        mock_log_error.reset_mock()

        # Test error case with empty corrID
        num1_error = "not_a_number"
        result_error = add_two_numbers(num1_error, num2, corrID=empty_corr_id)
        self.assertIsNone(result_error)
        self.assertEqual(mock_log_info.call_count, 2)
        mock_log_error.assert_called_once()

        # Verify error log has "correlation_ID:" prefix followed by no ID
        expected_error_message_pattern = (
            f"correlation_ID: Failed to convert inputs to integers. "
            f"Input num1=\"{num1_error}\", num2=\"{num2}\". Error: invalid literal for int() with base 10: '{num1_error}'"
        )
        mock_log_error.assert_called_with(expected_error_message_pattern)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
