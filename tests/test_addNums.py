To validate the fix for the `add_two_numbers` function, we'll create a self-contained unit test file. This test will verify:
1.  **Correctness for valid inputs**: Ensure the function still sums numbers correctly, including various integer and string representations.
2.  **Robustness for invalid inputs**: Crucially, verify that the function now raises `ValueError` for non-numeric strings and `TypeError` for unsupported types (like `None`, `list`, `dict`), with the expected error messages.
3.  **Correlation ID handling**: Check that the `corrID` parameter correctly overrides or defaults to the global `correlation_ID`.

**File Name**: `tests/test_addNums.py`


# tests/test_addNums.py

import unittest
import logging
import sys
from io import StringIO

# --- Start of the self-contained code under test ---
# This section contains the 'fixed' version of the add_two_numbers function
# and its dependencies (correlation_ID and logging configuration).

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

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')

    try:
        logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')
        # Attempt to convert inputs to integers.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError as e:
        # This occurs if the string representation is not a valid integer (e.g., int("abc")).
        error_message = f"Invalid input. Please provide numbers (e.g., '10', 25). Details: {e}"
        logging.error(f'{corr_id_prefix}Input conversion failed (ValueError): {error_message}')
        raise ValueError(error_message)
    except TypeError as e:
        # This occurs if the input is of a type that cannot be implicitly converted to int
        # (e.g., None, list, dict).
        error_message = f"Invalid input type. Please provide numbers (or strings convertible to numbers). Details: {e}"
        logging.error(f'{corr_id_prefix}Input conversion failed (TypeError): {error_message}')
        raise TypeError(error_message)

    # Calculate the sum using the successfully converted integer values.
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Calculation successful. Result: {result}.')

    # Return the result.
    return result

# --- End of the self-contained code under test ---


