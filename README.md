# Enterprise CI/CD Platform with DevSecOps Gates

An enterprise-style DevSecOps project demonstrating automated testing, code quality analysis, security scanning, container publishing, image signing, Kubernetes deployment, and rollout failure handling.

## Technology Stack

- CI/CD: GitHub Actions
- Code quality: Ruff and SonarQube Cloud
- Security scanning: Trivy and Checkov
- Containerization: Docker
- Registry: GitHub Container Registry (GHCR)
- Image signing: Cosign
- Orchestration: Kubernetes and Kind
- Progressive delivery: Argo Rollouts
- Application: Python

## Architecture

Developer Push -> GitHub Actions -> Lint and Unit Tests -> Checkov -> SonarQube Quality Gate -> Build Docker Images -> Trivy Scan -> Publish to GHCR -> Sign with Cosign -> Kubernetes -> Argo Rollouts

## Sample Services

| Service | Example Endpoint |
|---|---|
| API | /health |
| Auth | /auth |
| Catalog | /products |
| Orders | /orders |
| Notifications | /notifications |

These are simplified demonstration services used to test the CI/CD pipeline.

## CI/CD Pipeline

GitHub Actions runs linting, unit tests, Kubernetes manifest security scanning, SonarQube analysis and quality-gate enforcement, and builds five Docker images.

The workflow scans the API image with Trivy and enforces a critical-vulnerability gate for that image. On pushes to the main branch, it publishes five images to GHCR and signs their image digests using Cosign.

The current blocking Trivy gate applies to the API image; do not assume that all five images have equivalent blocking vulnerability gates.

## Kubernetes Security

The API deployment demonstrates:

- Non-root container execution
- Dropped Linux capabilities
- Read-only root filesystem
- Resource requests and limits
- Readiness and liveness probes
- Disabled automatic service-account token mounting
- Kubernetes NetworkPolicy
- Checkov Kubernetes manifest scanning

Some Checkov checks are explicitly skipped for the local Kind environment. Refer to the Kubernetes manifests for details.

## Argo Rollouts and Automated Rollback

A separate devsecops-api-canary Rollout runs two replicas and uses HTTP readiness and liveness probes.

During a controlled failure test, a nonexistent image tag caused the new revision to stop progressing. Argo Rollouts reported RolloutAborted, scaled down the failed ReplicaSet, and retained the previous stable revision with two ready replicas.

The Rollout can remain Degraded after an aborted update even while the stable ReplicaSet is healthy.

Traffic-routing limitation: Canary weights are not actual HTTP traffic splitting because a traffic-routing integration has not been configured.

## Run Locally

Prerequisites: Python 3, Docker, kubectl, Kind, and a running Kubernetes cluster.

Run unit tests:

    python3 -m unittest discover -s tests -v

Run linting:

    ruff check services/ tests/

Inspect Kubernetes resources:

    kubectl get rollout,deploy,svc,pods -n devsecops

Inspect the canary rollout:

    kubectl argo rollouts get rollout devsecops-api-canary -n devsecops

## Repository Structure

    .github/workflows/ci.yml
    k8s/
    services/
      api/
      auth/
      catalog/
      orders/
      notifications/
    tests/
    docs/evidence/
    Dockerfile
    README.md

## Scope and Limitations

This is a learning and portfolio project running on a local Kind cluster, not a production deployment.

- Sample services have simplified demonstration behavior.
- Canary weights are not connected to a traffic router.
- The demonstrated blocking Trivy gate applies to critical vulnerabilities in the API image.
- A passing SonarQube quality gate does not necessarily mean every reported issue has been eliminated.
- Some Kubernetes security exceptions are specific to the local Kind environment.

## Author

Muhammad Rinas

GitHub: https://github.com/rinas-ck
