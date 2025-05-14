#!/bin/bash
# deploy-product-service-fix.sh

# Set environment variables
RESOURCE_GROUP="alt-aks-kk-demo"
AKS_CLUSTER="aks-kk-demo"
NAMESPACE="pets"

# Log in to Azure and set the AKS context
echo "Logging in to Azure..."
az login

echo "Setting AKS context..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --overwrite-existing

# Apply the fix to the AKS cluster
echo "Applying product-service fix to the AKS cluster..."
kubectl apply -f product-service-mutex-fix.yaml -n $NAMESPACE

# Check the deployment status
echo "Checking deployment status..."
kubectl -n $NAMESPACE rollout status deployment/product-service

# Get pod info and logs
echo "Getting pods information..."
kubectl -n $NAMESPACE get pods -l app=product-service
kubectl -n $NAMESPACE logs -l app=product-service --tail=50

# Check the service endpoint
echo "Checking service endpoint..."
SERVICE_IP=$(kubectl -n $NAMESPACE get service product-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Product service is available at: http://${SERVICE_IP}"
echo "Testing health endpoint..."
curl -s -o /dev/null -w "%{http_code}" http://${SERVICE_IP}/health

echo "Deployment complete."
