# Infrastructure Setup & Configuration (GCP)

This document details the architectural standards and setup procedures for provisioning the **Product Quality Alert Processor** infrastructure on Google Cloud Platform.

**Philosophy:** While the current deployment leverages `gcloud CLI` commands, our philosophy embraces **Immutable Infrastructure**. Future enhancements will aim for full Infrastructure as Code (IaC) using Terraform, ensuring that the environment is reproducible, secure, and version-controlled. Manual changes in the GCP Console are discouraged (Read-Only Policy), except for emergency break-glass scenarios.

---

## 1. Prerequisites (Local Environment)

Before interacting with the infrastructure, ensure your local machine is configured with the necessary tools. Explicit version pinning (e.g., via `.tool-versions`) is not currently implemented in this codebase, but is a recommended best practice.

*   **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install):** For authentication, API interaction, and deploying the Cloud Function.
*   **[Terraform](https://www.terraform.io/):** (v1.5.0+) **(Recommended for future IaC)** For declarative infrastructure provisioning.
*   **[Python](https://www.python.org/):** (v3.9+) For running local scripts and the Cloud Function runtime.

**Initial Auth**
```bash
gcloud auth login
gcloud auth application-default login
```

-----

## 2. Project Topology

The current implementation utilizes a single GCP project to host the Cloud Function and associated services. While this simplifies initial setup, for robust multi-environment deployments (e.g., staging, production), a multi-project hierarchy is strongly recommended to ensure strict isolation.

| Environment | GCP Project ID          | Purpose                                                                                                  | Access Level          |
| :---------- | :---------------------- | :------------------------------------------------------------------------------------------------------- | :-------------------- |
| **Main**    | `sada-joseph-shorter-sada` | Hosts the `product-quality-jira-processor` Cloud Function, Pub/Sub topic, and Secret Manager secrets. Acts as the primary operational environment. | Developers (Editor), CI/CD |

-----

## 3. Infrastructure Deployment & Configuration

While the long-term goal is to manage infrastructure through Terraform, the current setup primarily uses `gcloud CLI` commands for deploying and managing the Cloud Function.

### Deployment Method

The `product-quality-jira-processor` Cloud Function is deployed using a shell script that wraps `gcloud functions deploy`.

```bash
# cloud_function_jira_processor/deploy.sh
gcloud functions deploy product-quality-jira-processor \
    --gen2 \
    --runtime=python311 \
    --region=us-central1 \
    --source=. \
    --entry-point=process_quality_alert \
    --trigger-topic=product-quality-alerts \
    --memory=512MB \
    --timeout=300s \
    --env-vars-file=.env.yaml \
    --service-account=sada-joseph-shorter-sada@appspot.gserviceaccount.com \
    --retry # Added for automatic retry
```

### Configuration Files

Environment variables for the Cloud Function are defined in `.env.yaml` and passed during deployment.

```yaml
# cloud_function_jira_processor/.env.yaml
JIRA_PROJECT_ID: "AITD"
JIRA_ISSUE_TYPE: "Task"
JIRA_SERVER: "https://sadaadvservices.atlassian.net"
USER_EMAIL: "joseph.shorter@sada.com"
GOOGLE_CLOUD_PROJECT: "sada-joseph-shorter-sada"
```

-----

## 4. Network Overview

The `product-quality-jira-processor` is deployed as a Google Cloud Function. For Cloud Functions, much of the underlying network infrastructure (VPC, subnets, NAT) is managed by Google.

*   **Cloud Function Connectivity:** The Cloud Function receives messages via a Pub/Sub push subscription and makes outbound calls to the external JIRA API.
*   **Outbound Internet Access:** Cloud Functions have default internet egress. If specific static egress IPs were required (e.g., for allow-listing by 3rd party APIs), a Serverless VPC Access connector combined with Cloud NAT would be implemented in a custom VPC.
*   **Private Service Networking (Future Consideration):** Should this function need to connect to other private Google-managed services (e.g., Cloud SQL, Memorystore) within a private subnet, a Serverless VPC Access connector would be configured to allow private IP connectivity.

-----

## 5. Configuration Management

We separate **Infrastructure Config** (e.g., Cloud Function memory, timeout) from **Application Config** (API Keys, JIRA settings).

### Environment Variables (`.env.yaml`)

Used for non-sensitive application settings passed to the Cloud Function.

```yaml
# cloud_function_jira_processor/.env.yaml
JIRA_PROJECT_ID: "AITD"
JIRA_ISSUE_TYPE: "Task"
JIRA_SERVER: "https://sadaadvservices.atlassian.net"
USER_EMAIL: "joseph.shorter@sada.com"
GOOGLE_CLOUD_PROJECT: "sada-joseph-shorter-sada"
```

### Secret Management

Sensitive data, such as API keys, is stored and injected at runtime via **Google Secret Manager**.

*   **Example Secret:** The `JIRA_API_KEY` is stored in Secret Manager.
*   **Secret ID:** `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`

To reference a secret in the Cloud Function:

```python
# cloud_function_jira_processor/main.py
from google.cloud import secretmanager

def access_secret_version(secret_id: str) -> str:
    """Access a secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_id})
    return response.payload.data.decode("UTF-8")

# ... later in the code ...
JIRA_API_KEY = access_secret_version("projects/900228280944/secrets/JIRA_API_KEY/versions/latest")
```

-----

## 6. IAM & Security Policies

We adhere to the **Principle of Least Privilege** for all service accounts.

### Service Accounts (SA)

*   **Cloud Function Service Account:**
    The `product-quality-jira-processor` Cloud Function runs as `sada-joseph-shorter-sada@appspot.gserviceaccount.com`. While this is the default App Engine service account, its permissions have been explicitly granted and restricted to only what's necessary:
    *   `roles/pubsub.subscriber` (to receive messages from the topic)
    *   `roles/secretmanager.secretAccessor` (to access the `JIRA_API_KEY`)
    *   Other implicit Cloud Function runner permissions.

*   **Pub/Sub Service Account:**
    For Pub/Sub to push messages to the Cloud Function, the Google-managed Pub/Sub service account `service-900228280944@gcp-sa-pubsub.iam.gserviceaccount.com` has been granted `roles/run.invoker` on the Cloud Function.

### Organization Policies

The following constraints are enforced at the Organization level (recommended best practices):

*   `iam.disableServiceAccountKeyCreation`: Prevents download of `.json` key files (Use Workload Identity or Google-managed SAs instead).
*   `storage.uniformBucketLevelAccess`: Enforces IAM on buckets (no ACLs).

-----

## 7. "Day 0" Bootstrapping

Follow these steps only when setting up the GCP project and deploying the function for the first time.

1.  **Enable Required APIs:**
    Ensure the following APIs are enabled in your GCP project:

    ```bash
    gcloud services enable functions.googleapis.com \
                           cloudbuild.googleapis.com \
                           secretmanager.googleapis.com \
                           pubsub.googleapis.com
    ```

2.  **Create Pub/Sub Topic (if not already existing):**
    The `product-quality-alerts` Pub/Sub topic is required. It's often set up by a dedicated script (e.g., `setup-product-quality-pubsub.sh` as mentioned in a README).

    ```bash
    gcloud pubsub topics create product-quality-alerts --project=sada-joseph-shorter-sada
    ```

3.  **Deploy the Cloud Function:**
    Navigate to the `cloud_function_jira_processor` directory and run the deployment script.

    ```bash
    cd cloud_function_jira_processor
    chmod +x deploy.sh
    ./deploy.sh
    ```

    Alternatively, use the manual `gcloud functions deploy` command:
    ```bash
    gcloud functions deploy product-quality-jira-processor \
        --gen2 \
        --runtime=python311 \
        --region=us-central1 \
        --source=. \
        --entry-point=process_quality_alert \
        --trigger-topic=product-quality-alerts \
        --memory=512MB \
        --timeout=300s \
        --env-vars-file=.env.yaml \
        --service-account=sada-joseph-shorter-sada@appspot.gserviceaccount.com \
        --retry
    