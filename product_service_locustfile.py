"""
Product Service Load Test Script
This Locust script tests the Product Service API endpoints based on the test-product-service.http file.
It includes health checks, listing products, creating products, updating products, fetching by ID, and deleting products.
"""

import json
import random
import string
import logging
from locust import HttpUser, task, between, tag

class ProductServiceUser(HttpUser):
    """
    Simulates a user interacting with the Product Service API.
    """
    # Wait between 1 and 3 seconds between tasks
    wait_time = between(1, 3)
    
    # Store created product IDs for later use
    created_product_ids = []
    
    def on_start(self):
        """Initialize the user session"""
        self.client.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    @tag('health')
    @task(2)
    def health_check(self):
        """Check the health endpoint of the product service"""
        with self.client.get(
            "/health",
            name="Health Check",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed with status {response.status_code}")
    
    @tag('list')
    @task(3)
    def get_products(self):
        """Get all products"""
        with self.client.get(
            "/",
            name="Get All Products",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    products = response.json()
                    # Store product IDs for later operations
                    if products and isinstance(products, list):
                        for product in products:
                            if "id" in product and product["id"] not in self.created_product_ids:
                                self.created_product_ids.append(product["id"])
                        response.success()
                    else:
                        response.failure("Invalid products response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to get products: {response.status_code}")
    
    @tag('create')
    @task(1)
    def add_product(self):
        """Add a new product"""
        # Generate a random product name
        product_name = f"Test Product {random.randint(1000, 9999)}"
        
        # Create product payload
        payload = {
            "id": 0,  # The API will assign an actual ID
            "name": product_name,
            "price": round(random.uniform(5.99, 199.99), 2),
            "description": f"This is a test product {product_name} created for load testing. " +
                          f"It features multiple great qualities and is perfect for testing. " +
                          f"Every pet owner should have this amazing product for their furry friend.",
            "image": "/placeholder.png"
        }
        
        with self.client.post(
            "/",
            name="Add Product",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    product = response.json()
                    if product and "id" in product:
                        # Store the ID for later operations
                        self.created_product_ids.append(product["id"])
                        response.success()
                    else:
                        response.failure("Invalid product creation response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to create product: {response.status_code}")
    
    @tag('detail')
    @task(2)
    def get_product_by_id(self):
        """Get a single product by ID"""
        if not self.created_product_ids:
            self.get_products()  # Fetch products first if we don't have any IDs
            return
            
        # Pick a random product ID
        product_id = random.choice(self.created_product_ids)
        
        with self.client.get(
            f"/{product_id}",
            name="Get Product By ID",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    product = response.json()
                    if product and "id" in product:
                        response.success()
                    else:
                        response.failure("Invalid product details")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            elif response.status_code == 404:
                # Product might have been deleted, remove from our list
                if product_id in self.created_product_ids:
                    self.created_product_ids.remove(product_id)
                response.failure(f"Product {product_id} not found")
            else:
                response.failure(f"Failed to get product {product_id}: {response.status_code}")
    
    @tag('update')
    @task(1)
    def update_product(self):
        """Update an existing product"""
        if not self.created_product_ids:
            self.get_products()  # Fetch products first if we don't have any IDs
            return
            
        # Pick a random product ID
        product_id = random.choice(self.created_product_ids)
        
        # Create update payload
        payload = {
            "id": product_id,
            "name": f"Updated Product {random.randint(1000, 9999)}",
            "price": round(random.uniform(5.99, 199.99), 2),
            "description": f"This is an updated test product description with plenty of text to meet the minimum " +
                          f"length requirements. It provides detailed information about the product features " +
                          f"and benefits for your pets. Every pet owner would love this amazing product.",
            "image": "/placeholder.png"
        }
        
        with self.client.put(
            "/",
            name="Update Product",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    product = response.json()
                    if product and "id" in product:
                        response.success()
                    else:
                        response.failure("Invalid product update response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            elif response.status_code == 404:
                # Product might not exist, remove from our list
                if product_id in self.created_product_ids:
                    self.created_product_ids.remove(product_id)
                response.failure(f"Product {product_id} not found for update")
            else:
                response.failure(f"Failed to update product {product_id}: {response.status_code}")
    
    @tag('delete')
    @task(1)
    def delete_product(self):
        """Delete a product"""
        if not self.created_product_ids:
            self.get_products()  # Fetch products first if we don't have any IDs
            return
            
        # Pick a random product ID to delete
        product_id = random.choice(self.created_product_ids)
        
        with self.client.delete(
            f"/{product_id}",
            name="Delete Product",
            catch_response=True
        ) as response:
            if response.status_code in [200, 204]:
                # Remove the product ID from our list
                if product_id in self.created_product_ids:
                    self.created_product_ids.remove(product_id)
                response.success()
            elif response.status_code == 404:
                # Product might not exist, remove from our list anyway
                if product_id in self.created_product_ids:
                    self.created_product_ids.remove(product_id)
                response.failure(f"Product {product_id} not found for deletion")
            else:
                response.failure(f"Failed to delete product {product_id}: {response.status_code}")
    
    
if __name__ == "__main__":
    # This allows running the script directly for testing purposes
    pass
