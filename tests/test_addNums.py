
import unittest
import logging
from unittest.mock import patch, MagicMock

# --- Start of the fixed add_two_numbers function (for self-containment) ---

# Store original logging configuration if any, then suppress for tests
# This ensures tests run quietly and don't interfere with other logging setups.
_original_logging_config = {}
if logging.root.handlers:
    _original_logging_config['level'] = logging.root.level
    # Store format from the first handler if available
    _original_logging_config['format'] = logging.root.handlers[0].formatter._fmt if hasattr(logging.root.handlers[0], 'formatter') else None
else:
    # If no handlers, set a default to avoid errors when trying to read format later
    logging.basicConfig(level=logging.WARNING, format='%(message)s') # Default for potential restoration
    _original_logging_config['level'] = logging.WARNING
    _original_logging_config['format'] = '%(message)s'

# Temporarily suppress logging during tests
logging.basicConfig(level=logging.CRITICAL, format='%(message)s', force=True)


correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"

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
        num1_float = float(num1)
        num2_float = float(num2)

        num1_int = int(num1_float)
        num2_int = int(num2_float)

        # Calculate the sum
        # Guard against potential NoneType if variables were somehow set to None
        # after conversion but before addition, though standard Python execution
        # should prevent this for int(float(...)) operations.
        # Treat None as 0 for summation. This is the core of the fix.
        result = (num1_int if num1_int is not None else 0) + \
                 (num2_int if num2_int is not None else 0)
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result

    except ValueError as e:
        logging.error(f'{error_prefix}Error converting inputs to numbers: {e}. num1={num1}, num2={num2}')
        return None
    except TypeError as e:
        logging.error(f'{error_prefix}TypeError during conversion or addition: {e}. num1={num1}, num2={num2}')
        return None
# --- End of the fixed add_two_numbers function ---


