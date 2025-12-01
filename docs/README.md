# `addNums.py` - Simple Number Addition Utility

This repository contains a single Python script, `addNums.py`, designed to perform the addition of two numbers. The script prioritizes clear logging and incorporates correlation IDs for traceability, making it suitable for integration into systems requiring detailed operational insights.

## Overview

`addNums.py` exposes a single function, `add_two_numbers`, which takes two inputs, attempts to convert them to integers, and returns their sum. It includes robust logging with dynamic correlation IDs to track the execution flow of each function call.

## Features

*   **Number Addition:** Core functionality to sum two numerical inputs.
*   **Input Conversion:** Automatically attempts to convert string representations of numbers to integers.
*   **Detailed Logging:** Utilizes Python's `logging` module to provide informative messages about function calls, input processing, and results.
*   **Correlation IDs:** Supports explicit and implicit correlation IDs for tracking individual function executions, crucial for debugging and monitoring in distributed systems.

## Getting Started

### Prerequisites

*   Python 3.x

### Usage

To use the `add_two_numbers` function, you can import it into your Python project or run the script directly for testing purposes (though no main execution block is provided in the current script).

#### Example:

```python
import logging
from addNums import add_two_numbers

# Configure logging if not already done, matching the script's basicConfig
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Example 1: Basic addition
print("\n--- Example 1: Basic Addition ---")
result1 = add_two_numbers(5, 3)
print(f"Result for (5, 3): {result1}") # Expected output: 8

# Example 2: Addition with string numbers
print("\n--- Example 2: String Numbers ---")
result2 = add_two_numbers("10", "20")
print(f"Result for ('10', '20'): {result2}") # Expected output: 30

# Example 3: Using a custom correlation ID
print("\n--- Example 3: Custom Correlation ID ---")
custom_corr_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef"
result3 = add_two_numbers(15, 7, corrID=custom_corr_id)
print(f"Result for (15, 7) with custom ID: {result3}") # Expected output: 22

# Example 4: Input that cannot be converted (will raise ValueError)
print("\n--- Example 4: Invalid Input (will raise ValueError) ---")
try:
    add_two_numbers("hello", 5)
except ValueError as e:
    print(f"Caught expected error: {e}") # Expected: invalid literal for int()
```

## Core Functionality

### `add_two_numbers(num1, num2, corrID=None)`

This function calculates the sum of two inputs after attempting to convert them to integers.

*   **Parameters:**
    *   `num1`: The first number. Can be an integer or a string representation of an integer.
    *   `num2`: The second number. Can be an integer or a string representation of an integer.
    *   `corrID` (optional): A string representing a correlation ID to be used for logging within this function call. If `None` (or not provided), a global default `correlation_ID` from the `addNums.py` script will be used.

*   **Return Value:**
    *   Returns an `int` representing the sum of `num1` and `num2`.

*   **Behavior & Error Handling:**
    1.  Logs the initiation of the function call with the inputs and the chosen correlation ID.
    2.  Attempts to convert both `num1` and `num2` to integers using `int()`.
    3.  If either `num1` or `num2` cannot be converted to an integer (e.g., if they are non-numeric strings or other incompatible types), a `ValueError` will be raised by the `int()` conversion, terminating the function execution.
    4.  If both inputs are successfully converted, their sum is calculated and returned.
    5.  Logs the successful addition and the final result.

    **Note on Error Handling:** While the function's docstring indicates graceful handling of unconvertible inputs, the current implementation *directly* calls `int()`, which will raise a `ValueError` for invalid input formats. This means the function does *not* gracefully handle such cases but instead propagates the `ValueError`. Consumers of this function should wrap calls in `try-except ValueError` blocks if robust error handling is required.

## Logging & Correlation IDs

The script is configured to use Python's standard `logging` module.

*   **Configuration:** Logging is set to `INFO` level, with a format `%(message)s`, ensuring that log entries appear as direct messages.
*   **Correlation ID (`correlation_ID`):** A global `correlation_ID` is defined at the top of the script. This serves as a default ID for all log messages if no specific `corrID` is provided to `add_two_numbers`.
*   **Dynamic Correlation:** The `add_two_numbers` function prioritizes a `corrID` provided as an argument. If an argument `corrID` is given, it overrides the global default for that specific function call, allowing for per-request traceability.
*   **Log Message Format:**
    *   `INFO` messages include a prefix like `[correlation_ID] - [message]`.
    *   (Currently, there are no explicit `ERROR` logs within the function, but if added, they would use a format like `correlation_ID:[ID] [message]`.)