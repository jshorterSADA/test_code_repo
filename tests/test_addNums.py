
import unittest
import logging
from unittest.mock import patch, MagicMock

# --- Start of self-contained code to be tested (the fixed version of addNums.py) ---

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# In a test environment, we typically mock logging, but this setup ensures the
# logger exists and is configured as expected by the original module if not mocked.
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global correlation ID as per the original script
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
    except (ValueError, TypeError) as e:
        # Gracefully handle cases where inputs cannot be converted to numbers.
        # Log an error message indicating the failure and return None.
        logging.error(f"{error_prefix}Failed to convert inputs to numbers for addition. num1='{num1}', num2='{num2}'. Error: {type(e).__name__}: {e}")
        return None

# --- End of self-contained code to be tested ---


class TestAddTwoNumbers(unittest.TestCase):
    """
    Test suite for the add_two_numbers function, validating the proposed fix.
    The fix introduces an except block to gracefully handle conversion errors
    (ValueError, TypeError) by logging the error and returning None, instead of crashing.
    """

    def setUp(self):
        # Store original global correlation_ID for potential restoration in some tests
        self._original_correlation_ID = globals().get('correlation_ID')

    def tearDown(self):
        # Restore global correlation_ID after each test
        if self._original_correlation_ID is not None:
            globals()['correlation_ID'] = self._original_correlation_ID
        elif 'correlation_ID' in globals():
            del globals()['correlation_ID']

    @patch('logging.info')
    @patch('logging.error')
    def test_add_valid_integers(self, mock_error_log, mock_info_log):
        """Test with standard integer inputs."""
        result = add_two_numbers(10, 5)
        self.assertEqual(result, 15)
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3) # Function called, Attempting, Success
        self.assertIn("Successfully added 10 and 5. Result: 15", mock_info_log.call_args_list[2].args[0])
        self.assertTrue(mock_info_log.call_args_list[0].args[0].startswith(f'{correlation_ID} - '))

    @patch('logging.info')
    @patch('logging.error')
    def test_add_valid_string_integers(self, mock_error_log, mock_info_log):
        """Test with string representations of integers."""
        result = add_two_numbers("20", "7")
        self.assertEqual(result, 27)
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3)
        self.assertIn("Successfully added 20 and 7. Result: 27", mock_info_log.call_args_list[2].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_add_valid_floats_with_truncation(self, mock_error_log, mock_info_log):
        """Test with float inputs, expecting truncation as per int() conversion."""
        result = add_two_numbers(10.7, 5.3)
        self.assertEqual(result, 15)  # 10 + 5 due to int() truncation
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3)
        self.assertIn("Successfully added 10 and 5. Result: 15", mock_info_log.call_args_list[2].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_add_scientific_notation_strings(self, mock_error_log, mock_info_log):
        """Test with scientific notation strings, expecting float conversion then truncation."""
        result = add_two_numbers("1e1", "2.7")  # "1e1" is 10.0 -> 10. "2.7" is 2.7 -> 2. Sum = 12.
        self.assertEqual(result, 12)
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3)
        self.assertIn("Successfully added 10 and 2. Result: 12", mock_info_log.call_args_list[2].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_invalid_string_input_num1(self, mock_error_log, mock_info_log):
        """Test case where num1 cannot be converted to float (ValueError)."""
        num1 = "abc"
        num2 = 5
        result = add_two_numbers(num1, num2)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)  # 'Function called', 'Attempting conversion'
        self.assertEqual(mock_error_log.call_count, 1)
        expected_error_log_start = f"correlation_ID:{correlation_ID} Failed to convert inputs to numbers for addition. num1='{num1}', num2='{num2}'. Error: ValueError: could not convert string to float:"
        self.assertTrue(mock_error_log.call_args[0][0].startswith(expected_error_log_start))

    @patch('logging.info')
    @patch('logging.error')
    def test_none_input_num1(self, mock_error_log, mock_info_log):
        """Test case where num1 is None (TypeError during float conversion)."""
        num1 = None
        num2 = 5
        result = add_two_numbers(num1, num2)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)
        self.assertEqual(mock_error_log.call_count, 1)
        # Expected TypeError from float(None)
        expected_error_log_start = f"correlation_ID:{correlation_ID} Failed to convert inputs to numbers for addition. num1='{num1}', num2='{num2}'. Error: TypeError: float() argument must be a string or a real number, not 'NoneType'"
        self.assertTrue(mock_error_log.call_args[0][0].startswith(expected_error_log_start))

    @patch('logging.info')
    @patch('logging.error')
    def test_invalid_string_input_num2(self, mock_error_log, mock_info_log):
        """Test case where num2 cannot be converted to float (ValueError)."""
        num1 = 10
        num2 = "xyz"
        result = add_two_numbers(num1, num2)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)
        self.assertEqual(mock_error_log.call_count, 1)
        expected_error_log_start = f"correlation_ID:{correlation_ID} Failed to convert inputs to numbers for addition. num1='{num1}', num2='{num2}'. Error: ValueError: could not convert string to float:"
        self.assertTrue(mock_error_log.call_args[0][0].startswith(expected_error_log_start))

    @patch('logging.info')
    @patch('logging.error')
    def test_none_input_num2(self, mock_error_log, mock_info_log):
        """Test case where num2 is None (TypeError during float conversion)."""
        num1 = 10
        num2 = None
        result = add_two_numbers(num1, num2)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)
        self.assertEqual(mock_error_log.call_count, 1)
        expected_error_log_start = f"correlation_ID:{correlation_ID} Failed to convert inputs to numbers for addition. num1='{num1}', num2='{num2}'. Error: TypeError: float() argument must be a string or a real number, not 'NoneType'"
        self.assertTrue(mock_error_log.call_args[0][0].startswith(expected_error_log_start))

    @patch('logging.info')
    @patch('logging.error')
    def test_custom_correlation_id_success(self, mock_error_log, mock_info_log):
        """Test using a custom correlation ID for successful operation."""
        custom_corr_id = "test-corr-id-123"
        result = add_two_numbers(1, 2, corrID=custom_corr_id)
        self.assertEqual(result, 3)
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3)
        # Check that info messages use the custom_corr_id
        self.assertTrue(mock_info_log.call_args_list[0].args[0].startswith(f'{custom_corr_id} - '))
        self.assertIn(f'{custom_corr_id} - Successfully added 1 and 2. Result: 3', mock_info_log.call_args_list[2].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_custom_correlation_id_error(self, mock_error_log, mock_info_log):
        """Test using a custom correlation ID for failed operation."""
        custom_corr_id = "error-test-corr-id"
        result = add_two_numbers("bad", 2, corrID=custom_corr_id)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)
        self.assertEqual(mock_error_log.call_count, 1)
        # Check that error message uses the custom_corr_id
        expected_error_log_start = f"correlation_ID:{custom_corr_id} Failed to convert inputs to numbers for addition. num1='bad', num2='2'. Error: ValueError:"
        self.assertTrue(mock_error_log.call_args[0][0].startswith(expected_error_log_start))

    @patch('logging.info')
    @patch('logging.error')
    def test_no_correlation_id_available_success(self, mock_error_log, mock_info_log):
        """
        Test behavior when neither global nor argument correlation ID is provided.
        Prefixes should be empty.
        """
        del globals()['correlation_ID'] # Simulate no global ID
        result = add_two_numbers(1, 2, corrID=None)
        self.assertEqual(result, 3)
        self.assertEqual(mock_error_log.call_count, 0)
        self.assertGreaterEqual(mock_info_log.call_count, 3)
        # Check that info messages have no prefix
        self.assertFalse(mock_info_log.call_args_list[0].args[0].startswith(' - '))
        self.assertIn("Function `add_two_numbers` called with num1=1, num2=2.", mock_info_log.call_args_list[0].args[0])
        self.assertIn("Successfully added 1 and 2. Result: 3", mock_info_log.call_args_list[2].args[0])


    @patch('logging.info')
    @patch('logging.error')
    def test_no_correlation_id_available_error(self, mock_error_log, mock_info_log):
        """
        Test error behavior when no correlation ID is available.
        Error prefix should also be empty.
        """
        del globals()['correlation_ID'] # Simulate no global ID
        result = add_two_numbers("bad", 2, corrID=None)
        self.assertIsNone(result)
        self.assertEqual(mock_info_log.call_count, 2)
        self.assertEqual(mock_error_log.call_count, 1)
        # Check that error message has no prefix
        self.assertFalse(mock_error_log.call_args[0][0].startswith('correlation_ID: '))
        self.assertIn("Failed to convert inputs to numbers for addition. num1='bad', num2='2'. Error: ValueError:", mock_error_log.call_args[0][0])

if __name__ == '__main__':
    unittest.main()
