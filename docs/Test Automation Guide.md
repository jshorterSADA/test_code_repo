# Test Automation & Quality Assurance

This guide defines the tools, strategies, and standards for automated testing within the Number Adder Service repository. Our goal is to enable high-velocity deployments with high confidence.

## 1. The Testing Philosophy

We follow the **Testing Pyramid** approach. We prioritize fast, cheap unit tests at the base and reserve expensive, slow End-to-End (E2E) tests for critical user journeys.

| Level | Scope | Tooling | Target Coverage |
| :--- | :--- | :--- | :--- |
| **Unit** | Individual functions/modules | pytest | > 90% |
| **Integration** | External module interactions | N/A (for current scope) | N/A |
| **E2E** | Full user flows | N/A (for current scope) | N/A |

---

## 2. The Tech Stack

We utilize a standard Python-based testing stack.

*   **Runner & Assertions:** [pytest](https://docs.pytest.org/en/stable/)

---

## 3. Directory Structure

Tests should be located close to the code they test (colocation).

```text
/project-root
  addNums.py
  test_addNums.py      <-- Unit Tests (Colocated)
```

-----

## 4. Writing Tests

### Unit Testing (Python Logic)

Focus on individual function logic and error handling. Mock all external dependencies, especially for side effects like logging.

```python
# test_addNums.py
import pytest
import logging
from unittest.mock import patch
from addNums import add_two_numbers

# A pytest fixture to capture log messages during tests
@pytest.fixture
def caplog_for_corr_id(caplog):
    # Ensure logs are captured from the root logger as configured in addNums.py
    caplog.set_level(logging.INFO)
    return caplog

def test_add_two_numbers_valid_integers(caplog_for_corr_id):
    """
    Tests that add_two_numbers correctly sums two integers.
    """
    result = add_two_numbers(5, 3)
    assert result == 8
    # Assert specific log messages
    assert "Function `add_two_numbers` called with num1=5, num2=3." in caplog_for_corr_id.text
    assert "Attempting to convert inputs to integers." in caplog_for_corr_id.text
    assert "Successfully added 5 and 3. Result: 8" in caplog_for_corr_id.text

def test_add_two_numbers_string_integers(caplog_for_corr_id):
    """
    Tests that add_two_numbers correctly sums string representations of integers.
    """
    result = add_two_numbers("10", "20", corrID="custom-id-1")
    assert result == 30
    # Assert specific log messages, checking for custom correlation ID
    assert "custom-id-1 - Function `add_two_numbers` called with num1=10, num2=20." in caplog_for_corr_id.text
    assert "custom-id-1 - Attempting to convert inputs to integers." in caplog_for_corr_id.text
    assert "custom-id-1 - Successfully added 10 and 20. Result: 30" in caplog_for_corr_id.text

@patch('addNums.logging.info')
def test_add_two_numbers_invalid_inputs_raises_value_error(mock_info):
    """
    Tests that add_two_numbers raises a ValueError for non-numeric inputs
    due to the direct int() conversion in the implementation.
    """
    with pytest.raises(ValueError) as excinfo:
        add_two_numbers("abc", 5)
    
    assert "invalid literal for int()" in str(excinfo.value)
    
    # Ensure info logs were made before the error occurred
    assert any("Function `add_two_numbers` called with num1=abc, num2=5." in call.args[0] for call in mock_info.call_args_list)
    assert any("Attempting to convert inputs to integers." in call.args[0] for call in mock_info.call_args_list)
```

### Integration Testing

This section is not applicable to the current simple utility service, which has no external dependencies beyond standard Python libraries. Should the service expand to interact with external APIs, databases, or message queues, integration tests would be introduced here to verify these interactions.

### End-to-End (E2E)

This type of testing is not applicable for this backend utility service as there is no user interface or complex multi-service workflow to simulate.

-----

## 5. Test Data Management

*   **Factories:** For simple numerical inputs as in `add_two_numbers`, direct values are often sufficient. For more complex Python applications, libraries like [Faker](https://faker.readthedocs.io/en/master/) can be used to generate realistic test data.
*   **Seeding:** Not applicable for this stateless utility.
*   **Mocking:** When testing functions that interact with external services or resources (e.g., databases, external APIs, or in this case, the `logging` module), use Python's `unittest.mock` or `pytest-mock` to isolate the unit under test and control its dependencies.

```python
# Example of mocking the logging module to assert log messages using unittest.mock.patch
from unittest.mock import patch
from addNums import add_two_numbers

@patch('addNums.logging.info')
def test_add_two_numbers_logs_info_with_default_corr_id(mock_info):
    # Calling without specifying corrID should use the global one
    add_two_numbers(1, 2)
    
    # Check the calls made to logging.info
    # Verify that the default correlation_ID is used in log messages
    assert mock_info.call_count == 3 # 1 for function call, 1 for conversion attempt, 1 for result
    assert "41131d34-334c-488a-bce2-a7642b27cf35 - Function `add_two_numbers` called with num1=1, num2=2." in mock_info.call_args_list[0].args[0]
    assert "41131d34-334c-488a-bce2-a7642b27cf35 - Attempting to convert inputs to integers." in mock_info.call_args_list[1].args[0]
    assert "41131d34-334c-488a-bce2-a7642b27cf35 - Successfully added 1 and 2. Result: 3" in mock_info.call_args_list[2].args[0]
```

-----

## 6. CI/CD Integration

Tests are executed automatically via GitHub Actions.

1.  **Pull Request:** Runs Lint + Unit Tests. (Must pass to merge).

**Handling Flaky Tests:**
If a test fails randomly (flaky):

1.  Do not ignore it.
2.  Mark it with `pytest.mark.skip` and open a ticket to fix it immediately.
3.  Flaky tests destroy trust in the deployment pipeline.
