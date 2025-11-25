# Deployment Guide: Product Quality Alert Processor Cloud Function

## 1. Introduction

This document provides comprehensive instructions for deploying, configuring, and maintaining the **Product Quality Alert Processor Cloud Function**. This function is a critical component of the automated product quality alert system, designed to create JIRA tickets immediately upon receiving product quality alerts via a Google Cloud Pub/Sub topic.

The system aims to drastically reduce the time-to-action for critical product quality issues by automating the alert-to-ticket workflow.

### System Flow:

```
Analytics Agent → Pub/Sub Topic → Cloud Function (AUTO) → JIRA Ticket Created
(detects issues)   (queue)         (triggers instantly)    (< 5 seconds)
```

**Key Capabilities:**

*   **Real-time Processing:** Processes alerts within seconds of publication to Pub/Sub.
*   **Automated JIRA Creation:** Automatically generates detailed JIRA tickets, including product metrics, financial impact, and recommended actions.
*   **Resilience:** Configured for automatic retries of transient errors (e.g., JIRA unavailability) using Pub/Sub's built-in retry mechanisms and the Cloud Function's `--retry` flag.
*   **Secure Credential Handling:** Utilizes Google Secret Manager for sensitive JIRA API keys.

## 2. Prerequisites

Before proceeding with the deployment, ensure the following prerequisites are met:

*   **Google Cloud SDK Installed and Authenticated:**
    ```bash
    gcloud auth login
    gcloud config set project sada-joseph-shorter-sada
    ```
*   **Required Google Cloud APIs Enabled:**
    *   Cloud Functions API
    *   Cloud Build API
    *   Secret Manager API
    *   Pub/Sub API
    *   You can enable these via the GCP Console or `gcloud services enable <API_NAME>.googleapis.com`.
*   **JIRA API Key in Secret Manager:**
    *   A JIRA API key must be stored in Google Secret Manager. The function expects it at: `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`.
*   **Pub/Sub Topic Created:**
    *   A Pub/Sub topic named `product-quality-alerts` must exist. This is typically set up via `setup-product-quality-pubsub.sh` or similar automation.
*   **Source Code:**
    *   You must have the `cloud_function_jira_processor` directory from the codebase. The deployment assumes this directory is your current working directory for local deployment.

## 3. Deployment Steps

The Cloud Function can be deployed using an automated script or manually via `gcloud` commands.

### 3.1. Automated Deployment (Recommended)

Navigate to the Cloud Function's directory and execute the deployment script:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor # Adjust path as needed
chmod +x deploy.sh
./deploy.sh
```

The `deploy.sh` script orchestrates the `gcloud functions deploy` command with all necessary parameters, ensuring consistency and including the `--retry` flag for enhanced resilience.

### 3.2. Manual Deployment

If you prefer to deploy manually or need to customize parameters, use the `gcloud functions deploy` command directly:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor # Adjust path as needed

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
    --retry # Enable automatic retry for transient errors
```

**Explanation of Flags:**

*   `product-quality-jira-processor`: The unique name for the Cloud Function.
*   `--gen2`: Specifies a 2nd generation Cloud Function, offering enhanced capabilities and integrations.
*   `--runtime=python311`: Sets the execution environment to Python 3.11.
*   `--region=us-central1`: Deploys the function to the `us-central1` region.
*   `--source=.`: Specifies that the source code is in the current directory.
*   `--entry-point=process_quality_alert`: Defines the function within `main.py` that will be executed when triggered.
*   `--trigger-topic=product-quality-alerts`: Configures the function to trigger upon messages published to the `product-quality-alerts` Pub/Sub topic.
*   `--memory=512MB`: Allocates 512MB of memory for the function instance. This is generally sufficient for JIRA API calls.
*   `--timeout=300s`: Sets the maximum execution time to 300 seconds (5 minutes).
*   `--env-vars-file=.env.yaml`: Loads environment variables from the specified `.env.yaml` file.
*   `--service-account=sada-joseph-shorter-sada@appspot.gserviceaccount.com`: Assigns a specific service account to the function, which must have necessary permissions (e.g., `roles/secretmanager.secretAccessor` for JIRA API key, `roles/run.invoker` for internal calls, etc.).
*   `--retry`: Crucially enables automatic retries for failed executions, which is essential for handling transient issues like JIRA service unavailability.

## 4. Configuration

The Cloud Function's behavior is configured primarily through environment variables and function settings.

### 4.1. Environment Variables (`.env.yaml`)

The `cloud_function_jira_processor/.env.yaml` file defines key configuration parameters:

