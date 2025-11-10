
import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import os
import logging

# --- Helper code for the test environment ---
# These string literals represent the fixed demo_log_examples.py script
# and a mock implementation of the add_two_numbers function.
# They are used to create a self-contained test environment.

_fixed_demo_log_examples_code = """
#!/usr/bin/env python3
\"\"\"
Demo script to show log outputs for various edge cases in add_two_numbers function.
This will demonstrate what the application logs look like for different error scenarios.
\"\"\"

import sys
import os
import logging

# Configure basic logging to capture output (for demonstration)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Add the parent directory to sys.path to import addNums
# This line is effectively bypassed/handled by mocking sys.modules and os.path.
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from addNums import add_two_numbers

def demo_log_output(description, *args, **kwargs):
    \"\"\"Helper function to demonstrate log output for different inputs.\"\"\"
    print(f"\\n{'='*60}")
    print(f"SCENARIO: {description}")
    print(f"{'='*60}")
    print(f"Input: add_two_numbers{args}")
    if kwargs:
        print(f"Kwargs: {kwargs}")
    print("Log Output:")
    print("-" * 40)
    
    result = None
    try:
        result = add_two_numbers(*args, **kwargs)
    except (ValueError, TypeError) as e:
        # The fix: Catching TypeError and ValueError and logging the exception details
        print(f"ERROR: {type(e).__name__}: {e}")
        result = f"Exception caught: {type(e).__name__}"
    
    print("-" * 40)
    print(f"Return Value: {result}")
    print(f"{'='*60}")

# The if __name__ == "__main__": block is not executed by this unittest,
# as we directly call the demo_log_output function.
"""

_add_two_numbers_mock_impl = """
def add_two_numbers(a, b, **kwargs):
    # This mock function simulates the behavior of the original add_two_numbers
    # including raising specific errors (TypeError for None, ValueError for non-numeric strings)
    # and successful conversion for numeric strings.
    
    def _to_num(val):
        if isinstance(val, (int, float)):
            return val
        if val is None:
            # This specific TypeError message matches the original problem's error
            raise TypeError("unsupported operand type(s) for +: 'NoneType' and 'int'")
        if isinstance(val, str):
            try:
                # Try integer conversion first
                return int(val)
            except ValueError:
                try:
                    # Then try float conversion
                    return float(val)
                except ValueError:
                    # For non-numeric strings, including empty/whitespace/invalid characters
                    raise ValueError(f"Could not convert string '{val}' to a number.")
        # For other unexpected types (e.g., list, dict)
        raise TypeError(f"Unsupported input type: {type(val).__name__}")

    try:
        num_a = _to_num(a)
        num_b = _to_num(b)
    except (TypeError, ValueError) as e:
        # Re-raise the exception to be caught by the `demo_log_output`'s try-except block
        raise e
        
    return num_a + num_b
"""

# --- End Helper code ---


