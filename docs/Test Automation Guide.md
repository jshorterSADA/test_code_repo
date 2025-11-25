# Test Automation Guide

This guide outlines the testing strategies and automation practices employed within this codebase to ensure reliability, correctness, and maintainability of its components. It details the methodologies for validating utility functions and the critical Cloud Function responsible for processing product quality alerts.

## 1. Introduction

The objective of this Test Automation Guide is to provide a comprehensive overview of how software components within this repository are tested. It serves as a resource for developers, quality assurance engineers, and architects to understand the test philosophy, tools, procedures, and expected outcomes. Effective test automation is crucial for delivering robust and high-quality software, especially in distributed systems involving multiple integrations.

## 2. Test Philosophy and Principles

Our test automation strategy is built upon the following core principles:

*   **Comprehensive Coverage**: Aim for a balance of unit-level validation for individual functions and end-to-end integration testing for system workflows.
*   **Robust Error Handling Verification**: Explicitly test error conditions, invalid inputs, and external service unavailability to ensure graceful degradation and appropriate retry mechanisms.
*   **Logging as a Primary Diagnostic Tool**: Utilize detailed and structured logging not only for operational monitoring but also as a verifiable output for test assertions, particularly for edge cases.
*   **Automated Recovery**: Integrate testing of inherent retry mechanisms (ee.g., Pub/Sub's exponential backoff) to confirm system resilience.
*   **Reproducibility**: Ensure tests are deterministic and can be run consistently across different environments.

## 3. Core Testing Components and Tools

This codebase leverages a combination of standard Python libraries and Google Cloud Platform (GCP) services for its test automation efforts.

### 3.1. General Utilities and Local Testing

*   **Python `logging` module**: Utilized extensively to verify that functions produce expected log outputs under various scenarios, including normal execution and error conditions.
*   **Direct Script Execution**: Test scripts are designed to be run directly from the command line, providing immediate feedback.

### 3.2. Cloud Function and Integration Testing

*   **Google Cloud Platform (GCP)**: The primary environment for deploying and running the `product-quality-jira-processor` Cloud Function, making GCP's monitoring and logging capabilities integral to testing.
*   **`gcloud` CLI**: The command-line interface for Google Cloud, used for deploying Cloud Functions, reading function logs, and monitoring Pub/Sub subscriptions.
*   **`requests` library**: A Python HTTP library used within test scripts (`test_jira_status.py`) to perform direct HTTP requests for checking external service availability (e.g., JIRA).
*   **`google-cloud-secret-manager`**: The Python client library for GCP Secret Manager, used in `test_jira_status.py` to securely access and validate credentials required for integration.
*   **`jira` Python library**: The official Python client for the JIRA API, used both within the Cloud Function for ticket creation and within test scripts (e.g., `test_jira_status.py`) for authentication verification.
*   **Google Cloud Pub/Sub**: Serves as the event backbone and retry mechanism. Testing involves publishing messages and observing their processing flow and retry behavior.

## 4. Test Automation for `add_two_numbers` Utility

### 4.1. Purpose

This section details the testing approach for the `add_two_numbers` function. The primary goals are to ensure arithmetic correctness, validate robust input handling across various data types, and confirm that all operations, especially error conditions, are logged accurately and with appropriate correlation IDs.

### 4.2. Test Script: `demo_log_examples.py`

The `demo_log_examples.py` script acts as a comprehensive set of demonstration tests for the `add_two_numbers` function. It executes the function with a wide range of inputs and explicitly prints the function's log outputs and return values, allowing for direct verification of behavior.

### 4.3. Covered Scenarios and Expected Behavior

The `demo_log_examples.py` script validates the `add_two_numbers` function across numerous scenarios, as detailed below. Note that the `add_two_numbers` function tested here is designed for robust error handling and logging, returning `None` upon conversion failure.

*   **Normal Addition**: Verifies that standard integer inputs yield the correct sum.
    *   _Example_: `add_two_numbers(5, 10)`
    *   _Expected_: Logs successful addition and returns `15`.
*   **Invalid Inputs**: Tests the function's resilience against non-numeric strings, `None` values, empty strings, and strings composed solely of whitespace.
    *   _Examples_: `add_two_numbers("hello", 5)`, `add_two_numbers(None, 5)`, `add_two_numbers("", 5)`, `add_two_numbers("   ", 5)`
    *   _Expected_: Logs a "Value Error: Failed to convert one or both inputs to integers." message (prefixed with `correlation_ID:ID `) and returns `None`.
*   **Float/Scientific/Hex Inputs**: Examines how string representations of numbers that cannot be directly converted to `int` (e.g., `"3.14"`, `"1e5"`, `"0xFF"`) are handled.
    *   _Examples_: `add_two_numbers("3.14", "2.71")`, `add_two_numbers("1e5", "2e3")`, `add_two_numbers("0xFF", "0x10")`
    *   _Expected_: Logs a "Value Error: Failed to convert one or both inputs to integers." message and returns `None`, as direct `int()` conversion fails for these formats.
*   **Unicode Digits**: Checks conversion for full-width Unicode digits.
    *   _Example_: `add_two_numbers("５", "３")`
    *   _Expected_: Depends on Python's `int()` behavior; typically converts to `int` successfully.
*   **Large Numbers**: Confirms correct summation for very large integer strings, ensuring no overflow or parsing issues for Python's arbitrary-precision integers.
    *   _Example_: `add_two_numbers("9" * 50, "1" * 50)`
    *   _Expected_: Logs successful addition and returns the correct sum.
*   **Correlation ID Management**: Validates that custom and empty correlation IDs (`corrID` argument) are correctly incorporated into log message prefixes (`ID - ` for info, `correlation_ID:ID ` for errors).
    *   _Examples_: `add_two_numbers("invalid", 5, corrID="custom-test-id-123")`, `add_two_numbers("invalid", 5, corrID="")`
    *   _Expected_: Log messages show the specified correlation ID or no prefix if `corrID=""`.
*   **Log Injection Protection**: Investigates how inputs containing potentially disruptive characters (like newlines) are handled in log outputs to prevent log forging.
    *   _Example_: `add_two_numbers("5\nFAKE ERROR: ...", 5)`
    *   _Expected_: The entire input string is typically logged as part of the message content.
*   **Mixed Valid/Invalid Inputs**: Ensures consistent error handling when only one of the two inputs is invalid.
    *   _Example_: `add_two_numbers(10, "not_a_number")`
    *   _Expected_: Logs a "Value Error: Failed to convert..." and returns `None`.

### 4.4. How to Run `demo_log_examples.py`

To execute the demonstration test suite for `add_two_numbers`, navigate to the `m_analytical_demo` directory (or the parent directory if running from another location that allows `addNums` to be imported) and run the script:

```bash
python demo_log_examples.py
```

### 4.5. Expected Log Output and Return Values

For each scenario, the script will print a section header, the function call, and then the captured log output followed by the function's return value. Successful operations will typically show `INFO` messages and an integer return, while failures will display `ERROR` messages (prefixed with `correlation_ID:ID `) and return `None`.

## 5. Test Automation for Product Quality Alert Processor (Cloud Function)

### 5.1. Purpose

This section details the testing procedures for the `product-quality-jira-processor` Cloud Function. The primary objective is to validate the end-to-end workflow, from receiving a Pub/Sub message to successfully creating a JIRA ticket, including robust error handling, credential management, and the system's ability to self-recover from transient failures.

### 5.2. JIRA Connectivity and Credential Validation

Before attempting to create JIRA tickets, it is essential to verify that the JIRA service is accessible and the configured credentials are valid.

*   **Test Script**: `cloud_function_jira_processor/test_jira_status.py`
*   **Functionality**: This script performs a multi-step check:
    1.  **Basic Connectivity**: Attempts to reach the JIRA server URL (`https://sadaadvservices.atlassian.net`).
    2.  **API Endpoint Accessibility**: Tries to access a public JIRA API endpoint (`/rest/api/2/serverInfo`) to confirm the API is responsive.
    3.  **Credential Retrieval and Authentication**: Accesses the JIRA API key from Google Secret Manager (`projects/900228280944/secrets/JIRA_API_KEY/versions/latest`) and attempts to authenticate with the JIRA service using the retrieved key and `USER_EMAIL`.
*   **How to Run**:
    ```bash
    cd /Users/joseph.shorter/repos/cloud_function_jira_processor
    python test_jira_status.py
    ```
*   **Expected Output**:
    *   **Success**: `✅ JIRA is ONLINE and credentials are VALID`
    *   **Failure (JIRA Down)**: `❌ JIRA SERVICE IS CURRENTLY UNAVAILABLE` with details on specific connection or API errors, and a note on Pub/Sub's retry policy.

### 5.3. End-to-End Alert Processing

This methodology tests the full pipeline, from an originating event (simulated by publishing a Pub/Sub message) to the final action (JIRA ticket creation).

*   **Components Involved**:
    *   **Simulated Publisher**: An `agent.py` script (`m_analytical_demo/agent.py`) is used to mimic the analytics agent that detects issues and publishes alerts.
    *   **Google Cloud Pub/Sub**: The `product-quality-alerts` topic acts as the message queue and triggers the Cloud Function.
    *   **Cloud Function Logic**: `cloud_function_jira_processor/main.py` contains the core logic for processing alerts and interacting with JIRA.
    *   **JIRA**: The target system where tickets are created in the `AITD` project.
*   **Key Scenarios**:
    *   **Successful Ticket Creation**:
        *   **Action**: Publish a well-formed product quality alert message to the `product-quality-alerts` Pub/Sub topic.
        *   **Expected**: The Cloud Function processes the message, logs a `✅ SUCCESS` message with the JIRA ticket key and URL, and a new JIRA ticket is created in the `AITD` project with detailed information (summary, description, priority, labels, etc.) derived from the alert data.
    *   **Transient Error Handling (JIRA Downtime)**:
        *   **Action**: Publish a valid alert when the JIRA service is known to be unavailable (e.g., confirmed via `test_jira_status.py`).
        *   **Expected**: The Cloud Function attempts to create a ticket, logs an `❌ FAILED` error message with details indicating JIRA unavailability (e.g., "Site temporarily unavailable", "404"), and raises an exception. This exception triggers Pub/Sub's automatic retry mechanism, causing the message to be redelivered with exponential backoff. Once JIRA recovers, the same message is processed successfully, leading to ticket creation.
    *   **Permanent Error Handling (Malformed Message)**:
        *   **Action**: Publish a Pub/Sub message that contains malformed JSON or invalid data that the Cloud Function cannot parse or process meaningfully.
        *   **Expected**: The Cloud Function catches `json.JSONDecodeError` or other processing errors, logs an `❌ FAILED` error, and crucially, acknowledges the message (does not re-raise a transient error). This prevents the malformed message from entering an infinite retry loop.
    *   **Logging Consistency**:
        *   **Action**: Observe Cloud Function logs during both success and failure scenarios.
        *   **Expected**: All critical steps (`📨 Received alert`, `🔍 Processing`, `✅ SUCCESS`, `❌ FAILED`, `⚠️ JIRA service appears to be unavailable`, `🔄 Transient error detected`) are logged with appropriate severity levels and context (product ID, revenue at risk, severity).
    *   **Special Character Handling**:
        *   **Action**: Publish an alert containing product names or descriptions with special characters (e.g., `K'NEX`).
        *   **Expected**: The Cloud Function successfully processes and encodes these characters, and the JIRA ticket displays them correctly.

### 5.4. How to Perform End-to-End Tests

1.  **Deploy the Cloud Function**: Ensure the `product-quality-jira-processor` Cloud Function is deployed and active in your GCP project. Refer to `cloud_function_jira_processor/README.md` for deployment instructions (e.g., `./deploy.sh`).
2.  **Check JIRA Status (Optional but Recommended)**: Before publishing alerts, run `python test_jira_status.py` to confirm JIRA connectivity and valid credentials.
3.  **Publish a Test Alert**: Use the `agent.py` script to publish a sample alert message to the Pub/Sub topic. Navigate to the `m_analytical_demo` directory and run:
    ```bash
    cd /Users/joseph.shorter/repos/m_analytical_demo
    source ../.venv/bin/activate # Activate virtual environment if applicable
    python -c "from agent import detect_product_quality_issues, publish_product_alert; \
               alerts = detect_product_quality_issues(7, 'high'); \
               publish_product_alert(alerts)"
    ```
4.  **Monitor Cloud Function Logs**: In a separate terminal, continuously monitor the Cloud Function logs for real-time feedback:
    ```bash
    gcloud functions logs read product-quality-jira-processor \
      --region=us-central1 \
      --gen2 \
      --limit=50 \
      --project=sada-joseph-shorter-sada
    ```
5.  **Verify JIRA Tickets**: Log in to JIRA (`https://sadaadvservices.atlassian.net/browse/AITD`) and confirm that new tickets have been created with the expected content.

### 5.5. Expected Outcomes

*   **Cloud Function Logs**: You should observe `INFO` messages for message reception and processing, followed by `✅ SUCCESS` for successful JIRA ticket creation, or `❌ FAILED` and `⚠️ JIRA service appears to be unavailable`/`🔄 Transient error detected` messages during transient failures, indicating Pub/Sub's retry mechanism is engaged.
*   **JIRA**: New tickets will appear in the specified JIRA project (`AITD`), fully populated with detailed product quality information, metrics, recommended actions, correct priority, and relevant labels.
*   **Automatic Recovery**: In scenarios of temporary JIRA unavailability, the system is expected to automatically recover. Messages will be retried by Pub/Sub, and tickets will be created once JIRA service is restored, without requiring manual intervention.

## 6. Monitoring and Observability for Test Verification

Effective testing extends beyond initial execution; it includes continuous monitoring to verify expected behavior in a production-like environment and to diagnose issues.

*   **`gcloud functions logs read`**: The primary tool for inspecting real-time and historical execution logs of the Cloud Function. This is critical for debugging and confirming the flow of alerts.
*   **`gcloud pubsub subscriptions describe`**: Used to check the status of Pub/Sub subscriptions, including the number of undelivered messages, which is a key indicator of pending retries due to transient errors.
    ```bash
    gcloud pubsub subscriptions describe \
      eventarc-us-central1-product-quality-jira-processor-612217-sub-916 \
      --project=sada-joseph-shorter-sada
    ```
*   **`gcloud monitoring time-series list`**: Provides access to comprehensive metrics for GCP services, including Pub/Sub subscription health, enabling deeper analysis of retry behavior and message flow.
    ```bash
    gcloud monitoring time-series list \
      --filter='metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages"' \
      --project=sada-joseph-shorter-sada
    