| Variable             | Value                                 | Description                                                         |
| :------------------- | :------------------------------------ | :------------------------------------------------------------------ |
| `JIRA_PROJECT_ID`    | `AITD`                                | The JIRA project key where tickets will be created.                 |
| `JIRA_ISSUE_TYPE`    | `Task`                                | The default type of JIRA issue to create (e.g., Task, Bug, Story).  |
| `JIRA_SERVER`        | `https://sadaadvservices.atlassian.net` | The base URL of the JIRA instance.                                  |
| `USER_EMAIL`         | `joseph.shorter@sada.com`             | The email address associated with the JIRA API key for authentication. |
| `GOOGLE_CLOUD_PROJECT` | `sada-joseph-shorter-sada`            | The Google Cloud project ID where the function is deployed.         |

### 4.2. JIRA API Key

The JIRA API key is securely retrieved from Google Secret Manager during function execution. It is NOT stored in environment variables or directly in the codebase.
**Secret ID:** `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`

### 4.3. Function Settings

*   **Memory:** 512MB (sufficient for JIRA API calls and processing)
*   **Timeout:** 300s (5 minutes maximum execution duration)
*   **Concurrency:** Up to 10 instances (can process 10 alerts simultaneously)
*   **Min Instances:** 0 (scales to zero when idle, minimizing costs)

## 5. Verification & Testing

After deployment, it's crucial to verify the function's correct operation.

### 5.1. Check JIRA Status (Pre-test or Troubleshooting)

Before testing the function itself, ensure the JIRA service is online and accessible. The `test_jira_status.py` script can be used for this:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor # Adjust path as needed
python test_jira_status.py
```

**Expected output when JIRA is back:**
```
✅ JIRA is ONLINE and credentials are VALID
```

### 5.2. Publish Test Alerts

Simulate an alert by publishing a message to the `product-quality-alerts` Pub/Sub topic using the analytical agent:

```bash
cd /Users/joseph.shorter/repos/m_analytical_demo # Adjust path as needed
source ../.venv/bin/activate # Activate your Python virtual environment if applicable

python -c "from agent import detect_product_quality_issues, publish_product_alert; \
           import json; \
           issues = detect_product_quality_issues(7, 'high'); \
           data = json.loads(issues); \
           print(f'Detected {data[\"issues_found\"]} issues'); \
           result = publish_product_alert(issues); \
           print(result)"
```

This command will detect high-severity product quality issues and publish them to the configured Pub/Sub topic, triggering the Cloud Function.

### 5.3. Watch the Function Logs (Real-time)

Monitor the function's execution logs in real-time to confirm it receives and processes the messages:

```bash
gcloud functions logs read product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --limit=50 \
    --format="value(severity,log)"
```

You should see log entries similar to:
```
INFO: 📨 Received alert from Pub/Sub (Message ID: ...)
INFO: 🔍 Processing: Fisher-Price Code-a-Pillar (ID: ..., Severity: HIGH, Revenue at Risk: $13,082.00)
INFO: ✅ JIRA ticket created: AITD-XXX for Fisher-Price Code-a-Pillar (severity: HIGH)
INFO:    URL: https://sadaadvservices.atlassian.net/browse/AITD-XXX
INFO:    Product ID: ..., Revenue at Risk: $13,082.00
```

### 5.4. Verify JIRA Tickets

Finally, check your JIRA project to confirm that new tickets have been created as expected:
*   [https://sadaadvservices.atlassian.net/browse/AITD](https://sadaadvservices.atlassian.net/browse/AITD)

## 6. Monitoring

Continuous monitoring is essential to ensure the Cloud Function operates correctly and to detect any issues proactively.

### 6.1. View Recent Executions and Details

*   **View Recent Logs:**
    ```bash
    gcloud functions logs read product-quality-jira-processor \
        --region=us-central1 \
        --gen2 \
        --limit=100
    ```
*   **View Function Configuration and Status:**
    ```bash
    gcloud functions describe product-quality-jira-processor \
        --region=us-central1 \
        --gen2
    ```

### 6.2. Check Error Rate

To identify and investigate errors, filter the logs for entries with `ERROR` severity:

```bash
gcloud logging read "resource.type=cloud_function \
    AND resource.labels.function_name=product-quality-jira-processor \
    AND severity>=ERROR" \
    --limit=20 \
    --format=json
