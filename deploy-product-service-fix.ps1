# deploy-product-service-fix.ps1

# Set environment variables
$RESOURCE_GROUP = "alt-aks-kk-demo"
$AKS_CLUSTER = "aks-kk-demo"
$NAMESPACE = "pets"

# Log in to Azure and set the AKS context
Write-Host "Logging in to Azure..."
az login

Write-Host "Setting AKS context..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --overwrite-existing

# Apply the fix to the AKS cluster
Write-Host "Applying product-service fix to the AKS cluster..."
kubectl apply -f product-service-mutex-fix.yaml -n $NAMESPACE

# Check the deployment status
Write-Host "Checking deployment status..."
kubectl -n $NAMESPACE rollout status deployment/product-service

# Get pod info and logs
Write-Host "Getting pods information..."
kubectl -n $NAMESPACE get pods -l app=product-service
kubectl -n $NAMESPACE logs -l app=product-service --tail=50

# Check the service endpoint
Write-Host "Checking service endpoint..."
$SERVICE_IP = kubectl -n $NAMESPACE get service product-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
Write-Host "Product service is available at: http://${SERVICE_IP}"
Write-Host "Testing health endpoint..."
$response = Invoke-WebRequest -Uri "http://${SERVICE_IP}/health" -Method Get -UseBasicParsing
Write-Host "Health endpoint status code: $($response.StatusCode)"

Write-Host "Deployment complete."
