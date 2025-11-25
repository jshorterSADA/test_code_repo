# Deployment Guide: Product Quality Alert Processor

This document provides comprehensive instructions and details for deploying, configuring, and maintaining the Product Quality Alert Processor Cloud Function. This function automatically creates JIRA tickets in response to product quality alerts published to a Google Cloud Pub/Sub topic.

## 🚀 What This Does

The Product Quality Alert Processor is a Google Cloud Function designed to process product quality alerts in near real-time, eliminating the need for manual intervention or scheduled batch jobs. Upon receiving an alert via Pub/Sub, the function instantly parses the alert data and creates a corresponding JIRA ticket.

### Flow:
```
Analytics Agent → Pub/Sub Topic → Cloud Function (AUTO) → JIRA Ticket Created
(detects issues)   (queue)         (triggers instantly)    (< 5 seconds)
```

## 📊 System Architecture

The overall system for detecting, publishing, and processing product quality alerts follows this architecture:

```
[BigQuery Analytics] 
        ↓
[detect_product_quality_issues()]
        ↓
[publish_product_alert()]
        ↓
[Pub/Sub Topic: product-quality-alerts]
        ↓
[Push Subscription with Retry]
        ↓
[Cloud Function: product-quality-jira-processor]
        ↓
[JIRA API] → Create Ticket
        ↓
[JIRA Project: AITD]
```

## 📦 Project Structure

The key components for this deployment reside within the `cloud_function_jira_processor` directory:

-   `main.py`: The core Python code for the Cloud Function, handling Pub/Sub message processing and JIRA ticket creation.
-   `requirements.txt`: Specifies Python dependencies required by `main.py`.
-   `.env.yaml`: Contains environment variables for the Cloud Function, such as JIRA configuration details.
-   `deploy.sh`: An executable script for automated deployment of the Cloud Function.
-   `test_jira_status.py`: A utility script to verify JIRA connectivity and credential validity.
-   `README.md`: The original documentation for the Cloud Function (this deployment guide consolidates and expands upon its content).

## 🔧 Prerequisites

Before deploying the Cloud Function, ensure the following prerequisites are met:

1.  **Google Cloud SDK Installed and Authenticated**:
    Ensure you have the `gcloud` command-line tool installed and authenticated with your Google Cloud account.
    ```bash
    gcloud auth login
    gcloud config set project sada-joseph-shorter-sada
    ```

2.  **Required APIs Enabled**:
    The following Google Cloud APIs must be enabled in your project:
    -   Cloud Functions API
    -   Cloud Build API
    -   Secret Manager API
    -   Pub/Sub API

3.  **JIRA API Key in Secret Manager**:
    A JIRA API key must be securely stored in Google Secret Manager. It is already configured at:
    `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`

4.  **Pub/Sub Topic Created**:
    The Pub/Sub topic named `product-quality-alerts` must exist. This topic serves as the trigger for the Cloud Function. It is typically set up via `setup-product-quality-pubsub.sh` (not provided in this codebase, but referenced).

## 🚀 Deployment

The Cloud Function can be deployed using either an automated script or a manual `gcloud` command.

### Option 1: Automated (Recommended)

Navigate to the function's directory and execute the deployment script:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual

Alternatively, you can deploy the function using the `gcloud` command directly:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor

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
    --retry # Enables automatic retry for transient errors
```

The `--retry` flag ensures that the function is configured with automatic retry logic for transient failures, aligning with the resilience built into the function's `main.py` and Pub/Sub's subscription settings.

## 🔧 Configuration

The Cloud Function's behavior is controlled by environment variables and function settings.

### Environment Variables (`.env.yaml`)

The `.env.yaml` file specifies critical JIRA and GCP project details:

| Variable             | Value                                 | Description                                 |
| :------------------- | :------------------------------------ | :------------------------------------------ |
| `JIRA_PROJECT_ID`    | `AITD`                                | The JIRA project key for new tickets        |
| `JIRA_ISSUE_TYPE`    | `Task`                                | The type of JIRA issue to create            |
| `JIRA_SERVER`        | `https://sadaadvservices.atlassian.net` | The base URL of your JIRA instance          |
| `USER_EMAIL`         | `joseph.shorter@sada.com`             | The JIRA user email for authentication      |
| `GOOGLE_CLOUD_PROJECT` | `sada-joseph-shorter-sada`            | The Google Cloud project ID for this deployment |

