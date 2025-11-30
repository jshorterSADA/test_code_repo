# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Insight Enterprises Python Utilities repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `v3.9+` | Runtime for Python scripts and utilities. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extension). |

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/PythonUtilities.git
cd PythonUtilities
```

### Install Dependencies
We use `pip` to manage Python packages. It's highly recommended to use a virtual environment to isolate project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows (cmd.exe):
venv\Scripts\activate.bat
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install project dependencies (if a requirements.txt file exists)
# pip install -r requirements.txt

# The current codebase relies only on standard Python libraries.
```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit sensitive information (like API keys or production secrets) directly into code or `.env` files that are committed to version control. We use **Google Secret Manager** for production secrets.

### Local Configuration
Currently, `addNums.py` includes a hardcoded `correlation_ID`. For a real-world application, such values would typically be managed via environment variables (e.g., using `python-dotenv`) or a dedicated configuration service.

If future development introduces `.env` files for local configuration:
1.  Copy the template file to create your local config:
    ```bash
    cp .env.example .env
    ```
2.  Fill in the required values. Ask your **Team Lead** or check the **1Password Engineering Vault** for shared development keys.

---

## 4. Running the Application

The `addNums.py` script provides a function `add_two_numbers`. It's designed to be imported and called from other Python scripts or an interactive session.

### Running Python Scripts
First, ensure your virtual environment is activated (see "Install Dependencies" above).

You can test the `add_two_numbers` function by importing it into a Python interpreter:

```bash
# Activate your virtual environment if not already active
# source venv/bin/activate

# Start a Python REPL
python
```

Within the Python REPL:
```python
import addNums

# Call the function with integers
result_int = addNums.add_two_numbers(10, 20)
print(f"Result with integers: {result_int}")

# Call the function with string representations of numbers
result_str = addNums.add_two_numbers("10", "20")
print(f"Result with strings: {result_str}")

# To exit the REPL
exit()
```

If you were to create a separate script (e.g., `main.py`) in the same directory:
```python
# main.py
import addNums

if __name__ == "__main__":
    print("Running addNums.add_two_numbers examples:")
    # Example 1: Valid numbers
    sum1 = addNums.add_two_numbers(5, 7)
    print(f"Sum of 5 and 7: {sum1}")

    # Example 2: String numbers
    sum2 = addNums.add_two_numbers("15", "25")
    print(f"Sum of '15' and '25': {sum2}")

    # Example 3: Mixed types (will convert successfully)
    sum3 = addNums.add_two_numbers(30, "40")
    print(f"Sum of 30 and '40': {sum3}")

    # Example 4: Invalid input (will log an error, returns None) - Note: current addNums.py expects `int` directly after conversion.
    # The current addNums.py snippet lacks the try/except block for int conversion errors, but it's good practice to consider.
    # For now, it will attempt `int()` conversion directly.
    # sum_error = addNums.add_two_numbers("hello", 50)
    # print(f"Sum of 'hello' and 50: {sum_error}")
```

Then run `main.py` from your terminal:
```bash
python main.py
```

---

## 5. Testing & Quality Assurance

We adhere to a strict **Testing Pyramid**. Please refer to the **[Test Automation Guide](Test%20Automation%20Guide.md)** for detailed protocols.

### Run Unit Tests
While no dedicated test files are provided in the current codebase, for Python projects, we typically use `pytest` for running unit and integration tests.

```bash
# Example if tests were present and pytest installed:
# pip install pytest
# pytest
```

### Linting & Formatting
We enforce code style via tools like **Black** (formatter) and **Flake8** (linter). These can be integrated with `pre-commit` hooks for automatic checks.

```bash
# Install linting/formatting tools (if not already in requirements.txt)
# pip install black flake8 isort

# Manually run Black (code formatter)
# black .

# Manually run Flake8 (linter)
# flake8 .

# Manually run isort (import sorter)
# isort .
```

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy. Please refer to the **[Branching Strategy](Branching%20Strategy.md)** document for naming conventions.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`ModuleNotFoundError`**: Ensure you have activated your virtual environment (`source venv/bin/activate`) and installed all dependencies (`pip install -r requirements.txt` if applicable).
*   **`Permission denied`**: You might need to fix file permissions for Python scripts or directories. Avoid running `python` with `sudo` unless absolutely necessary; instead, fix ownership (`sudo chown -R $(whoami) .`).
*   **`IndentationError` or `SyntaxError`**: Python is sensitive to whitespace and syntax. Use a good IDE like VS Code with the Python extension to catch these errors early.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*