
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
    corr_id_prefix = f'{current_corr_id} - ' if current_corr_id else ''

    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')

    try:
        # Corrected indentation for these lines (they were over-indented in the original file)
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError:
        # Log the error message in the format specified by the problem description
        # (correlation_ID Value Error: Message)
        logging.error(f'{current_corr_id} Value Error: Failed to convert one or both inputs to integers.')
        return None # Indicate that the operation failed by returning None

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result
