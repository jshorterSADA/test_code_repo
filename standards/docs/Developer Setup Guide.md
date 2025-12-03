# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Core Number Addition Service repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.8+` | Runtime environment for the Core Number Addition Service. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE. |

### Cloud & Infrastructure Tools
* **Cloud CLI:** N/A, as this project does not interact with any cloud services.
* **IaC Tool:** N/A, as this project does not utilize Infrastructure as Code.

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone [Repository URL]
cd [repo-name]
```

### Install Dependencies
Since this is a single Python script, there are no external dependencies to install using a package manager like `npm`. However, ensure you have the required Python version installed.

```bash
# Verify Python version
python3 --version
```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit `.env` files to version control.

### Local Environment Variables
1. No `.env` file is needed. However, if integrating into a larger application, create a `.env` file in your project root.
2. Fill in any required values needed by the integrating application.

---

## 4. Running the Application

### Start Local Development Server
This will execute the script directly:

```bash
python3 addNums.py
```
*   **Note:** This command assumes the `addNums.py` script has direct execution logic. If not, you'll need to import the `add_two_numbers` function into another Python script or interactive session.

### Running Infrastructure (Docker)
N/A, Docker is not required for this project.

---

## 5. Testing & Quality Assurance

We adhere to a strict **Testing Pyramid**. Please refer to the **[Test Automation Guide](Test%20Automation%20Guide.md)** for detailed protocols.

### Run Unit Tests
Executes Pytest for logic and components.

```bash
# Install pytest (if not already installed)
pip install pytest

# Run tests from the 'tests' directory (create it if it doesn't exist)
pytest tests/unit
```

### Run End-to-End (E2E) Tests
N/A

### Linting & Formatting
N/A. However, consider using a linter like `flake8` or `pylint` for larger projects.

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy. Please refer to the **[Branching Strategy](Branching%20Strategy.md)** document for naming conventions.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`python3: command not found`**: Ensure Python 3 is installed and in your system's `$PATH`.
*   **`ModuleNotFoundError: No module named 'addNums'`**: Ensure the `addNums.py` file is in the same directory as your script or that the directory is in your Python path.
*   **`ValueError: invalid literal for int() with base 10: '...'`**: This error occurs when the `add_two_numbers` function receives non-numeric input.  After applying the recommended fix (implementing `try-except` blocks), ensure that this exception is handled gracefully.
*   **Tests failing due to unhandled ValueError**: The original code is vulnerable to crashing when non-numeric inputs are passed. Write unit tests for the original, vulnerable code to assert that the ValueError occurs and causes a crash. Then, after the error handling is implemented, change the tests to assert that a non-numeric argument is handled gracefully (e.g., returns `None`).

---

*Need help? Reach out to the **[Support Channel]** on Slack.*