#!/bin/bash

# Deploy Cloud Function for Product Quality Alert Processing
# This function is triggered automatically when messages arrive in Pub/Sub

set -e

echo "=============================================="
echo "Deploying Product Quality Alert Processor"
echo "=============================================="
echo ""

# Configuration
PROJECT_ID="sada-joseph-shorter-sada"
FUNCTION_NAME="product-quality-jira-processor"
REGION="us-central1"
PUBSUB_TOPIC="product-quality-alerts"
RUNTIME="python311"
ENTRY_POINT="process_quality_alert"
MEMORY="512MB"
TIMEOUT="300s"

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Function Name: $FUNCTION_NAME"
echo "  Region: $REGION"
echo "  Pub/Sub Topic: $PUBSUB_TOPIC"
echo "  Runtime: $RUNTIME"
echo ""

# Check if gcloud is authenticated
echo "🔐 Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ Error: Not authenticated with gcloud"
    echo "   Run: gcloud auth login"
    exit 1
fi
echo "✅ Authenticated"
echo ""

# Set project
echo "🎯 Setting project..."
gcloud config set project $PROJECT_ID
echo ""

# Deploy Cloud Function
echo "🚀 Deploying Cloud Function..."
echo ""

gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=$RUNTIME \
    --region=$REGION \
    --source=. \
    --entry-point=$ENTRY_POINT \
    --trigger-topic=$PUBSUB_TOPIC \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --env-vars-file=.env.yaml \
    --service-account="${PROJECT_ID}@appspot.gserviceaccount.com" \
    --max-instances=10 \
    --min-instances=0 \
    --retry

echo ""
echo "🔄 Configuring retry policy for Pub/Sub subscription..."
# The --retry flag enables automatic retries for failed messages
# Messages will be retried with exponential backoff until they succeed or expire (7 days default)
echo "✅ Retry policy enabled - messages will auto-retry on JIRA failures"
echo ""
echo "=============================================="
echo "✨ Deployment Complete!"
echo "=============================================="
echo ""
echo "📊 Function Details:"
gcloud functions describe $FUNCTION_NAME --region=$REGION --gen2 --format="value(serviceConfig.uri)"
echo ""
echo "🎯 What happens now:"
echo "  1. Analytics agent detects quality issues"
echo "  2. Issues published to Pub/Sub topic: $PUBSUB_TOPIC"
echo "  3. Cloud Function triggers AUTOMATICALLY (within seconds)"
echo "  4. JIRA tickets created with priority and metrics"
echo ""
echo "📝 View logs:"
echo "  gcloud functions logs read $FUNCTION_NAME --region=$REGION --gen2 --limit=50"
echo ""
echo "🧪 Test the function:"
echo "  cd /Users/joseph.shorter/repos/m_analytical_demo"
echo "  python -c \"from agent import detect_product_quality_issues, publish_product_alert; \\"
echo "             publish_product_alert(detect_product_quality_issues(7, 'high'))\""
echo ""
echo "  Then check logs to see automatic JIRA ticket creation!"
echo "=============================================="
