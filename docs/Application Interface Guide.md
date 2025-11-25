# Application Interface Guide (API v1)

Welcome to the Simple Math API documentation. This API provides access to basic arithmetic operations.

## Introduction

This API follows RESTful conventions and returns data in **JSON** format. It is designed to offer simple, stateless arithmetic computations.

> **Base URL**
> ```
> https://api.simplemath.com/v1
> ```

---

## Correlation IDs

Each request is processed with a unique `correlation_ID` for tracing and debugging purposes. This ID is included in log messages and can be optionally provided by the client.

To include a custom correlation ID in your request, use the `X-Correlation-ID` header. If not provided, the system will generate one.

```bash
curl https://api.simplemath.com/v1/math/add \
  -H "X-Correlation-ID: your-custom-id-123" \
  -d '{
    "num1": "10",
    "num2": 25
  }'
```

---

## Endpoints

### Add Two Numbers

Performs addition of two numbers. Inputs can be integers or string representations of numbers. The API will attempt to convert string inputs to integers.

**Request**
`POST /math/add`

**Body Attributes**
| Attribute | Type | Description |
| :--- | :--- | :--- |
| `num1` | string or integer | The first number to add. |
| `num2` | string or integer | The second number to add. |

**Example Request**

```bash
curl https://api.simplemath.com/v1/math/add \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: add-request-001" \
  -d '{
    "num1": "10",
    "num2": 25
  }'
```

**Response**

```json
{
  "result": 35,
  "correlation_id": "add-request-001",
  "message": "Successfully added 10 and 25."
}
```

---

## Errors

This API uses standard HTTP status codes along with custom error details.

| Code | Status | Description |
| :--- | :--- | :--- |
| 200 | OK | Request succeeded. |
| 400 | Bad Request | Malformed JSON or invalid input parameters (e.g., non-numeric values). |
| 500 | Internal Server Error | An unexpected error occurred on the server. |

**Error Response Body**

```json
{
  "error": {
    "code": "INVALID_INPUT_TYPE",
    "message": "Input 'num1' could not be converted to a number. Received: 'abc'.",
    "correlation_id": "add-request-002"
  }
}
