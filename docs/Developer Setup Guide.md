# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the **Product Quality Alert System** repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `3.9+` (recommended `3.11` for Cloud Functions) | Primary language for the project. |
| **pip** | Latest | Python package installer. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python extension). |

### Cloud & Infrastructure Tools
*   **Google Cloud SDK:** [Install gcloud CLI](https://cloud.google.com/sdk/docs/install) for deploying Cloud Functions, managing Pub/Sub, and accessing Secret Manager.
*   **Terraform:** `v1.5.0+` (Required only if working on Infrastructure as Code to manage GCP resources).

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:Insight-Enterprises/product-quality-alert-system.git
cd product-quality-alert-system
```

### Install Dependencies
We use Python's `pip` with virtual environments to manage packages.

```bash
# Create a Python virtual environment in the project root
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies required for the Cloud Function and local scripts
# The requirements.txt for the Cloud Function is located in its directory.
pip install -r cloud_function_jira_processor/requirements.txt
# If 'm_analytical_demo' or other top-level scripts have specific dependencies,
# ensure they are listed in a requirements.txt file and installed similarly.
```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit sensitive credentials to version control. We use **Google Secret Manager** for production secrets like `JIRA_API_KEY`.

### Cloud Function Environment Variables
For the `cloud_function_jira_processor`, non-sensitive environment variables are defined in `.env.yaml` and injected during deployment to Google Cloud Functions. This file is committed to the repository.

```yaml
# cloud_function_jira_processor/.env.yaml
JIRA_PROJECT_ID: "AITD"
JIRA_ISSUE_TYPE: "Task"
JIRA_SERVER: "https://sadaadvservices.atlassian.net"
USER_EMAIL: "joseph.shorter@sada.com"
GOOGLE_CLOUD_PROJECT: "sada-joseph-shorter-sada"
```

*   **Sensitive Keys:** The `JIRA_API_KEY` is retrieved dynamically from **Google Secret Manager** using its resource ID: `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`. Ensure your Google Cloud user or the Cloud Function's service account has permissions to access this secret.

### Local Development Variables
When running scripts locally (e.g., `test_jira_status.py`), your `gcloud` authentication must be active to access GCP services (like Secret Manager).

```bash
# Authenticate your gcloud CLI to access GCP resources
gcloud auth login
# Set application default credentials (used by Google Cloud client libraries)
gcloud auth application-default login
```

---

## 4. Running the Application

This project primarily involves a Google Cloud Function that responds to Pub/Sub messages. There isn't a long-running local development server typical of web applications.

### Activate Virtual Environment
Always ensure your Python virtual environment is active before running Python commands:
```bash
source .venv/bin/activate
```

### Deploying the Cloud Function
The `cloud_function_jira_processor` is deployed to Google Cloud Functions (2nd gen).

1.  Navigate to the Cloud Function directory:
    ```bash
    cd cloud_function_jira_processor
    ```
2.  Make the deployment script executable and run it:
    ```bash
    chmod +x deploy.sh
    ./deploy.sh
    ```
    This script executes the `gcloud functions deploy` command with all necessary configurations.

### Running Local Demo/Utility Scripts

*   **Demonstrate Log Outputs:**
    To see how the `add_two_numbers` function handles various inputs and generates logs, run this script from the project root:
    ```bash
    python demo_log_examples.py
    ```
*   **Check JIRA Service Status:**
    To verify if JIRA is online and your credentials (retrieved via Secret Manager) are valid, run this script from the project root:
    ```bash
    python cloud_function_jira_processor/test_jira_status.py
    ```

### Publishing Test Alerts (to trigger Cloud Function)
To manually trigger the deployed Cloud Function, you can use the `m_analytical_demo/agent.py` script to publish messages to the `product-quality-alerts` Pub/Sub topic.

1.  From the project root, navigate to the `m_analytical_demo` directory:
    ```bash
    cd m_analytical_demo
    ```
2.  Ensure your virtual environment is active (if not already):
    ```bash
    source ../.venv/bin/activate # Adjust path based on your venv location
    ```
3.  Run the Python command to detect and publish alerts:
    ```bash
    python -c "from agent import detect_product_quality_issues, publish_product_alert; \
               import json; \
               issues = detect_product_quality_issues(7, 'high'); \
               data = json.loads(issues); \
               print(f'Detected {data[\"issues_found\"]} issues'); \
               result = publish_product_alert(issues); \
               print(result)"
    ```

---

## 5. Testing & Quality Assurance

### Activate Virtual Environment
```bash
source .venv/bin/activate
```

### Run Demo/Test Scripts
While dedicated unit test suites for individual functions are not included in the provided snippets, you can use the following scripts to verify overall functionality and log outputs:

*   **Log Output Demonstration for `add_two_numbers`:**
    ```bash
    python demo_log_examples.py
    ```
*   **JIRA Connectivity and Credential Test:**
    ```bash
    python cloud_function_jira_processor/test_jira_status.py
    ```
    This script checks JIRA service availability and validates access to the `JIRA_API_KEY` in Secret Manager.

### Linting & Formatting
We recommend using standard Python linters and formatters like `flake8` and `black`. You can install them via pip:

```bash
pip install flake8 black
```

Then run them manually from the project root (adjust paths or configuration as needed):

```bash
# Lint all Python files for style and common errors
flake8 .

# Auto-format all Python files to adhere to PEP 8 standards
black .
```

---

## 6. Workflow & Branching

We follow a **Gitflow** strategy. Please refer to your team's **[Branching Strategy](Branching%20Strategy.md)** document for naming conventions, or follow standard practices:

*   **Feature Work:** Branch off `develop` (`feature/my-feature`).
*   **Hotfixes:** Branch off `main` (`hotfix/critical-bug`).
*   **Pull Requests:** Must pass CI checks and receive at least one peer review before merging.

---

## 7. Troubleshooting

**Common Issues:**

*   **`python: command not found` or `pip: command not found`**: Ensure Python and pip are installed and added to your system's `$PATH`.
*   **`gcloud: command not found`**: Ensure the Google Cloud SDK `bin` folder is in your system `$PATH` and you've completed `gcloud init`.
*   **`ModuleNotFoundError`**: Ensure you've activated your Python virtual environment (`source .venv/bin/activate`) and installed all dependencies (`pip install -r requirements.txt`).
*   **`Permission denied` during `pip install`**: You might need to fix ownership of your Python environment or use `pip install --user` (though using virtual environments is generally preferred).
*   **Cloud Function deployment errors**: Check the `gcloud functions deploy` output carefully for missing permissions, incorrect `--entry-point`, or issues with `requirements.txt`. Refer to the Cloud Function logs (`gcloud functions logs read ...`) for runtime errors.
*   **JIRA connectivity issues (`404`, `Site temporarily unavailable`)**: As highlighted in `PRODUCT_QUALITY_ALERT_STATUS.md`, the JIRA instance can occasionally be temporarily unavailable. Use `python cloud_function_jira_processor/test_jira_status.py` to check its current status. Messages will be retried automatically by Pub/Sub if JIRA is unavailable.
*   **Secret Manager access denied**: Ensure your `gcloud` authenticated user (for local testing) or the Cloud Function's service account has the `Secret Manager Secret Accessor` role for the `JIRA_API_KEY` secret.

---

*Need help? Reach out to the **#engineering-support** channel on Slack (or your team's equivalent support channel).*