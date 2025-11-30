# Application Interface Guide (v1)

Welcome to the **Numerical Operations Module** documentation. This module provides **fundamental numerical operations and robust error logging for internal Python applications**.

## Introduction

This module exposes programmatic functions designed for direct integration into Python applications. It does not follow RESTful conventions, nor does it operate over HTTP. Data is passed directly via function arguments, and results are returned as standard Python types.

> **Module Usage**
> ```python
> import addNums
> # Use functions like: addNums.add_two_numbers(...)
> ```

---

## Functions

### `add_two_numbers`

Calculates the sum of two numbers, gracefully handling both integer and string representations.

**Function Signature**
```python
from typing import Union, Optional

def add_two_numbers(num1: Union[int, str], num2: Union[int, str], corrID: Optional[str] = None) -> int:
```

**Description**
This function takes two numbers (integers or string representations) as input and returns their sum. It attempts to convert inputs to integers. If conversion fails, it raises a `ValueError`. All operations are logged with an optional correlation ID for traceability.

**Parameters**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `num1` | `int` or `str` | Yes | The first number to be added. If a string, it must be convertible to an an integer. |
| `num2` | `int` or `str` | Yes | The second number to be added. If a string, it must be convertible to an an integer. |
| `corrID` | `str` | No | An optional, unique identifier for correlating log messages. If omitted, a default internal `correlation_ID` is used (default: `41131d34-334c-488a-bce2-a7642b27cf35`). |

**Returns**
`int` - The integer sum of `num1` and `num2`.

**Example Usage**

```python
import logging
from addNums import add_two_numbers # Assuming addNums.py is accessible in the Python path

# Configure logging to observe the function's internal messages
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Example 1: Adding integers
result1 = add_two_numbers(5, 7)
print(f"Result 1: {result1}")
# Expected log output (using default correlation ID from addNums.py):
# 41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=5, num2=7.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers.
# 41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 5 and 7. Result: 12
# Output: Result 1: 12

# Example 2: Adding strings convertible to integers with a custom correlation ID
result2 = add_two_numbers("10", "20", corrID="my-custom-trace-001")
print(f"Result 2: {result2}")
# Expected log output:
# my-custom-trace-001 - Function `add_two_numbers` called with num1=10, num2=20.
# my-custom-trace-001 - Attempting to convert inputs to integers.
# my-custom-trace-001 - Successfully added 10 and 20. Result: 30
# Output: Result 2: 30

# Example 3: Invalid input (will raise ValueError)
try:
    add_two_numbers("five", 7, corrID="invalid-input-test")
except ValueError as e:
    print(f"Caught expected error: {e}")
# Expected log output before the exception is raised:
# invalid-input-test - Function `add_two_numbers` called with num1=five, num2=7.
# invalid-input-test - Attempting to convert inputs to integers.
# Output: Caught expected error: invalid literal for int() with base 10: 'five'
```

-----

## Error Handling

The `add_two_numbers` function reports issues primarily by raising standard Python exceptions. Detailed diagnostic messages are also emitted via the `logging` module, incorporating a correlation ID for tracing.

*   **`ValueError`**: This exception is raised if either `num1` or `num2` cannot be successfully converted into an integer. For instance, providing a non-numeric string (e.g., `"abc"`) or a floating-point string (e.g., `"3.14"`) will result in a `ValueError`.

**Logging for Traceability**
All informational and error-related events within the function are logged using the configured Python `logging` module. Each log entry is prefixed with a correlation ID (either the provided `corrID` or the default internal `41131d34-334c-488a-bce2-a7642b27cf35`), facilitating debugging and tracing across system components.

**Log Format Example (Informational Messages)**
```
<correlation_ID> - Function `add_two_numbers` called with num1=X, num2=Y.
<correlation_ID> - Attempting to convert inputs to integers.
<correlation_ID> - Successfully added X and Y. Result: Z
```
(Where `<correlation_ID>` is either the provided `corrID` or `41131d34-334c-488a-bce2-a7642b27cf35`.)

> [\!NOTE]
> The function itself raises `ValueError` directly on invalid input conversion. While the `error_prefix` is prepared for `logging.error` calls within the function's scope, the current implementation only actively utilizes `logging.info` before a `ValueError` is potentially raised. It is the responsibility of the calling application to catch these exceptions and log them as appropriate for comprehensive error reporting.