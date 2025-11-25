# Project Overview: Product Quality Alert System & Utilities

This repository contains a collection of components, primarily focused on an automated **Product Quality Alert System** designed to detect product quality issues, publish them to Google Cloud Pub/Sub, and automatically create JIRA tickets via a Cloud Function. Additionally, it includes a separate utility demonstrating robust logging and error handling for numeric operations.

## ⚠️ Important Note on Document Template

Please be aware that no specific template was provided for this `README-temp.md` document. As an expert software architect and technical writer, I have utilized standard best practices for repository documentation structure, style, and tone, adapting the content directly from the provided codebase to ensure accuracy and comprehensiveness.

---

## 1. Product Quality Alert System

This is the core system, providing an end-to-end solution for proactive product quality management. It integrates analytics, messaging, cloud functions, and JIRA to streamline the alert processing workflow.

### 1.1. System Overview

The Product Quality Alert System automates the process of identifying significant product quality issues based on analytical data (e.g., sentiment analysis, revenue impact) and ensures these issues are rapidly translated into actionable JIRA tickets for engineering and product teams. It's designed for resilience, immediate action, and detailed tracking.

### 1.2. Architecture

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

### 1.3. Key Capabilities & Features

*   **Analytics & Detection**: Identifies high-severity quality issues with significant revenue at risk (e.g., Fisher-Price Code-a-Pillar, K'NEX Plants vs Zombies). Utilizes sentiment-revenue correlation models.
*   **Message Publishing**: `publish_product_alert()` function handles alerts, including special characters, and publishes them to Pub/Sub.
*   **Cloud Function (JIRA Processor)**: Automatically processes Pub/Sub messages to create detailed JIRA tickets.
    *   **Enhanced Error Handling**: Differentiates between transient and permanent errors, preventing infinite retry loops for malformed messages and triggering retries for temporary service unavailability.
    *   **Detailed Logging**: Provides extensive logs with product ID, revenue at risk, severity, and processing status.
*   **Cloud Infrastructure**: Leverages Pub/Sub topics, Cloud Functions (Gen2), and Eventarc triggers with automatic retry policies.
*   **IAM & Security**: Properly configured service accounts with least privilege, JIRA API key stored securely in Google Secret Manager, and no credentials in source control.
*   **Automatic Recovery**: Pub/Sub retains messages for up to 7 days, and the system automatically retries failed messages with exponential backoff if JIRA or other transient services are unavailable.

### 1.4. Cloud Function: JIRA Processor (`cloud_function_jira_processor/`)

This directory contains the core Cloud Function responsible for integrating with JIRA.

*   **`main.py`**: The Python Cloud Function code (`process_quality_alert` entry point) that receives Pub/Sub messages, extracts alert details, and constructs/creates JIRA tickets.
*   **`README.md`**: Provides comprehensive documentation for this specific Cloud Function, including prerequisites, deployment instructions, testing procedures, monitoring guidelines, configuration details, and troubleshooting tips. **Refer to this `README.md` for in-depth information about the Cloud Function.**
*   **`test_jira_status.py`**: A utility script to verify JIRA service availability and credentials from Secret Manager.
*   **`.env.yaml`**: Defines environment variables used by the Cloud Function for JIRA configuration (Project ID, Issue Type, Server URL, User Email).

### 1.5. Current System Status and Recovery (`PRODUCT_QUALITY_ALERT_STATUS.md`)

As of the last update (November 13, 2025), the system is fully operational and awaiting JIRA service resumption.

*   **Working Components**: Analytics, message publishing, cloud infrastructure, IAM, enhanced error handling, and credential retrieval are all confirmed working.
*   **Current Blocker**: The JIRA instance (`https://sadaadvservices.atlassian.net`) is returning HTTP 404 ("Site temporarily unavailable"). This prevents JIRA tickets from being created.
*   **Impact**: Cloud Function executes successfully, but JIRA ticket creation fails. Logs indicate the JIRA service is down.
*   **Automatic Recovery**: Once JIRA comes back online, the system will **automatically recover**. Pub/Sub will re-deliver queued messages, and the Cloud Function will process them to create pending JIRA tickets without manual intervention. Messages are retained for up to 7 days with exponential backoff for retries (initial: 10s, max: 600s).

### 1.6. Testing & Monitoring

*   **JIRA Status Check**: Use `cloud_function_jira_processor/test_jira_status.py` to monitor JIRA availability and credential validity.
*   **Publish New Alerts**: Use the provided Python commands (referencing `m_analytical_demo/agent.py`) to simulate new alert generation and publishing.
*   **Cloud Function Logs**: Monitor Cloud Function logs using `gcloud functions logs read` for real-time execution details.
*   **Pub/Sub Monitoring**: Check Pub/Sub subscription metrics for undelivered messages.

---

## 2. `add_two_numbers` Logging Demo Utility

This is a standalone Python utility demonstrating best practices for function design, input validation, and structured logging.

### 2.1. Overview (`addNums.py`)

The `add_two_numbers` function in `addNums.py` is designed to sum two numbers, gracefully handling various input types including integers, floats, and string representations of numbers (including scientific notation). It incorporates robust error handling and detailed logging with correlation IDs.

### 2.2. Key Features

*   **Flexible Input Handling**: Accepts numbers as integers, floats, or string representations.
*   **Type Conversion**: Attempts to convert all inputs to integers, first via `float()` to handle scientific notation or decimal strings, then `int()` for truncation.
*   **Graceful Error Handling**: Catches `ValueError` and `TypeError` for non-convertible inputs (e.g., `None`, empty strings, non-numeric text) and logs errors with specific messages and correlation IDs.
*   **Structured Logging**: All informational and error messages include a correlation ID for traceability, following a consistent format.
*   **`demo_log_examples.py`**: A script to showcase various success and failure scenarios, demonstrating the detailed log outputs produced by `add_two_numbers`.

### 2.3. Usage

To understand the `add_two_numbers` function in detail, including its specific behavior and logging outputs for different scenarios, refer to the comments within `addNums.py` and execute `demo_log_examples.py`.

---

## 3. Repository Structure

```
.
├── addNums.py                        # Utility function for adding numbers with logging
├── README.md                         # README for the addNums.py utility
├── demo_log_examples.py              # Demonstrates addNums.py logging behavior
├── PRODUCT_QUALITY_ALERT_STATUS.md   # Status report for the Product Quality Alert System
└── cloud_function_jira_processor/    # Directory for the JIRA Cloud Function
    ├── .env.yaml                     # Environment variables for the Cloud Function
    ├── README.md                     # Comprehensive README for the Cloud Function
    ├── main.py                       # Cloud Function source code
    └── test_jira_status.py           # Script to check JIRA status and credentials
```

---

## 4. General Prerequisites

*   Google Cloud SDK installed and authenticated.
*   Required Google Cloud APIs enabled (Cloud Functions, Pub/Sub, Secret Manager, Cloud Build).
*   Python 3.x.
*   Access to the specified Google Cloud Project (`sada-joseph-shorter-sada`).
*   Access to the JIRA instance (`https://sadaadvservices.atlassian.net`).

---

## 5. Contributing

Contributions are welcome! Please follow standard practices:
1.  Fork the repository.
2.  Create a new branch for your feature or bugfix.
3.  Implement your changes and write tests.
4.  Ensure all existing tests pass and new tests cover your changes.
5.  Submit a pull request with a clear description of your changes.

---

## 6. License

(License information not provided in codebase, placeholder)
This project is licensed under the [LICENSE NAME] License - see the LICENSE.md file for details.