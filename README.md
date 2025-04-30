# GitOps Demo Repository

This repository demonstrates GitOps practices using a simple FastAPI application deployed with Kubernetes and managed by Argo CD. It showcases the complete pipeline from application development to automated deployment using GitOps principles.

## Repository Structure

```
.
├── cat-validator/              # Sample FastAPI Application
│   ├── main.py                # API implementation
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Container image definition
│   ├── .dockerignore        # Docker build exclusions
│   └── tests/               # Unit and integration tests
├── cat-validator-deploy/      # Kubernetes Manifests
│   ├── deployment.yaml       # Pod deployment configuration
│   └── service.yaml         # Service exposure configuration
└── devops-setup/             # GitOps Configuration
    └── cat-validator-app.yaml # Argo CD application manifest
```

## Components

### 1. Cat Validator Application (`cat-validator/`)
A sample REST API that validates cat data. This application serves as an example microservice with:
- Data validation using Pydantic models
- Comprehensive test coverage
- Containerization using Docker
- OpenAPI documentation

To build and run locally:
```bash
cd cat-validator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

To build the Docker image:
```bash
cd cat-validator
docker build -t cat-validator .
docker run -p 8000:8000 cat-validator
```

### 2. Kubernetes Manifests (`cat-validator-deploy/`)
Contains the Kubernetes resource definitions needed to run the application in a cluster:
- `deployment.yaml`: Defines how the application runs in Kubernetes
  - Resource limits and requests
  - Health probes
  - Container configuration
- `service.yaml`: Defines how the application is exposed
  - Internal access via ClusterIP
  - Port 80 mapped to container port 8000

To apply manually (without Argo CD):
```bash
kubectl apply -f cat-validator-deploy/
```

### 3. GitOps Configuration (`devops-setup/`)
Contains Argo CD configuration for automated deployment:
- Defines the connection between this Git repository and the Kubernetes cluster
- Configures automated sync and self-healing
- Manages the application lifecycle

To set up with Argo CD:
```bash
kubectl apply -f devops-setup/cat-validator-app.yaml
```

## Getting Started

1. **Prerequisites**
   - Kubernetes cluster
   - Argo CD installed in the cluster
   - Docker for building images
   - kubectl configured for your cluster

2. **Initial Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/philipus/gitops-test.git
   cd gitops-test

   # Build the application image
   cd cat-validator
   docker build -t cat-validator .

   # Deploy via Argo CD
   kubectl apply -f ../devops-setup/cat-validator-app.yaml
   ```

3. **Verify Deployment**
   - Check Argo CD UI for sync status
   - Access the API via the service endpoint
   - View application logs through Kubernetes

## Development Workflow

1. Make changes to the application in `cat-validator/`
2. Run tests to verify changes
3. Build and test new Docker image
4. Update Kubernetes manifests if needed
5. Commit and push changes
6. Argo CD will automatically detect and apply changes

## Monitoring

- **Application**: Access OpenAPI docs at `/docs` endpoint
- **Kubernetes**: Monitor pods, services, and logs via kubectl
- **GitOps**: Track sync status and history in Argo CD dashboard

## Purpose

This repository serves as:
1. A demonstration of GitOps practices
2. A template for setting up similar applications
3. An example of integrating various DevOps tools
4. A reference for Kubernetes deployment patterns 