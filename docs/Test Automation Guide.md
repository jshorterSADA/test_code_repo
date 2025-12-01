# Test Automation & Quality Assurance

This guide defines the tools, strategies, and standards for automated testing within the **Python Calculation Module** repository. Our goal is to enable high-velocity deployments with high confidence.

## 1. The Testing Philosophy

We follow the **Testing Pyramid** approach. We prioritize fast, cheap unit tests at the base and reserve more comprehensive functional tests for critical module behaviors.

| Level | Scope | Tooling | Target Coverage |
| :--- | :--- | :--- | :--- |
| **Unit** | Individual functions/methods, pure logic | Pytest | > 80% |
| **Functional** | Module-level behavior, ensuring side effects (e.g., logging) | Pytest, `unittest.mock` | Critical Paths |

---

## 2. The Tech Stack

We utilize a standard Python-based testing stack to reduce context switching.

*   **Runner & Assertions:** [Pytest](https://docs.pytest.org/en/stable/)
*   **Mocking:** `unittest.mock` (standard library) or `pytest-mock`

---

## 3. Directory Structure

Tests should be located in a dedicated `tests/` directory within the project root.

```text
/project-root
  addNums.py
  /tests
    test_addNums.py        <-- Unit & Functional Tests
```

---

## 4. Writing Tests

### Unit Testing (Logic)

Focus on pure logic, input validation, and expected outputs of individual functions.

```python
# tests/test_addNums.py
import pytest
from addNums import add_two_numbers

def test_add_two_numbers_positive_integers():
    """Test with two positive integer inputs."""
    assert add_two_numbers(1, 2, corrID="test-corr-id") == 3

def test_add_two_numbers_string_integers():
    """Test with string representations of integers."""
    assert add_two_numbers("10", "20", corrID="test-corr-id") == 30

def test_add_two_numbers_mixed_types():
    """Test with mixed integer and string-integer inputs."""
    assert add_two_numbers(5, "5", corrID="test-corr-id") == 10

def test_add_two_numbers_invalid_input_type():
    """Test that invalid non-numeric inputs raise a ValueError."""
    with pytest.raises(ValueError):
        add_two_numbers("invalid", 2, corrID="test-corr-id")

def test_add_two_numbers_none_input():
    """Test that None inputs raise a TypeError."""
    with pytest.raises(TypeError):
        add_two_numbers(None, 2, corrID="test-corr-id")
```

### Functional Testing (Logging)

Ensure that module-level behaviors, such as logging, function as expected. This involves capturing log output and asserting its content.

```python
# tests/test_addNums.py (continued)
import logging
import pytest
from addNums import add_two_numbers

def test_add_two_numbers_logs_info_messages(caplog):
    """Test that add_two_numbers logs appropriate info messages."""
    caplog.set_level(logging.INFO)
    corr_id = "func-test-corr-id"
    add_two_numbers(1, 2, corrID=corr_id)

    # Check for specific log messages
    assert len(caplog.records) == 3
    assert f'{corr_id} - Function `add_two_numbers` called with num1=1, num2=2.' in caplog.text
    assert f'{corr_id} - Attempting to convert inputs to integers.' in caplog.text
    assert f'{corr_id} - Successfully added 1 and 2. Result: 3' in caplog.text

def test_add_two_numbers_logs_error_on_conversion_failure(caplog):
    """Test that add_two_numbers logs an error on input conversion failure."""
    caplog.set_level(logging.ERROR) # Set level to ERROR to capture potential errors
    corr_id = "error-test-corr-id"
    
    # We expect a ValueError, but also check the logs for its handling if any specific error logging was implemented
    try:
        add_two_numbers("a", 2, corrID=corr_id)
    except ValueError:
        pass # Expected exception

    # In this specific codebase, ValueError is raised and not explicitly logged as an error
    # If it were, we'd assert on error log messages here.
    # The current implementation only logs INFO messages before the exception.
    assert len(caplog.records) == 0 # No ERROR level logs expected before the ValueError is raised
```

---

## 5. Test Data Management

*   **Factories:** Use factories (e.g., [Faker](https://faker.readthedocs.io/en/master/)) to generate random data rather than hardcoding strings, especially for more complex data structures. For this simple module, direct values are sufficient.
*   **Seeding:** For modules interacting with databases or external systems, each test suite should spin up a fresh sandbox and tear it down after. (Not directly applicable to this simple calculation module).
*   **Mocking:** Never hit real external APIs or services in unit tests. Use `unittest.mock.patch` or `pytest-mock` to isolate the code under test.

---

## 6. CI/CD Integration

Tests are executed automatically via GitHub Actions.

1.  **Pull Request:** Runs Lint + Unit & Functional Tests. (Must pass to merge).
2.  **Nightly Build:** Runs comprehensive unit/functional suite.

**Handling Flaky Tests:**
If a test fails randomly (flaky):

1.  Do not ignore it.
2.  Mark it with `pytest.mark.skip` and open a ticket to fix it immediately.
3.  Flaky tests destroy trust in the deployment pipeline.