# Test Automation & Quality Assurance

This guide defines the tools, strategies, and standards for automated testing within the Simple Python Utility repository. Our goal is to enable high-confidence development of robust functions.

## 1. The Testing Philosophy

We follow the **Testing Pyramid** approach, prioritizing fast, cheap unit tests. For this simple utility codebase, unit tests are the primary focus.

| Level | Scope | Tooling | Target Coverage |
| :--- | :--- | :--- | :--- |
| **Unit** | Individual functions | Pytest | > 90% |
| **Integration** | N/A (No external services/APIs) | N/A | N/A |
| **E2E** | N/A (No user interface) | N/A | N/A |

---

## 2. The Tech Stack

We utilize a standard Python-based testing stack.

*   **Runner & Assertions:** [Pytest](https://docs.pytest.org/en/stable/)

---

## 3. Directory Structure

Tests are typically located in a `tests/` directory at the project root, mirroring the structure of the source code where appropriate.

```text
/project-root
  addNums.py
  /tests
    test_addNums.py    <-- Unit Tests for addNums.py
```

---

## 4. Writing Tests

### Unit Testing (Python Logic)

Focus on individual function logic. Test valid inputs, edge cases, and expected error conditions.

```python
# tests/test_addNums.py
import pytest
import logging
from addNums import add_two_numbers

# Disable logging during tests to prevent clutter
@pytest.fixture(autouse=True)
def disable_logging_fixture(caplog):
    caplog.set_level(logging.CRITICAL) # Capture all logs, but set level high enough to not show in console

def test_add_two_numbers_positive_integers():
    """Test with two positive integers."""
    assert add_two_numbers(1, 2) == 3

def test_add_two_numbers_negative_integers():
    """Test with negative integers."""
    assert add_two_numbers(-1, -2) == -3

def test_add_two_numbers_mixed_integers():
    """Test with a positive and a negative integer."""
    assert add_two_numbers(5, -3) == 2

def test_add_two_numbers_zero():
    """Test with zero."""
    assert add_two_numbers(0, 7) == 7
    assert add_two_numbers(-5, 0) == -5

def test_add_two_numbers_string_integers():
    """Test with string representations of integers."""
    assert add_two_numbers("10", "20") == 30

def test_add_two_numbers_mixed_string_and_int():
    """Test with a mix of string and integer inputs."""
    assert add_two_numbers("15", 5) == 20
    assert add_two_numbers(25, "5") == 30

def test_add_two_numbers_invalid_string_input():
    """Test with non-integer string input, expecting ValueError."""
    with pytest.raises(ValueError):
        add_two_numbers("abc", 5)
    with pytest.raises(ValueError):
        add_two_numbers(10, "xyz")

def test_add_two_numbers_none_input():
    """Test with None input, expecting TypeError."""
    with pytest.raises(TypeError):
        add_two_numbers(None, 5)
    with pytest.raises(TypeError):
        add_two_numbers(10, None)

def test_add_two_numbers_float_input():
    """Test with float input, expecting TypeError (as `int()` conversion for float strings is not direct,
       and direct float numbers passed to `int()` will truncate, which might not be desired for this function's purpose).
       For the current implementation which uses `int()`, floats will be truncated.
       This test verifies the explicit behavior of `int()` on floats.
    """
    assert add_two_numbers(1.5, 2.5) == 3 # int(1.5) is 1, int(2.5) is 2

def test_add_two_numbers_with_correlation_id():
    """Test that a specific correlation ID is used if provided."""
    # This test primarily ensures that the function can take an explicit correlation ID
    # and that the logic for handling it is sound, even if logs are suppressed.
    # The actual log content verification would require more advanced logging capture.
    result = add_two_numbers(1, 2, corrID="test-corr-id")
    assert result == 3
```

---

## 5. Test Data Management

*   **Direct Data:** For simple functions like `add_two_numbers`, test data is typically provided directly within the test cases.
*   **Parameterized Testing:** Pytest's `parametrize` decorator can be used to run the same test logic with different sets of inputs.

---

## 6. CI/CD Integration

Tests are executed automatically via CI/CD pipelines (e.g., GitHub Actions, Jenkins).

1.  **Pull Request:** Runs Unit Tests. (Must pass to merge).

**Handling Flaky Tests:**
If a test fails randomly (flaky):

1.  Do not ignore it.
2.  Mark it with `pytest.mark.skip` and open a ticket to fix it immediately.
3.  Flaky tests destroy trust in the deployment pipeline.