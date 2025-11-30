# Simple Add Numbers Utility

## Description

This repository contains a standalone Python module, `addNums.py`, designed to perform a basic arithmetic operation: summing two numbers. The primary function, `add_two_numbers`, is built with a focus on traceability through integrated logging, utilizing correlation IDs to track the flow of operations. While it aims for simplicity in its core functionality, it also demonstrates a pattern for incorporating context-aware logging into utility functions.

## Features

*   **Basic Arithmetic:** Computes the sum of two numbers.
*   **Flexible Input:** Accepts both integer values and string representations of integers.
*   **Correlation ID Logging:** Integrates a mechanism for logging messages with a unique correlation ID, enhancing debugging and monitoring capabilities.
*   **Informative Logging:** Provides `INFO` level logs for function calls, input conversion attempts, and successful calculation results.

## Getting Started

### Prerequisites

To run this module, you only need:

*   Python 3.x installed on your system.

### Installation

No special installation steps are required. Simply download the `addNums.py` file to your local machine.

```bash
# Example (if hosted in a git repository)
git clone <repository_url>
cd <repository_directory>
```

## Usage

The `add_two_numbers` function can be imported and called directly from any Python script. Logging messages will be printed to the console (standard output).

### Function Signature

```python
def add_two_numbers(num1, num2, corrID=None):
```

*   `num1`: The first number to be added. Can be an integer or a string that can be converted to an integer.
*   `num2`: The second number to be added. Can be an integer or a string that can be converted to an integer.
*   `corrID` (optional): An optional string representing a correlation ID for this specific function call. If not provided, a global `correlation_ID` from the module will be used.

### Examples

```python
from addNums import add_two_numbers

# Example 1: Basic addition with default correlation ID
print("\n--- Example 1: Basic addition ---")
result1 = add_two_numbers(5, 3)
print(f"Function call result: {result1}")
# Expected log output (correlation ID will vary):
# 41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=5, num2=3.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 5 and 3. Result: 8

# Example 2: Adding numbers as strings
print("\n--- Example 2: Adding strings ---")
result2 = add_two_numbers("10", "20")
print(f"Function call result: {result2}")
# Expected log output (correlation ID will vary):
# 41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=10, num2=20.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 10 and 20. Result: 30

# Example 3: Using a custom correlation ID
print("\n--- Example 3: Custom Correlation ID ---")
result3 = add_two_numbers(7, 1, corrID="my-specific-transaction-123")
print(f"Function call result: {result3}")
# Expected log output:
# my-specific-transaction-123 - Function `add_two_numbers` called with num1=7, num2=1.
# my-specific-transaction-123 - Attempting to convert inputs to integers.
# my-specific-transaction-123 - Successfully added 7 and 1. Result: 8
```

## Configuration

### Logging

The `addNums.py` module configures the Python `logging` system upon import.

*   **Level:** Set to `INFO`, meaning all `INFO`, `WARNING`, `ERROR`, and `CRITICAL` messages will be displayed.
*   **Format:** Configured to `%(message)s`. This ensures that the correlation ID, which is manually prefixed to each log message, is the first and primary piece of information displayed.

### Global Correlation ID

A global `correlation_ID` variable is defined at the module level:

```python
correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"
```

This ID is used as a fallback if no `corrID` is explicitly passed to the `add_two_numbers` function. You can modify this variable directly in the `addNums.py` file to change the default ID for all operations not specifying their own.

## Limitations and Error Handling

It is important to note the current state of error handling within the `add_two_numbers` function:

*   **Input Conversion:** The function attempts to convert `num1` and `num2` to integers using `int()`.
*   **Lack of Robust Error Handling:** The current implementation **does not include explicit `try-except` blocks** around these `int()` conversions. This means that if either `num1` or `num2` cannot be successfully converted into an integer (e.g., if you pass `"hello"` or `None` as an argument), the function will raise a `ValueError` at runtime, causing the program to terminate or requiring the calling code to handle the exception.

### Example of Current Behavior with Invalid Input

```python
from addNums import add_two_numbers

# This call will raise a ValueError: invalid literal for int() with base 10: 'invalid_num'
add_two_numbers("invalid_num", 5)
```

### Recommendation

For production environments or scenarios where input validation is critical, it is highly recommended to enhance the `add_two_numbers` function by adding `try-except ValueError` blocks to gracefully handle non-integer inputs, potentially logging an error message and returning a predefined error value or raising a custom exception.