
import logging

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
