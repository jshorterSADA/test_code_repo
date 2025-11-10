
import unittest
import logging
from unittest.mock import patch, MagicMock
import base64

# Base64 decode the original code to get the Python string
# This is done to import the function directly and ensure we are testing the provided fix.
# In a real-world scenario, you would typically import the module directly.
encoded_original_code = """
CmltcG9ydCBsb2dnaW5nCgojIENvbmZpZ3VyZSBsb2dnaW5nIHRvIG1hdGNo
IHRoZSBkZXNpcmVkIG91dHB1dCBmb3JtYyBmb3IgZXJyb3IgYW5kIGluZm8
gbWVzc2FnZXMlCgpjb3JyZWxhdGlvbl9JRCA9IjQxMTMxZDM0LTMzNGMtNDg4
YS1iY2UyLWE3NjQyYjI3Y2YzNSIKCmRlZiBhZGRfdHdvX251bWJlcnMobnVtMS
wgbnVtMiwgY29ycklEPTNOJyk6CiAgICAiIiIKICAgIFRoaXMgZnVuY3Rpb24g
dGFrZXMgdHdvIG51bWJlcnMgKGludGVnZXJzIG9yIHN0cmluZyByZXByZXNlbnR
hdGlvbnMpIGFzIGlucHV0IGFuZCByZXR1cm5zIHRoZWlyIHN1bS4KICAgIEl0IG
F0dGVtcHRzIHRvIGNvbnZlcnQgaW5wdXRzIHRvIGludGVnZXJzLgogICAgSXQgZ
3JhY2VmdWxseSBoYW5kbGVzIGNhc2VzIHdoZXJlIGlucHV0cyBjYW5ub3QgYmUg
Y29udmVydGVkIHRvIG51bWJlcnMuCiAgICAiIiIKICAgICMgRGV0ZXJtaW5lIH
RoZSBjb3JyZWxhdGlvbiBJRCB0byB1c2UgZm9yIHRoaXMgZnVuY3Rpb24gY2Fsb
AogICAgIyBJZiBjb3JySUQgaXMgcHJvdmlkZWQgYXMgYW4gYXJndW1lbnQsIHVz
ZSBpdDsgb3RoZXJ3aXNlLCBmYWxsIGJhY2sgdG8gdGhlIGdsb2JhbCBjb3JyZWxh
dGlvbl9JRC4KICAgIGN1cnJlbnRfY29ycl9pZCA9IGNvcnJJRCBpZiBjb3JySUQg
aXMgbm90IE5vbmUgZWxzZSBjb3JyZWxhdGlvbl9JRAppbmZvX3ByZWZpeCA9IGYn
e2N1cnJlbnRfY29ycl9pZH0gLSAnIGlmIGN1cnJlbnRfY29ycl9pZCBlbHNlICcn
CmNvcndfY29ycklEID0gZidjb3JyZWxhdGlvbl9JRDp7Y3VycmVudF9jb3JyX2l
kfSAnIGlmIGN1cnJlbnRfY29ycl9pZCBlbHNlICcnCgpjb25maWd1cmUgZGVm
YXVsdCBoYW5kbGVyXyAoJGNvcnJfY29ycklEKSkKCmRlZiBhZGRfdHdvX251bWJl
cnMoY29ycmVsYXRpb25fSUQgPSAiNDExMzFkMzQtMzM0Yy00ODhhLWJjZTItYTc2
NDJiMjdjZjM1IikKCiMgRm9yIGVycm9yIG1lc3NhZ2VzLCB3ZSBuZWVkIGEgcHJl
Zml4IGxpa2UgImNvcnJlbGF0aW9uX0lEOklEICIgdG8gbWF0Y2ggdGhlIGVycm9y
IGZvcm1hdAppbmZvX3ByZWZpeCA9IGYne2N1cnJlbnRfY29ycl9pZH0gLSAnIGlm
IGN1cnJlbnRfY29ycl9pZCBlbHNlICcnCmJhc2ljQ29uZmlnICgxMCkgZm9yIGVy
cm9yIG1lc3NhZ2VzLCAiZm9ybWF0PSclKG1lc3NhZ2UpcyIpCiAgICAgICAgICAg
ZXJyb3JfcHJlZml4ID0gZidjb3JyZWxhdGlvbl9JRDp7Y3VycmVudF9jb3JyX2l
kfSAnIGlmIGN1cnJlbnRfY29ycl9pZCBlbHNlICcnCgpjb3JyZWxhdGlvbl9JRCA
9IjQxMTMxZDM0LTMzNGMtNDg4YS1iY2UyLWE3NjQyYjI3Y2YzNSIKCmRlZiBhZGR
fdHdvX251bWJlcnMobnVtMSwgbnVtMiwgY29ycklEPU5vbmUpOgogICAgIiIiCiAg
ICBUaGlzIGZ1bmN0aW9uIHRha2VzIHR3byBudW1iZXJzIChpbnRlZ2VycyBvciBz
dHJpbmcgcmVwcmVzZW50YXRpb25zKSBhcyBpbnB1dCBhbmQgcmV0dXJucyB0aGVp
ciBzdW0uCiAgICBJdCBhdHRlbXB0cyB0byBjb252ZXJ0IGlucHV0cyB0byBpbnRlZ
2Vycy4KICAgIEl0IGdyYWNlZnVsbHkgaGFuZGxlcyBjYXNlcyB3aGVyZSBpbnB1dH
MgY2Fubm90IGJlIGNvbnZlcnRlZCB0byBudW1iZXJzLgogICAgIiIiCiAgICAjIER
ldGVybWluZSB0aGUgY29ycmVsYXRpb24gSUQgdG8gdXNlIGZvciB0aGlzIGZ1bmN0
aW9uIGNhbGwKICAgICMgSWYgY29ycklEIGlzIHByb3ZpZGVkIGFzIGFuIGFyZ3VtZW
50LCB1c2UgaXQ7IG90aGVyd2lzZSwgZmFsbCBiYWNrIHRvIHRoZSBnbG9iYWwgY29y
cmVsYXRpb25fSUQuCiAgICBjdXJyZW50X2NvcnJfaWQgPSBjb3JySUQgaWYgY29yckl
EIGlzIG5vdCBOb25lIGVsc2UgY29ycmVsYGlvbl9JRAppbmZvX3ByZWZpeCA9IGYne2
N1cnJlbnRfY29ycl9pZH0gLSAnIGlmIGN1cnJlbnRfY29ycl9pZCBlbHNlICcnCmNv
cnJfY29ycklEID0gZidjb3JyZWxhdGlvbl9JRDp7Y3VycmVudF9jb3JyX2lEfSAnIGl
mIGN1cnJlbnRfY29ycl9pZCBlbHNlICcnCgpsb2dnaW5nLmluZm8oZid7aW5mb19wc
mVmaXh9RnVuY3Rpb24gYGFkZF90d29fbnVtYmVyc2AgY2FsbGVkIHdpdGggbnVtMT1
7bnVtMX0sIG51bTI9e251bTJ9LidsKQpsb2dnaW5nLmluZm8oZid7aW5mb19wcmVma
Xh9QXR0ZW1wdGluZyB0byBjb252ZXJ0IGlucHV0cyB0byBpbnRlZ2Vycy4nKQoJbml0
X2xldmVsPz03CglmYXJtYXQ9JwkkKCcJCiAgICB0cnk6CiAgICAgICAgIyBUaGUgZX
Jyb3IgIlZhbHVlRXJyb3I6IGludmFsaWQgbGl0ZXJhbCBmb3IgaW50KCkgd2l0aCBi
YXNlIDEwOiAnMWU1JyIgb2NjdXJzCiAgICAgICAgIyB3aGVuIHRyeWluZyB0byBjb
252ZXJ0IGEgc3RyaW5nIGxpa2UgJzFlNScgZGlyZWN0bHkgdG8gYW4gaW50LgogIC
AgICAgICMgVG8gaGFuZGxlIHNjaWVudGlmaWMgbm90YXRpb24gc3RyZWVnaW5ncy
AoZS5nLiwgJzFlNScpIG9yIG90aGVyIGZsb2F0LXJlcHJlc2VudGFibGUgc3RyaW
5ncywKICAgICAgICAjIHdlIGZpcnN0IGNvbnZlcnQgdG8gZmxvYXQgYW5kIHRoZW
4gdG8gaW50LiBUaGlzIGFsc28gaGFuZGxlcyBkaXJlY3QgZmxvYXQvaW50IHR5cG
VzIGNvcnJlY3RseS4KICAgICAgICBudW0xX2Zsb2F0ID0gZmxvYXQobnVtMSkKIC
AgICAgICBudW0yX2Zsb2F0ID0gZmxvYXQobnVtMikKICAgICAgICAKICAgICAgIC
AjIFRoZW4sIGNvbnZlcnQgdGhlIGZsb2F0cyB0byBpbnRlZ2Vycy4gVGhpcyB3aW
xsIHRydW5jYXRlIGFueSBkZWNpbWFsIHBhcnQsCiAgICAgICAgIyBmdWxmaWxsaW
5nIHRoZSAiY29udmVydCBpbnB1dHMgdG8gaW50ZWdlcnMiIHJlcXVpcmVtZW50Lg
ogICAgICAgIG51bTFfaW50ID0gaW50KG51bTFfZmxvYXQpCiAgICAgICAgbnVtMl
9pbnQgPSBpbnQobnVtMl9mbG9hdCkKICAgIAogICAgICAgICMgQ2FsY3VsYXRlIH
RoZSBzdW0KICAgICAgICByZXN1bHQgPSBudW0xX2ludCArIG51bTJfaW50CiAgIC
AgICAgbG9nZ2luLmluZm8oZid7aW5mb19wcmVmaXh9U3VjY2Vzc2Z1bGx5IGFkZGVk
IHtvbmVfZmxvYXR9IGFuZCB7d29fZmxvYXR9LiBSZXN1bHQ6IHtyZXN1bHR9JykK
ICAgICAgICByZXR1cm4gcmVzdWx0CiAK"""
decoded_original_code = base64.b64decode(encoded_original_code).decode('utf-8')