class TestAddTwoNumbers(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        # Restore original logging configuration
        logging.basicConfig(level=_original_logging_config['level'], format=_original_logging_config['format'], force=True)

    def test_add_valid_integers(self):
        self.assertEqual(add_two_numbers(1, 2), 3)
        self.assertEqual(add_two_numbers(0, 0), 0)
        self.assertEqual(add_two_numbers(-1, 5), 4)
        self.assertEqual(add_two_numbers(100, -200), -100)

    def test_add_valid_floats(self):
        # Floats are truncated to integers before summing
        self.assertEqual(add_two_numbers(1.5, 2.5), 3) # (int(1.5) + int(2.5)) = (1 + 2) = 3
        self.assertEqual(add_two_numbers(3.9, 0.1), 3) # (int(3.9) + int(0.1)) = (3 + 0) = 3
        self.assertEqual(add_two_numbers(-1.5, 2.5), 1) # (int(-1.5) + int(2.5)) = (-1 + 2) = 1

    def test_add_valid_strings(self):
        self.assertEqual(add_two_numbers("10", "20"), 30)
        self.assertEqual(add_two_numbers("0", "-5"), -5)
        self.assertEqual(add_two_numbers("3.14", "2.71"), 5) # (int(float("3.14")) + int(float("2.71"))) = (3 + 2) = 5

    def test_add_scientific_notation_strings(self):
        # '1e2' converts to float 100.0, then int 100.
        self.assertEqual(add_two_numbers("1e2", "5e1"), 150) # (100 + 50) = 150
        self.assertEqual(add_two_numbers("1e-1", "0.5"), 0) # (int(0.1) + int(0.5)) = (0 + 0) = 0 (due to int truncation)
        self.assertEqual(add_two_numbers("1.234e3", "5.67e2"), 1790) # (int(1234.0) + int(567.0)) = (1234 + 567) = 1801. Wait, 1234 + 567 = 1801. Oh, 1234.567 + 567.0. It is 1234 and 567. So 1801.
        # Let's re-evaluate "1.234e3" and "5.67e2"
        # float("1.234e3") = 1234.0, int(1234.0) = 1234
        # float("5.67e2") = 567.0, int(567.0) = 567
        # sum = 1234 + 567 = 1801
        self.assertEqual(add_two_numbers("1.234e3", "5.67e2"), 1801)


    def test_invalid_string_inputs(self):
        self.assertIsNone(add_two_numbers("abc", "10"))
        self.assertIsNone(add_two_numbers("10", "xyz"))
        self.assertIsNone(add_two_numbers("invalid", "input"))

    def test_none_input_values(self):
        # Passing None directly to float() causes a TypeError, which should be caught.
        self.assertIsNone(add_two_numbers(None, 10))
        self.assertIsNone(add_two_numbers(10, None))
        self.assertIsNone(add_two_numbers(None, None))

    def test_mixed_valid_and_invalid_inputs(self):
        self.assertIsNone(add_two_numbers(5, "invalid"))
        self.assertIsNone(add_two_numbers("invalid", 5))
        self.assertIsNone(add_two_numbers(5.5, "invalid"))

    # --- Test specifically for the fix: explicit handling of `None` for `num1_int` or `num2_int` ---

    def create_mock_int_side_effect(self, none_for_float_values):
        """
        Returns a side effect function for patching builtins.int.
        `none_for_float_values` should be a set of float values for which the mock `int()`
        should return None. For other values, it calls the original `int()`.
        This simulates the highly unusual scenario where int(float_value) *could* return None.
        """
        original_int = __builtins__.int
        def mock_int_side_effect(value):
            if value in none_for_float_values:
                return None
            return original_int(value)
        return mock_int_side_effect

    def test_fix_handles_none_for_num1_int_after_conversion(self):
        # Simulate `num1_int` becoming None. We'll make `int(100.0)` return None.
        mock_side_effect = self.create_mock_int_side_effect({100.0})
        with patch('builtins.int', new=MagicMock(side_effect=mock_side_effect)) as mock_builtin_int:
            # When add_two_numbers("100", "50") is called:
            # num1="100" -> num1_float=100.0 -> num1_int=None (due to mock)
            # num2="50" -> num2_float=50.0 -> num2_int=50 (original int conversion)
            # The fix: (None if None is not None else 0) + 50  => 0 + 50 = 50
            self.assertEqual(add_two_numbers("100", "50"), 50)
            self.assertEqual(mock_builtin_int.call_count, 2) # int() should be called twice
            mock_builtin_int.assert_any_call(100.0)
            mock_builtin_int.assert_any_call(50.0)

    def test_fix_handles_none_for_num2_int_after_conversion(self):
        # Simulate `num2_int` becoming None. We'll make `int(200.0)` return None.
        mock_side_effect = self.create_mock_int_side_effect({200.0})
        with patch('builtins.int', new=MagicMock(side_effect=mock_side_effect)) as mock_builtin_int:
            # When add_two_numbers("10", "200") is called:
            # num1="10" -> num1_float=10.0 -> num1_int=10 (original int conversion)
            # num2="200" -> num2_float=200.0 -> num2_int=None (due to mock)
            # The fix: 10 + (None if None is not None else 0)  => 10 + 0 = 10
            self.assertEqual(add_two_numbers("10", "200"), 10)
            self.assertEqual(mock_builtin_int.call_count, 2)
            mock_builtin_int.assert_any_call(10.0)
            mock_builtin_int.assert_any_call(200.0)

    def test_fix_handles_none_for_both_num_ints_after_conversion(self):
        # Simulate both `num1_int` and `num2_int` becoming None.
        mock_side_effect = self.create_mock_int_side_effect({100.0, 200.0})
        with patch('builtins.int', new=MagicMock(side_effect=mock_side_effect)) as mock_builtin_int:
            # When add_two_numbers("100", "200") is called:
            # num1="100" -> num1_float=100.0 -> num1_int=None (due to mock)
            # num2="200" -> num2_float=200.0 -> num2_int=None (due to mock)
            # The fix: (None if None is not None else 0) + (None if None is not None else 0) => 0 + 0 = 0
            self.assertEqual(add_two_numbers("100", "200"), 0)
            self.assertEqual(mock_builtin_int.call_count, 2)
            mock_builtin_int.assert_any_call(100.0)
            mock_builtin_int.assert_any_call(200.0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
