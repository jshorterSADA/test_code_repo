# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the `Python Number Adder` repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.8+` | The runtime for our Python application. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extension). |

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/python-number-adder.git
cd python-number-adder
```

### Install Dependencies
This project is a simple Python script with no external library dependencies specified in a `requirements.txt` file. If this project were to grow and include external libraries, you would typically:

1.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    ```
2.  **Activate the Virtual Environment:**
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
3.  **Install Dependencies (if `requirements.txt` existed):**
    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit sensitive information directly into source code or version control.

### Local Environment Variables
For this specific project, there are no external configuration files or environment variables required as all necessary settings (e.g., `correlation_ID`) are currently hardcoded within the `addNums.py` script.

For more complex Python projects, you might use `.env` files with a library like `python-dotenv`. If that were the case, you would:

1.  Copy a template file:
    ```bash
    cp .env.example .env
    ```
2.  Fill in the required values.

---

## 4. Running the Application

### Start the Python Script
You can execute the Python script directly.

```bash
# Ensure you are in the project root directory
python addNums.py
```
Note: To execute the `add_two_numbers` function, you would need to call it within the script or from an interactive Python session. For example, by adding `print(add_two_numbers(5, 7))` to `addNums.py`.

---

## 5. Testing & Quality Assurance

This project currently does not have an explicit testing suite or dedicated linting/formatting configurations.

### Recommended Practices for Python
For larger Python projects, we recommend:

*   **Unit Tests:** Using `unittest` or `pytest` for verifying individual functions.
*   **Linting:** Tools like `Flake8` or `Pylint` to enforce code style and catch common errors.
*   **Formatting:** Tools like `Black` or `isort` for automatic code formatting.

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy. Please refer to the **[Branching Strategy](Branching%20Strategy.md)** document for naming conventions.

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks (if implemented) and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`python: command not found`**: Ensure Python is installed and added to your system's `$PATH`.
*   **`ModuleNotFoundError: No module named 'xyz'`**: If you add external libraries, ensure you've activated your virtual environment and installed dependencies using `pip install -r requirements.txt`.
*   **Indentation Errors (`IndentationError`)**: Python relies heavily on consistent indentation. Ensure your editor is set up to use spaces (usually 4 spaces) consistently for indentation.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*