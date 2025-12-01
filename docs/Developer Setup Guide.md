# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Python Simple Adder repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `v3.8+` | Runtime for executing the Python script. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extensions). |

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/python-simple-adder.git
cd python-simple-adder
```

### Install Dependencies
This project is a simple Python script and currently does not have external dependencies beyond the Python standard library. Therefore, no explicit `pip install` step is required. For larger Python projects, a `requirements.txt` file would be used with `pip install -r requirements.txt`.

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit `.env` files to version control. We use **Google Secret Manager** for production secrets.

### Local Environment Variables
This project does not currently utilize external environment variables. All necessary configuration, such as the `correlation_ID`, is defined directly within the `addNums.py` script. For projects requiring external configuration, `.env` files would typically be used for local development, copied from an `.env.example` template.

---

## 4. Running the Application

### Running the Script
This project contains a standalone Python script, `addNums.py`, which defines a function `add_two_numbers`. To execute this function or experiment with the script, you can run it directly using the Python interpreter.

```bash
# To run the script (which will define the function)
python addNums.py

# To interact with the function, you would typically import it into another script
# or use a Python interactive shell:
# python
# >>> from addNums import add_two_numbers
# >>> add_two_numbers(1, 2)
```

---

## 5. Testing & Quality Assurance

For this simple script, formal testing frameworks and linting configurations are not currently implemented. However, for larger Python projects, we adhere to a strict **Testing Pyramid** and enforce code quality. Please refer to the **[Test Automation Guide](Test%20Automation%20Guide.md)** for detailed protocols applicable to more complex systems.

### Run Unit Tests (Conceptual)
For projects with tests, `pytest` would be used to execute unit tests.
```bash
# pytest
```
*Not applicable to the current `addNums.py` script.*

### Linting & Formatting (Conceptual)
We enforce code style using tools like **flake8** and **black** for Python. These would typically be run as pre-commit hooks or CI/CD steps.
```bash
# flake8 .
# black .
```
*Not currently configured for this script.*

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy. Please refer to the **[Branching Strategy](Branching%20Strategy.md)** document for naming conventions.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`python: command not found`**: Ensure Python is correctly installed on your system and its executable is added to your system's `$PATH` environment variable.
*   **`ModuleNotFoundError: No module named 'some_module'`**: If the project were to include external dependencies (e.g., in a `requirements.txt`), this error indicates that a required package has not been installed. Use `pip install -r requirements.txt` (or specific package names) within a virtual environment.
*   **`IndentationError` / `SyntaxError`**: Python is sensitive to whitespace. These errors indicate issues with code structure. Double-check your code against Python's syntax rules.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*