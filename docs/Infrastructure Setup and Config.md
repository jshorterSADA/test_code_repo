# Infrastructure Setup & Configuration (GCP)

This document outlines the architectural standards and setup procedures for provisioning infrastructure on Google Cloud Platform. However, based on the provided codebase (`addNums.py`), it is important to note that the code is an application-level Python script and **does not contain any infrastructure definition or configuration details**. Therefore, the sections below largely reflect the *intended* architectural approach for infrastructure, rather than specifics derived from the current codebase.

**Philosophy:** While the provided codebase is an application script, our general philosophy for infrastructure is to utilize **Immutable Infrastructure**. All resources are provisioned via Terraform. Manual changes in the GCP Console are strictly prohibited (Read-Only Policy), except for emergency break-glass scenarios. This script itself does not interact with or define such infrastructure.

---

## 1. Prerequisites (Local Environment)

To run the provided `addNums.py` script, only a Python 3 environment is required.

For managing the intended infrastructure (which the `addNums.py` script does not define), the following tools would typically be required, with versions as defined in `.tool-versions` for an IaC project:

*   **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install):** For authentication and direct API interaction with GCP.
*   **[Terraform](https://www.terraform.io/):** (v1.5.0+) For infrastructure provisioning.
*   **[Docker](https://www.docker.com/):** For building container images locally, if the application were to be containerized.

**Initial Auth (for infrastructure management, not for `addNums.py`):**
```bash
gcloud auth login
gcloud auth application-default login
```

-----

## 2. Project Topology

The `addNums.py` script does not define or interact with any GCP project topology. For projects requiring infrastructure, a multi-project hierarchy is typically utilized to ensure strict isolation between environments:

| Environment | GCP Project ID | Purpose | Access Level |
| :--- | :--- | :--- | :--- |
| **Ops / Shared** | `project-ops-core` | Terraform State, Artifact Registry, CI/CD runners. | DevOps Lead Only |
| **Staging** | `project-staging` | Mirror of production for QA and Integration testing. | Developers (Editor) |
| **Production** | `project-prod` | Live traffic. | Read-Only (CI/CD Deployer) |

-----

## 3. Infrastructure as Code (Terraform)

The provided `addNums.py` is a Python script and is not written using Terraform. Therefore, this section does not apply to the codebase itself.

### Directory Structure

An infrastructure project would typically follow a modularized Terraform configuration, like so:

```text
/terraform
  /modules
    /networking      # VPC, Subnets, Firewalls
    /cloud-run       # Service definitions
    /database        # Cloud SQL & Redis instances
  /environments
    /staging         # State: bucket-staging
    /prod            # State: bucket-prod
```

### State Management

For an IaC project, a **GCS Backend** would be used to store the Terraform state file, ensuring locking and preventing concurrent changes. This is not applicable to `addNums.py`.

```hcl
// terraform/environments/prod/backend.tf
terraform {
  backend "gcs" {
    bucket  = "insight-terraform-state-prod"
    prefix  = "terraform/state"
  }
}
```

-----

## 4. Network Configuration

The `addNums.py` script does not define or configure any network resources. In an infrastructure context, network configuration would adhere to the following principles:

### Virtual Private Cloud (VPC)

*   **Custom Mode:** Custom VPCs are used instead of the "default" VPC.
*   **Subnets:** Private subnets for resources; Public subnets only for Load Balancers.

### Cloud NAT

Resources in private subnets would reach the internet via Cloud NAT to ensure a static egress IP.

### Database Access (Private Service Connect)

If a database were present, Cloud SQL would not be exposed to the public internet. Access would be granted only via:

1.  **VPC Peering:** For internal services (e.g., Cloud Run).
2.  **IAP (Identity-Aware Proxy):** For developer access (bastion host).

> \[!WARNING]
> **Web3 Note:** If running a self-hosted RPC node, ensure the JSON-RPC port (8545) is firewall-restricted to internal VPC traffic only.

-----

## 5. Configuration Management

The `addNums.py` script contains its own internal application configuration, such as a hardcoded `correlation_ID` and `logging.basicConfig` settings for output format. This is distinct from infrastructure configuration.

### Terraform Variables (`.tfvars`)

Not applicable to `addNums.py`. For infrastructure, non-sensitive settings are managed via Terraform variables.

```hcl
// prod.tfvars
region          = "us-central1"
machine_type    = "db-custom-2-3840"
min_instances   = 2
```

### Secret Management

Not applicable to `addNums.py` as it handles no sensitive data. For infrastructure, sensitive data is injected at runtime via **Google Secret Manager**.

*   **Naming Convention:** `[SERVICE_NAME]_[SECRET_KEY]_[ENV]`
*   **Example:** `backend_web3_provider_key_prod`

To reference a secret in Terraform (without exposing the value):

```hcl
resource "google_cloud_run_service" "api" {
  template {
    spec {
      containers {
        env {
          name = "WEB3_PROVIDER_KEY"
          value_from {
            secret_key_ref {
              name = "backend_web3_provider_key_prod"
              key  = "latest"
            }
          }
        }
      }
    }
  }
}
```

-----

## 6. IAM & Security Policies

The `addNums.py` script does not define any IAM roles or security policies. For an infrastructure project, the **Principle of Least Privilege** is strictly adhered to.

### Service Accounts (SA)

Each application service would run as its own dedicated Service Account.

*   **Bad:** Using the "Default Compute Engine Service Account".
*   **Good:** Creating `sa-backend-api@...` which only has `Cloud SQL Client` and `Secret Accessor` roles.

### Organization Policies

Organization-level policies, if applied, would enforce constraints such as:

*   `iam.disableServiceAccountKeyCreation`: Prevents download of `.json` key files (relying on Workload Identity instead).
*   `storage.uniformBucketLevelAccess`: Enforces IAM on buckets (no ACLs).

-----

## 7. "Day 0" Bootstrapping

These steps are for creating a new GCP environment from scratch using Terraform and are not applicable to the `addNums.py` script.

1.  **Enable Required APIs:**

    ```bash
    gcloud services enable compute.googleapis.com \
                           run.googleapis.com \
                           sqladmin.googleapis.com \
                           secretmanager.googleapis.com
    ```

2.  **Create State Bucket:**
    Manually create the GCS bucket for Terraform state (this is the chicken-and-egg problem).

    ```bash
    gsutil mb -l us-central1 gs://insight-terraform-state-[ENV]
    gsutil versioning set on gs://insight-terraform-state-[ENV]
    ```

3.  **Initialize & Apply:**

    ```bash
    cd terraform/environments/[ENV]
    terraform init
    terraform plan -out=tfplan
    terraform apply tfplan
    ```

-----

## 8. Database Initialization

The `addNums.py` script does not interact with a database. If a database were provisioned by Terraform, the following steps would be taken to initialize it:

1.  **Connect via Proxy:**
    ```bash
    ./cloud_sql_proxy -instances=[CONNECTION_NAME]=tcp:5432
    ```
2.  **Run Migrations:**
    Execute migration scripts (e.g., TypeORM/Prisma) from the local repository to build the schema.