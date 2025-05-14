"""
AKS Store Demo - Storefront Load Test Script
This Locust script simulates real user behavior on the AKS Store Demo storefront application.
It includes browsing products, viewing product details, adding items to cart, and completing checkout.
"""

import json
import random
import logging
from locust import HttpUser, task, between, tag

class StoreUser(HttpUser):
    """
    Simulates a user browsing the AKS Store Demo storefront application.
    """
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    # Store user session data
    product_ids = []
    cart_items = []
    
    def on_start(self):
        """Initialize the user session"""
        self.client.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # Get products list to use in subsequent requests
        self.get_all_products()
    
    @tag('browse')
    @task(3)
    def get_all_products(self):
        """Browse the product catalog"""
        with self.client.get(
            "/api/products",
            name="Get All Products",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    products = response.json()
                    if products and isinstance(products, list) and len(products) > 0:
                        # Store product IDs for later use
                        self.product_ids = [product["productId"] for product in products if "productId" in product]
                        response.success()
                    else:
                        response.failure("No products found in the response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to get products: {response.status_code}")
    
    @tag('product_detail')
    @task(2)
    def get_product_details(self):
        """View product details"""
        if not self.product_ids:
            self.get_all_products()
            return
        
        # Randomly select a product
        product_id = random.choice(self.product_ids)
        
        with self.client.get(
            f"/api/products/{product_id}",
            name="Get Product Details",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    product = response.json()
                    if product and "productId" in product:
                        response.success()
                    else:
                        response.failure("Invalid product details")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to get product details: {response.status_code}")
    
    @tag('cart')
    @task(1)
    def add_to_cart(self):
        """Add a product to the shopping cart"""
        if not self.product_ids:
            self.get_all_products()
            return
        
        # Randomly select a product
        product_id = random.choice(self.product_ids)
        quantity = random.randint(1, 3)
        
        payload = {
            "productId": product_id,
            "quantity": quantity
        }
        
        with self.client.post(
            "/api/orders/items",
            name="Add to Cart",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    item = response.json()
                    if item:
                        self.cart_items.append(item)
                        response.success()
                    else:
                        response.failure("Invalid cart item response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to add item to cart: {response.status_code}")
    
    @tag('cart')
    @task(1)
    def view_cart(self):
        """View the shopping cart"""
        with self.client.get(
            "/api/orders/cart",
            name="View Cart",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    cart = response.json()
                    response.success()
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to view cart: {response.status_code}")
    
    @tag('checkout')
    @task(1)
    def checkout(self):
        """Complete checkout process"""
        if not self.cart_items:
            # Add at least one item to cart before checkout
            self.add_to_cart()
            
        # Customer information for checkout
        customer = {
            "firstName": "Test",
            "lastName": "User",
            "email": f"test.user.{random.randint(1000, 9999)}@example.com",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "TS",
            "zipCode": "12345"
        }
        
        with self.client.post(
            "/api/orders/checkout",
            name="Checkout",
            json=customer,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                try:
                    order = response.json()
                    if order and "orderId" in order:
                        # Reset cart after successful checkout
                        self.cart_items = []
                        response.success()
                    else:
                        response.failure("Invalid order response")
                except json.JSONDecodeError:
                    response.failure("Failed to parse JSON response")
            else:
                response.failure(f"Failed to checkout: {response.status_code}")
    
    @tag('browse')
    @task(2)
    def browse_random_products(self):
        """Browse random products from the catalog"""
        if not self.product_ids:
            self.get_all_products()
            return
            
        # Simulate a user browsing multiple products
        for _ in range(random.randint(2, 5)):
            if self.product_ids:
                product_id = random.choice(self.product_ids)
                self.client.get(
                    f"/api/products/{product_id}",
                    name="Browse Random Products"
                )
                # Pause briefly between product views
                self.wait()

if __name__ == "__main__":
    # This allows running the script directly for testing purposes
    pass
