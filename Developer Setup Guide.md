# Developer Setup Guide - Core Number Addition Service

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Core Number Addition Service repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.8+` | Runtime for the Core Number Addition Service. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with the official Python extension). |

### Cloud & Infrastructure Tools
*   **None required**: The Core Number Addition Service is a standalone Python script without cloud infrastructure dependencies for local development or execution.

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:your-org/core-number-addition-service.git
cd core-number-addition-service
```

### Install Dependencies
The Core Number Addition Service currently has no external Python dependencies beyond the standard library. If future additions require packages, `pip` would be used for installation.

```bash
# Example if future dependencies are introduced (e.g., for testing):
# pip install -r requirements.txt
```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING & Architectural Note**
> The `correlation_ID` within `addNums.py` is currently hardcoded as a global variable. For production environments or complex systems, dynamic correlation ID management (e.g., via `contextvars` or `logging.LoggerAdapter`) is highly recommended to avoid global mutable state and enhance traceability.
>
> **Secrets**: The Core Number Addition Service does not use external secrets or `.env` files.

---

## 4. Running the Application

The Core Number Addition Service is a Python module. You can execute its core function directly from a Python interpreter or import it into another script.

### Executing the `add_two_numbers` function
```bash
# Directly from the command line
python3 -c "from addNums import add_two_numbers; print(add_two_numbers(5, 3))"

# Example of importing into another Python script (e.g., main.py)
# from addNums import add_two_numbers
#
# # Call the function with various inputs
# print(f"Sum of 10 and 20: {add_two_numbers(10, 20)}")
# print(f"Sum of '5' and '7': {add_two_numbers('5', '7')}")
#
# # Test with a correlation ID
# print(f"Sum with corrID: {add_two_numbers(1, 2, 'my-request-123')}")
```

> [!WARNING]
> **Critical DoS Vulnerability (Input Validation)**
> As extensively identified in the `ARCHITECTURE.md` and `TECHNICAL_DESIGN_DOCUMENT.md`, the `add_two_numbers` function currently lacks robust error handling for non-numeric inputs. If you call it with values that cannot be converted to integers (e.g., `add_two_numbers("hello", 5)`), the script will crash with a `ValueError`. This is a known critical issue and a high-priority fix is recommended to prevent Denial of Service.

---

## 5. Testing & Quality Assurance

We advocate for rigorous testing to ensure the reliability and correctness of our code. Please refer to the [Test Automation Guide](Test%20Automation%20Guide.md) for detailed protocols, including how to set up and run tests.

### Run Unit Tests
We recommend and use `pytest` for Python unit tests.

```bash
# Install pytest if you don't have it already
# pip install pytest

# Run all unit tests for the addNums module (assuming 'tests' directory exists)
pytest tests/unit/test_addNums.py
```
*(Note: As of the current codebase, the `tests` directory and `test_addNums.py` may not yet exist but are strongly recommended to be created as per the [Test Automation Guide](Test%20Automation%20Guide.md).)*

### Linting & Formatting
No automated linting or formatting tools (like `ruff` or `black`) are currently explicitly configured for this Python script. Developers are encouraged to adhere to [PEP 8](https://peps.python.org/pep-0008/) style guidelines and use IDE integrations (e.g., VS Code Python extension's linting features).

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy to manage our codebase. Please refer to the [Branching Strategy](Branching%20Strategy.md) document for detailed naming conventions and workflow steps.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass any configured CI checks (if applicable) and receive at least one peer review approval before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`python3: command not found`**: Ensure Python 3.x is installed on your system and its executable is correctly configured in your system's `$PATH` environment variable.
*   **`ModuleNotFoundError: No module named 'addNums'`**: This typically means the Python interpreter cannot find the `addNums.py` file. Ensure you are running the Python command from the directory containing `addNums.py` or that the directory is correctly added to your Python path.
*   **`ValueError: invalid literal for int() with base 10: '...'`**: This error occurs when you provide non-numeric input to the `add_two_numbers` function. This is a known critical issue (Denial of Service vulnerability) that requires a code fix for graceful error handling.

---

*Need help? Reach out to the **Team Lead** or a designated **Python Expert** on your team via your usual communication channels.*