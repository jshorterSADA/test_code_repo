
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
        # Attempt to convert inputs to integers.
        # This is where the ValueError can occur if inputs are not valid.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError:
        # The problem statement indicates a ValueError occurs when converting inputs.
        # The function's docstring also states it should "gracefully handles cases where inputs cannot be converted".
        # The required error output format is: "correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 Value Error: Failed to convert one or both inputs to integers."
        # This implies that "correlation_ID:" is a literal prefix in the error message.
        error_message_for_log = f'correlation_ID:{current_corr_id} Value Error: Failed to convert one or both inputs to integers.'
        logging.error(error_message_for_log)
        return None # Return None to indicate that the operation failed gracefully

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{corr_id_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

