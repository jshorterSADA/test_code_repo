# Test Automation & Quality Assurance

This guide defines the tools, strategies, and standards for automated testing within the Core Number Addition Service repository. Our goal is to enable high-velocity deployments with high confidence.

## 1. The Testing Philosophy

Given the current scope of the "Core Number Addition Service," a full Testing Pyramid is not yet implemented. However, we advocate for the **Testing Pyramid** approach as the system grows. We prioritize fast, cheap unit tests at the base and reserve expensive, slow End-to-End (E2E) tests for critical user journeys.

Currently, the primary focus for testing would be at the **Unit Test** level, specifically for the `add_two_numbers` function, to ensure its correctness, robustness, and graceful error handling as highlighted by the code analysis.

| Level | Scope | Tooling (Examples) | Target Coverage |
| :--- | :--- | :--- | :--- |
| **Unit** | Individual functions/components (e.g., `add_two_numbers`) | [Pytest, unittest] | > 80% (especially for core logic) |
| **Integration** | N/A for current scope | N/A | N/A |
| **E2E** | N/A for current scope | N/A | N/A |

---

## 2. The Tech Stack

As the Core Number Addition Service is a standalone Python script, a formal testing stack is not yet defined or required beyond standard Python libraries. However, if testing were to be implemented, the following stack would be recommended:

*   **Runner & Assertions:** [Pytest] - A popular and flexible testing framework for Python.
*   **Mocking:** [unittest.mock] (built-in Python module) - For isolating units under test by replacing external dependencies.
*   **Fuzzing/Property-based testing (Optional but Recommended):** [Hypothesis] - For generating diverse test inputs to find edge cases, especially relevant for numerical functions.
*   **Component Testing:** N/A for this type of service.
*   **End-to-End:** N/A for this type of service.
*   **Smart Contracts:** N/A for this type of service.

---

## 3. Directory Structure

While no dedicated test directory exists currently, for a Python project, tests should be located either in a dedicated `tests/` directory at the project root or co-located with the module they test (e.g., `test_addNums.py` alongside `addNums.py`). This addresses the `quality.moderate` insight regarding the lack of a defined test directory.

```text
/project-root
  /addNums.py          <-- Core logic
  /tests
    /unit
      test_addNums.py  <-- Unit Tests for addNums.py
```

---

## 4. Writing Tests

### Unit Testing (Core Logic)

Focus on the `add_two_numbers` function's pure logic, including valid inputs, edge cases, and, critically, error handling for invalid inputs as identified in the code analysis.

The current `add_two_numbers` function has a critical security vulnerability and quality issue related to unhandled `ValueError` when non-numeric inputs are provided (`security.critical`, `quality.critical`). Unit tests should be designed to explicitly cover these failure scenarios.

```python
# tests/unit/test_addNums.py
import pytest
from addNums import add_two_numbers # Assuming addNums.py is importable

# Mock the logging for cleaner test output, if needed, or assert log calls
# from unittest.mock import patch

def test_add_two_numbers_valid_integers():
    """Test with valid integer inputs."""
    assert add_two_numbers(1, 2, corrID="test-id-1") == 3
    assert add_two_numbers(0, 0, corrID="test-id-2") == 0
    assert add_two_numbers(-5, 10, corrID="test-id-3") == 5

def test_add_two_numbers_valid_string_integers():
    """Test with valid string representations of integers."""
    assert add_two_numbers("10", "20", corrID="test-id-4") == 30
    assert add_two_numbers("-10", "5", corrID="test-id-5") == -5

# --- Addressing critical issues from code analysis ---
def test_add_two_numbers_non_numeric_input_raises_value_error():
    """
    Test that non-numeric inputs raise a ValueError, as per current (vulnerable) implementation.
    This test verifies the *current behavior* (crash) which needs to be fixed.
    After fixing the DoS vulnerability, this test would need to be updated
    to assert graceful handling or a custom exception.
    """
    with pytest.raises(ValueError) as excinfo:
        add_two_numbers("a", 2, corrID="test-id-6")
    assert "invalid literal for int()" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        add_two_numbers(1, "b", corrID="test-id-7")
    assert "invalid literal for int()" in str(excinfo.value)

def test_add_two_numbers_mixed_non_numeric_input_raises_value_error():
    """Test mixed valid/invalid inputs."""
    with pytest.raises(ValueError):
        add_two_numbers(1, "invalid", corrID="test-id-8")

# --- Example of how a fixed version would be tested ---
# Assuming add_two_numbers is updated to handle errors gracefully,
# e.g., by returning None or raising a custom exception.
# This part is commented out as it represents a future state.

# def test_add_two_numbers_non_numeric_input_returns_none_after_fix():
#     """Test that non-numeric inputs return None after error handling fix."""
#     # This test would only pass AFTER the DoS vulnerability is fixed.
#     # (e.g., by implementing try-except blocks as recommended in ARCHITECTURE.md)
#     assert add_two_numbers("a", 2, corrID="test-id-fixed") is None
#     # Or if a custom exception is raised
#     # with pytest.raises(InvalidInputError):
#     #     add_two_numbers("a", 2)
```

### Integration Testing (API/Smart Contracts)

N/A for the current scope of the Core Number Addition Service.

### End-to-End (E2E)

N/A for the current scope of the Core Number Addition Service.

---

## 5. Test Data Management

For simple unit tests of the `add_two_numbers` function, test data will typically be hardcoded directly within the test cases. For more complex scenarios, techniques like `pytest.mark.parametrize` can be used to run the same test with different input sets.

If the service were to expand to include more complex data types or external dependencies:

*   **Factories:** For generating complex test objects (e.g., `Faker` for Python).
*   **Seeding:** For integration tests involving a database (N/A here).
*   **Mocking:** Use `unittest.mock` for isolating units that interact with external systems (e.g., if the `add_two_numbers` function were to fetch numbers from an external API).

---

## 6. CI/CD Integration

Currently, there is no CI/CD pipeline integrated with the Core Number Addition Service. However, for any production-ready system, tests should be executed automatically as part of a Continuous Integration process.

1.  **Pull Request (Pre-Merge):** All unit tests (e.g., using `pytest`) should run on every pull request. This ensures that new code changes do not introduce regressions and adhere to quality standards. The build should fail if any tests do not pass, blocking the merge.
2.  **Nightly/Scheduled Builds:** For more extensive test suites (if the system were to grow), a nightly build could run a broader set of tests.

**Handling Flaky Tests:**
If a test fails randomly (flaky):

1.  Do not ignore it.
2.  Mark it with `@pytest.mark.skip("Reason for skipping, e.g., known flake")` and open a ticket to fix it immediately.
3.  Flaky tests destroy trust in the deployment pipeline.

---

## 7. Web3 Specific: Fuzzing & Invariants

N/A for the Core Number Addition Service, as it is not a Web3 application. However, for numerical functions, especially those handling financial or sensitive calculations, property-based testing (e.g., using Python's Hypothesis library) can provide similar benefits to fuzzing by exploring a wide range of valid and edge-case inputs automatically. This would help ensure the function behaves correctly across its domain, beyond just the explicitly coded test cases.