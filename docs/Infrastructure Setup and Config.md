# Infrastructure Setup & Configuration (GCP)

This document details the architectural standards and setup procedures for provisioning the Product Quality Alert System infrastructure on Google Cloud Platform.

**Philosophy:** We utilize **Immutable Infrastructure**. All resources are provisioned via Infrastructure as Code (IaC). Manual changes in the GCP Console are strictly prohibited (Read-Only Policy), except for emergency break-glass scenarios. While application components (like Cloud Functions) may use direct deployment scripts, the underlying infrastructure should follow IaC principles.

---

## 1. Prerequisites (Local Environment)

Before interacting with the infrastructure, ensure your local machine is configured with the following tools. For specific tool versions, refer to `.tool-versions` if present (not provided in this codebase).

*   **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install):** For authentication, direct API interaction, and deploying Cloud Functions.
*   **[Terraform](https://www.terraform.io/):** (v1.5.0+) For provisioning underlying infrastructure resources, adhering to IaC principles.
*   **[Docker](https://www.docker.com/):** For building container images locally (e.g., if Cloud Run or GKE were used).

**Initial Auth**
```bash
gcloud auth login
gcloud auth application-default login
```

-----

## 2. Project Topology

For a comprehensive environment, a multi-project hierarchy is recommended to ensure strict isolation between environments. For the Product Quality Alert System, the primary operational project is `sada-joseph-shorter-sada`.

| Environment | GCP Project ID | Purpose | Access Level |
| :--- | :--- | :--- | :--- |
| **Ops / Shared** | `project-ops-core` | Terraform State, Artifact Registry, CI/CD runners. | DevOps Lead Only |
| **Development** | `sada-joseph-shorter-sada` | Core project for product quality alert system components (Cloud Function, Pub/Sub, Secret Manager). | Developers (Editor) |
| **Staging** | `project-staging` | Mirror of production for QA and Integration testing. | Developers (Editor) |
| **Production** | `project-prod` | Live traffic. | Read-Only (CI/CD Deployer) |

-----

## 3. Infrastructure as Code (IaC)

Our architectural standard emphasizes IaC using Terraform for provisioning and managing core infrastructure. While some application-level deployments (e.g., Cloud Functions) may be handled via `gcloud` scripting, the underlying network, IAM, and shared services should be defined in Terraform.

### Terraform Philosophy

Our Terraform configuration is modularized, discouraging monolithic `main.tf` files.
*Note: This specific codebase does not contain Terraform files for the demonstrated components, which are deployed using `gcloud` commands.*

### State Management (Architectural Standard)

We use a **GCS Backend** to store the Terraform state file. This ensures locking prevents two developers from applying changes simultaneously.
*Note: For the provided Cloud Function example, explicit Terraform state management is not demonstrated as the deployment uses `gcloud` commands.*

```hcl
// Example for a project using Terraform
terraform {
  backend "gcs" {
    bucket  = "insight-terraform-state-dev" // Adapt for sada-joseph-shorter-sada
    prefix  = "terraform/state"
  }
}
```

-----

## 4. Network Configuration (Architectural Standard)

### Virtual Private Cloud (VPC)

*   **Custom Mode:** We do not use the "default" VPC.
*   **Subnets:** Private subnets for resources; Public subnets only for Load Balancers.

### Cloud NAT

Resources in private subnets (e.g., Cloud Run connectors or internal Cloud Functions) reach the internet via Cloud NAT to ensure a static egress IP (useful for allow-listing our API with 3rd party providers, though not explicitly required for this JIRA integration).

### Database Access (Private Service Connect)

**Cloud SQL** is not exposed to the public internet. Access is granted only via:

1.  **VPC Peering / Private Service Access:** For internal services.
2.  **IAP (Identity-Aware Proxy):** For developer access (bastion host).

> \[!WARNING]
> **Web3 Note:** If running a self-hosted RPC node, ensure the JSON-RPC port (8545) is firewall-restricted to internal VPC traffic only.

-----

## 5. Configuration Management

We separate **Infrastructure Config** (Machine types, Regions) from **Application Config** (API Keys, Secrets).

### Cloud Function Environment Variables (`.env.yaml`)

Used for non-sensitive configuration settings specific to the Cloud Function, injected during deployment.

```yaml
# cloud_function_jira_processor/.env.yaml
JIRA_PROJECT_ID: "AITD"
JIRA_ISSUE_TYPE: "Task"
JIRA_SERVER: "https://sadaadvservices.atlassian.net"
USER_EMAIL: "joseph.shorter@sada.com"
GOOGLE_CLOUD_PROJECT: "sada-joseph-shorter-sada"
```

### Secret Management

Sensitive data like the JIRA API key is injected at runtime via **Google Secret Manager**.

*   **Naming Convention:** Follow a clear convention, e.g., `[SERVICE_NAME]_[SECRET_KEY]_[ENV]`.
*   **Example:** The JIRA API key is stored as `JIRA_API_KEY`.

To reference a secret in the Cloud Function:

```python
# cloud_function_jira_processor/main.py
from google.cloud import secretmanager

def access_secret_version(secret_id: str) -> str:
    """Access a secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_id})
    return response.payload.data.decode("UTF-8")

# In create_product_quality_ticket function:
JIRA_API_KEY = access_secret_version("projects/900228280944/secrets/JIRA_API_KEY/versions/latest")
```

-----

## 6. IAM & Security Policies

We adhere to the **Principle of Least Privilege**.

### Service Accounts (SA)

Each application service runs as its own SA. While the provided Cloud Function uses the default App Engine service account, architectural best practice is to create dedicated, granular service accounts.

*   **Bad (Example from Codebase):** Using the "Default App Engine Service Account" (`sada-joseph-shorter-sada@appspot.gserviceaccount.com`) for a specific function.
*   **Good (Architectural Standard):** Creating `sa-product-quality-jira-processor@...` which only has necessary roles.

For the Product Quality Alert system, the following service accounts and permissions are configured:
*   `sada-joseph-shorter-sada@appspot.gserviceaccount.com` (used by the Cloud Function) has:
    *   `roles/pubsub.subscriber` (can receive messages from Pub/Sub)
    *   `roles/secretmanager.secretAccessor` (can access `JIRA_API_KEY` from Secret Manager)
    *   `roles/run.invoker` (if invoking Cloud Run services)
*   `service-900228280944@gcp-sa-pubsub.iam.gserviceaccount.com` (Pub/Sub service account) has:
    *   `roles/run.invoker` (allows Pub/Sub to push messages to the Cloud Function, which runs on Cloud Run infrastructure).

### Organization Policies (Architectural Standard)

The following constraints are enforced at the Organization level:

*   `iam.disableServiceAccountKeyCreation`: Prevents download of `.json` key files (Use Workload Identity instead).
*   `storage.uniformBucketLevelAccess`: Enforces IAM on buckets (no ACLs).

-----

## 7. "Day 0" Bootstrapping

Follow these steps only when creating a new environment from scratch.

1.  **Enable Required APIs:**

    ```bash
    gcloud services enable functions.googleapis.com \
                           cloudbuild.googleapis.com \
                           secretmanager.googleapis.com \
                           pubsub.googleapis.com \
                           run.googleapis.com # Required for Cloud Functions (2nd Gen)
    ```

2.  **Create State Bucket (Architectural Standard):**
    Manually create the GCS bucket for Terraform state (this is the chicken-and-egg problem).
    *Note: This step is for projects managed via Terraform for infrastructure.*

    ```bash
    gsutil mb -l us-central1 gs://sada-joseph-shorter-sada-terraform-state
    gsutil versioning set on gs://sada-joseph-shorter-sada-terraform-state
    ```

3.  **Initialize & Apply (Architectural Standard):**
    *Note: This step is for projects managed via Terraform for infrastructure.*

    ```bash
    cd terraform/environments/[ENV] # Placeholder if Terraform files were present
    terraform init
    terraform plan -out=tfplan
    terraform apply tfplan
    ```

-----

## 8. Database Initialization (Architectural Standard)

After Terraform provisions a Cloud SQL instance (if applicable), the database will be empty. This section is a general architectural standard and not directly applicable to the current Cloud Function, which interacts with JIRA.

1.  **Connect via Proxy:**
    ```bash
    ./cloud_sql_proxy -instances=[CONNECTION_NAME]=tcp:5432
    ```
2.  **Run Migrations:**
    Execute the relevant migration script from the local repository to build the schema.