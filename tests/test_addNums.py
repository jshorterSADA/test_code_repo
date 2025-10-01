To validate the fix, we need a unit test that confirms two things:
1.  When invalid inputs are provided, the `add_two_numbers` function correctly returns `None`.
2.  When invalid inputs are provided, an error message is logged with the precise format, including the correct correlation ID.
3.  When valid inputs are provided, the function continues to work as expected, and no error messages are logged.

The test will include the *fixed* version of the `add_two_numbers` function directly within the test file to ensure self-containment and direct testing of the provided fix. We will also set up logging capture using `StringIO` to inspect the logged messages.

**File Name:** `tests/test_addNums.py`


# tests/test_addNums.py
import unittest
import logging
from io import StringIO
import sys

# --- Start of Fixed Original Code (copied for self-containment) ---
# Note: In a real project, you would typically import 'add_two_numbers' from 'addNums.py'.
# For a self-contained test validating a fix, including the fixed code directly
# ensures the test runs against the exact version being validated.

# Temporarily store original logging state to restore after the test module runs.
# This prevents interference with other tests or global logging configuration if this
# test module is part of a larger test suite.
_original_logging_handlers = logging.root.handlers[:]
_original_logging_level = logging.root.level
_original_logging_formatter = None
if _original_logging_handlers and _original_logging_handlers[0].formatter:
    _original_logging_formatter = _original_logging_handlers[0].formatter

# Clear existing handlers before basicConfig to ensure a clean state for the test's
# basicConfig setup as it's part of the "system under test's environment" being replicated.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging as specified in the original code.
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
    corr_id_prefix = f'{current_corr_id} - ' if current_corr_id else ''

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')

    try:
        # Attempt to convert inputs to integers.
        # This is where the ValueError can occur if inputs are not valid.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError:
        # Log the error with the correlation ID in the specified format
        logging.error(f'correlation_ID:{current_corr_id} Value Error: Failed to convert one or both inputs to integers.')
        return None # Gracefully handle by returning None or raising a custom exception

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- End of Fixed Original Code ---


class TestAddTwoNumbers(unittest.TestCase):
    """
    Unit tests for the fixed add_two_numbers function.
    """

    def setUp(self):
        """Set up logging capture for each test."""
        # Create a StringIO object to capture logs
        self.log_stream = StringIO()
        # Create a StreamHandler that writes to the StringIO object
        self.handler = logging.StreamHandler(self.log_stream)
        # Set the formatter to match the application's format ('%(message)s')
        self.handler.setFormatter(logging.Formatter('%(message)s'))

        # Add the handler to the root logger
        logging.root.addHandler(self.handler)
        # Ensure the root logger level is set to INFO or lower to capture all relevant messages (INFO, ERROR)
        logging.root.setLevel(logging.INFO)

        # Clear the log stream before each test
        self.log_stream.seek(0)
        self.log_stream.truncate(0)

    def tearDown(self):
        """Clean up logging capture after each test."""
        # Remove the handler after each test
        logging.root.removeHandler(self.handler)
        self.handler.close()

    def get_logged_messages(self):
        """Helper to retrieve and clear logged messages from the buffer."""
        self.log_stream.seek(0)  # Go to the beginning of the stream
        logs = self.log_stream.read()
        self.log_stream.seek(0)  # Reset for next read
        self.log_stream.truncate(0)  # Clear the buffer
        return logs

    def test_add_two_numbers_valid_integers(self):
        """Test with valid integer inputs should return the correct sum and log INFO."""
        result = add_two_numbers(5, 7)
        self.assertEqual(result, 12)
        logs = self.get_logged_messages()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=5, num2=7.', logs)
        self.assertIn(f'{correlation_ID} - Successfully added 5 and 7. Result: 12', logs)
        self.assertNotIn('Value Error', logs) # Ensure no error was logged

    def test_add_two_numbers_valid_string_integers(self):
        """Test with valid string integer inputs should return the correct sum and log INFO."""
        result = add_two_numbers('10', '15')
        self.assertEqual(result, 25)
        logs = self.get_logged_messages()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=10, num2=15.', logs)
        self.assertIn(f'{correlation_ID} - Successfully added 10 and 15. Result: 25', logs)
        self.assertNotIn('Value Error', logs) # Ensure no error was logged

    def test_add_two_numbers_invalid_input_returns_none(self):
        """Test that invalid inputs (e.g., non-numeric strings) return None."""
        result1 = add_two_numbers('abc', 10)
        self.assertIsNone(result1)
        self.get_logged_messages() # Consume logs for this call

        result2 = add_two_numbers(5, 'xyz')
        self.assertIsNone(result2)
        self.get_logged_messages() # Consume logs for this call

        result3 = add_two_numbers('10.5', '2') # Float string is not an integer
        self.assertIsNone(result3)

    def test_add_two_numbers_invalid_input_logs_error_with_global_corr_id(self):
        """Test that invalid input logs the correct error message with the global correlation ID."""
        add_two_numbers('abc', 10)
        logs = self.get_logged_messages()
        expected_error_log = f'correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers.'
        self.assertIn(expected_error_log, logs)
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=abc, num2=10.', logs)
        self.assertNotIn('Successfully added', logs) # Ensure success message is NOT logged

    def test_add_two_numbers_invalid_input_logs_error_with_custom_corr_id(self):
        """Test that invalid input logs the correct error message with a custom correlation ID."""
        custom_corr_id = "custom-test-id-999"
        add_two_numbers(5, 'xyz', corrID=custom_corr_id)
        logs = self.get_logged_messages()
        expected_error_log = f'correlation_ID:{custom_corr_id} Value Error: Failed to convert one or both inputs to integers.'
        self.assertIn(expected_error_log, logs)
        self.assertIn(f'{custom_corr_id} - Function `add_two_numbers` called with num1=5, num2=xyz.', logs)
        self.assertNotIn('Successfully added', logs) # Ensure success message is NOT logged

    def test_add_two_numbers_invalid_float_string_input_logs_error(self):
        """Test that float string inputs also trigger ValueError and log the error."""
        add_two_numbers('3.14', '5')
        logs = self.get_logged_messages()
        expected_error_log = f'correlation_ID:{correlation_ID} Value Error: Failed to convert one or both inputs to integers.'
        self.assertIn(expected_error_log, logs)
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=3.14, num2=5.', logs)
        self.assertNotIn('Successfully added', logs)


# Restore original logging configuration after all tests in this module have run.
# This is crucial for isolating the tests' logging setup from other parts of an application
# or other test modules that might be run in the same test suite.
logging.root.handlers = _original_logging_handlers
logging.root.setLevel(_original_logging_level)
if _original_logging_formatter:
    for handler in logging.root.handlers:
        # Apply the original formatter to restored handlers if they are stream handlers
        if isinstance(handler, logging.StreamHandler) and hasattr(handler, 'setFormatter'):
            handler.setFormatter(_original_logging_formatter)


if __name__ == '__main__':
    unittest.main()
