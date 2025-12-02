# Test Automation & Quality Assurance

This guide defines the tools, strategies, and standards for automated testing within the Python Number Operations Utility repository. Our goal is to enable high-velocity deployments with high confidence.

## 1. The Testing Philosophy

We follow the **Testing Pyramid** approach. We prioritize fast, cheap unit tests at the base and reserve expensive, slow End-to-End (E2E) tests for critical user journeys.

| Level | Scope | Tooling | Target Coverage |
| :--- | :--- | :--- | :--- |
| **Unit** | Individual functions/methods (e.g., `add_two_numbers`) | `pytest` | `> 90%` |
| **Integration** | Interactions between core modules or with system components (e.g., logging). For `addNums.py`, this scope is minimal. | `pytest` (potentially with `pytest-mock`) | `Minimal / N/A for addNums.py` |
| **E2E** | Full application flows | `N/A` | `N/A` |

---

## 2. The Tech Stack

We utilize a standard Python-based testing stack to reduce context switching.

*   **Runner & Assertions:** `pytest`

---

## 3. Directory Structure

Tests should be located close to the code they test (colocation) for unit tests.

```text
/project-root
  addNums.py
  test_addNums.py      <-- Unit Tests (Colocated)
```

-----

## 4. Writing Tests

### Unit Testing (Python Functions)

Focus on pure logic and function behavior. Ensure the function handles various inputs, including valid numbers, string representations of numbers, and invalid types that should raise errors. Also, verify expected logging output.

```python
# test_addNums.py
import pytest
import logging
from addNums import add_two_numbers, correlation_ID

# Fixture to capture logs for assertion
@pytest.fixture
def caplog_setup(caplog):
    caplog.set_level(logging.INFO, logger='addNums') # Capture INFO logs from addNums module
    yield caplog

def test_add_two_numbers_valid_integers(caplog_setup):
    """Test with valid integer inputs."""
    result = add_two_numbers(1, 2)
    assert result == 3
    assert f'{correlation_ID} - Successfully added 1 and 2. Result: 3' in caplog_setup.text

def test_add_two_numbers_string_integers(caplog_setup):
    """Test with valid string integer inputs."""
    result = add_two_numbers("10", "20")
    assert result == 30
    assert f'{correlation_ID} - Successfully added 10 and 20. Result: 30' in caplog_setup.text

def test_add_two_numbers_invalid_input_raises_value_error(caplog_setup):
    """Test with invalid input that cannot be converted to int, expecting ValueError."""
    with pytest.raises(ValueError) as excinfo:
        add_two_numbers("a", 2)
    assert "invalid literal for int()" in str(excinfo.value)
    # Verify that expected info logs up to the point of failure are present
    assert f'{correlation_ID} - Function `add_two_numbers` called with num1=a, num2=2.' in caplog_setup.text
    assert f'{correlation_ID} - Attempting to convert inputs to integers.' in caplog_setup.text

def test_add_two_numbers_custom_corr_id(caplog_setup):
    """Test that a custom correlation ID is used in logs when provided."""
    custom_id = "test-123"
    result = add_two_numbers(5, 7, corrID=custom_id)
    assert result == 12
    assert f'{custom_id} - Successfully added 5 and 7. Result: 12' in caplog_setup.text
    assert f'{custom_id} - Function `add_two_numbers` called with num1=5, num2=7.' in caplog_setup.text

```

### Integration Testing (Python Modules)

For this specific module (`addNums.py`), typical integration testing of external services or databases is not applicable as it is a pure function. However, if this module were part of a larger system, integration tests would focus on interactions between `addNums.py` and other internal modules or mock external dependencies (e.g., ensuring data flows correctly through multiple processing steps).

### End-to-End (N/A)

End-to-End testing is not applicable for this single utility module.

-----

## 5. Test Data Management

*   **Parametrization:** For tests requiring varied inputs, utilize `pytest.mark.parametrize` to cover multiple scenarios efficiently within a single test function.
*   **Seeding:** Not applicable for this pure function module.
*   **Mocking:** If `add_two_numbers` were to interact with external systems (e.g., a database or API), `unittest.mock` or `pytest-mock` would be used to isolate the function under test and simulate external dependencies.

-----

## 6. CI/CD Integration

Tests are executed automatically via GitHub Actions (or similar CI/CD pipeline).

1.  **Pull Request:** Runs Lint + Unit Tests (`pytest`). (Must pass to merge).
2.  **Nightly Build:** Runs more extensive suites if they existed (e.g., performance tests), but for this module, it would primarily be unit tests.

**Handling Flaky Tests:**
If a test fails randomly (flaky):

1.  Do not ignore it.
2.  Mark it with `pytest.mark.skip` and open a ticket to fix it immediately.
3.  Flaky tests destroy trust in the deployment pipeline.