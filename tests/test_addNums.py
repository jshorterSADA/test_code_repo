
import unittest
import logging

# --- Start of the fixed code snippet from the prompt ---
# This part is included to make the test self-contained.

# Configure logging to match the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
# We set level to CRITICAL to suppress INFO messages during tests unless specifically asserting them,
# as too many INFO messages can clutter test output. assertLogs will temporarily override this.
logging.basicConfig(level=logging.CRITICAL, format='%(message)s')

# Define a global correlation_ID as it's used by the function if not overridden
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

    # The original file had these lines incorrectly indented and lacked error handling.
    # They are now correctly indented within a try block to catch conversion errors.
    try:
        num1_int = int(num1)
        num2_int = int(num2)
    except (ValueError, TypeError) as e:
        # Log the error and return None to gracefully handle conversion failures
        logging.error(f'{error_prefix}Failed to convert inputs to integers. num1="{num1}", num2="{num2}". Error: {e}')
        return None # Indicate failure as inputs could not be converted

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- End of the fixed code snippet ---


class TestAddTwoNumbers(unittest.TestCase):
    """
    Unit tests for the fixed add_two_numbers function.
    Validates correct behavior for valid inputs and graceful handling of invalid inputs.
    """

    def setUp(self):
        # Reset the logging level for tests that assert logs
        # This is important because basicConfig might have been called with CRITICAL
        # and assertLogs temporarily sets the level higher, but it's good practice
        # to ensure the logger is ready for capturing at INFO level for some tests.
        # For this specific test set, CRITICAL as default for basicConfig is fine,
        # as assertLogs handles setting the level within its context.
        pass

    def test_valid_integers(self):
        """Test with valid integer inputs."""
        self.assertEqual(add_two_numbers(1, 2), 3)
        self.assertEqual(add_two_numbers(-5, 10), 5)
        self.assertEqual(add_two_numbers(0, 0), 0)

    def test_valid_string_numbers(self):
        """Test with valid string representations of numbers."""
        self.assertEqual(add_two_numbers("10", "20"), 30)
        self.assertEqual(add_two_numbers("-100", "50"), -50)

    def test_mixed_valid_types(self):
        """Test with mixed integer and string number inputs."""
        self.assertEqual(add_two_numbers(5, "7"), 12)
        self.assertEqual(add_two_numbers("12", -3), 9)

    def test_invalid_string_input_returns_none_and_logs_error(self):
        """Test with non-numeric string inputs; should return None and log an error."""
        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("abc", 5))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="abc", num2="5". Error: invalid literal for int() with base 10: \'abc\'',
                cm.output[0]
            )

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers(10, "xyz"))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="10", num2="xyz". Error: invalid literal for int() with base 10: \'xyz\'',
                cm.output[0]
            )

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("abc", "xyz"))
            # The first conversion error encountered (for "abc") will be logged
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="abc", num2="xyz". Error: invalid literal for int() with base 10: \'abc\'',
                cm.output[0]
            )

    def test_none_input_returns_none_and_logs_error(self):
        """Test with None as input; should return None and log a TypeError."""
        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers(None, 5))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="None", num2="5". Error: int() argument must be a string, a bytes-like object or a number, not \'NoneType\'',
                cm.output[0]
            )

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers(10, None))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="10", num2="None". Error: int() argument must be a string, a bytes-like object or a number, not \'NoneType\'',
                cm.output[0]
            )

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers(None, None))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="None", num2="None". Error: int() argument must be a string, a bytes-like object or a number, not \'NoneType\'',
                cm.output[0]
            )

    def test_empty_string_input_returns_none_and_logs_error(self):
        """Test with empty string inputs; should return None and log a ValueError."""
        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("", "1"))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="", num2="1". Error: invalid literal for int() with base 10: \'\'',
                cm.output[0]
            )

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("1", ""))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="1", num2="". Error: invalid literal for int() with base 10: \'\'',
                cm.output[0]
            )

    def test_float_string_input_returns_none_and_logs_error(self):
        """Test with string representation of a float; should return None and log a ValueError."""
        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("1.5", "2"))
            self.assertIn(
                f'correlation_ID:{correlation_ID} Failed to convert inputs to integers. num1="1.5", num2="2". Error: invalid literal for int() with base 10: \'1.5\'',
                cm.output[0]
            )
            
    def test_correlation_id_override(self):
        """Test that the corrID argument correctly overrides the global correlation_ID."""
        custom_id = "test-corr-id-123"
        # Test with valid inputs and custom corrID
        with self.assertLogs(level='INFO') as cm:
            result = add_two_numbers(1, 2, corrID=custom_id)
            self.assertEqual(result, 3)
            # Check for info logs containing the custom ID
            self.assertIn(f'{custom_id} - Function `add_two_numbers` called with num1=1, num2=2.', cm.output[0])
            self.assertIn(f'{custom_id} - Successfully added 1 and 2. Result: 3', cm.output[2])
        
        # Test with invalid inputs and custom corrID, ensuring error logs use it
        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(add_two_numbers("bad_num", 2, corrID=custom_id))
            # Check for error log containing the custom ID
            self.assertIn(
                f'correlation_ID:{custom_id} Failed to convert inputs to integers. num1="bad_num", num2="2". Error: invalid literal for int() with base 10: \'bad_num\'',
                cm.output[0]
            )


# This ensures the tests run when the script is executed directly
if __name__ == '__main__':
    unittest.main()