```

### 6.3. Monitor Pub/Sub Subscription

Check the Pub/Sub subscription for any undelivered messages, which might indicate issues with the Cloud Function processing.

*   **Check messages waiting in queue:**
    ```bash
    gcloud pubsub subscriptions describe \
      eventarc-us-central1-product-quality-jira-processor-612217-sub-916 \
      --project=sada-joseph-shorter-sada
    ```
*   **View subscription metrics (e.g., `num_undelivered_messages`):**
    ```bash
    gcloud monitoring time-series list \
      --filter='metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages"' \
      --project=sada-joseph-shorter-sada
    ```

## 7. Troubleshooting

### 7.1. Function Not Triggering?

*   **Check if topic exists:**
    ```bash
    gcloud pubsub topics describe product-quality-alerts
    ```
*   **Check function status:**
    ```bash
    gcloud functions describe product-quality-jira-processor --region=us-central1 --gen2
    ```
*   **Verify Eventarc trigger:** Ensure the Eventarc trigger is correctly configured and pointing to the Pub/Sub topic.

### 7.2. JIRA Tickets Not Created?

*   **Check function logs for errors:**
    ```bash
    gcloud functions logs read product-quality-jira-processor \
        --region=us-central1 \
        --gen2 \
        --limit=20 \
        --filter="severity>=WARNING"
    ```
    Look for messages indicating JIRA API errors, authentication failures, or transient issues.
*   **Test Secret Manager access:** Ensure the service account has permission to access the JIRA API key.
    ```bash
    gcloud secrets versions access latest --secret=JIRA_API_KEY --project=sada-joseph-shorter-sada
    ```
*   **JIRA Service Unavailable:** If JIRA is returning 404s or "Site temporarily unavailable" (as noted in `PRODUCT_QUALITY_ALERT_STATUS.md`), the function will log errors and Pub/Sub will retry the messages with exponential backoff. Use `test_jira_status.py` to confirm JIRA's status.

### 7.3. High Error Rate?

*   **Review environment variables:** Ensure all JIRA-related environment variables are correctly set and match your JIRA instance's configuration.
    ```bash
    gcloud functions describe product-quality-jira-processor \
        --region=us-central1 \
        --gen2 \
        --format="value(serviceConfig.environmentVariables)"
    ```
*   **Check Pub/Sub message format:** If `json.JSONDecodeError` appears, the incoming Pub/Sub messages might be malformed. The function will acknowledge these to prevent infinite retries.

### 7.4. Retry Behavior (JIRA Unavailability)

The function is designed with resilience in mind. If JIRA is temporarily unavailable (e.g., HTTP 404, 502, 503 errors, or connection timeouts), the function will explicitly `raise` an exception. This signals Pub/Sub to:
*   **Retain Messages:** Pub/Sub retains messages for up to 7 days by default.
*   **Retry Schedule:** Messages will be retried with exponential backoff:
    *   Initial retry: 10 seconds after failure.
    *   Exponential backoff up to 600 seconds (10 minutes).
    *   Continues retrying until success or message expiration.
*   **Automatic Recovery:** Once JIRA comes back online, the system will automatically process the queued messages and create tickets without manual intervention.

## 8. Updating the Function

To deploy updates to the Cloud Function after making code changes:

1.  Navigate to the `cloud_function_jira_processor` directory.
2.  Execute the deployment script again:
    ```bash
    cd /Users/joseph.shorter/repos/cloud_function_jira_processor # Adjust path
    ./deploy.sh
    ```
    Alternatively, use the manual `gcloud functions deploy` command.

The deployment process typically takes 2-3 minutes. Google Cloud Functions performs a rolling update, meaning the new version will be deployed without any downtime for the function.

## 9. Cost Estimate

The expected operational cost for this Cloud Function is **very low**, often falling within Google Cloud's free tier limits.

*   **Function Invocations:** Google Cloud provides 2 million free invocations per month. Typical usage for this function (e.g., 1,000 alerts/month) is well within this limit.
*   **Compute Time:** 400K GB-seconds of compute time are free per month. With an execution time of 3-5 seconds per alert and 512MB memory, typical usage will be negligible (e.g., ~100 GB-seconds/month).
*   **Pub/Sub:** 10 GB of message throughput is free per month. Alert messages are small, so usage will be minimal (< 1 MB/month).

**Estimated monthly cost: $0.00** (within free tier for typical workloads).

## 10. Security Considerations

*   **Secret Management:** The JIRA API key is securely stored in Google Secret Manager and accessed via a service account, preventing sensitive credentials from being hardcoded or exposed in source control or environment variables.
*   **Least Privilege:** The associated service account (`sada-joseph-shorter-sada@appspot.gserviceaccount.com`) should be configured with the principle of least privilege, granting only the necessary IAM roles (e.g., `roles/secretmanager.secretAccessor`, `roles/run.invoker`, `roles/pubsub.subscriber`).
*   **Cloud Run Security:** As a Gen2 Cloud Function, it leverages Cloud Run's secure infrastructure, which requires authentication for invocation.
*   **No Credentials in Source Control:** No sensitive credentials are committed to the codebase.

## 11. Resources

*   [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
*   [Pub/Sub Triggers for Cloud Functions](https://cloud.google.com/functions/docs/calling/pubsub)
*   [Google Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
*   [JIRA Python Library Documentation](https://jira.readthedocs.io/)