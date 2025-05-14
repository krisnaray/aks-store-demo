# Product Service Load Testing Instructions

This document provides instructions for running load tests against the product-service API using the Locust script.

## Prerequisites

1. Ensure you have Python installed (Python 3.8 or higher recommended)
2. Install Locust:
   ```bash
   pip install locust
   ```

## Running the Load Test

### Option 1: Command Line Interface

To run the load test from the command line:

```bash
# Replace with your actual product-service external IP
locust -f product_service_locustfile.py --host=http://132.164.231.75 -u 30 -r 5 --run-time 5m
```

Parameters:
- `-f product_service_locustfile.py`: Specifies the Locust test script
- `--host`: The base URL of the product-service (use the external IP address)
- `-u 30`: Simulates 30 concurrent users
- `-r 5`: User spawn rate (5 users per second)
- `--run-time 5m`: Run the test for 5 minutes

### Option 2: Web UI

To run the load test with the Locust web interface:

```bash
# Replace with your actual product-service external IP
locust -f product_service_locustfile.py --host=http://132.164.231.75
```

1. Navigate to http://localhost:8089 in your web browser
2. Set the desired number of users and spawn rate
3. Click "Start swarming" to begin the test
4. Monitor real-time statistics and charts in the web interface

## Test Scenarios

The load test simulates the following API operations:

1. **Health Check**: Verifies the API's health endpoint
2. **List Products**: Fetches all products
3. **Get Product by ID**: Fetches a specific product by ID
4. **Add Product**: Creates a new product
5. **Update Product**: Updates an existing product
6. **Delete Product**: Deletes a product
7. **AI Health Check**: Checks the health of the AI integration
8. **Generate Description**: Uses the AI service to generate product descriptions

Each scenario is tagged, allowing you to run specific test cases:

```bash
# Run only the product creation tests
locust -f product_service_locustfile.py --host=http://132.164.231.75 -u 10 -r 2 --tags create

# Run only AI-related tests
locust -f product_service_locustfile.py --host=http://132.164.231.75 -u 5 -r 1 --tags ai
```

## Tips for Testing

1. **Start with a low number of users**: Begin with 5-10 users to ensure your test works properly
2. **Watch for errors**: Monitor the error rate - if it's high, your service might be overloaded
3. **Balance create/delete operations**: The script is designed to create and delete products to avoid filling the database
4. **AI service testing**: AI-related tests are set to not fail the entire test if the AI service is unavailable

## Understanding the Results

After running the test, Locust provides:

1. **Request Statistics**: Shows response times, error rates, and requests per second for each endpoint
2. **Charts**: Visualizes response times and request rates over time
3. **Failures**: Lists any failed requests with detailed error messages
4. **Download Data**: Option to download CSV reports for further analysis

## Potential Issues

1. If you see 404 errors on product operations, it might be because products are being deleted by other users
2. AI endpoints may fail if the AI service is not properly configured or available
3. High response times could indicate performance bottlenecks in your service

Remember to update the host URL with your actual product-service external IP address in the commands above.
