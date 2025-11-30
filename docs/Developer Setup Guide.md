# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Simple Python Utility repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `v3.9+` (LTS) | Python runtime for scripts. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extension). |

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/[repo-name].git
cd [repo-name]
```

### Install Dependencies
This project currently has no external Python dependencies beyond the standard library.

---

## 3. Environment Configuration

This utility currently hardcodes configuration directly within the `addNums.py` file (e.g., `correlation_ID`). No external environment variables or `.env` files are required for local execution.

---

## 4. Running the Application

### Executing the Script
The `addNums.py` file defines a function `add_two_numbers`. To use it, you can import it into another Python script or execute it interactively in a Python interpreter.

Example of interactive execution:

```python
# Open a Python interpreter in your terminal
python

# Import the function
from addNums import add_two_numbers

# Call the function
result = add_two_numbers(10, 20)
print(result) # Expected output: 30

result_error = add_two_numbers('a', 20) # This will cause an unhandled ValueError due to current implementation
```
*Note: The current `addNums.py` lacks an `if __name__ == "__main__":` block for direct script execution and does not gracefully handle non-numeric inputs within the `int()` conversion block.*

---

## 5. Testing & Quality Assurance

Currently, no specific testing framework or QA processes are defined for this utility.

### Run Unit Tests
No dedicated unit test suite is configured. Consider using `pytest` for future additions to ensure code correctness.

### Linting & Formatting
No automated linting or formatting tools (e.g., `flake8`, `black`) are currently configured. Please ensure code adheres to PEP 8 standards and maintain consistent code style manually.

---

## 6. Workflow & Branching

We follow a standard Gitflow strategy.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks (if configured) and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`ModuleNotFoundError: No module named 'some_module'`**: Ensure all necessary Python packages are installed (though this project currently has none).
*   **`SyntaxError: invalid syntax`**: Check for typos, incorrect Python grammar, or missing colons/parentheses.
*   **`IndentationError: unexpected indent`**: Python relies on consistent indentation. Check your code for mixed spaces/tabs or incorrect indents, especially around `def`, `try`, `except`, `if`, `for`, `while` blocks.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*