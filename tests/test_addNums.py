
import unittest
import logging
import io

# Self-contained fixed code: addNums.py (decoded and fixed)
# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# Note: In a real application, logging.basicConfig is typically called once at startup.
# For unit testing, we'll manage handlers directly in setUp/tearDown.

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

    num1_int = None
    num2_int = None

    # The original file had these lines incorrectly indented and lacked error handling.
    # They are now correctly indented within a try block to catch conversion errors.
    try:
        num1_int = int(num1)
    except (ValueError, TypeError) as e:
        logging.error(f'{error_prefix}Error converting num1="{num1}" to an integer: {e}')
        # num1_int remains None if conversion fails

    try:
        num2_int = int(num2)
    except (ValueError, TypeError) as e:
        logging.error(f'{error_prefix}Error converting num2="{num2}" to an integer: {e}')
        # num2_int remains None if conversion fails
    
    if num1_int is None or num2_int is None:
        logging.error(f'{error_prefix}Cannot perform addition as one or both inputs are not valid integers (num1_int={num1_int}, num2_int={num2_int}).')
        return None # Graceful handling: return None if any input is invalid

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result


class TestAddTwoNumbers(unittest.TestCase):
    """
    Unit tests for the add_two_numbers function, validating the error handling fix.
    """

    def setUp(self):
        """Set up logging to capture output during tests."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Capture INFO and ERROR messages

        # Save original handlers and level to restore them later
        self.original_level = self.logger.level
        self.original_handlers = self.logger.handlers[:]

        # Remove all existing handlers to prevent log messages from going to console/other places
        for handler in self.original_handlers:
            self.logger.removeHandler(handler)

        # Create a new StringIO object to capture log messages
        self.log_stream = io.StringIO()
        self.handler = logging.StreamHandler(self.log_stream)
        
        # Apply the desired log format to the handler
        formatter = logging.Formatter('%(message)s')
        self.handler.setFormatter(formatter)
        
        self.logger.addHandler(self.handler)

    def tearDown(self):
        """Clean up logging after each test."""
        self.logger.removeHandler(self.handler)
        self.handler.close()

        # Restore original handlers and level
        self.logger.handlers = self.original_handlers[:]
        self.logger.setLevel(self.original_level)

    def _get_logged_messages(self):
        """Helper to get captured log messages and clear the stream."""
        self.handler.flush() # Ensure all logs are written to the stream
        log_contents = self.log_stream.getvalue()
        self.log_stream.truncate(0) # Clear the stream for the next test
        self.log_stream.seek(0)
        return log_contents

    def test_add_valid_integers(self):
        """Test with valid integer inputs."""
        result = add_two_numbers(1, 2)
        self.assertEqual(result, 3)
        logs = self._get_logged_messages()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=1, num2=2.', logs)
        self.assertIn(f'{correlation_ID} - Successfully added 1 and 2. Result: 3', logs)

    def test_add_valid_strings(self):
        """Test with valid string-represented integer inputs."""
        result = add_two_numbers('5', '7')
        self.assertEqual(result, 12)
        logs = self._get_logged_messages()
        self.assertIn(f'{correlation_ID} - Function `add_two_numbers` called with num1=5, num2=7.', logs)
        self.assertIn(f'{correlation_ID} - Successfully added 5 and 7. Result: 12', logs)

    def test_invalid_num1_string(self):
        """Test graceful handling when num1 is an invalid string."""
        result = add_two_numbers('abc', 2)
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num1=\"abc\" to an integer: invalid literal for int() with base 10: 'abc'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Cannot perform addition as one or both inputs are not valid integers (num1_int=None, num2_int=2).", logs)
        # Ensure no TypeError was raised

    def test_invalid_num2_string(self):
        """Test graceful handling when num2 is an invalid string."""
        result = add_two_numbers(1, 'xyz')
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num2=\"xyz\" to an integer: invalid literal for int() with base 10: 'xyz'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Cannot perform addition as one or both inputs are not valid integers (num1_int=1, num2_int=None).", logs)

    def test_invalid_num1_none(self):
        """Test graceful handling when num1 is None."""
        result = add_two_numbers(None, 2)
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num1=\"None\" to an integer: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Cannot perform addition as one or both inputs are not valid integers (num1_int=None, num2_int=2).", logs)

    def test_invalid_num2_none(self):
        """Test graceful handling when num2 is None."""
        result = add_two_numbers(1, None)
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num2=\"None\" to an integer: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Cannot perform addition as one or both inputs are not valid integers (num1_int=1, num2_int=None).", logs)

    def test_both_invalid_inputs_strings(self):
        """Test graceful handling when both inputs are invalid strings."""
        result = add_two_numbers('a', 'b')
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num1=\"a\" to an integer: invalid literal for int() with base 10: 'a'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Error converting num2=\"b\" to an integer: invalid literal for int() with base 10: 'b'", logs)
        self.assertIn(f"correlation_ID:{correlation_ID} Cannot perform addition as one or both inputs are not valid integers (num1_int=None, num2_int=None).", logs)

    def test_custom_correlation_id_success(self):
        """Test with a custom correlation ID for successful operation."""
        custom_id = "test-corr-id-123"
        result = add_two_numbers(10, 20, corrID=custom_id)
        self.assertEqual(result, 30)
        logs = self._get_logged_messages()
        self.assertIn(f'{custom_id} - Function `add_two_numbers` called with num1=10, num2=20.', logs)
        self.assertIn(f'{custom_id} - Successfully added 10 and 20. Result: 30', logs)

    def test_custom_correlation_id_error(self):
        """Test with a custom correlation ID for an erroneous operation."""
        custom_id = "error-corr-id-456"
        result = add_two_numbers('bad', 5, corrID=custom_id)
        self.assertIsNone(result)
        logs = self._get_logged_messages()
        self.assertIn(f'correlation_ID:{custom_id} Error converting num1="bad" to an integer: invalid literal for int() with base 10: \'bad\'', logs)
        self.assertIn(f'correlation_ID:{custom_id} Cannot perform addition as one or both inputs are not valid integers (num1_int=None, num2_int=5).', logs)


if __name__ == '__main__':
    unittest.main()
