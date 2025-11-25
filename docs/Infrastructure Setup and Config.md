# Infrastructure Setup & Configuration (GCP)

This document details the architectural standards and setup procedures for provisioning the **Python Utility Service** infrastructure on Google Cloud Platform.

**Philosophy:** We utilize **Immutable Infrastructure**. All resources are provisioned via Terraform. Manual changes in the GCP Console are strictly prohibited (Read-Only Policy), except for emergency break-glass scenarios.

---

## 1. Prerequisites (Local Environment)

Before interacting with the infrastructure, ensure your local machine is configured with the specific tool versions defined in `.tool-versions`.

*   **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install):** For authentication and direct API interaction.
*   **[Terraform](https://www.terraform.io/):** (v1.5.0+) For infrastructure provisioning.
*   **[Docker](https://www.docker.com/):** For building container images locally.

**Note:** The provided `addNums.py` codebase is a simple Python script and does not directly utilize these infrastructure tools. Its local execution only requires a Python interpreter.

**Initial Auth**
```bash
gcloud auth login
gcloud auth application-default login
```

-----

## 2. Project Topology

We utilize a multi-project hierarchy to ensure strict isolation between environments.

The provided `addNums.py` script is application code; its deployment environment and project topology would be defined by a larger infrastructure setup, not within the script itself. These project IDs are placeholders for a typical multi-environment GCP setup that *would* host such an application.

| Environment | GCP Project ID | Purpose | Access Level |
| :--- | :--- | :--- | :--- |
| **Ops / Shared** | `python-utility-ops-core` | Terraform State, Artifact Registry, CI/CD runners. | DevOps Lead Only |
| **Staging** | `python-utility-staging` | Mirror of production for QA and Integration testing. | Developers (Editor) |
| **Production** | `python-utility-prod` | Live traffic. | Read-Only (CI/CD Deployer) |

-----

## 3. Infrastructure as Code (Terraform)

The provided codebase (`addNums.py`) is a standalone Python script and does not contain any Infrastructure as Code (Terraform) definitions. The following describes the standard Terraform structure and practices that would be used to deploy and manage such an application.

Our Terraform configuration is modularized. Do not write monolithic `main.tf` files.

### Directory Structure

```text
/terraform
  /modules
    /networking      # VPC, Subnets, Firewalls
    /cloud-run       # Service definitions for deploying the Python service
    /database        # Cloud SQL & Redis instances (if applicable)
  /environments
    /staging         # State: bucket-staging
    /prod            # State: bucket-prod
```

### State Management

We use a **GCS Backend** to store the Terraform state file. This ensures locking prevents two developers from applying changes simultaneously. This would be configured in a hypothetical Terraform setup for the Python Utility Service.

```hcl
// terraform/environments/prod/backend.tf
terraform {
  backend "gcs" {
    bucket  = "python-utility-terraform-state-prod"
    prefix  = "terraform/state"
  }
}
```

-----

## 4. Network Configuration

The `addNums.py` script is purely business logic and contains no network configuration details. The following outlines a standard network setup for a service that would host such an application on GCP.

### Virtual Private Cloud (VPC)

*   **Custom Mode:** We do not use the "default" VPC.
*   **Subnets:** Private subnets for resources; Public subnets only for Load Balancers.

### Cloud NAT

Resources in private subnets (e.g., Cloud Run connectors) reach the internet via Cloud NAT to ensure a static egress IP (useful for allow-listing our API with 3rd party providers).

### Database Access (Private Service Connect)

**Cloud SQL** is not exposed to the public internet. Access is granted only via:

1.  **VPC Peering:** For internal services (Cloud Run).
2.  **IAP (Identity-Aware Proxy):** For developer access (bastion host).

> [\!WARNING]
> **Web3 Note:** If running a self-hosted RPC node, ensure the JSON-RPC port (8545) is firewall-restricted to internal VPC traffic only.

-----

## 5. Configuration Management

The `addNums.py` script manages configuration through function parameters and a global variable for `correlation_ID`. It does not utilize `.tfvars` for infrastructure settings or Google Secret Manager for sensitive application secrets, as these are typically part of a larger deployment infrastructure. The following outlines how infrastructure and application configuration would be managed in a deployed environment.

We separate **Infrastructure Config** (Machine types, Regions) from **Application Config** (API Keys, Secrets).

### Terraform Variables (`.tfvars`)

Used for non-sensitive infrastructure settings.

```hcl
// prod.tfvars
region          = "us-central1"
machine_type    = "e2-small" // Example for a Python utility
min_instances   = 1
```

### Secret Management

Sensitive data is injected at runtime via **Google Secret Manager**.

*   **Naming Convention:** `[SERVICE_NAME]_[SECRET_KEY]_[ENV]`
*   **Example:** `python_utility_api_key_prod`

To reference a secret in Terraform (without exposing the value), if the Python Utility Service needed one:

```hcl
resource "google_cloud_run_service" "utility" {
  template {
    spec {
      containers {
        env {
          name = "SERVICE_API_KEY"
          value_from {
            secret_key_ref {
              name = "python_utility_api_key_prod"
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

The `addNums.py` script does not define IAM roles or security policies directly. These are configured at the GCP project level to govern the service account under which an application containing this script would run.

We adhere to the **Principle of Least Privilege**.

### Service Accounts (SA)

Each application service runs as its own SA.

*   **Bad:** Using the "Default Compute Engine Service Account".
*   **Good:** Creating `sa-python-utility@...` which only has necessary roles (e.g., `Cloud Run Invoker`, `Secret Accessor` if secrets are used).

### Organization Policies

The following constraints are enforced at the Organization level:

*   `iam.disableServiceAccountKeyCreation`: Prevents download of `.json` key files (Use Workload Identity instead).
*   `storage.uniformBucketLevelAccess`: Enforces IAM on buckets (no ACLs).

-----

## 7. "Day 0" Bootstrapping

These steps are for bootstrapping a new GCP environment using Terraform, which is not present in the `addNums.py` codebase. This section is provided as a reference for a typical infrastructure provisioning process.

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
    gsutil mb -l us-central1 gs://python-utility-terraform-state-[ENV]
    gsutil versioning set on gs://python-utility-terraform-state-[ENV]
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

The `addNums.py` script does not interact with a database. This section is included for completeness, outlining database setup procedures for a typical application that would be deployed within this infrastructure.

After Terraform provisions the Cloud SQL instance, the database will be empty.

1.  **Connect via Proxy:**
    ```bash
    ./cloud_sql_proxy -instances=[CONNECTION_NAME]=tcp:5432
    ```
2.  **Run Migrations:**
    Execute the TypeORM/Prisma migration script from the local repository to build the schema.