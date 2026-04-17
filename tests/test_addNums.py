
import unittest
import logging
from unittest.mock import patch, call
import sys
import io

# --- Fixed Code (as provided in the prompt) ---
# This section contains the 'fixed' add_two_numbers function and its
# associated global variables and logging configuration, making the test self-contained.

# Configure logging to match the desired output format for error and info
# messages. The 'message' format ensures that correlation IDs are printed
# directly as specified.
# ThisbasicConfig call might execute only once if handlers are already present.
# The setUp method in TestAddTwoNumbers addresses this by clearing handlers.
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global correlation_ID from the fixed code
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

    try:
        # The original file had these lines incorrectly indented and lacked error handling.
        # They are now correctly indented within a try block to catch conversion errors.
        num1_int = int(num1)
        num2_int = int(num2)
    except (ValueError, TypeError) as e:
        # Log the error and return None to indicate failure to convert and perform addition gracefully.
        logging.error(f'{error_prefix}Failed to convert inputs to integers. num1={num1}, num2={num2}. Error: {e}')
        return None

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- End of Fixed Code ---


class TestAddTwoNumbers(unittest.TestCase):

    def setUp(self):
        """
        Set up method to ensure a clean logging state before each test.
        This preventsbasicConfig from being ignored if handlers were added previously.
        """
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    @patch('logging.info')
    @patch('logging.error')
    def test_successful_addition_integers(self, mock_error, mock_info):
        """Test add_two_numbers with valid integer inputs and default correlation ID."""
        result = add_two_numbers(1, 2)
        self.assertEqual(result, 3)
        mock_error.assert_not_called() # No error logs expected for valid inputs

        # Verify correct info logs are made
        expected_info_calls = [
            call(f'{correlation_ID} - Function `add_two_numbers` called with num1=1, num2=2.'),
            call(f'{correlation_ID} - Attempting to convert inputs to integers.'),
            call(f'{correlation_ID} - Successfully added 1 and 2. Result: 3.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

    @patch('logging.info')
    @patch('logging.error')
    def test_successful_addition_strings(self, mock_error, mock_info):
        """Test add_two_numbers with valid string representations of numbers and default correlation ID."""
        result = add_two_numbers("10", "20")
        self.assertEqual(result, 30)
        mock_error.assert_not_called()

        expected_info_calls = [
            call(f'{correlation_ID} - Function `add_two_numbers` called with num1=10, num2=20.'),
            call(f'{correlation_ID} - Attempting to convert inputs to integers.'),
            call(f'{correlation_ID} - Successfully added 10 and 20. Result: 30.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

    @patch('logging.info')
    @patch('logging.error')
    def test_successful_addition_mixed_types(self, mock_error, mock_info):
        """Test add_two_numbers with mixed valid input types (int and string) and default correlation ID."""
        result = add_two_numbers(5, "7")
        self.assertEqual(result, 12)
        mock_error.assert_not_called()

        expected_info_calls = [
            call(f'{correlation_ID} - Function `add_two_numbers` called with num1=5, num2=7.'),
            call(f'{correlation_ID} - Attempting to convert inputs to integers.'),
            call(f'{correlation_ID} - Successfully added 5 and 7. Result: 12.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

    @patch('logging.info')
    @patch('logging.error')
    def test_addition_with_custom_correlation_id(self, mock_error, mock_info):
        """Test add_two_numbers with a custom correlation ID for successful addition."""
        custom_id = "test-corr-id-123"
        result = add_two_numbers(100, 200, corrID=custom_id)
        self.assertEqual(result, 300)
        mock_error.assert_not_called()

        expected_info_calls = [
            call(f'{custom_id} - Function `add_two_numbers` called with num1=100, num2=200.'),
            call(f'{custom_id} - Attempting to convert inputs to integers.'),
            call(f'{custom_id} - Successfully added 100 and 200. Result: 300.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

    @patch('logging.info')
    @patch('logging.error')
    def test_invalid_string_input_returns_none_and_logs_error(self, mock_error, mock_info):
        """Test add_two_numbers with an invalid string input, verifying None return and error log."""
        invalid_num = "abc"
        result = add_two_numbers(invalid_num, 5)
        self.assertIsNone(result) # Should return None on conversion failure

        # Verify info logs are made before the conversion attempt fails
        expected_info_calls = [
            call(f'{correlation_ID} - Function `add_two_numbers` called with num1={invalid_num}, num2=5.'),
            call(f'{correlation_ID} - Attempting to convert inputs to integers.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

        # Verify error log content and prefix
        mock_error.assert_called_once()
        error_message = mock_error.call_args[0][0]
        self.assertTrue(error_message.startswith(f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1={invalid_num}, num2=5. Error:'))
        self.assertIn("invalid literal for int()", error_message) # Check for specific ValueError message

    @patch('logging.info')
    @patch('logging.error')
    def test_none_input_returns_none_and_logs_error(self, mock_error, mock_info):
        """Test add_two_numbers with a None input, verifying None return and error log."""
        invalid_num = None
        result = add_two_numbers(10, invalid_num)
        self.assertIsNone(result) # Should return None on conversion failure

        # Verify info logs are made before the conversion attempt fails
        expected_info_calls = [
            call(f'{correlation_ID} - Function `add_two_numbers` called with num1=10, num2={invalid_num}.'),
            call(f'{correlation_ID} - Attempting to convert inputs to integers.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

        # Verify error log content and prefix
        mock_error.assert_called_once()
        error_message = mock_error.call_args[0][0]
        self.assertTrue(error_message.startswith(f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1=10, num2={invalid_num}. Error:'))
        # Check for specific TypeError message (varies slightly between Python versions)
        self.assertIn("int() argument must be a string, a bytes-like object or a real number, not 'NoneType'", error_message)

    @patch('logging.info')
    @patch('logging.error')
    def test_invalid_input_with_custom_correlation_id_logs_error(self, mock_error, mock_info):
        """Test add_two_numbers with invalid input and a custom correlation ID, ensuring error log uses custom ID prefix."""
        custom_id = "error-corr-id"
        result = add_two_numbers("bad", "data", corrID=custom_id)
        self.assertIsNone(result)

        # Verify info logs are made
        expected_info_calls = [
            call(f'{custom_id} - Function `add_two_numbers` called with num1=bad, num2=data.'),
            call(f'{custom_id} - Attempting to convert inputs to integers.')
        ]
        mock_info.assert_has_calls(expected_info_calls, any_order=False)
        self.assertEqual(mock_info.call_count, len(expected_info_calls))

        # Verify error log content and prefix
        mock_error.assert_called_once()
        error_message = mock_error.call_args[0][0]
        self.assertTrue(error_message.startswith(f'correlation_ID:{custom_id} Failed to convert inputs to integers. num1=bad, num2=data. Error:'))
        self.assertIn("invalid literal for int()", error_message)


# This allows running the tests directly from the file if needed, e.g., `python your_test_file.py`
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
