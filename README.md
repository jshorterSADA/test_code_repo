
import uuid
import logging

# In a typical application, logging would be configured globally, not inside the function.
# For the purpose of providing a complete, runnable code snippet that produces
# the specified log outputs, a basic configuration is included here.
# If this code is integrated into a larger system with existing logging,
# this basicConfig call might be removed or adjusted.
if not logging.root.handlers:
    logging.basicConfig(level=logging.INFO, format='%(message)s')

def add_two_numbers(num1, num2, corrID=None):
    """
    Adds two numbers after attempting to convert them to integers.
    Logs operations and errors according to specified formats.

    Args:
        num1: The first input, expected to be convertible to an integer.
        num2: The second input, expected to be convertible to an integer.
        corrID (str, optional): A correlation ID for logging.
                                If None, a new UUID is generated.
                                If an empty string, no correlation ID prefix is used in logs.

    Returns:
        int: The sum of the two numbers if conversion and addition are successful,
             otherwise None.
    """
    effective_corrID = None
    log_prefix = ""
    error_log_prefix = ""

    # Determine the effective correlation ID and log prefixes based on corrID input
    if corrID is None:
        effective_corrID = str(uuid.uuid4())
        log_prefix = f"{effective_corrID} - "
        error_log_prefix = f"correlation_ID:{effective_corrID} "
    elif corrID == '':
        # If corrID is an empty string, no prefix is used for logs or error messages.
        effective_corrID = ''
        log_prefix = ""
        error_log_prefix = ""
    else:
        effective_corrID = corrID
        log_prefix = f"{effective_corrID} - "
        error_log_prefix = f"correlation_ID:{effective_corrID} "
    
    # Log the initial function call and attempt to convert inputs
    logging.info(f"{log_prefix}Function add_two_numbers called with num1={num1}, num2={num2}.")
    logging.info(f"{log_prefix}Attempting to convert inputs to integers.")

    try:
        # Attempt to convert both inputs to integers.
        # int() raises ValueError for invalid string formats (e.g., 'hello', '', '3.14', '0xFF')
        # and TypeError for non-string/non-numeric types like None.
        int_num1 = int(num1)
        int_num2 = int(num2)
    except (ValueError, TypeError):
        # FIX: Catch both ValueError and TypeError here.
        # The original behavior for `None` inputs resulted in a generic "An unexpected error occurred: ... not 'NoneType'" message,
        # while other non-convertible inputs (like 'hello') correctly triggered the "Value Error: Failed to convert..." message.
        # By catching TypeError alongside ValueError, we ensure that `None` inputs (and any other TypeErrors during int() conversion)
        # also produce the consistent custom "Value Error: Failed to convert..." message, as suggested by the error context.
        logging.error(f"{error_log_prefix}Value Error: Failed to convert one or both inputs to integers.")
        return None
    except Exception as e:
        # Catch any other truly unexpected exceptions that might occur during conversion.
        logging.error(f"{error_log_prefix}An unexpected error occurred: {e}")
        return None

    # If conversion is successful, perform the addition and log the result
    result = int_num1 + int_num2
    logging.info(f"{log_prefix}Successfully added {int_num1} and {int_num2}. Result: {result}")
    return result
