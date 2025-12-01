# Deployment Guide (GCP)

This document outlines the infrastructure architecture and deployment procedures for the Python Addition Service application on Google Cloud Platform (GCP).

## 1. Infrastructure Overview

While the current codebase is a single Python script (`addNums.py`), a future robust deployment would typically involve infrastructure defined as code (IaC) using **Terraform** and deployed via **GitHub Actions**. We envision a containerized architecture to ensure consistency between development and production for this service.

### Core Components
| Service | Purpose |
| :--- | :--- |
| **Cloud Run** | Serverless container execution for the Python Addition Service. |
| **Artifact Registry** | Storage for Docker container images of the service. |
| **Secret Manager** | (Future) Secure storage for any configuration or credentials the service might need. |
| **Cloud Load Balancing** | (Future) Global HTTPS termination and CDN, if the service were part of a larger microservices architecture. |

---

## 2. Environments

We would maintain strict isolation between environments to prevent accidental impact on live users. For this service, the following mapping is envisioned:

> **Project Mapping**
> *   **Staging:** `gcp-project-staging` (Deploys from `develop` branch)
> *   **Production:** `gcp-project-prod` (Deploys from `main` branch)

---

## 3. Prerequisites

Before attempting a manual deployment or infrastructure update, ensure you have:

1.  **GCP Access:** IAM role `Editor` or `Cloud Run Admin` on the target project.
2.  **CLI Tools:** Installed and authenticated locally.
    ```bash
    gcloud auth login
    gcloud config set project [PROJECT_ID]
    ```
3.  **Terraform:** Version `1.5.0+` installed (if modifying or creating infrastructure for this service).

---

## 4. Deployment Pipeline (CI/CD)

For a production-ready setup, automated deployments would be triggered via GitHub Actions. Currently, no CI/CD pipeline is defined for the `addNums.py` script within the provided codebase. The following describes the conceptual pipeline flow. No manual deployments should occur unless there is a critical outage of the CI system.

### The Pipeline Flow
1.  **Test:** Unit and Integration tests run (if defined for the Python script).
2.  **Build:** Docker image built from the `addNums.py` script and tagged with the Commit SHA.
3.  **Push:** Image uploaded to Google Artifact Registry.
4.  **Deploy:** `gcloud run deploy` updates the Cloud Run service with the new image.
5.  **Migrate:** (Not applicable for this script as it has no database dependencies).

### Triggering a Deploy
*   **Staging:** Push code to `develop`.
*   **Production:** Merge a Release PR into `main`.

---

## 5. Manual Deployment (Emergency Only)

In the event of a CI/CD failure, or for initial setup, use the following steps to manually deploy a revision. This assumes you have a `Dockerfile` for the `addNums.py` script.

**Step 1: Build the Container**
```bash
gcloud builds submit --tag gcr.io/[PROJECT_ID]/python-addition-service:latest .
```

**Step 2: Deploy to Cloud Run**

```bash
gcloud run deploy python-addition-service \
  --image gcr.io/[PROJECT_ID]/python-addition-service:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --concurrency=80
```

> [!WARNING]
> The `addNums.py` script has no database dependencies; therefore, database migrations are not applicable to this service.

---

## 6. Managing Secrets

**Never commit `.env` files to Git.**
The current `addNums.py` script hardcodes the `correlation_ID`. In a production environment, if this or other configuration values needed to be dynamic or sensitive, they would be injected at runtime via Google Secret Manager.

To add a new secret (e.g., a hypothetical API key for an external service):

1.  Navigate to **Security > Secret Manager** in the GCP Console.
2.  Create a new secret (e.g., `EXTERNAL_API_KEY`).
3.  Reference it in the Cloud Run service configuration as an environment variable:
    ```yaml
    # Cloud Run Env Var Reference (in a YAML configuration file or gcloud command)
    - name: EXTERNAL_API_KEY
      valueFrom:
        secretKeyRef:
          name: EXTERNAL_API_KEY
          key: latest
    ```

---

## 7. Rollback Procedure

If a deployment introduces a critical bug, rollback immediately to the previous stable revision.

**Method A: via GCP Console**

1.  Go to **Cloud Run** > **python-addition-service** > **Revisions**.
2.  Locate the previous healthy revision (Green checkmark).
3.  Click **"Manage Traffic"** and route 100% to that revision.

**Method B: via CLI**

```bash
# 1. List revisions to find the previous one
gcloud run revisions list --service python-addition-service

# 2. Rollback traffic
gcloud run services update-traffic python-addition-service \
  --to-revisions=[PREVIOUS_REVISION_ID]=100
```

---

## 8. Verification

After deployment, verify the health of the service:

*   **Health Check Endpoint:** `https://[SERVICE_URL]/health` (if implemented) should return `200 OK`.
*   **Logs:** Check **Cloud Logging** for "Application Startup" or "Error" flags related to `python-addition-service`.
*   **Functionality:** Test the core functionality (e.g., `POST /add` with two numbers) to ensure it returns correct results and logs as expected.
*   **Latency:** Ensure **Cloud Monitoring** shows latency within P95 thresholds for the service.