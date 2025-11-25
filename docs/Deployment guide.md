# Deployment Guide for `addNums.py`

## 1. Introduction

This document provides a deployment and usage guide for the `addNums.py` Python script. This script defines a single function, `add_two_numbers`, designed to add two numerical inputs. It includes basic logging for tracing function calls and their outcomes, supporting correlation IDs for clearer log analysis.

## 2. Prerequisites

To utilize the `addNums.py` module, you will need the following installed on your system:

*   **Python 3.x**: Specifically, Python 3.6 or a more recent version is recommended.

No external libraries or packages are required beyond Python's standard library.

## 3. Deployment Steps

The `addNums.py` file is a standalone Python module. Deployment primarily involves making the file accessible to your Python environment and then importing its function.

### 3.1 Obtain the Code

1.  **Save the file**: Create a file named `addNums.py` in your desired project directory.
2.  **Populate the file**: Copy the entire content of the `addNums.py` script into this newly created file.

### 3.2 Install Dependencies

No specific installation steps are required as the script only uses Python's built-in `logging` module.

### 3.3 Usage

The `add_two_numbers` function can be imported and called from any other Python script or directly in an interactive Python session.

**Function Signature:**
`add_two_numbers(num1, num2, corrID=None)`

*   `num1`, `num2`: The two numbers to be added. These can be integers or string representations of integers.
*   `corrID`: (Optional) A string representing a correlation ID for the specific function call. If provided, it overrides the global `correlation_ID`.

**Example Usage:**

To use the function, you would typically import it and then call it with your desired inputs:

```python
# In your_application.py or an interactive Python interpreter

from addNums import add_two_numbers

# Example 1: Adding two integers
result1 = add_two_numbers(5, 3)
print(f"Result of 5 + 3: {result1}")
# Expected log output (similar to): 41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=5, num2=3.
# Expected log output (similar to): 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# Expected log output (similar to): 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 5 and 3. Result: 8

# Example 2: Adding an integer and a string representation of an integer
result2 = add_two_numbers('10', 20)
print(f"Result of '10' + 20: {result2}")

# Example 3: Adding with a custom correlation ID
result3 = add_two_numbers(7, 8, corrID='my-specific-transaction-123')
print(f"Result of 7 + 8 (with custom ID): {result3}")
# Expected log output (similar to): my-specific-transaction-123 - Function `add_two_numbers` called with num1=7, num2=8.

# Example 4: Invalid input (will cause a ValueError and terminate the script)
# Uncommenting the following line will crash the program:
# add_two_numbers('hello', 5)
# Expected log output (similar to): correlation_ID:41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# Followed by a Python traceback and ValueError.
```

## 4. Configuration

The `addNums.py` module includes internal logging configuration and a default correlation ID:

*   **Logging Configuration**:
    *   `logging.basicConfig(level=logging.INFO, format='%(message)s')`
    *   This line configures the root logger to output messages at the `INFO` level and above. The `format='%(message)s'` ensures that log messages are printed exactly as provided by the `logging.info()` calls, which already include the correlation ID prefixes.
*   **Global Correlation ID**:
    *   `correlation_ID = "41131d34-334c-488a-bce2-a7642b27cf35"`
    *   This variable defines a default correlation ID used for logging if no `corrID` is explicitly passed to the `add_two_numbers` function. This ID is set globally within the module.

## 5. Troubleshooting

### 5.1 `ValueError: invalid literal for int()`

*   **Issue**: The `add_two_numbers` function directly attempts to convert its inputs (`num1`, `num2`) to integers using `int()`. If either input is not a valid integer or a string that can be perfectly converted to an integer (e.g., `'5'` is valid, but `'5.0'` or `'hello'` are not), Python will raise a `ValueError`. The current implementation does not internally catch these conversion errors, which will lead to the termination of the script.
*   **Log Message**: Before crashing, an `INFO` message indicating the function call and the problematic inputs will likely be logged.
*   **Solution**:
    *   Ensure that inputs passed to `add_two_numbers` are strictly integers or strings representing whole numbers.
    *   If your application needs to handle floating-point numbers or other non-integer string representations, you must pre-process these inputs (e.g., using `float()` then `int()`, or more robust validation) *before* calling `add_two_numbers`, or modify the `add_two_numbers` function to include its own `try-except` blocks for `ValueError`.

## 6. Verification

To confirm the `addNums.py` module is operating as expected:

*   **Console Output**: Run the example usage provided in Section 3.3. Verify that `INFO` level logs are printed to the console, showing the function calls, conversion attempts, and successful additions, along with the correct correlation IDs.
*   **Return Values**: Confirm that the `add_two_numbers` function returns the correct integer sum for valid inputs.
*   **Error Handling (or lack thereof)**: Test with invalid inputs (e.g., `add_two_numbers('abc', 1)`) and observe that the script terminates with a `ValueError` traceback, preceded by the relevant `INFO` log message.