# API Documentation

## Overview

This project contains five simplified Python HTTP services for demonstrating a DevSecOps CI/CD pipeline. The endpoints below are based on the current service implementations.

## Endpoints

| Service | Method | Endpoint | Successful response example |
|---|---|---|---|
| API | GET | `/` | `{"service":"devsecops-api","version":"1.0.0"}` |
| API | GET | `/health` | `{"status":"healthy"}` |
| Auth | GET | `/auth` | `{"service":"auth-service","authenticated":true}` |
| Catalog | GET | `/products` | `{"service":"catalog-service","products":["item-1","item-2"]}` |
| Orders | GET | `/orders` | `{"service":"orders-service","orders":[]}` |
| Notifications | GET | `/notifications` | `{"service":"notifications-service","status":"ready"}` |

## Health Checks

Each service exposes `GET /health`, returning HTTP 200 and a JSON response indicating that the service is healthy. The four supporting services include their service name in the health response; the API returns `{"status":"healthy"}`.

## Error Handling

The API service returns HTTP 404 for paths other than `/` and `/health`. The supporting services should be checked in their source files for their exact behavior on unknown paths.

## Testing

Run the project unit tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

## Scope

These are demonstration endpoints, not a complete authentication, product-management, order-processing, or notification platform. The sample responses do not demonstrate real persistence or integrations.
