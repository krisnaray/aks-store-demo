# Product Service Fix - GitHub Actions Deployment

This document describes the mutex poisoning fix for the product-service component and how to deploy it using GitHub Actions.

## The Problem: Mutex Poisoning

The product-service was experiencing panic issues due to mutex poisoning. This occurs when a thread holding a mutex panics, causing the mutex to be marked as poisoned. Subsequent attempts to acquire the mutex using `unwrap()` would then panic, leading to service disruption.

## The Solution

We've implemented the following fixes:

1. Replaced all instances of `data.products.lock().unwrap()` with a more robust pattern that handles poisoned mutexes gracefully:

```rust
let products = match data.products.lock() {
    Ok(guard) => guard,
    Err(e) => {
        log::error!("Mutex poisoned in function_name: {:?}", e);
        return Ok(HttpResponse::InternalServerError().body("Internal server error"));
    }
};
```

2. Added proper error handling for unwrapped indices to prevent panics when a product ID is not found.

3. Created a Kubernetes patch file (`product-service-fix.yaml`) that can be applied to restart the deployment with the fixed code.

## Deployment with GitHub Actions

This repository is configured with GitHub Actions to automatically:

1. Build and push the product-service container image when changes are pushed to the `main` branch (`package-product-service.yaml` workflow)
2. Deploy the updated container image to your AKS cluster (`deploy-to-aks.yml` workflow)

The deployment workflow will:
- Authenticate to Azure
- Connect to your AKS cluster
- Update the product-service deployment with the latest image
- Force a rolling update with a timestamp annotation
- Verify the deployment status

## GitHub Action Setup

### Prerequisites

To enable the GitHub Actions deployment workflow, you need to set up the following secrets in your GitHub repository:

1. `AZURE_CREDENTIALS`: Azure service principal credentials with permissions to deploy to your AKS cluster

You can create these credentials using the Azure CLI:

```bash
# Create a service principal and get its credentials
az ad sp create-for-rbac --name "github-aks-deployer" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/alt-aks-kk-demo \
  --sdk-auth
```

Copy the output JSON and add it as a repository secret named `AZURE_CREDENTIALS`.

### Workflow Customization

The deployment workflow can be customized by modifying the following variables in the `deploy-to-aks.yml` file:

- `RESOURCE_GROUP`: The name of your Azure resource group (currently set to `alt-aks-kk-demo`)
- `AKS_CLUSTER`: The name of your AKS cluster (currently set to `aks-kk-demo`)
- `NAMESPACE`: The Kubernetes namespace where the application is deployed (currently set to `pets`)

### Running the Workflow Manually

You can manually trigger the deployment workflow by:

1. Going to the "Actions" tab in your GitHub repository
2. Selecting the "deploy-to-aks" workflow
3. Clicking "Run workflow"
4. Selecting the environment (pets, staging, or production)
5. Clicking "Run workflow"

## Monitoring and Verification

After deployment, you can verify the status by:

1. Checking the GitHub Actions workflow run logs
2. Running the Locust load testing script to verify the service handles requests properly
3. Using `kubectl` to check the pod status:

```bash
kubectl -n pets get pods -l app=product-service
kubectl -n pets logs -l app=product-service
```

## Troubleshooting

If the deployment fails:

1. Check the GitHub Actions workflow run logs for errors
2. Verify Azure credentials are set up correctly
3. Check if the AKS cluster and namespace exist
4. Verify the Kubernetes resources:

```bash
kubectl -n pets describe deployment product-service
kubectl -n pets describe pod -l app=product-service
```
