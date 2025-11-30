# Infrastructure Setup & Configuration (GCP)

This document details the architectural standards and setup procedures for provisioning the Simple Python Script infrastructure on Google Cloud Platform.

**Philosophy:** We utilize **Immutable Infrastructure**. All resources are provisioned via Terraform. Manual changes in the GCP Console are strictly prohibited (Read-Only Policy), except for emergency break-glass scenarios.

> **Note:** The provided codebase (`addNums.py`) consists of a single Python script and does not define any cloud infrastructure. Therefore, most sections of this guide, which describe Google Cloud Platform and Terraform practices, are not directly applicable to the current codebase but represent our general architectural philosophy for projects that *do* involve cloud infrastructure.

---

## 1. Prerequisites (Local Environment)

For the execution of the provided `addNums.py` script, only a Python interpreter is required.
There is no `.tool-versions` file or equivalent for version management within this codebase.

*   **[Python](https://www.python.org/downloads/):** (v3.x) For executing the Python script.

The script `addNums.py` does not interact with GCP services or require authentication mechanisms like `gcloud auth login`.

---

## 2. Project Topology

The provided codebase (`addNums.py`) is a standalone script and does not include definitions for a multi-project GCP hierarchy or distinct environments (Ops, Staging, Production). The concept of isolated GCP projects for different environments is a standard practice for larger, cloud-deployed applications, but it is not applicable to the current code.

| Environment | GCP Project ID | Purpose | Access Level |
| :--- | :--- | :--- | :--- |
| **Ops / Shared** | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* |
| **Staging** | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* |
| **Production** | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* | *N/A (Not defined in codebase)* |

---

## 3. Infrastructure as Code (Terraform)

The provided codebase (`addNums.py`) does not contain any Infrastructure as Code definitions using Terraform. The project does not include a `/terraform` directory or any `.tf` files.

### Directory Structure

```text
/
  addNums.py
```

### State Management

Since no Terraform configurations are present, there is no Terraform state to manage. The concept of a GCS Backend for state storage is not applicable to this codebase.

---

## 4. Network Configuration

The `addNums.py` script is a local execution script and does not define or interact with any network infrastructure such as Virtual Private Cloud (VPC), Subnets, Cloud NAT, or Private Service Connect for database access. These networking components are crucial for cloud-deployed applications but are not relevant to the standalone script.

> [\!WARNING]
> The Web3 note regarding JSON-RPC port restrictions is specific to cloud deployments with RPC nodes and is not applicable to this codebase.

---

## 5. Configuration Management

The `addNums.py` script does not utilize formal configuration management systems like Terraform variables (`.tfvars`) or Google Secret Manager.

### Terraform Variables (`.tfvars`)

No Terraform configurations are present, thus `.tfvars` files are not used.

### Secret Management

The script includes a hardcoded `correlation_ID`: `correlation_ID ="41131d34-334c-488a-bce2-a7642b27cf35"`. While this is a configuration item, it is hardcoded directly in the source file, which is not aligned with best practices for sensitive data or dynamic configuration.

There is no integration with Google Secret Manager or any other secret management solution within the provided code. For cloud-native applications, sensitive data should be externalized and managed securely, such as through Google Secret Manager.

---

## 6. IAM & Security Policies

The `addNums.py` script does not define or interact with Identity and Access Management (IAM) roles, Service Accounts (SA), or Google Cloud Organization Policies. These security mechanisms are fundamental for controlling access and enforcing compliance in a GCP environment but are not part of a simple Python script.

*   **Service Accounts (SA):** Not applicable as the script runs locally.
*   **Organization Policies:** Not applicable as no GCP organization policies are defined or enforced by the script.

---

## 7. "Day 0" Bootstrapping

The "Day 0" bootstrapping steps provided in the template are for initializing a GCP environment for cloud-deployed applications using Terraform. These steps are not applicable to the `addNums.py` script, which is executed locally.

To "bootstrap" and run the provided script:

1.  **Ensure Python is installed.**
2.  **Execute the script:**
    ```bash
    python addNums.py
    ```
    The script contains an example of calling `add_two_numbers` that will produce log output.

---

## 8. Database Initialization

The `addNums.py` script does not interact with any database, including Cloud SQL. Therefore, steps for database initialization, connection via proxy, or running migrations are not applicable to this codebase.