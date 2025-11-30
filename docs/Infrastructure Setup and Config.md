# Infrastructure Setup & Configuration (GCP)

This document details the architectural standards and setup procedures for provisioning the provided codebase's infrastructure on Google Cloud Platform.

**Philosophy:** We utilize **Immutable Infrastructure**. All resources are provisioned via Terraform. Manual changes in the GCP Console are strictly prohibited (Read-Only Policy), except for emergency break-glass scenarios.

**Note on Codebase:** The provided codebase, `addNums.py`, consists solely of a Python script for adding numbers and logging. It does not contain any infrastructure definition files (e.g., Terraform, Dockerfiles, GCP configurations). Therefore, the following sections will primarily outline the theoretical infrastructure setup based on the template, noting the absence of these elements in the current code.

---

## 1. Prerequisites (Local Environment)

For a typical GCP project utilizing Infrastructure as Code, your local machine would be configured with the specific tool versions defined in `.tool-versions`. However, the provided `addNums.py` file does not require these tools directly for execution. For any potential future deployment to GCP, these would be essential:

*   **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install):** For authentication and direct API interaction with GCP.
*   **[Terraform](https://www.terraform.io/):** (v1.5.0+) For infrastructure provisioning.
*   **[Docker](https://www.docker.com/):** For building container images locally if `addNums.py` were to be containerized (e.g., for Cloud Run).

**Initial Auth**
```bash
gcloud auth login
gcloud auth application-default login
```
*(No specific authentication is required by `addNums.py` itself, but this is standard for GCP interaction.)*

-----

## 2. Project Topology

The provided `addNums.py` file does not define or imply any GCP project topology. In a typical project, a multi-project hierarchy would be used to ensure strict isolation between environments:

| Environment | GCP Project ID | Purpose | Access Level |
| :--- | :--- | :--- | :--- |
| **Ops / Shared** | `project-ops-core` | Terraform State, Artifact Registry, CI/CD runners. | DevOps Lead Only |
| **Staging** | `project-staging` | Mirror of production for QA and Integration testing. | Developers (Editor) |
| **Production** | `project-prod` | Live traffic. | Read-Only (CI/CD Deployer) |

-----

## 3. Infrastructure as Code (Terraform)

The `addNums.py` codebase does not contain any Infrastructure as Code definitions. If this Python script were part of a larger project, its infrastructure would be defined using Terraform. Our Terraform configuration would be modularized, avoiding monolithic `main.tf` files.

### Directory Structure

```text
/terraform
  /modules
    /networking      # VPC, Subnets, Firewalls
    /cloud-run       # Service definitions (if addNums.py were deployed as a Cloud Run service)
    /database        # Cloud SQL & Redis instances (not relevant for addNums.py)
  /environments
    /staging         # State: bucket-staging
    /prod            # State: bucket-prod
```

### State Management

For any Terraform-managed infrastructure, a **GCS Backend** would be used to store the Terraform state file, ensuring locking and collaborative development.

```hcl
// terraform/environments/prod/backend.tf
terraform {
  backend "gcs" {
    bucket  = "insight-terraform-state-prod" # Example bucket
    prefix  = "terraform/state"
  }
}
```
*(As no Terraform is present, this is a conceptual example.)*

-----

## 4. Network Configuration

The `addNums.py` file does not contain any network configuration. If this Python application were deployed to GCP, it would adhere to the following network standards:

### Virtual Private Cloud (VPC)

*   **Custom Mode:** We do not use the "default" VPC.
*   **Subnets:** Private subnets for resources; Public subnets only for Load Balancers.

### Cloud NAT

Resources in private subnets (e.g., Cloud Run connectors, if `addNums.py` were containerized) would reach the internet via Cloud NAT to ensure a static egress IP.

### Database Access (Private Service Connect)

**Cloud SQL** is not exposed to the public internet. Access would be granted only via:

1.  **VPC Peering:** For internal services.
2.  **IAP (Identity-Aware Proxy):** For developer access (bastion host).

> [!WARNING]
> The `addNums.py` script itself does not interact with databases, thus this section is purely hypothetical for a broader project context.

-----

## 5. Configuration Management

The `addNums.py` script manages a `correlation_ID` variable and uses Python's `logging.basicConfig` for its application-level configuration. For infrastructure and sensitive data, we separate **Infrastructure Config** (Machine types, Regions) from **Application Config** (API Keys, Secrets).

### Terraform Variables (`.tfvars`)

Used for non-sensitive infrastructure settings (not applicable to `addNums.py`).

```hcl
// prod.tfvars
region          = "us-central1"
machine_type    = "e2-medium" # Example for a compute resource
min_instances   = 1           # Example for a scalable service
```

### Secret Management

Sensitive data would be injected at runtime via **Google Secret Manager**. The `correlation_ID` in `addNums.py` is hardcoded, but sensitive application configurations would typically follow this pattern.

*   **Naming Convention:** `[SERVICE_NAME]_[SECRET_KEY]_[ENV]`
*   **Example:** `adder_api_key_prod`

To reference a secret in Terraform (without exposing the value):

```hcl
resource "google_cloud_run_service" "adder_service" {
  # ... other Cloud Run service configuration
  template {
    spec {
      containers {
        env {
          name = "SERVICE_API_KEY"
          value_from {
            secret_key_ref {
              name = "adder_api_key_prod" # Example secret for addNums.py if it needed one
              key  = "latest"
            }
          }
        }
      }
    }
  }
}
```
*(This is a conceptual example, as `addNums.py` does not use external secrets.)*

-----

## 6. IAM & Security Policies

The `addNums.py` script does not define any IAM or security policies. For any deployed application on GCP, we adhere to the **Principle of Least Privilege**.

### Service Accounts (SA)

Each application service (e.g., if `addNums.py` was deployed as a Cloud Run service) would run as its own SA.

*   **Bad:** Using the "Default Compute Engine Service Account".
*   **Good:** Creating `sa-adder-service@...` which only has the necessary roles.

### Organization Policies

The following constraints are enforced at the Organization level:

*   `iam.disableServiceAccountKeyCreation`: Prevents download of `.json` key files (Use Workload Identity instead).
*   `storage.uniformBucketLevelAccess`: Enforces IAM on buckets (no ACLs).

-----

## 7. "Day 0" Bootstrapping

These steps are for creating a new environment from scratch, assuming the `addNums.py` script would be part of an application requiring GCP resources.

1.  **Enable Required APIs:**
    ```bash
    gcloud services enable run.googleapis.com \
                           logging.googleapis.com \
                           # Add any other APIs needed for Cloud Run, Secret Manager, etc.
    ```
    *(`addNums.py` only uses Python's built-in `logging` and basic arithmetic, so no specific GCP APIs are strictly required by the script itself.)*

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
    *(These steps are theoretical as no Terraform files are provided for `addNums.py`.)*

-----

## 8. Database Initialization

The `addNums.py` script does not interact with any database. This section is purely for illustrative purposes for a project that would include a database.

1.  **Connect via Proxy:**
    ```bash
    ./cloud_sql_proxy -instances=[CONNECTION_NAME]=tcp:5432
    ```
2.  **Run Migrations:**
    Execute the TypeORM/Prisma migration script from the local repository to build the schema.