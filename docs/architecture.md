# Enterprise CI/CD Platform Architecture

## Workflow

```mermaid
flowchart TD
    A["Developer Commit or Pull Request"] --> B["GitHub Actions"]
    B --> C["Ruff Lint and Unit Tests"]
    C --> D["Checkov Kubernetes Scan"]
    D --> E["SonarQube Quality Gate"]
    E --> F["Build Five Docker Images"]
    F --> G["Trivy API Image Scan"]
    G --> H{"Critical Vulnerability Gate"}
    H -->|Pass| I{"Push to main?"}
    H -->|Fail| J["Fail CI Job"]
    I -->|Yes| K["Publish Images to GHCR"]
    K --> L["Cosign Image Signing"]
    L --> M["Kubernetes Deployment"]
    M --> N["Argo Rollouts Canary"]
    N --> O["Health Checks"]
    O -->|Failure| P["Abort Failed Revision"]
    O -->|Healthy| Q["Stable Revision"]
```

## Components

- GitHub Actions: CI/CD orchestration.
- Ruff and unit tests: Python quality and behavior checks.
- Checkov: Kubernetes manifest security scanning.
- SonarQube Cloud: Code-quality analysis and quality-gate evaluation.
- Trivy: API image vulnerability scanning with a blocking CRITICAL gate.
- GHCR: Container image registry.
- Cosign: Container image digest signing.
- Kubernetes and Argo Rollouts: Deployment and rollout management.

## Limitations

- This is a portfolio demonstration using a local Kind cluster.
- The blocking Trivy gate applies to the API image only.
- Canary percentage steps are configured, but no traffic router is configured for actual percentage-based HTTP traffic splitting.
- A failed rollout can leave the Rollout resource Degraded even if the previous stable ReplicaSet remains healthy.
