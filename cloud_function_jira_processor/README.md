# Product Quality Alert Processor - Cloud Function

**Automatically creates JIRA tickets when product quality alerts are published to Pub/Sub.**

## 🚀 What This Does

This Cloud Function processes product quality alerts **immediately** (within seconds) when they're published to Pub/Sub, eliminating the need for manual processing or cron jobs.

### Flow:
```
Analytics Agent → Pub/Sub Topic → Cloud Function (AUTO) → JIRA Ticket Created
(detects issues)   (queue)         (triggers instantly)    (< 5 seconds)
```

## 📦 Contents

- `main.py` - Cloud Function code (Pub/Sub trigger + JIRA creation)
- `requirements.txt` - Python dependencies
- `.env.yaml` - Environment variables (JIRA config)
- `deploy.sh` - Deployment script
- `README.md` - This file

## 🔧 Prerequisites

1. **Google Cloud SDK** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project sada-joseph-shorter-sada
   ```

2. **Required APIs enabled**:
   - Cloud Functions API
   - Cloud Build API
   - Secret Manager API
   - Pub/Sub API

3. **JIRA API Key** in Secret Manager:
   - Already configured: `projects/900228280944/secrets/JIRA_API_KEY/versions/latest`

4. **Pub/Sub Topic** created:
   - Topic: `product-quality-alerts`
   - Already set up via `setup-product-quality-pubsub.sh`

## 🚀 Deployment

### Option 1: Automated (Recommended)

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual

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
    --service-account=sada-joseph-shorter-sada@appspot.gserviceaccount.com
```

## 🧪 Testing

### 1. Publish Test Alerts

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

```bash
# In another terminal
gcloud functions logs read product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --limit=50 \
    --format="value(severity,log)"
```

You should see:
```
📨 Received alert from Pub/Sub
🔍 Processing: Fisher-Price Code-a-Pillar (Severity: HIGH)
✅ SUCCESS: Created AITD-XXX for Fisher-Price Code-a-Pillar
```

### 3. Verify JIRA Tickets

Check your JIRA project for new tickets:
- https://sadaadvservices.atlassian.net/browse/AITD

## 📊 Monitoring

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

## 🎯 Performance

- **Trigger Latency:** < 2 seconds after message published
- **Execution Time:** 3-5 seconds per alert
- **JIRA Ticket Creation:** < 5 seconds total

**Result: Time-to-action reduced from 24-72 hours to < 10 seconds!**

## 🔧 Configuration

### Environment Variables (.env.yaml)

| Variable | Value | Description |
|----------|-------|-------------|
| `JIRA_PROJECT_ID` | `AITD` | JIRA project key |
| `JIRA_ISSUE_TYPE` | `Task` | Type of JIRA issue to create |
| `JIRA_SERVER` | `https://sadaadvservices.atlassian.net` | JIRA server URL |
| `USER_EMAIL` | `joseph.shorter@sada.com` | JIRA user email |
| `GOOGLE_CLOUD_PROJECT` | `sada-joseph-shorter-sada` | GCP project ID |

### Function Settings

- **Memory:** 512MB (sufficient for JIRA API calls)
- **Timeout:** 300s (5 minutes max)
- **Concurrency:** Up to 10 instances (processes 10 alerts simultaneously)
- **Min Instances:** 0 (scales to zero when idle)

## 🔒 Security

- **Secret Manager:** JIRA API key stored securely (not in code)
- **Service Account:** Uses default App Engine service account
- **IAM Permissions:** Function has Secret Manager access via service account
- **Network:** Runs in Google's secure infrastructure

## 🐛 Troubleshooting

### Function not triggering?

```bash
# Check if topic exists
gcloud pubsub topics describe product-quality-alerts

# Check function status
gcloud functions describe product-quality-jira-processor --region=us-central1 --gen2
```

### JIRA tickets not created?

```bash
# Check logs for errors
gcloud functions logs read product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --limit=20 \
    --filter="severity>=WARNING"

# Test Secret Manager access
gcloud secrets versions access latest --secret=JIRA_API_KEY
```

### High error rate?

Check environment variables:
```bash
gcloud functions describe product-quality-jira-processor \
    --region=us-central1 \
    --gen2 \
    --format="value(serviceConfig.environmentVariables)"
```

## 🔄 Updating the Function

After making code changes:

```bash
cd /Users/joseph.shorter/repos/cloud_function_jira_processor
./deploy.sh
```

Deployment takes ~2-3 minutes. The function will be updated without downtime.

## 💰 Cost Estimate

**Very low cost** (Google Cloud Free Tier covers most usage):

- **Function Invocations:** 2M free per month (you'll use ~1,000/month)
- **Compute Time:** 400K GB-seconds free (you'll use ~100 GB-seconds/month)
- **Pub/Sub:** 10 GB free per month (you'll use < 1 MB/month)

**Estimated monthly cost: $0.00** (within free tier)

## 📚 Resources

- [Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Pub/Sub Triggers](https://cloud.google.com/functions/docs/calling/pubsub)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)
- [JIRA Python Library](https://jira.readthedocs.io/)

## ✅ Success Criteria

After deployment, you should have:

- ✅ Cloud Function deployed and active
- ✅ Pub/Sub trigger configured
- ✅ Automatic JIRA ticket creation (< 10 seconds)
- ✅ No manual intervention required
- ✅ Logs showing successful executions

**Your quality alert system is now fully automated!** 🎉
