
import logging

# Configure logging to match
# the desired output format for error and info messages.
# The 'message' format ensures that correlation IDs are printed directly as specified.
logging.basicConfig(level=logging.INFO, format='%(message)s')

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