### Function Settings

The deployment command configures the following resource and operational settings:

-   **Memory:** `512MB` (Sufficient for JIRA API calls and processing).
-   **Timeout:** `300s` (5 minutes maximum execution time per invocation).
-   **Concurrency:** Configured to handle up to 10 simultaneous invocations (processes 10 alerts concurrently).
-   **Min Instances:** `0` (Allows the function to scale to zero when idle, minimizing costs).

## 🧪 Testing

To verify successful deployment and functionality:

### 1. Publish Test Alerts

Use the analytical agent script to detect and publish new alerts:

```bash
cd /Users/joseph.shorter/repos/m_analytical_demo
source ../.venv/bin/activate

python -c "from agent import detect_product_quality_issues, publish_product_alert; \
           import json; \
           issues = detect_product_quality_issues(7, 'high'); \
           data = json.loads(issues); \
           print(f'Detected {data[\"issues_found\"]} issues'); \
           result = publish_product_alert(issues); \
           print(result)"
```

### 2. Watch the Logs (Real-time)

In a separate terminal, monitor the Cloud Function logs:

```bash
gcloud functions logs read product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --limit=50 \
    --format="value(severity,log)"
```

Expected log output for a successful alert processing:

```
📨 Received alert from Pub/Sub
🔍 Processing: Fisher-Price Code-a-Pillar (ID: <product_id>, Severity: HIGH, Revenue at Risk: $13,082.00)
✅ JIRA ticket created: AITD-XXX for Fisher-Price Code-a-Pillar (severity: HIGH)
✅ SUCCESS: Created AITD-XXX for Fisher-Price Code-a-Pillar
   URL: https://sadaadvservices.atlassian.net/browse/AITD-XXX
   Product ID: <product_id>, Revenue at Risk: $13,082.00
```

### 3. Verify JIRA Tickets

