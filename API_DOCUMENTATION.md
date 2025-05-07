# Vetty Backend API Documentation

This document provides information on how to access and use the API for the Vetty Backend application deployed at Render.

## API Status (Updated: May 7, 2025)

The API is **PARTIALLY WORKING** with a 61.9% success rate based on comprehensive testing. Most read-only endpoints are functioning correctly, while endpoints requiring authentication may have issues.

### ✅ Confirmed Working Endpoints

- `GET /products` - Returns all products successfully
- `GET /products/{id}` - Returns specific product details
- `GET /products?name=dog` - Search functionality works for filtering products by name
- `GET /products?category=food` - Category filtering works
- `GET /services` - Returns all available services
- `GET /services/{id}` - Returns specific service details
- `GET /carts` - Returns an empty array (authentication likely needed for populated results)

## API Base URL

The API is accessible at the following base URL (note: no `/api` prefix is needed):

```
https://phase-5-vetty-backend.onrender.com
```

## API Endpoints

The API is organized into the following sections. Please note that while all endpoints are documented here, only the endpoints marked with ✅ have been confirmed working in the current deployment.

### Authentication (⚠️ Authentication currently has issues)
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Login with existing credentials
- `POST /auth/logout` - Logout the current user
- `GET /auth/auto-login` - Automatically login a user with a valid JWT token

### Users 
- `GET /users` - Get all users (requires authentication)
- `GET /users/{user_id}` - Get a specific user by ID (requires authentication)
- `PUT /users/{user_id}` - Update a user (requires authentication)
- `DELETE /users/{user_id}` - Delete a user (requires authentication)
- `POST /users/verify-otp` - Verify OTP for user email verification

### Products
- ✅ `GET /products` - Get all products
- ✅ `GET /products?name=search_term` - Search products by name
- ✅ `GET /products?category=category_name` - Filter products by category
- ✅ `GET /products/{product_id}` - Get a specific product by ID
- `POST /products` - Create a new product (requires authentication)
- `PUT /products/{product_id}` - Update a product (requires authentication)
- `DELETE /products/{product_id}` - Delete a product (requires authentication)

### Services
- ✅ `GET /services` - Get all services
- ✅ `GET /services/{service_id}` - Get a specific service by ID
- `POST /services` - Create a new service (requires authentication)
- `PUT /services/{service_id}` - Update a service (requires authentication)
- `DELETE /services/{service_id}` - Delete a service (requires authentication)

### Carts
- ✅ `GET /carts` - Get all carts (returns empty array without authentication)
- `POST /carts` - Create a new cart (requires authentication)
- `GET /carts/{cart_id}` - Get a specific cart by ID (requires authentication)
- `DELETE /carts/{cart_id}` - Delete a cart by ID (requires authentication)
- `POST /carts/items` - Add an item to a cart (requires authentication)

### Orders
- `GET /orders` - Get all orders for the authenticated user (requires authentication)
- `POST /orders` - Create a new order (requires authentication)
- `GET /orders/{order_id}` - Get a specific order by ID (requires authentication)
- `GET /orders/{order_id}/items` - Get all items for a specific order (requires authentication)

## Sample Request and Response Examples

### Working Endpoint: Get All Products
```
GET /products

Response (200 OK):
[
  {
    "category": "Food",
    "created_at": "Tue, 06 May 2025 17:22:12 GMT",
    "description": "Premium dog food",
    "id": 1,
    "name": "Dog Food",
    "price": 20.99,
    "stock_quantity": 100,
    "updated_at": null
  },
  {
    "category": "Toys",
    "created_at": "Tue, 06 May 2025 17:22:12 GMT",
    "description": "Interactive cat toy",
    "id": 2,
    "name": "Cat Toy",
    "price": 5.99,
    "stock_quantity": 50,
    "updated_at": null
  }
]
```

### Working Endpoint: Get Product by ID
```
GET /products/1

Response (200 OK):
{
  "category": "Food",
  "created_at": "Tue, 06 May 2025 17:22:12 GMT",
  "description": "Premium dog food",
  "id": 1,
  "name": "Dog Food",
  "price": 20.99,
  "stock_quantity": 100,
  "updated_at": null
}
```

### Working Endpoint: Get All Services
```
GET /services

Response (200 OK):
[
  {
    "created_at": "Tue, 06 May 2025 17:22:12 GMT",
    "description": "Full grooming service for pets",
    "id": 1,
    "name": "Grooming",
    "price": 50.0,
    "updated_at": null
  },
  {
    "created_at": "Tue, 06 May 2025 17:22:12 GMT",
    "description": "Comprehensive health checkup for pets",
    "id": 2,
    "name": "Veterinary Checkup",
    "price": 75.0,
    "updated_at": null
  }
]
```

### Authentication (Not Currently Working)

Most endpoints require authentication using JWT tokens. To authenticate when the service is fully operational:

1. Make a POST request to `/auth/login` with your credentials:
   ```json
   POST /auth/login
   {
     "email": "your.email@example.com",
     "password": "your_password"
   }
   ```

2. Use the returned access token in subsequent requests by adding it to the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```

## Deployment Information

This API is deployed on Render with a PostgreSQL database. The following information may be useful for debugging connection issues:

- The backend is configured to use CORS to allow requests from the frontend domain
- The database schema includes foreign key constraints that require specific creation order (users before carts, etc.)
- The API does not require the `/api` prefix in the URL which was originally documented

## Known Issues

1. Authentication endpoints are currently not working as expected
2. Endpoints requiring authentication cannot be tested without a valid token
3. Some POST operations may result in 500 Internal Server Error due to database issues