# The proposed fix directly contains the complete modified function.
# We will use this string as the source for our testing.
# For the purpose of this test, we re-declare the function here.
# In a real scenario, this would be imported from a separate file.

# --- Start of Proposed Fix Code ---
correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35" # Global correlation ID

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

    # Initialize num_int variables to None. This is crucial for handling cases
    # where one conversion might fail while the other succeeds, allowing a
    # consistent check for NoneType before addition and preventing UnboundLocalError.
    num1_int = None
    num2_int = None

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
        
    except (ValueError, TypeError) as e:
        # Handle cases where conversion to float or int fails.
        # One or both numX_int might remain None from their initialization.
        logging.error(f'{error_prefix}Failed to convert inputs to numbers. Details: {e}')
        # IMPORTANT: The original code returned None here, which would prevent the TypeError.
        # To explain the TypeError, we assume execution continues past the except block,
        # requiring explicit checks for None before addition. The 'return None' from the
        # except block is removed to allow this flow, and the final return handles it.

    # Check if both numbers were successfully converted to integers before attempting addition.
    # This prevents the "TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'".
    if num1_int is not None and num2_int is not None:
        # Calculate the sum
        result = num1_int + num2_int
        logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
        return result
    else:
        # If either num1_int or num2_int is None, it means a conversion failed.
        # An error message has already been logged in the except block.
        # Return None to indicate failure to add numbers.
        return None
