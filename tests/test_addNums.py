
To create a self-contained Python unittest for the fix, we'll place the corrected `add_two_numbers` function directly within the test file. This allows the test to run without external dependencies on `addNums.py`.

**Test File Name:** `tests/test_add_nums.py`



import unittest
import logging

from unittest.mock import patch, MagicMock

# --- Start of the fixed add_two_numbers function (self-contained for the test) ---
# This is the exact fixed code provided in the prompt.

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
    corr_id_prefix = f'{current_corr_id} - ' if current_corr_id else ''


    # Logging messages are included as they are part of the function's behavior.
    # During testing, we might configure logging to suppress output or capture it for specific log tests.

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')

    try:
        # Attempt to convert inputs to integers.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError as e:
        # Gracefully handle cases where conversion fails by logging the detailed error
        # and raising a user-friendly ValueError, consistent with the observed error message.
        logging.error(f'{corr_id_prefix}Failed to convert inputs to integers. Input num1="{num1}", num2="{num2}". Original error: {e}')
        raise ValueError("Invalid input. Please provide numbers.") from e

    # Calculate the sum using the successfully converted integer values.
    result = num1_int + num2_int

    # Return the result.
    return result

# --- End of self-contained `add_two_numbers` function ---


class TestAddNums(unittest.TestCase):

    def setUp(self):
        """
        Set up method to configure logging for tests.
        We'll replace existing handlers with a NullHandler to prevent test logs
        from cluttering the console, as we are primarily testing the function's
        return value or raised exceptions, not its logging output directly.
        """
        # Store original logging handlers to restore them later
        self.original_logging_handlers = logging.root.handlers[:]
        # Clear existing handlers
        logging.root.handlers = []
        # Add a NullHandler to suppress logging output during tests
        logging.root.addHandler(logging.NullHandler())
        # Set level to INFO to ensure info calls inside the function are processed by the NullHandler
        logging.root.setLevel(logging.INFO)

    def tearDown(self):
        """
        Tear down method to restore original logging configuration.
        """
        # Restore original logging handlers
        logging.root.handlers = self.original_logging_handlers
        # Reset logging level if necessary (though NullHandler doesn't care much)
        # logging.root.setLevel(logging.WARNING) # Or whatever default level is desired

    def test_valid_integer_inputs(self):
        """
        Test `add_two_numbers` with valid integer inputs.
        """
        self.assertEqual(add_two_numbers(1, 2), 3)
        self.assertEqual(add_two_numbers(0, 0), 0)
        self.assertEqual(add_two_numbers(-5, 10), 5)
        self.assertEqual(add_two_numbers(100, -50), 50)

    def test_valid_string_number_inputs(self):
        """
        Test `add_two_numbers` with valid string representations of numbers.
        """
        self.assertEqual(add_two_numbers("1", "2"), 3)
        self.assertEqual(add_two_numbers("0", "0"), 0)
        self.assertEqual(add_two_numbers("-5", "10"), 5)
        self.assertEqual(add_two_numbers("100", "-50"), 50)

    def test_invalid_non_numeric_input_raises_value_error(self):
        """
        Test that `add_two_numbers` raises a ValueError for non-numeric inputs
        and that the error message matches the fixed implementation.
        This directly validates the proposed fix.
        """
        # Test cases that should trigger the ValueError
        invalid_inputs = [
            ("abc", "123"),
            ("123", "xyz"),
            ("hello", "world"),
            ("", "10"),  # Empty string cannot be converted to int
            ("10", ""),  # Empty string cannot be converted to int
            (None, 5),   # NoneType cannot be converted to int
            (5, None),   # NoneType cannot be converted to int
            ([1], 2),    # List cannot be converted to int
            (1, {"a": 1}), # Dictionary cannot be converted to int
        ]

        expected_error_message = "Invalid input. Please provide numbers."

        for num1, num2 in invalid_inputs:
            with self.subTest(num1=num1, num2=num2):
                with self.assertRaisesRegex(ValueError, expected_error_message) as cm:
                    add_two_numbers(num1, num2)

                # Assert that the raised exception is exactly a ValueError
                self.assertIsInstance(cm.exception, ValueError)
                # Assert that the message matches the expected fix message
                self.assertEqual(str(cm.exception), expected_error_message)
                # Assert that the original ValueError from int() conversion is the cause
                # This checks that 'from e' part of the fix is working as intended.
                self.assertIsNotNone(cm.exception.__cause__)
                self.assertIsInstance(cm.exception.__cause__, ValueError)


# This allows running the tests directly from the command line
if __name__ == '__main__':
    unittest.main()
