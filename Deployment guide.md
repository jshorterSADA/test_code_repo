# Deployment Guide (Local Execution / Python Runtime)

This document outlines the execution and operational procedures for the Core Number Addition Utility, a standalone Python script. Given its current scope as a single-file utility, many sections typical for cloud-deployed applications are marked as Not Applicable (N/A) or adapted for local execution.

## 1. Infrastructure Overview

The Core Number Addition Utility is a simple Python script (`addNums.py`) designed for local execution or integration into other Python applications. It does not currently utilize Infrastructure as Code (IaC) or a Continuous Integration/Continuous Deployment (CI/CD) pipeline for deployment in a cloud environment.

### Core Components
| Service | Purpose |
| :--- | :--- |
| **Python Runtime / Local Machine** | Execution environment for the script. |
| **N/A (Database Service)** | No external database is used or required. |
| **N/A (Registry Service)** | The script is not containerized for image registry storage. |
| **N/A (Secret Manager)** | Secrets (like `correlation_ID`) are hardcoded within the script. **(See Section 6 for details and recommendations)** |
| **N/A (Load Balancer)** | Not applicable for a local utility script. |

---

## 2. Environments

For a standalone utility script like the Core Number Addition Utility, the concept of distinct environments (e.g., Staging, Production) as found in larger applications does not apply. The script runs in the environment it is invoked within.

> **Project Mapping**
> *   **N/A (Staging)**
> *   **N/A (Production)**

---

## 3. Prerequisites

Before running the `addNums.py` script, ensure you have:

1.  **Python Interpreter:** Python 3.x installed and accessible on your system.
    ```bash
    python3 --version
    ```
2.  **Codebase:** The `addNums.py` file available locally.
    **[IaC Tool]:** Not Applicable (no Infrastructure as Code is used).

---

## 4. Deployment Pipeline (CI/CD)

The Core Number Addition Utility currently does not have an automated CI/CD pipeline as it is a standalone script. "Deployment" primarily means having the script available in the execution environment.

### The Pipeline Flow
N/A (No CI/CD pipeline).

### Triggering a Deploy
N/A (No automated deployment triggers).

---

## 5. Manual Execution

To execute the `addNums.py` script or integrate it into another Python application:

**Step 1: Place the Script**
Ensure `addNums.py` is in your desired working directory or part of your Python project structure.

**Step 2: Run the Script (Example)**

To test the function directly:

```bash
python3 -c "from addNums import add_two_numbers; print(add_two_numbers(5, 3))"
```

To run the file if it had direct execution logic:

```bash
python3 addNums.py
```

**Integrating the function:**

```python
# In your_application.py
from addNums import add_two_numbers

# Example: Valid inputs
result = add_two_numbers("10", "20", corrID="my-app-001")
if result is not None:
    print(f"Calculated sum: {result}")
else:
    print("Failed to calculate sum due to invalid input.")

# Example: Invalid inputs - CURRENTLY WILL CRASH!
# add_two_numbers("five", 3)
```

> [!WARNING]
> **Database Migrations**
> Not applicable. This utility does not interact with a database.

---

## 6. Managing Secrets

**Never commit `.env` files to Git.**
The current version of the Core Number Addition Utility hardcodes a `correlation_ID`. As identified in the code analysis, this is generally an anti-pattern as it limits traceability to a static value and does not reflect a dynamic, per-request identifier.

For a real-world system that this utility might be part of, or if this utility were to handle sensitive configuration:

1.  **Avoid hardcoding:** Replace hardcoded values (like `correlation_ID`) with configuration loaded from environment variables or a dedicated secret management service (e.g., AWS Secrets Manager, Google Secret Manager, Azure Key Vault, HashiCorp Vault).
2.  **Environment Variables:** Pass sensitive information as environment variables at runtime.
    ```bash
    # Example for passing a dynamic correlation ID
    export MY_APP_CORRELATION_ID="unique-request-id-456"
    python3 -c "import os; from addNums import add_two_numbers; print(add_two_numbers(5, 3, corrID=os.getenv('MY_APP_CORRELATION_ID')))"
    ```

---

## 7. Rollback Procedure

For a standalone Python script, "rollback" typically means reverting changes in your version control system.

**Method A: via Version Control (e.g., Git)**

1.  **Identify last stable commit:** Use `git log` to find the hash of the last known good version.
2.  **Revert to previous version (if current is problematic):**
    ```bash
    # To revert only the addNums.py file to a previous state
    git checkout [previous_stable_commit_hash] -- addNums.py

    # Or, to revert the last commit that introduced issues (creates a new commit)
    git revert HEAD
    ```
3.  **Confirm the change:** Verify the `addNums.py` file content has reverted to the desired state.

**Method B: Manual File Replacement**

If version control is not in use or accessible, replace the current `addNums.py` file with a known good backup.

---

## 8. Verification

After execution or integration, verify the utility's behavior:

*   **Function Output:** Check the return value of `add_two_numbers`.
    *   `add_two_numbers(5, 3)` should return `8`.
    *   `add_two_numbers("10", "2")` should return `12`.
    *   **Post-Fix for DoS Vulnerability:** As noted in the code analysis (`ARCHITECTURE.md`, `Application Interface Guide.md`, `TECHNICAL_DESIGN_DOCUMENT.md`), the current implementation crashes on non-numeric input. After the recommended fix to implement robust error handling (e.g., using `try-except ValueError`), verify that `add_two_numbers("five", 3)` gracefully handles the error (e.g., by returning `None` or raising a custom exception) instead of crashing.
*   **Logs:** Observe the console output for `logging.info` messages, which should include the correlation ID.
    *   Ensure messages like "Function `add_two_numbers` called..." and "Successfully added..." appear as expected.
    *   **Post-Fix:** Verify that error logs are generated correctly for invalid inputs when error handling is added.