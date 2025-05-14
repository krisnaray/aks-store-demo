# AKS Store Demo - Load Testing Instructions

This document provides instructions for running load tests against the AKS Store Demo storefront application using Locust.

## Prerequisites

1. Ensure you have Python installed (Python 3.8 or higher recommended)
2. Install Locust:
   ```
   pip install locust
   ```

## Running the Load Test

### Option 1: Command Line Interface

To run the load test from the command line:

```bash
# Replace with your actual store-front service URL (from kubectl get services -n pets)
locust -f locustfile_storefront.py --host=http://20.166.98.36 -u 50 -r 5 --run-time 5m
```

Parameters:
- `-f locustfile_storefront.py`: Specifies the Locust test script
- `--host`: The base URL of the store-front service
- `-u 50`: Simulates 50 concurrent users
- `-r 5`: User spawn rate (5 users per second)
- `--run-time 5m`: Run the test for 5 minutes

### Option 2: Web UI

To run the load test with the Locust web interface:

```bash
# Replace with your actual store-front service URL (from kubectl get services -n pets)
locust -f locustfile_storefront.py --host=http://20.166.98.36
```

1. Navigate to http://localhost:8089 in your web browser
2. Set the desired number of users and spawn rate
3. Click "Start swarming" to begin the test
4. Monitor real-time statistics and charts in the web interface

## Understanding Test Scenarios

The load test simulates the following user behaviors:

1. **Browsing Products**: Users view the product catalog
2. **Product Details**: Users view detailed information about specific products
3. **Cart Management**: Users add items to cart and view cart contents
4. **Checkout Process**: Users complete purchases with simulated customer information

## Analyzing Results

After running the load test, you can analyze:

1. Response times for each API endpoint
2. Error rates and specific error messages
3. Request rates (RPS) that the system can handle
4. System behavior under different load conditions

## Integration with Azure Load Testing

You can also use this script with Azure Load Testing:

1. Create a new Azure Load Testing resource in the Azure Portal
2. Upload the locustfile_storefront.py script
3. Configure test parameters (virtual users, test duration, etc.)
4. Run the test and analyze results through the Azure Portal

## Troubleshooting Common Issues

- If you encounter connection errors, verify that the store-front service is accessible
- If API endpoint paths return 404 errors, you may need to adjust the paths in the script
- If authentication is required, modify the script to include appropriate headers

Remember to update the AKS service URL in the above commands with the actual external IP of your store-front service.