Check your configured JIRA project (`AITD` by default) for newly created tickets:
-   [https://sadaadvservices.atlassian.net/browse/AITD](https://sadaadvservices.atlassian.net/browse/AITD)

### 4. Check JIRA Status Utility

The `test_jira_status.py` script can be used to independently verify JIRA connectivity and credential validity:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor
python test_jira_status.py
```

Expected output when JIRA is online and credentials are valid:
```
✅ JIRA is ONLINE and credentials are VALID
```

## 📊 Monitoring

Regularly monitor the function for health and performance:

### View Recent Executions

```bash
gcloud functions logs read product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --limit=100
```

### View Function Details

```bash
gcloud functions describe product-quality-jira-processor \
    --region=us-central1 \
    --gen2
```

### Check Error Rate

```bash
gcloud logging read "resource.type=cloud_function \
    AND resource.labels.function_name=product-quality-jira-processor \
    AND severity>=ERROR" \
    --limit=20 \
    --format=json
```

### Monitor Pub/Sub Subscription

To check messages pending in the queue or overall subscription health:

```bash
# Check messages waiting in queue
gcloud pubsub subscriptions describe \
  eventarc-us-central1-product-quality-jira-processor-612217-sub-916 \
  --project=sada-joseph-shorter-sada

# View subscription metrics
gcloud monitoring time-series list \
  --filter='metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages"' \
  --project=sada-joseph-shorter-sada
```

## 🎯 Performance

The system is designed for high responsiveness:

-   **Trigger Latency:** Typically less than 2 seconds after a message is published to Pub/Sub.
-   **Execution Time:** Approximately 3-5 seconds per alert for JIRA ticket creation.
-   **Total Time-to-Action:** Less than 10 seconds from alert detection to JIRA ticket creation.

This significantly reduces time-to-action from potentially 24-72 hours to under 10 seconds.

## 🔒 Security

Security considerations for this deployment include:

-   **Secret Manager:** The JIRA API key is stored securely in Google Secret Manager and not hardcoded or exposed in source control.
-   **Service Account:** The function utilizes the default App Engine service account (`sada-joseph-shorter-sada@appspot.gserviceaccount.com`).
-   **IAM Permissions:** The service account is granted necessary IAM roles, including `roles/pubsub.subscriber` (for receiving messages) and `roles/run.invoker` (for invoking Cloud Run services, which Cloud Functions Gen2 relies on). It also has permissions to access Secret Manager.
-   **Principle of Least Privilege:** Service accounts are configured with the minimum required permissions.
-   **Cloud Run Authentication:** Cloud Functions (Gen2) run on Cloud Run, which by default requires authenticated invocations.
-   **Secure Infrastructure:** The function runs within Google's secure and managed infrastructure.

## 🐛 Troubleshooting

### Function not triggering?

-   **Check Topic Existence:**
    ```bash
    gcloud pubsub topics describe product-quality-alerts
    ```
-   **Check Function Status:**
    ```bash
    gcloud functions describe product-quality-jira-processor --region=us-central1 --gen2
    ```

### JIRA tickets not created?

-   **Check Logs for Errors:**
    ```bash
    gcloud functions logs read product-quality-jira-processor \
        --region=us-central1 \
        --gen2 \
        --limit=20 \
        --filter="severity>=WARNING"
    ```
    Look for messages indicating JIRA unavailability (e.g., "Site temporarily unavailable", 404, 502, 503 errors) or credential issues.
-   **Test Secret Manager Access:**
    ```bash
    gcloud secrets versions access latest --secret=JIRA_API_KEY --project=sada-joseph-shorter-sada
    ```
    (Note: This will output the secret. Handle with care.)
-   **Test JIRA Connectivity and Credentials:** Use the `test_jira_status.py` script.
-   **JIRA Unavailability:** If JIRA is confirmed unavailable, the system is designed to automatically retry messages with exponential backoff for up to 7 days. No manual intervention is needed; tickets will be created once JIRA service resumes.

### High error rate?

-   **Verify Environment Variables:**
    ```bash
    gcloud functions describe product-quality-jira-processor \
        --region=us-central1 \
        --gen2 \
        --format="value(serviceConfig.environmentVariables)"
    ```
    Ensure all JIRA-related variables (PROJECT_ID, SERVER, USER_EMAIL) are correctly set.
-   **Malformed Messages:** Check logs for `json.JSONDecodeError` if messages from Pub/Sub are not valid JSON.

## 🔄 Updating the Function

After making any code changes in `main.py` or updating `requirements.txt` or `.env.yaml`:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor
./deploy.sh
```

The deployment process typically takes 2-3 minutes. The Cloud Function will be updated without incurring downtime.

## 💰 Cost Estimate

The estimated cost for this solution is very low, generally falling within the Google Cloud Free Tier limits for typical usage:

-   **Function Invocations:** The free tier includes 2 million invocations per month. With approximately 1,000 alerts per month, usage is well within this limit.
-   **Compute Time:** The free tier provides 400,000 GB-seconds of compute time. Assuming an average execution time, monthly usage will be significantly less than 100 GB-seconds.
-   **Pub/Sub:** The free tier includes 10 GB of message throughput per month. The alert data volume is minimal, typically less than 1 MB per month.

**Estimated monthly cost: $0.00** (within free tier for typical usage).

## 📚 Resources

For further information and troubleshooting:

-   [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
-   [Cloud Functions Pub/Sub Triggers](https://cloud.google.com/functions/docs/calling/pubsub)
-   [Google Secret Manager](https://cloud.google.com/secret-manager/docs)
-   [JIRA Python Library](https://jira.readthedocs.io/)

## ✅ Success Criteria

Upon successful deployment and operation, you should observe:

-   ✅ The Cloud Function `product-quality-jira-processor` is deployed and active in the `us-central1` region.
-   ✅ A Pub/Sub trigger is correctly configured, linking the `product-quality-alerts` topic to the function.
-   ✅ Automatic JIRA ticket creation occurs within ~10 seconds of an alert being published.
-   ✅ No manual intervention is required for the creation of JIRA tickets from alerts.
-   ✅ Function logs consistently show successful executions and relevant information.

**Your automated product quality alert system is now fully operational!**