
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

    try:
        # The original file had these lines incorrectly indented and lacked error handling.
        # They are now correctly indented within a try block to catch conversion errors.
        num1_int = int(num1)
        num2_int = int(num2)
    except ValueError as e:
        # Log the specific error and return None to indicate failure gracefully.
        # The error message from the prompt "Value Error: Failed to convert one or both inputs to integers."
        # matches the error_message generated and logged here.
        error_message = f"Failed to convert one or both inputs to integers. Original inputs: num1='{num1}', num2='{num2}'. Error: {e}"
        logging.error(f'{error_prefix}{error_message}')
        return None # Indicate failure as per docstring for graceful handling

    # Calculate the sum
    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# The provided code already correctly handles the ValueError by logging it and returning None.
# The "Value Error: Failed to convert one or both inputs to integers." is the logged message.
# The fix therefore is to add example calls to the function to demonstrate its correct behavior
# and its robust error handling as described in the problem statement, making the file executable.
if __name__ == "__main__":
    logging.info("\n--- Demonstrating Functionality and Error Handling ---")

    # Test Case 1: Valid integer inputs
    logging.info("\n--- Test Case 1: Valid integer inputs ---")
    result1 = add_two_numbers(5, 10)
    if result1 is not None:
        logging.info(f'{correlation_ID} - Main script: Sum of 5 and 10 is {result1}')
    else:
        logging.info(f'{correlation_ID} - Main script: Failed to add 5 and 10.')

    # Test Case 2: Valid string inputs representing integers
    logging.info("\n--- Test Case 2: Valid string inputs ---")
    result2 = add_two_numbers("20", "25", corrID="custom-id-valid")
    if result2 is not None:
        logging.info(f'{correlation_ID} - Main script: Sum of "20" and "25" is {result2}')
    else:
        logging.info(f'{correlation_ID} - Main script: Failed to add "20" and "25".')

    # Test Case 3: Invalid string inputs (triggers the logged ValueError)
    logging.info("\n--- Test Case 3: Invalid string inputs (expected error log) ---")
    result3 = add_two_numbers("abc", "def")
    if result3 is not None:
        logging.info(f'{correlation_ID} - Main script: Sum of "abc" and "def" is {result3}')
    else:
        # This confirms that the function gracefully handled the invalid input.
        logging.info(f'{correlation_ID} - Main script: Function correctly handled invalid inputs "abc" and "def" by returning None.')

    # Test Case 4: Mixed valid and invalid inputs
    logging.info("\n--- Test Case 4: Mixed valid and invalid inputs (expected error log) ---")
    result4 = add_two_numbers("100", "xyz", corrID="another-custom-id")
    if result4 is not None:
        logging.info(f'{correlation_ID} - Main script: Sum of "100" and "xyz" is {result4}')
    else:
        # This confirms that the function gracefully handled the invalid input.
        logging.info(f'{correlation_ID} - Main script: Function correctly handled mixed invalid inputs "100" and "xyz" by returning None.')

    logging.info("\n--- End of Demonstration ---")