class TestAddTwoNumbers(unittest.TestCase):
    """
    Test suite for the add_two_numbers function, focusing on its
    correctness and the newly implemented error handling.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up logging configuration for the entire test class.
        This captures log messages to an in-memory stream for assertions.
        """
        cls.log_stream = StringIO()
        cls.handler = logging.StreamHandler(cls.log_stream)
        cls.formatter = logging.Formatter('%(levelname)s:%(message)s')
        cls.handler.setFormatter(cls.formatter)
        
        # Get the root logger and add our handler
        cls.root_logger = logging.getLogger()
        # Set level to INFO to capture all logs from the function
        cls.root_logger.setLevel(logging.INFO) 
        cls.root_logger.addHandler(cls.handler)
        # Prevent logs from propagating to the console if other handlers are present
        cls.root_logger.propagate = False 

    @classmethod
    def tearDownClass(cls):
        """
        Clean up logging configuration after all tests in the class are done.
        """
        cls.root_logger.removeHandler(cls.handler)
        cls.handler.close()
        cls.root_logger.propagate = True # Restore propagation

    def setUp(self):
        """
        Prepare for each test: Clear the log stream and reset global correlation_ID.
        """
        self.log_stream.truncate(0) # Clear content
        self.log_stream.seek(0)     # Reset position to the beginning

        # Ensure the global correlation_ID is at its default for each test
        # (Though it's a string constant, good practice if it were mutable)
        global correlation_ID
        correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

    # --- Test Cases for Valid Inputs ---

    def test_add_positive_integers(self):
        """Test summing two positive integers."""
        self.assertEqual(add_two_numbers(5, 3), 8)
        self.assertEqual(add_two_numbers(100, 200), 300)

    def test_add_negative_integers(self):
        """Test summing two negative integers."""
        self.assertEqual(add_two_numbers(-5, -3), -8)
        self.assertEqual(add_two_numbers(-10, -20), -30)

    def test_add_mixed_integers(self):
        """Test summing mixed positive/negative integers and zeros."""
        self.assertEqual(add_two_numbers(5, -3), 2)
        self.assertEqual(add_two_numbers(-5, 3), -2)
        self.assertEqual(add_two_numbers(0, 0), 0)
        self.assertEqual(add_two_numbers(10, 0), 10)
        self.assertEqual(add_two_numbers(0, -7), -7)

    def test_add_string_integers(self):
        """Test summing two integers provided as strings."""
        self.assertEqual(add_two_numbers("5", "3"), 8)
        self.assertEqual(add_two_numbers("-10", "20"), 10)
        self.assertEqual(add_two_numbers("0", "0"), 0)

    def test_add_mixed_types_string_and_int(self):
        """Test summing an integer and an integer-string."""
        self.assertEqual(add_two_numbers(5, "3"), 8)
        self.assertEqual(add_two_numbers("10", 20), 30)
        self.assertEqual(add_two_numbers(-5, "3"), -2)

    # --- Test Cases for Invalid Inputs (Validating the Fix) ---

    def test_invalid_string_input_value_error(self):
        """
        Test that `ValueError` is raised for non-numeric string inputs (e.g., "abc")
        and verify the error message content.
        """
        expected_regex = r"Invalid input\. Please provide numbers \(e\.g\., '10', 25\)\. Details: invalid literal for int\(\) with base 10: 'abc'"
        with self.assertRaisesRegex(ValueError, expected_regex):
            add_two_numbers("abc", 5)

        expected_regex = r"Invalid input\. Please provide numbers \(e\.g\., '10', 25\)\. Details: invalid literal for int\(\) with base 10: 'hello'"
        with self.assertRaisesRegex(ValueError, expected_regex):
            add_two_numbers(10, "hello")
        
        log_output = self.log_stream.getvalue()
        self.assertIn("Input conversion failed (ValueError):", log_output)
        self.assertIn("invalid literal for int() with base 10: 'abc'", log_output)


    def test_none_input_type_error(self):
        """
        Test that `TypeError` is raised for `None` inputs
        and verify the error message content.
        """
        expected_regex = r"Invalid input type\. Please provide numbers \(or strings convertible to numbers\)\. Details: int\(\) argument must be a string, a bytes-like object or a real number, not 'NoneType'"
        with self.assertRaisesRegex(TypeError, expected_regex):
            add_two_numbers(None, 5)
        
        with self.assertRaisesRegex(TypeError, expected_regex):
            add_two_numbers(10, None)
        
        log_output = self.log_stream.getvalue()
        self.assertIn("Input conversion failed (TypeError):", log_output)
        self.assertIn("int() argument must be a string, a bytes-like object or a real number, not 'NoneType'", log_output)


    def test_list_input_type_error(self):
        """
        Test that `TypeError` is raised for `list` inputs
        and verify the error message content.
        """
        expected_regex = r"Invalid input type\. Please provide numbers \(or strings convertible to numbers\)\. Details: int\(\) argument must be a string, a bytes-like object or a real number, not 'list'"
        with self.assertRaisesRegex(TypeError, expected_regex):
            add_two_numbers([1, 2], 5)
        
        log_output = self.log_stream.getvalue()
        self.assertIn("Input conversion failed (TypeError):", log_output)
        self.assertIn("int() argument must be a string, a bytes-like object or a real number, not 'list'", log_output)


    def test_dict_input_type_error(self):
        """
        Test that `TypeError` is raised for `dict` inputs
        and verify the error message content.
        """
        expected_regex = r"Invalid input type\. Please provide numbers \(or strings convertible to numbers\)\. Details: int\(\) argument must be a string, a bytes-like object or a real number, not 'dict'"
        with self.assertRaisesRegex(TypeError, expected_regex):
            add_two_numbers({"a": 1}, 5)
        
        log_output = self.log_stream.getvalue()
        self.assertIn("Input conversion failed (TypeError):", log_output)
        self.assertIn("int() argument must be a string, a bytes-like object or a real number, not 'dict'", log_output)

    # --- Test Cases for Correlation ID Handling ---

    def test_correlation_id_override(self):
        """Test that corrID parameter overrides the global correlation_ID."""
        test_corr_id = "custom-corr-id-123"
        result = add_two_numbers(1, 2, corrID=test_corr_id)
        self.assertEqual(result, 3)
        log_output = self.log_stream.getvalue()
        # Ensure the custom ID is in the logs
        self.assertIn(f"{test_corr_id} - Function `add_two_numbers` called with", log_output)
        self.assertIn(f"{test_corr_id} - Calculation successful. Result: 3.", log_output)
        # Ensure the default global ID is NOT in the logs when overridden
        self.assertNotIn(f"{correlation_ID} - Function `add_two_numbers` called with", log_output)


    def test_correlation_id_default(self):
        """Test that the global correlation_ID is used when corrID is not provided."""
        result = add_two_numbers(1, 2)
        self.assertEqual(result, 3)
        log_output = self.log_stream.getvalue()
        # Ensure the default global ID is in the logs
        self.assertIn(f"{correlation_ID} - Function `add_two_numbers` called with", log_output)
        self.assertIn(f"{correlation_ID} - Calculation successful. Result: 3.", log_output)
        
    def test_correlation_id_none_param(self):
        """Test that passing None to corrID parameter falls back to global correlation_ID."""
        result = add_two_numbers(1, 2, corrID=None)
        self.assertEqual(result, 3)
        log_output = self.log_stream.getvalue()
        # Ensure the default global ID is in the logs
        self.assertIn(f"{correlation_ID} - Function `add_two_numbers` called with", log_output)
        
    def test_correlation_id_empty_string_param(self):
        """Test that passing an empty string to corrID results in no prefix."""
        result = add_two_numbers(1, 2, corrID="")
        self.assertEqual(result, 3)
        log_output = self.log_stream.getvalue()
        # The prefix should be empty, so no correlation ID or hyphen
        self.assertIn("Function `add_two_numbers` called with num1=1, num2=2.", log_output)
        # Ensure no hyphenated prefix is present
        self.assertNotIn("- Function `add_two_numbers`", log_output) 
        self.assertNotIn(correlation_ID, log_output) # Default ID should not be present


# This block allows you to run the tests directly from the command line
# using `python -m unittest tests/test_addNums.py` or simply `python tests/test_addNums.py`
if __name__ == '__main__':
    unittest.main()

