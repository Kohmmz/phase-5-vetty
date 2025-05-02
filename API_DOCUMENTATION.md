# Vetty Backend API Documentation

This document provides information on how to access and use the API documentation for the Vetty Backend application.

## Accessing the API Documentation

Once the application is running, you can access the API documentation in JSON format at:

```
http://127.0.0.1:5001/api/docs/
```

This endpoint returns a comprehensive JSON object describing all available endpoints, their methods, required parameters, and expected responses.

## API Endpoints

The API is organized into the following sections:

### Authentication
- `POST /signup` - Create a new user account
- `POST /login` - Login with existing credentials
- `POST /logout` - Logout the current user

### Users
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get a specific user by ID

### Products
- `GET /products` - Get all products
- `POST /products` - Create a new product
- `GET /products/{product_id}` - Get a specific product by ID

### Services
- `GET /services` - Get all services
- `POST /services` - Create a new service
- `GET /services/{service_id}` - Get a specific service by ID

### Carts
- `GET /carts` - Get all carts
- `POST /carts` - Create a new cart
- `GET /carts/{cart_id}` - Get a specific cart by ID
- `DELETE /carts/{cart_id}` - Delete a cart by ID
- `POST /carts/items` - Add an item to a cart

### Orders
- `GET /orders` - Get all orders for the authenticated user
- `POST /orders` - Create a new order
- `GET /orders/{order_id}` - Get a specific order by ID
- `GET /orders/{order_id}/items` - Get all items for a specific order

## Request and Response Examples

### Creating a User
```json
POST /signup
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### Creating a Cart
```json
POST /carts
{
  "user_id": 1
}
```

### Adding an Item to a Cart
```json
POST /carts/items
{
  "cart_id": 1,
  "product_id": 1,
  "quantity": 2
}
```

### Creating an Order
```json
POST /orders
{
  "total_price": 199.98,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 99.99
    }
  ]
}
```

## Authentication

Most endpoints require authentication using JWT tokens. To authenticate:

1. Make a POST request to `/login` with your credentials
2. Use the returned access token in subsequent requests by adding it to the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```
