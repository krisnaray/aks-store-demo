# Debug instructions for fixing the mutex poison error in product-service

## Issue Description
The error message indicates a mutex poison error in the product-service application:
```
thread 'actix-rt|system:0|arbiter:0' panicked at src/routes/add.rs:11:45:
called `Result::unwrap()` on an `Err` value: PoisonError { .. }
```

This happens when a thread panics while holding a mutex lock, causing all future attempts to acquire the lock to return `PoisonError`.

## Fix Applied
1. Modified `add.rs` to properly handle mutex poisoning by using `into_inner()` to recover the mutex value even when poisoned.
2. Updated the deployment YAML to include proper resource settings and health checks.
3. Updated GitHub workflows to deploy specific versions of the image rather than just 'latest'.

## Manual Deployment Steps
To manually deploy the fixed version:

### For Windows users:
```powershell
# Run the PowerShell script
.\deploy-product-service-fix.ps1
```

### For Linux/MacOS users:
```bash
# Make the script executable
chmod +x deploy-product-service-fix.sh

# Run the script
./deploy-product-service-fix.sh
```

## Monitoring and Verification
After deployment, check the logs for any error messages:
```bash
kubectl -n pets logs -l app=product-service --tail=100
```

Verify that the service is healthy:
```bash
SERVICE_IP=$(kubectl -n pets get service product-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -v http://${SERVICE_IP}/health
```

## Additional Information
- The error is related to mutex handling in Rust, where locks that were held by threads that panicked are considered "poisoned"
- Our fix properly handles this case by recovering the mutex with `into_inner()` rather than simply unwrapping it
- We've also improved health checks and resource settings in the deployment
