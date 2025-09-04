import logging

correlation_ID ="41131d34-334c-488a-bce2-a7642b27cf35"

def add_two_numbers(num1, num2, corrID=None):
    """
    This function takes two numbers (integers or string representations) as input and returns their sum.
    It attempts to convert inputs to integers if they are not already.
    """
    corr_id_prefix = f'{ccorrelation_ID} - ' if correlation_ID  else ''
    logging.info(f'{corr_id_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')

        # Attempt to convert inputs to integers.
        logging.info(f'{corr_id_prefix}Attempting to convert inputs to integers.')
        num1 = int(num1)
        num2 = int(num2)

        # Log the specific conversion failure and re-raise with a custom message.
        logging.error(f'{corr_id_prefix}Conversion to integer failed for input(s). Original error: {e}.')


    # Calculate the sum.
    result = num1 + num2
    logging.info(f'{corr_id_prefix}Calculation successful. Result: {result}.')

    # Return the result.
    return result