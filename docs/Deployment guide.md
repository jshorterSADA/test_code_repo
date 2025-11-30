# Deployment Guide (GCP)

This document outlines the infrastructure architecture and deployment procedures for the "Number Addition Service" application on Google Cloud Platform (GCP).

## 1. Infrastructure Overview

Our infrastructure is defined as code (IaC) using **Terraform** and deployed via **GitHub Actions**. We utilize a containerized architecture to ensure consistency between development and production.

> **Note on Codebase:** The provided `addNums.py` script is a standalone Python function. For deployment to Cloud Run as a web service, it would need to be wrapped in a lightweight web framework (e.g., Flask, FastAPI) and containerized with a `Dockerfile`. The infrastructure described below assumes these additional components are in place.

### Core Components
| Service | Purpose |
| :--- | :--- |
| **Cloud Run** | Serverless container execution for the Python service. |
| **Artifact Registry** | Storage for Docker container images of the service. |
| **Secret Manager** | Secure storage for sensitive configuration (not currently used by `addNums.py` but available for future needs). |

---

## 2. Environments

We maintain strict isolation between environments to prevent accidental impact on live users.

> **Project Mapping**
> *   **Staging:** `number-addition-staging-XXXXXX` (Deploys from `develop` branch)
> *   **Production:** `number-addition-prod-XXXXXX` (Deploys from `main` branch)

---

## 3. Prerequisites

Before attempting a manual deployment or infrastructure update, ensure you have:

1.  **GCP Access:** IAM role `Editor` or `Cloud Run Admin` on the target project.
2.  **CLI Tools:** Installed and authenticated locally.
    ```bash
    gcloud auth login
    gcloud config set project [PROJECT_ID]
    ```
3.  **Terraform:** Version `1.5.0+` installed (if modifying infrastructure).

---

## 4. Deployment Pipeline (CI/CD)

Automated deployments are triggered via GitHub Actions. No manual deployments should occur unless there is a critical outage of the CI system.

> **Note on Codebase:** A GitHub Actions workflow file is not present in the provided codebase. The following describes a theoretical pipeline that would be implemented.

### The Pipeline Flow
1.  **Test:** Unit tests run (if any exist for `addNums.py`).
2.  **Build:** Docker image built from the `Dockerfile` (containing `addNums.py` and its web wrapper) and tagged with the Commit SHA.
3.  **Push:** Image uploaded to Google Artifact Registry.
4.  **Deploy:** `gcloud run deploy` updates the Cloud Run service with the new image.

### Triggering a Deploy
*   **Staging:** Push code to `develop`.
*   **Production:** Merge a Release PR into `main`.

---

## 5. Manual Deployment (Emergency Only)

In the event of a CI/CD failure, use the following steps to manually deploy a revision.

> **Note on Codebase:** These steps assume a `Dockerfile` exists at the root of your project, which includes `addNums.py` and a web server wrapper (e.g., Flask app).

**Step 1: Build the Container**
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/[PROJECT_ID]/number-addition-repo/number-addition-service:latest .
```

**Step 2: Deploy to Cloud Run**

```bash
gcloud run deploy number-addition-service \
  --image us-central1-docker.pkg.dev/[PROJECT_ID]/number-addition-repo/number-addition-service:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated # Adjust as per security requirements (e.g., --no-allow-unauthenticated)
```

---

## 6. Managing Secrets

**Never commit `.env` files to Git.**
All sensitive configuration is injected at runtime via Google Secret Manager.

> **Note on Codebase:** The `addNums.py` script currently hardcodes `correlation_ID`. For production, this (or any other configuration) could be dynamically supplied via environment variables, potentially managed by Secret Manager if it becomes sensitive.

To add a new secret (e.g., a new configuration value):

1.  Navigate to **Security > Secret Manager** in the GCP Console.
2.  Create a new secret (e.g., `APP_CONFIG_KEY`).
3.  Reference it in your Cloud Run service configuration via the GCP Console or `gcloud` commands, or in `terraform/main.tf` if using IaC:
    ```yaml
    # Cloud Run Env Var Reference (YAML for Cloud Run service config)
    - name: APP_CONFIG_KEY
      valueFrom:
        secretKeyRef:
          name: APP_CONFIG_KEY
          key: latest
    ```

---

## 7. Rollback Procedure

If a deployment introduces a critical bug, rollback immediately to the previous stable revision.

**Method A: via GCP Console**

1.  Go to **Cloud Run** > **number-addition-service** > **Revisions**.
2.  Locate the previous healthy revision (Green checkmark).
3.  Click **"Manage Traffic"** and route 100% to that revision.

**Method B: via CLI**

```bash
# 1. List revisions to find the previous one
gcloud run revisions list --service number-addition-service

# 2. Rollback traffic
gcloud run services update-traffic number-addition-service \
  --to-revisions=[PREVIOUS_REVISION_ID]=100
```

---

## 8. Verification

After deployment, verify the health of the service:

> **Note on Codebase:** A health check endpoint is not present in the provided `addNums.py`. This would be part of the web server wrapper.

*   **Health Check Endpoint:** `https://[SERVICE_URL]/health` (or `/status`) should return `200 OK`.
*   **Logs:** Check **Cloud Logging** for "Application Startup" or "Error" flags from the `number-addition-service`.
*   **Latency:** Ensure **Cloud Monitoring** shows latency within P95 thresholds for the service.