class TestDemoLogExamplesFix(unittest.TestCase):
    """
    Unit test to validate the fix applied to the demo_log_examples.py script.
    The fix ensures that the `demo_log_output` function can gracefully handle
    TypeError and ValueError from the `add_two_numbers` function.
    """

    def setUp(self):
        """
        Set up the test environment by mocking external dependencies and
        dynamically loading the fixed `demo_log_examples` script.
        """
        # 1. Mock the 'addNums' module and its 'add_two_numbers' function
        self.mock_add_nums_module = MagicMock()
        # Execute the mock implementation into the mock module's dictionary
        exec(_add_two_numbers_mock_impl, self.mock_add_nums_module.__dict__)
        
        # Patch sys.modules to ensure 'from addNums import add_two_numbers'
        # inside the demo script imports our mock.
        self.patcher_sys_modules = patch.dict(sys.modules, {'addNums': self.mock_add_nums_module})
        self.patcher_sys_modules.start()

        # 2. Patch sys.stdout to capture all print statements from demo_log_output
        self.stdout_patcher = patch('sys.stdout', new_callable=io.StringIO)
        self.mock_stdout = self.stdout_patcher.start()

        # 3. Patch os.path methods used in the demo script's sys.path manipulation
        # This prevents actual file system access and ensures self-contained testing.
        self.mock_dirname_patch = patch('os.path.dirname', return_value='/mock/dir')
        self.mock_abspath_patch = patch('os.path.abspath', return_value='/mock/dir/demo_log_examples.py')
        self.mock_dirname_patch.start()
        self.mock_abspath_patch.start()
        
        # 4. Capture and temporarily modify sys.path for `exec` context
        self._original_sys_path = sys.path[:]
        sys.path.insert(0, '/mock/dir') # Add a dummy path as the exec'd code expects sys.path modification

        # 5. Dynamically execute the fixed `demo_log_examples.py` code
        # This allows us to access `demo_log_output` directly without running the __main__ block.
        # It also ensures the script runs in a controlled environment with our mocks.
        globals_dict = {'sys': sys, 'os': os, 'logging': logging}
        exec(_fixed_demo_log_examples_code, globals_dict)
        self.demo_log_output = globals_dict['demo_log_output']

    def tearDown(self):
        """
        Clean up the test environment by stopping all patches and restoring system state.
        """
        self.mock_abspath_patch.stop()
        self.mock_dirname_patch.stop()
        self.stdout_patcher.stop()
        self.patcher_sys_modules.stop()
        sys.path = self._original_sys_path # Restore original sys.path
        # Clean up logging handlers to prevent interference with other tests
        logging.getLogger().handlers = []

    def test_type_error_handling_for_none_input(self):
        """
        Validate that `demo_log_output` catches and reports a TypeError
        when `add_two_numbers` receives `None` as input.
        """
        self.demo_log_output("None as first input", None, 5)
        output = self.mock_stdout.getvalue()
        
        self.assertIn("SCENARIO: None as first input", output)
        self.assertIn("Input: add_two_numbers(None, 5)", output)
        self.assertIn("ERROR: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'", output)
        self.assertIn("Return Value: Exception caught: TypeError", output)
        
        self.mock_add_nums_module.add_two_numbers.assert_called_with(None, 5)

    def test_value_error_handling_for_non_numeric_string(self):
        """
        Validate that `demo_log_output` catches and reports a ValueError
        when `add_two_numbers` receives a non-numeric string input.
        """
        self.demo_log_output("Non-numeric string input", "hello", 5)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Non-numeric string input", output)
        self.assertIn("Input: add_two_numbers('hello', 5)", output)
        self.assertIn("ERROR: ValueError: Could not convert string 'hello' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        
        self.mock_add_nums_module.add_two_numbers.assert_called_with("hello", 5)

    def test_normal_successful_addition(self):
        """
        Validate that `demo_log_output` correctly processes successful calls
        to `add_two_numbers` without reporting any errors.
        """
        # Configure the mock `add_two_numbers` to return a successful result
        self.mock_add_nums_module.add_two_numbers.return_value = 15

        self.demo_log_output("Normal successful addition", 10, 5)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Normal successful addition", output)
        self.assertIn("Input: add_two_numbers(10, 5)", output)
        self.assertIn("Return Value: 15", output)
        # Ensure no error messages are present for successful cases
        self.assertNotIn("ERROR:", output)
        self.assertNotIn("Exception caught:", output)
        
        self.mock_add_nums_module.add_two_numbers.assert_called_with(10, 5)

    def test_empty_string_causes_value_error(self):
        """
        Validate handling of empty string input, which should result in a ValueError.
        """
        self.demo_log_output("Empty string as first input", "", 5)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Empty string as first input", output)
        self.assertIn("Input: add_two_numbers('', 5)", output)
        self.assertIn("ERROR: ValueError: Could not convert string '' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("", 5)

    def test_whitespace_only_string_causes_value_error(self):
        """
        Validate handling of whitespace-only string input, resulting in a ValueError.
        """
        self.demo_log_output("Whitespace-only first input", "   ", 5)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Whitespace-only first input", output)
        self.assertIn("Input: add_two_numbers('   ', 5)", output)
        self.assertIn("ERROR: ValueError: Could not convert string '   ' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("   ", 5)

    def test_float_string_inputs_successful(self):
        """
        Validate that float strings are converted and added successfully by the mock.
        """
        self.mock_add_nums_module.add_two_numbers.return_value = 5.85 # 3.14 + 2.71

        self.demo_log_output("Float string inputs", "3.14", "2.71")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Float string inputs", output)
        self.assertIn("Input: add_two_numbers('3.14', '2.71')", output)
        self.assertIn("Return Value: 5.85", output)
        self.assertNotIn("ERROR:", output)
        self.assertNotIn("Exception caught:", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("3.14", "2.71")

    def test_scientific_notation_inputs_successful(self):
        """
        Validate that scientific notation strings are converted and added successfully.
        """
        self.mock_add_nums_module.add_two_numbers.return_value = 102000.0 # 1e5 + 2e3

        self.demo_log_output("Scientific notation", "1e5", "2e3")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Scientific notation", output)
        self.assertIn("Input: add_two_numbers('1e5', '2e3')", output)
        self.assertIn("Return Value: 102000.0", output)
        self.assertNotIn("ERROR:", output)
        self.assertNotIn("Exception caught:", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("1e5", "2e3")

    def test_hexadecimal_string_inputs_successful(self):
        """
        Validate that hexadecimal strings are converted and added successfully.
        """
        self.mock_add_nums_module.add_two_numbers.return_value = 271 # 0xFF (255) + 0x10 (16)

        self.demo_log_output("Hexadecimal strings", "0xFF", "0x10")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Hexadecimal strings", output)
        self.assertIn("Input: add_two_numbers('0xFF', '0x10')", output)
        self.assertIn("Return Value: 271", output)
        self.assertNotIn("ERROR:", output)
        self.assertNotIn("Exception caught:", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("0xFF", "0x10")

    def test_large_numbers_successful(self):
        """
        Validate handling of very large number strings.
        """
        num1 = "9" * 50
        num2 = "1" * 50
        expected_sum = int(num1) + int(num2)
        self.mock_add_nums_module.add_two_numbers.return_value = expected_sum

        self.demo_log_output("Very large numbers", num1, num2)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Very large numbers", output)
        self.assertIn(f"Input: add_two_numbers('{num1}', '{num2}')", output)
        self.assertIn(f"Return Value: {expected_sum}", output)
        self.assertNotIn("ERROR:", output)
        self.assertNotIn("Exception caught:", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with(num1, num2)

    def test_unicode_non_digits_cause_value_error(self):
        """
        Validate handling of unicode characters that cannot be converted to numbers,
        which should cause a ValueError. (Using 'v;lU' and 'v2mI' as per fixed code).
        """
        self.demo_log_output("Unicode full-width digits", "v;lU", "v2mI")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Unicode full-width digits", output)
        self.assertIn("Input: add_two_numbers('v;lU', 'v2mI')", output)
        # The mock raises ValueError on the first invalid argument.
        self.assertIn("ERROR: ValueError: Could not convert string 'v;lU' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("v;lU", "v2mI")

    def test_mixed_valid_invalid_causes_value_error(self):
        """
        Validate handling of mixed valid and invalid inputs, leading to a ValueError.
        """
        self.demo_log_output("One valid, one invalid", 10, "not_a_number")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: One valid, one invalid", output)
        self.assertIn("Input: add_two_numbers(10, 'not_a_number')", output)
        self.assertIn("ERROR: ValueError: Could not convert string 'not_a_number' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with(10, "not_a_number")
        
    def test_correlation_id_present_with_error(self):
        """
        Validate that kwargs are passed through and error handling works when corrID is present.
        """
        self.demo_log_output("Custom correlation ID with error", "invalid", 5, corrID="custom-test-id-123")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Custom correlation ID with error", output)
        self.assertIn("Input: add_two_numbers('invalid', 5)", output)
        self.assertIn("Kwargs: {'corrID': 'custom-test-id-123'}", output)
        self.assertIn("ERROR: ValueError: Could not convert string 'invalid' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("invalid", 5, corrID="custom-test-id-123")

    def test_empty_correlation_id_present_with_error(self):
        """
        Validate that an empty corrID is handled with error.
        """
        self.demo_log_output("Empty correlation ID", "invalid", 5, corrID="")
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Empty correlation ID", output)
        self.assertIn("Input: add_two_numbers('invalid', 5)", output)
        self.assertIn("Kwargs: {'corrID': ''}", output)
        self.assertIn("ERROR: ValueError: Could not convert string 'invalid' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with("invalid", 5, corrID="")

    def test_log_injection_attempt_causes_value_error(self):
        """
        Validate that a string resembling a log injection attempt in an argument
        is treated as invalid input, causing a ValueError.
        """
        injection_str = "5\nFAKE ERROR: correlation_ID:hacker-id Something bad"
        self.demo_log_output("Potential log injection", injection_str, 5)
        output = self.mock_stdout.getvalue()

        self.assertIn("SCENARIO: Potential log injection", output)
        self.assertIn(f"Input: add_two_numbers('{injection_str}', 5)", output)
        self.assertIn(f"ERROR: ValueError: Could not convert string '{injection_str}' to a number.", output)
        self.assertIn("Return Value: Exception caught: ValueError", output)
        self.mock_add_nums_module.add_two_numbers.assert_called_with(injection_str, 5)

if __name__ == '__main__':
    unittest.main()
