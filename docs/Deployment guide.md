# Deployment Guide (GCP)

This document outlines potential infrastructure architecture and deployment considerations for the `addNums.py` utility on Google Cloud Platform (GCP). Given its current form as a standalone Python script, much of the sophisticated infrastructure detailed below would typically be applied if `addNums.py` were integrated into a larger containerized application or deployed as a serverless function.

## 1. Infrastructure Overview

The `addNums.py` script is a simple Python function. If it were to be containerized and deployed as a microservice, our infrastructure would ideally be defined as code (IaC) using **Terraform** and deployed via **GitHub Actions**. This would ensure consistency and automation.

### Core Components (Applicable if containerized as a service)
| Service | Purpose |
| :--- | :--- |
| **Cloud Run** | Serverless container execution (if `addNums.py` were wrapped in a web framework). |
| **Cloud SQL** | Not applicable; `addNums.py` has no database dependencies. |
| **Artifact Registry** | Storage for Docker container images (if `addNums.py` were containerized). |
| **Secret Manager** | Not applicable; `addNums.py` currently uses no external secrets. |
| **Cloud Load Balancing** | Not applicable; `addNums.py` is not a web service unless integrated into one. |

---

## 2. Environments

For a standalone script like `addNums.py`, the concept of distinct environments (staging/production) is less directly applicable. However, if this utility were integrated into a larger application, environment isolation would be crucial.

> **Project Mapping (Hypothetical if integrated into a larger service)**
> * **Staging:** `add-nums-staging-gcp` (Deploys from `develop` branch)
> * **Production:** `add-nums-prod-gcp` (Deploys from `main` branch)

---

## 3. Prerequisites

Before attempting a manual deployment or infrastructure update (if `addNums.py` were part of a larger system), ensure you have:

1.  **GCP Access:** IAM role `Editor` or `Cloud Run Admin` on the target project (if deploying to Cloud Run).
2.  **CLI Tools:** Installed and authenticated locally.
    ```bash
    gcloud auth login
    gcloud config set project [ADD_NUMS_GCP_PROJECT_ID]
    ```
3.  **Terraform:** Version `1.5.0+` installed (if modifying surrounding infrastructure).

---

## 4. Deployment Pipeline (CI/CD)

The `addNums.py` script is a simple utility and does not inherently have a CI/CD pipeline. If it were containerized and exposed as a microservice (e.g., via Flask or FastAPI) and deployed to Cloud Run, an automated pipeline would be essential.

### The Pipeline Flow (Hypothetical for a containerized service)
1.  **Test:** Unit tests for `add_two_numbers` would run.
2.  **Build:** A Docker image containing the script and its dependencies would be built and tagged with the Commit SHA.
3.  **Push:** Image uploaded to Google Artifact Registry.
4.  **Deploy:** `gcloud run deploy` updates the service with the new image.
5.  **Migrate:** Not applicable; `addNums.py` does not interact with a database.

### Triggering a Deploy (Hypothetical for a containerized service)
* **Staging:** Push code to `develop`.
* **Production:** Merge a Release PR into `main`.

---

## 5. Manual Deployment (Emergency Only)

The `addNums.py` script is currently a standalone Python file. For direct execution, simply run `python addNums.py` (if it had a main execution block). If it were containerized and deployed to Cloud Run, the following manual steps would be used in an emergency.

**Step 1: Build the Container (Hypothetical - requires a `Dockerfile`)**
```bash
# Assuming a Dockerfile exists in the root of the project
gcloud builds submit --tag gcr.io/[ADD_NUMS_GCP_PROJECT_ID]/add-nums-service:latest .
```

**Step 2: Deploy to Cloud Run (Hypothetical)**

```bash
gcloud run deploy add-nums-service \
  --image gcr.io/[ADD_NUMS_GCP_PROJECT_ID]/add-nums-service:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated # Adjust as per security requirements
```

> [\!WARNING]
> **Database Migrations**
> `addNums.py` does not involve database schema updates. This warning is generally applicable for services that do.

-----

## 6. Managing Secrets

**Never commit `.env` files to Git.**
The `addNums.py` script does not currently utilize any external secrets or sensitive configuration. If it were to require API keys, credentials, or other sensitive information in the future, these should be managed via Google Secret Manager.

To add a new secret:

1.  Navigate to **Security \> Secret Manager** in the GCP Console.
2.  Create a new secret (e.g., `EXTERNAL_API_KEY`).
3.  Reference it in the Cloud Run service environment variables (if applicable):
    ```yaml
    # Cloud Run Env Var Reference
    - name: EXTERNAL_API_KEY
      valueFrom:
        secretKeyRef:
          name: EXTERNAL_API_KEY
          key: latest
    ```

-----

## 7. Rollback Procedure

For the `addNums.py` script as a standalone file, a "rollback" would involve replacing the file on the execution environment. If `addNums.py` were deployed as a Cloud Run service, the standard rollback procedures would apply.

**Method A: via GCP Console (Hypothetical for Cloud Run)**

1.  Go to **Cloud Run** \> **add-nums-service** \> **Revisions**.
2.  Locate the previous healthy revision (Green checkmark).
3.  Click **"Manage Traffic"** and route 100% to that revision.

**Method B: via CLI (Hypothetical for Cloud Run)**

```bash
# 1. List revisions to find the previous one
gcloud run revisions list --service add-nums-service

# 2. Rollback traffic
gcloud run services update-traffic add-nums-service \
  --to-revisions=[PREVIOUS_REVISION_ID]=100
```

-----

## 8. Verification

Verification steps depend heavily on how `addNums.py` is deployed.

  *   **Standalone Script:** Verify by executing the script locally and checking its output and logs.
  *   **Cloud Run Service (Hypothetical):**
      *   **Health Check Endpoint:** If the service has one, e.g., `https://[SERVICE_URL]/health`, it should return `200 OK`.
      *   **Logs:** Check **Cloud Logging** for service startup messages or any error logs from the `add_two_numbers` function. The script's logging includes a `correlation_ID` for easier tracing.
      *   **Functionality:** Test the specific endpoint that utilizes the `add_two_numbers` function to ensure correct calculations.