=======
        # Log the error and return None to indicate failure as per "gracefully handles"
        logging.error(f'{corr_id_prefix}Failed to convert one or both inputs to integers. Error: {e}. Inputs were num1="{num1}", num2="{num2}".')
        return None
   
    # Calculate the sum using the successfully converted integer values.
    result = num1_int + num2_int

    logging.info(f'{corr_id_prefix}Successfully calculated sum: {result}.')
    # Return the result.
    return result

# --- End of the fixed add_two_numbers function ---


class TestAddTwoNumbers(unittest.TestCase):

    def test_add_two_integers_successfully(self):
        """
        Test that two integer inputs are correctly summed.
        """
        self.assertEqual(add_two_numbers(1, 2), 3)
        self.assertEqual(add_two_numbers(0, 0), 0)
        self.assertEqual(add_two_numbers(-5, 10), 5)

    def test_add_two_string_integers_successfully(self):
        """
        Test that two string-representation integer inputs are correctly summed.
        """
        self.assertEqual(add_two_numbers("1", "2"), 3)
        self.assertEqual(add_two_numbers("-10", "20"), 10)
        self.assertEqual(add_two_numbers("0", "0"), 0)

    def test_add_mixed_integer_and_string_integer_successfully(self):
        """
        Test that mixed integer and string-integer inputs are correctly summed.
        """
        self.assertEqual(add_two_numbers(1, "2"), 3)
        self.assertEqual(add_two_numbers("-10", 20), 10)

    def test_invalid_string_input_returns_none(self):
        """
        Validate the fix: Test that an invalid string input (e.g., 'abc') results in None.
        """
        self.assertIsNone(add_two_numbers("abc", 2))
        self.assertIsNone(add_two_numbers(1, "xyz"))

    def test_both_invalid_string_inputs_returns_none(self):
        """
        Validate the fix: Test that two invalid string inputs result in None.
        """
        self.assertIsNone(add_two_numbers("abc", "def"))

    def test_float_string_input_returns_none(self):
        """
        Validate the fix: Test that string representations of floats, which int() cannot convert,
        also result in None.
        """
        self.assertIsNone(add_two_numbers("1.5", 2))
        self.assertIsNone(add_two_numbers(1, "2.0"))
        self.assertIsNone(add_two_numbers("3.14", "2.71"))

    def test_invalid_input_logs_error(self):
        """
        Validate the fix: Test that an ERROR level log message is generated when
        input conversion fails.
        """
        # Use unittest.mock.patch to capture logging.error calls
        with patch('logging.error') as mock_log_error:
            add_two_numbers("invalid", 5)
            mock_log_error.assert_called_once()
            # Assert content of the logged error message
            log_message = mock_log_error.call_args[0][0]
            self.assertIn('Failed to convert one or both inputs to integers.', log_message)
            self.assertIn('invalid', log_message)
            self.assertIn('5', log_message)
            self.assertIn('ValueError', log_message) # Check for the exception type

        with patch('logging.error') as mock_log_error:
            add_two_numbers(1, "invalid_num")
            mock_log_error.assert_called_once()
            log_message = mock_log_error.call_args[0][0]
            self.assertIn('Failed to convert one or both inputs to integers.', log_message)
            self.assertIn('1', log_message)
            self.assertIn('invalid_num', log_message)

    def test_successful_input_logs_info(self):
        """
        Test that INFO level log messages are generated for successful operations.
        """
        with patch('logging.info') as mock_log_info:
            add_two_numbers(10, 20)
            # Expect 3 INFO calls: 'function called', 'attempting conversion', 'successfully calculated'
            self.assertEqual(mock_log_info.call_count, 3)
            self.assertIn('Function `add_two_numbers` called with num1=10, num2=20.', mock_log_info.call_args_list[0][0][0])
            self.assertIn('Attempting to convert inputs to integers.', mock_log_info.call_args_list[1][0][0])
            self.assertIn('Successfully calculated sum: 30.', mock_log_info.call_args_list[2][0][0])

    def test_correlation_id_usage_in_logs(self):
        """
        Test that the correlation ID is correctly used in log messages.
        """
        test_corr_id = "custom-test-id-123"
        
        # Test with provided corrID
        with patch('logging.info') as mock_log_info:
            add_two_numbers(5, 7, corrID=test_corr_id)
            for call_args in mock_log_info.call_args_list:
                self.assertTrue(call_args[0][0].startswith(f'{test_corr_id} - '))

        # Test with global fallback corrID
        with patch('logging.info') as mock_log_info:
            add_two_numbers(1, 2) # No corrID specified
            global_corr_id_prefix = f'{correlation_ID} - '
            for call_args in mock_log_info.call_args_list:
                self.assertTrue(call_args[0][0].startswith(global_corr_id_prefix))


if __name__ == '__main__':
    unittest.main()

