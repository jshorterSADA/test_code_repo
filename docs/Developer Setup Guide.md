# Developer Setup Guide

**Welcome to the team!** This guide will help you set up your local development environment to contribute to the Product Quality Alert System repository. Follow these steps sequentially to ensure a smooth onboarding experience.

---

## 1. Prerequisites

Before cloning the repository, ensure your machine has the following tools installed.

### Required Software
| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Python** | `v3.11` (or `v3.9+`) | Core language for all components. |
| **Git** | `2.3+` | Version control. |
| **VS Code** | Latest | Recommended IDE (with Python, ESLint/Prettier extensions). |

### Cloud & Infrastructure Tools
*   **Google Cloud SDK:** [Install gcloud CLI](https://cloud.google.com/sdk/docs/install) for deployment, authentication, and interacting with Google Cloud services like Pub/Sub and Secret Manager.
*   **Terraform:** `v1.5.0+` (Required only if working on Infrastructure as Code).

---

## 2. Repository Setup

### Clone the Repository
We use **SSH** for secure access. Ensure your SSH keys are added to your GitHub account.

```bash
git clone git@github.com:sada-enterprises/product-quality-alert-system.git
cd product-quality-alert-system
```
_Note: Replace `sada-enterprises/product-quality-alert-system` with the actual repository path if different._

### Install Dependencies
We use `pip` with a Python virtual environment to manage packages.

```bash
# 1. Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Python dependencies for the Cloud Function and related scripts
pip install -r cloud_function_jira_processor/requirements.txt

# 3. Install development tools for linting, formatting, and local function emulation
pip install black flake8 isort functions-framework
```

---

## 3. Environment Configuration

> **⛔ SECURITY WARNING**
> Never commit `.env` files or hardcoded secrets to version control. We use **Google Secret Manager** for production secrets.

### Local Environment Variables
For local testing of the Cloud Function and related scripts, you will need to set up some environment variables.

1.  **Copy the template file** to create your local config. This file contains default values for the Cloud Function's environment:
    ```bash
    cp cloud_function_jira_processor/.env.yaml .env
    ```
2.  **Edit the `.env` file** to override values for your local development setup if necessary (e.g., `USER_EMAIL` for JIRA).
3.  **Authenticate `gcloud`** for Secret Manager access:
    The `cloud_function_jira_processor/main.py` accesses the JIRA API key from Google Secret Manager. For your local environment to do the same, you need to authenticate your `gcloud` CLI with application default credentials:
    ```bash
    gcloud auth application-default login
    ```
    Ensure your authenticated user has permissions to access the JIRA API Key secret (`projects/900228280944/secrets/JIRA_API_KEY`).

---

## 4. Running the Application

This codebase primarily consists of Python scripts and a Google Cloud Function. There isn't a single "local development server" like a web app. Instead, you'll run specific scripts or emulate the Cloud Function locally.

### 1. Run the `add_two_numbers` Demo Script
This script demonstrates the logging behavior of the `add_two_numbers` utility function.
```bash
# Ensure your virtual environment is active
source .venv/bin/activate

python demo_log_examples.py
```

### 2. Test JIRA Connectivity & Credentials
Use this script to verify your connection to JIRA and that your Google Cloud credentials allow access to the JIRA API key in Secret Manager.
```bash
# Ensure your virtual environment is active
source .venv/bin/activate

python cloud_function_jira_processor/test_jira_status.py
```

### 3. Locally Emulate the Cloud Function
The `cloud_function_jira_processor` is a Google Cloud Function triggered by Pub/Sub messages. You can emulate its execution locally using the `functions-framework`.

*   **In Terminal 1 (Cloud Function Emulator):**
    Start the local emulator. The `--source` flag points to your function's Python file.
    ```bash
    # Ensure your virtual environment is active
    source .venv/bin/activate
    functions-framework --target=process_quality_alert --port=8080 --debug --source cloud_function_jira_processor/main.py
    ```
    This terminal will show the function's logs as it processes messages.

*   **In Terminal 2 (Trigger the Function):**
    Send a POST request to the local emulator, simulating a Pub/Sub message.
    ```bash
    # Ensure your virtual environment is active
    source .venv/bin/activate
    python -c '
import requests
import json
import base64

# This is a sample alert message structure from the codebase (customize as needed)
test_alert = {
    "severity": "HIGH",
    "product_name": "Local Test Item",
    "product_id": "LTI-2023",
    "category": "Toys",
    "brand": "Acme",
    "avg_sentiment": 0.75,
    "negative_ratio": 0.1,
    "sentiment_change": 0.05,
    "review_count": 150,
    "recent_revenue": 5000.00,
    "revenue_change_pct": 12.5,
    "revenue_at_risk": 750.00,
    "alert_timestamp": "2023-10-27T10:00:00Z",
    "analysis_period_days": 7,
    "price": 25.00,
    "recommended_actions": ["Review recent customer feedback", "Investigate QA process"]
}

# Pub/Sub messages are base64 encoded JSON
pubsub_data = base64.b64encode(json.dumps(test_alert).encode("utf-8")).decode("utf-8")

# CloudEvent structure for Pub/Sub trigger (replace your-project-id)
cloud_event = {
    "message": {
        "data": pubsub_data,
        "messageId": "test-message-123",
        "publishTime": "2023-10-27T10:05:00Z"
    },
    "subscription": "projects/sada-joseph-shorter-sada/subscriptions/test-sub"
}

headers = {"Content-Type": "application/json"}
try:
    response = requests.post("http://localhost:8080", headers=headers, data=json.dumps(cloud_event))
    print(f"Trigger response status: {response.status_code}")
    print(f"Trigger response body: {response.text}")
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the local emulator. Is it running?")
'
    ```

---

## 5. Testing & Quality Assurance

We adhere to a strict **Testing Pyramid**. Please refer to the **[Test Automation Guide](Test%20Automation%20Guide.md)** for detailed protocols.

### Run Unit Tests
While no dedicated unit test files were provided in the snippets, standard practice involves `pytest` for Python projects.
```bash
# (Assuming pytest is configured for unit tests)
# Ensure your virtual environment is active
source .venv/bin/activate
pytest
```

### Run Integration/System Tests
The `test_jira_status.py` script serves as an integration test to verify connectivity and authentication with JIRA.
```bash
# Ensure your virtual environment is active
source .venv/bin/activate
python cloud_function_jira_processor/test_jira_status.py
```

### Linting & Formatting
We enforce code style via `black`, `flake8`, and `isort`. These can be run manually:

```bash
# Ensure your virtual environment is active and dev tools are installed (Section 2)
source .venv/bin/activate

# Run Black for code formatting
black .

# Run Flake8 for linting
flake8 .

# Run isort for import sorting
isort .
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

*   **`ModuleNotFoundError` or missing dependencies**: Ensure your Python virtual environment is activated (`source .venv/bin/activate`) and all dependencies from `requirements.txt` and developer tools are installed (`pip install -r requirements.txt` and `pip install functions-framework black flake8 isort`).
*   **`EACCES: permission denied`**: You might need to fix `pip` or directory permissions. Avoid `sudo pip`. Fix ownership instead (e.g., `sudo chown -R $(whoami) ~/.npm` or for virtual env related directories).
*   **`gcloud: command not found`**: Ensure the Google Cloud SDK `bin` folder is in your system `$PATH`.
*   **JIRA Connectivity Issues**: Run `python cloud_function_jira_processor/test_jira_status.py` to diagnose issues with JIRA server availability or credential access.
*   **Cloud Function Emulator not responding**: Double-check that the emulator is running on `http://localhost:8080`, and that the `--target` (`process_quality_alert`) and `--source` (`cloud_function_jira_processor/main.py`) flags are correct.

---

*Need help? Reach out to the **#engineering-support** channel on Slack.*