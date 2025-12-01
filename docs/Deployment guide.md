# Deployment Guide (GCP)

This document outlines the infrastructure architecture and deployment procedures for the Number Addition Service application on Google Cloud Platform (GCP).

## 1. Infrastructure Overview

Our infrastructure is defined as code (IaC) using **Terraform** and deployed via **GitHub Actions**. We utilize a containerized architecture to ensure consistency between development and production.

### Core Components
| Service | Purpose |
| :--- | :--- |
| **Cloud Run** | Serverless container execution for the Python service. |
| **Artifact Registry** | Storage for Docker container images. |
| **Secret Manager** | Secure storage for sensitive configuration (e.g., API keys, external correlation IDs). |
| **Cloud Load Balancing** | Global HTTPS termination and CDN. |

---

## 2. Environments

We maintain strict isolation between environments to prevent accidental impact on live users.

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
3.  **Terraform:** Version `1.5.0+` installed (if modifying infrastructure).

---

## 4. Deployment Pipeline (CI/CD)

Automated deployments are triggered via GitHub Actions. No manual deployments should occur unless there is a critical outage of the CI system.

### The Pipeline Flow
1.  **Test:** Unit and Integration tests run.
2.  **Build:** Docker image built and tagged with the Commit SHA.
3.  **Push:** Image uploaded to Google Artifact Registry.
4.  **Deploy:** `gcloud run deploy` updates the service with the new image.
5.  **Migrate:** (Not applicable for this service)

### Triggering a Deploy
*   **Staging:** Push code to `develop`.
*   **Production:** Merge a Release PR into `main`.

---

## 5. Manual Deployment (Emergency Only)

In the event of a CI/CD failure, use the following steps to manually deploy a revision.

**Step 1: Build the Container**
```bash
gcloud builds submit --tag gcr.io/[PROJECT_ID]/number-addition-service:latest .
```

**Step 2: Deploy to Cloud Run**

```bash
gcloud run deploy number-addition-service \
  --image gcr.io/[PROJECT_ID]/number-addition-service:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

---

## 6. Managing Secrets

**Never commit `.env` files or hardcoded sensitive configurations to Git.**
All sensitive configuration and external parameters should be injected at runtime via Google Secret Manager. While the current `addNums.py` script hardcodes `correlation_ID`, in a production environment, such configuration would be managed externally.

To add a new secret (e.g., an external `CORRELATION_ID` or another API key):

1.  Navigate to **Security > Secret Manager** in the GCP Console.
2.  Create a new secret (e.g., `CORRELATION_ID`).
3.  Reference it in `terraform/main.tf` or the Cloud Run environment variables:
    ```yaml
    # Cloud Run Env Var Reference
    - name: CORRELATION_ID
      valueFrom:
        secretKeyRef:
          name: CORRELATION_ID
          key: latest
    ```

-----

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

-----

## 8. Verification

After deployment, verify the health of the service:

*   **Health Check Endpoint:** `https://number-addition-service-XYZ.run.app/health` (replace XYZ with your service specific ID) should return `200 OK` or appropriate service response.
*   **Logs:** Check **Cloud Logging** for "Application Startup" or "Error" flags for `number-addition-service`.
*   **Latency:** Ensure **Cloud Monitoring** shows latency within P95 thresholds for `number-addition-service`.