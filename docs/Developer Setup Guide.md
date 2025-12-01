# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Python Number Adder with Logging Example repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.8+` | The runtime for executing the script. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extension). |

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/python-logging-example.git
cd python-logging-example
```

### Install Dependencies
This script has no external dependencies beyond the Python standard library. Therefore, no `pip install` command is necessary to run `addNums.py`.

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never hardcode sensitive information directly into source files. While the `correlation_ID` in this example is not sensitive, for production applications, all configuration and secrets should be managed externally (e.g., environment variables, a dedicated config service, or a secrets manager).

### Local Environment Variables
The `addNums.py` script currently has the `correlation_ID` hardcoded. For a more flexible setup, you might consider externalizing such values into environment variables or a configuration file.

Example of how `correlation_ID` could be set via an environment variable (not currently used by the script):
```bash
export CORRELATION_ID="a-dynamic-correlation-id"
```
To implement this, you would modify `addNums.py` to read `os.getenv('CORRELATION_ID', 'default-id')`.

---

## 4. Running the Application

### Run the Script
This will execute the `addNums.py` script.

```bash
python addNums.py
```

To call the `add_two_numbers` function interactively, you can run the script and then define/call the function in a Python shell, or add a main execution block (`if __name__ == "__main__":`) to the script.

Example with direct function call (assuming you modify `addNums.py` to include a main block):
```python
# Inside addNums.py, at the end of the file:
if __name__ == "__main__":
    print("\n--- Example Calls ---")
    add_two_numbers(10, 5, "test-call-1")
    add_two_numbers("20", "15", "test-call-2")
    # Example of an invalid call (will raise an unhandled ValueError as per current code)
    # add_two_numbers("abc", 5, "test-call-3")
```
Then run:
```bash
python addNums.py
```

---

## 5. Testing & Quality Assurance

### Run Unit Tests
While no dedicated test suite is provided in the current codebase, for future development, we recommend using `pytest` for unit testing.

```bash
# Example: Install pytest (if not already installed)
# pip install pytest

# Example: Run tests (assuming tests are in a 'tests/' directory)
# pytest
```

### Linting & Formatting
We enforce code style via `flake8` for linting and `black` for formatting. These can be run manually:

```bash
# Example: Install linting and formatting tools
# pip install flake8 black

# Run linting checks
# flake8 .

# Run auto-formatting
# black .
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

*   **`python: command not found`**: Ensure Python is installed and its executable is in your system's `$PATH`.
*   **`No module named ...`**: If you add external dependencies later, ensure they are installed via `pip install -r requirements.txt`.
*   **`IndentationError`**: Python relies heavily on correct indentation. Check your code for mixed spaces/tabs or incorrect indents.
*   **Unhandled exceptions**: The `add_two_numbers` function currently has a `try` block but an `except` block is missing to gracefully handle non-numeric inputs. If you input `add_two_numbers("abc", 5)`, it will raise a `ValueError`.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*