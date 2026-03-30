
import logging

# Configure logging to match the desired output format for error and info messages.
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