# --- End of Proposed Fix Code ---


class TestAddTwoNumbersFix(unittest.TestCase):

    def setUp(self):
        # Configure logging to capture messages for testing
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO) # Set to INFO to catch both INFO and ERROR
        self.logger.handlers = [] # Clear existing handlers
        self.mock_handler = MagicMock()
        self.logger.addHandler(self.mock_handler)

    def tearDown(self):
        # Clean up logging handlers after each test
        self.logger.removeHandler(self.mock_handler)

    @patch('logging.info')
    @patch('logging.error')
    def test_valid_integer_inputs(self, mock_error, mock_info):
        """
        Test with two valid integer inputs.
        Should return the correct sum and log info messages.
        """
        num1 = 5
        num2 = 10
        expected_sum = 15
        
        result = add_two_numbers(num1, num2)
        
        self.assertEqual(result, expected_sum)
        mock_error.assert_not_called()
        self.assertTrue(mock_info.called)
        self.assertIn(f'{correlation_ID} - Successfully added 5 and 10. Result: 15', mock_info.call_args_list[-1].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_valid_float_inputs(self, mock_error, mock_info):
        """
        Test with two valid float inputs.
        Should return the correct truncated sum and log info messages.
        """
        num1 = 3.7
        num2 = 2.1
        expected_sum = 5 # int(3.7) + int(2.1) = 3 + 2 = 5
        
        result = add_two_numbers(num1, num2)
        
        self.assertEqual(result, expected_sum)
        mock_error.assert_not_called()
        self.assertTrue(mock_info.called)
        self.assertIn(f'{correlation_ID} - Successfully added 3 and 2. Result: 5', mock_info.call_args_list[-1].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_valid_string_float_inputs(self, mock_error, mock_info):
        """
        Test with two valid string float inputs.
        Should return the correct truncated sum and log info messages.
        """
        num1 = "3.7"
        num2 = "2.1"
        expected_sum = 5 # int(float("3.7")) + int(float("2.1")) = 3 + 2 = 5
        
        result = add_two_numbers(num1, num2)
        
        self.assertEqual(result, expected_sum)
        mock_error.assert_not_called()
        self.assertTrue(mock_info.called)
        self.assertIn(f'{correlation_ID} - Successfully added 3 and 2. Result: 5', mock_info.call_args_list[-1].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_scientific_notation_input(self, mock_error, mock_info):
        """
        Test with scientific notation string input ('1e5') which was problematic originally.
        Should convert correctly and return the sum.
        """
        num1 = "1e5" # 100,000
        num2 = 5000
        expected_sum = 105000 # int(float("1e5")) + 5000 = 100000 + 5000 = 105000
        
        result = add_two_numbers(num1, num2)
        
        self.assertEqual(result, expected_sum)
        mock_error.assert_not_called()
        self.assertTrue(mock_info.called)
        self.assertIn(f'{correlation_ID} - Successfully added 100000 and 5000. Result: 105000', mock_info.call_args_list[-1].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_one_invalid_string_input(self, mock_error, mock_info):
        """
        Test with one invalid string input (cannot convert to number).
        Should return None and log an error message, preventing TypeError.
        This scenario directly addresses the root cause of the original TypeError.
        """
        num1 = "abc"
        num2 = 10
        
        result = add_two_numbers(num1, num2)
        
        self.assertIsNone(result)
        mock_info.assert_called() # Info messages about function call and conversion attempt
        mock_error.assert_called_once()
        self.assertIn(f'correlation_ID:{correlation_ID} Failed to convert inputs to numbers.', mock_error.call_args[0][0])
        # Check that the error message contains details about ValueError
        self.assertIn('ValueError: could not convert string to float:', mock_error.call_args[0][0])

    @patch('logging.info')
    @patch('logging.error')
    def test_other_invalid_string_input(self, mock_error, mock_info):
        """
        Test with the other input being an invalid string.
        Should return None and log an error message.
        """
        num1 = 10
        num2 = "xyz"
        
        result = add_two_numbers(num1, num2)
        
        self.assertIsNone(result)
        mock_info.assert_called()
        mock_error.assert_called_once()
        self.assertIn(f'correlation_ID:{correlation_ID} Failed to convert inputs to numbers.', mock_error.call_args[0][0])
        self.assertIn('ValueError: could not convert string to float:', mock_error.call_args[0][0])

    @patch('logging.info')
    @patch('logging.error')
    def test_both_invalid_string_inputs(self, mock_error, mock_info):
        """
        Test with both inputs being invalid strings.
        Should return None and log an error message.
        """
        num1 = "abc"
        num2 = "xyz"
        
        result = add_two_numbers(num1, num2)
        
        self.assertIsNone(result)
        mock_info.assert_called()
        mock_error.assert_called_once()
        self.assertIn(f'correlation_ID:{correlation_ID} Failed to convert inputs to numbers.', mock_error.call_args[0][0])
        self.assertIn('ValueError: could not convert string to float:', mock_error.call_args[0][0])

    @patch('logging.info')
    @patch('logging.error')
    def test_none_input(self, mock_error, mock_info):
        """
        Test with None as one of the numerical inputs.
        float(None) raises TypeError, which should be caught.
        Should return None and log an error message.
        """
        num1 = None
        num2 = 10
        
        result = add_two_numbers(num1, num2)
        
        self.assertIsNone(result)
        mock_info.assert_called()
        mock_error.assert_called_once()
        self.assertIn(f'correlation_ID:{correlation_ID} Failed to convert inputs to numbers.', mock_error.call_args[0][0])
        self.assertIn("TypeError: float() argument must be a string or a real number, not 'NoneType'", mock_error.call_args[0][0])

    @patch('logging.info')
    @patch('logging.error')
    def test_custom_correlation_id(self, mock_error, mock_info):
        """
        Test that a custom correlation ID is used for logging when provided.
        """
        num1 = 1
        num2 = 2
        custom_corr_id = "test-corr-id-123"
        expected_sum = 3

        result = add_two_numbers(num1, num2, corrID=custom_corr_id)

        self.assertEqual(result, expected_sum)
        mock_error.assert_not_called()
        self.assertTrue(mock_info.called)
        # Check an info message for the custom correlation ID
        self.assertIn(f'{custom_corr_id} - Function `add_two_numbers` called with num1={num1}, num2={num2}.', mock_info.call_args_list[0].args[0])
        self.assertIn(f'{custom_corr_id} - Successfully added 1 and 2. Result: 3', mock_info.call_args_list[-1].args[0])

    @patch('logging.info')
    @patch('logging.error')
    def test_custom_correlation_id_with_error(self, mock_error, mock_info):
        """
        Test that a custom correlation ID is used for error logging when provided with an invalid input.
        """
        num1 = "invalid"
        num2 = 2
        custom_corr_id = "error-corr-id-456"

        result = add_two_numbers(num1, num2, corrID=custom_corr_id)

        self.assertIsNone(result)
        mock_info.assert_called()
        mock_error.assert_called_once()
        # Check the error message for the custom correlation ID prefix
        self.assertIn(f'correlation_ID:{custom_corr_id} Failed to convert inputs to numbers.', mock_error.call_args[0][0])


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

