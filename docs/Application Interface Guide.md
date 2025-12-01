# Application Interface Guide (addNums Utility)

Welcome to the `addNums` Utility Function documentation. This document describes a core arithmetic utility function designed for straightforward numerical summation.

## Introduction

This document details the `add_two_numbers` Python function, a standalone utility that performs basic addition. It does not expose a traditional RESTful API, does not make network calls, and processes inputs directly within its execution environment.

> **Execution Context**
> This utility function is designed for local or in-process execution within a Python application.

---

## Security & Error Handling

This utility function operates locally and does not involve network calls, API keys, or Web3 cryptographic signatures. Therefore, the concepts of external authentication, API security, and Web3-specific security hazards as described in a typical API guide are not applicable here.

### Error Handling

The `add_two_numbers` function relies on Python's built-in error handling for input validation.
If the provided `num1` or `num2` arguments cannot be successfully converted to integers, a standard Python `ValueError` will be raised, leading to program termination unless explicitly caught and handled by the calling code.

### Logging

The function uses Python's `logging` module to output informational messages throughout its execution. All log messages include a correlation ID for tracing.

Informational messages (e.g., function entry, input conversion, successful computation) are logged using the `INFO` level. The format ensures that the correlation ID is printed directly as a prefix to the message: `[correlation_ID] - [Message]`.

```python
# Example Info Log:
# 41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=10, num2=20.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 10 and 20. Result: 30
```

---

## Functions

### `add_two_numbers`

Calculates the sum of two numerical inputs. The function attempts to convert both inputs to integers.

**Function Signature**
`add_two_numbers(num1, num2, corrID=None)`

**Parameters**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `num1` | `str` or `int` | Yes | The first number to be added. The function will attempt to convert this to an integer. |
| `num2` | `str` or `int` | Yes | The second number to be added. The function will attempt to convert this to an integer. |
| `corrID` | `str` | No | An optional correlation ID for logging purposes. If not provided, a globally defined default ID (`41131d34-334c-488a-bce2-a7642b27cf35`) will be used. |

**Returns**
`int` - The sum of `num1` and `num2` after successful conversion to integers.

**Raises**
`ValueError` - If either `num1` or `num2` cannot be converted into a valid integer.

**Example Usage**

```python
import logging

# Ensure logging is configured as per addNums.py
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Assuming correlation_ID is accessible, as defined in the codebase
global_correlation_ID ="41131d34-334c-488a-bce2-a7642b27cf35"

# (Simplified function definition for example clarity)
def add_two_numbers(num1, num2, corrID=None):
    current_corr_id = corrID if corrID is not None else global_correlation_ID
    info_prefix = f'{current_corr_id} - ' if current_corr_id else ''

    logging.info(f'{info_prefix}Function `add_two_numbers` called with num1={num1}, num2={num2}.')
    logging.info(f'{info_prefix}Attempting to convert inputs to integers.')

    num1_int = int(num1)
    num2_int = int(num2)

    result = num1_int + num2_int
    logging.info(f'{info_prefix}Successfully added {num1_int} and {num2_int}. Result: {result}')
    return result

# --- Examples ---

# Example 1: Valid integer inputs (uses global_correlation_ID)
try:
    result1 = add_two_numbers(10, 20)
    print(f"Sum (10, 20): {result1}")
    # Expected log output (prefix by global_correlation_ID):
    # Function `add_two_numbers` called with num1=10, num2=20.
    # Attempting to convert inputs to integers.
    # Successfully added 10 and 20. Result: 30
except ValueError as e:
    print(f"Error caught: {e}")

print("-" * 20)

# Example 2: Valid string inputs, with custom correlation ID
try:
    result2 = add_two_numbers("5", "7", "my-unique-corr")
    print(f"Sum ('5', '7'): {result2}")
    # Expected log output (prefix by my-unique-corr):
    # Function `add_two_numbers` called with num1=5, num2=7.
    # Attempting to convert inputs to integers.
    # Successfully added 5 and 7. Result: 12
except ValueError as e:
    print(f"Error caught: {e}")

print("-" * 20)

# Example 3: Invalid input (will raise ValueError)
try:
    result3 = add_two_numbers("hello", 15)
    print(f"Sum ('hello', 15): {result3}")
except ValueError as e:
    print(f"Attempted to add 'hello' and 15. Caught error: {e}")
    # Expected behavior: A ValueError will be raised here.
    # The logs will show the initial call and conversion attempt before the error.
