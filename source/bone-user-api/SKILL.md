---
name: bone-user-api
description: "Handles REST API endpoints for user management in Bone Framework applications using delboy1978uk/bone-user-api package with OAuth2 integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "api", "rest", "user-api", "oauth2", "json"]
trigger_patterns:
  - "bone-user-api"
  - "user-api"
  - "rest api"
  - "user endpoints"
  - "oauth2 api"
---

# Bone User API Skill

## When to Use
Activate this skill when implementing REST API endpoints for user management in Bone Framework applications using the delboy1978uk/bone-user-api package with OAuth2 integration.

## Package Information
- **Package**: `delboy1978uk/bone-user-api`
- **License**: MIT
- **PHP Version**: ^8.2
- **Dependencies**: bone-oauth2, bone-user

## Installation

```bash
composer require delboy1978uk/bone-user-api
```

## Package Features

### Key Features
- OAuth2 API endpoints for user operations
- RESTful user management endpoints
- JSON-based request/response format
- OAuth2 authentication and authorization
- Integration with bone-user package

## Package Registration

```php
// config/packages.php
return [
    'packages' => [
        \Bone\User\Api\BoneUserApiPackage::class,
        // ... other packages
    ]
];
```

## API Endpoints

### User Endpoints
```
GET    /api/users             - List all users (admin)
POST   /api/users             - Create user (admin)
GET    /api/users/{id}        - Get user by ID (admin)
PUT    /api/users/{id}        - Update user (admin)
DELETE /api/users/{id}        - Delete user (admin)
GET    /api/users/me          - Get current user (auth)
```

### Authentication Endpoints (via bone-oauth2)
```
POST   /oauth/token           - Get access token
GET    /oauth/info            - Get OAuth2 configuration
POST   /oauth/revoke          - Revoke token
```

## Request/Response Format

### Request Headers
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer {access_token}
```

### Success Response Format
```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "user@example.com",
        "firstName": "John",
        "lastName": "Doe"
    },
    "message": "Optional success message"
}
```

### Error Response Format
```json
{
    "success": false,
    "message": "Error description",
    "errors": {
        "field_name": "Field-specific error"
    },
    "code": 400
}
```

## API Endpoints in Detail

### List Users
```http
GET /api/users?page=1&limit=10&sort=createdAt&order=DESC
Authorization: Bearer {admin_token}
```

```json
{
    "success": true,
    "data": {
        "users": [
            {
                "id": 1,
                "email": "user1@example.com",
                "firstName": "John",
                "lastName": "Doe",
                "createdAt": "2024-01-15T10:30:00+00:00",
                "isActive": true
            }
        ],
        "meta": {
            "page": 1,
            "limit": 10,
            "total": 15,
            "totalPages": 2
        }
    }
}
```

### Get User by ID
```http
GET /api/users/123
Authorization: Bearer {admin_token}
```

```json
{
    "success": true,
    "data": {
        "id": 123,
        "email": "user@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "createdAt": "2024-01-15T10:30:00+00:00",
        "isActive": true,
        "roles": ["user"]
    }
}
```

### Create User (Admin)
```http
POST /api/users
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "email": "newuser@example.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "password": "password123",
    "isActive": true,
    "roles": ["user"]
}
```

```json
{
    "success": true,
    "data": {
        "id": 124,
        "email": "newuser@example.com",
        "firstName": "Jane",
        "lastName": "Smith",
        "createdAt": "2024-01-16T14:00:00+00:00",
        "isActive": true
    },
    "message": "User created successfully"
}
```

### Update User (Admin)
```http
PUT /api/users/123
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "firstName": "John",
    "lastName": "Smith",
    "isActive": false,
    "roles": ["user", "moderator"]
}
```

```json
{
    "success": true,
    "data": {
        "id": 123,
        "email": "user@example.com",
        "firstName": "John",
        "lastName": "Smith",
        "isActive": false,
        "roles": ["user", "moderator"]
    },
    "message": "User updated successfully"
}
```

### Delete User (Admin)
```http
DELETE /api/users/123
Authorization: Bearer {admin_token}
```

```json
{
    "success": true,
    "message": "User deleted successfully"
}
```

### Get Current User
```http
GET /api/users/me
Authorization: Bearer {user_token}
```

```json
{
    "success": true,
    "data": {
        "id": 123,
        "email": "user@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "createdAt": "2024-01-15T10:30:00+00:00",
        "roles": ["user"]
    }
}
```

## Profile Endpoints

### Update Profile
```http
PUT /api/profile
Authorization: Bearer {user_token}
Content-Type: application/json

{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com"
}
```

```json
{
    "success": true,
    "data": {
        "id": 123,
        "email": "john.doe@example.com",
        "firstName": "John",
        "lastName": "Doe"
    },
    "message": "Profile updated successfully"
}
```

### Change Password
```http
POST /api/profile/password
Authorization: Bearer {user_token}
Content-Type: application/json

{
    "currentPassword": "oldpassword123",
    "password": "newpassword456",
    "passwordConfirmation": "newpassword456"
}
```

```json
{
    "success": true,
    "message": "Password changed successfully"
}
```

## Query Parameters

### List Filters
| Parameter | Description | Example |
|-----------|-------------|---------|
| `page` | Page number | `1` |
| `limit` | Items per page | `10` |
| `sort` | Sort field | `createdAt` |
| `order` | Sort order | `ASC` or `DESC` |
| `filter[field]` | Filter by field | `filter[email]=john` |

### Filter Examples
```
GET /api/users?filter[isActive]=1
GET /api/users?filter[firstName]=John
GET /api/users?sort=createdAt&order=DESC&page=1&limit=20
```

## OAuth2 Integration

### Access Token Response
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 300,
    "refresh_token": "def50200d51c28b8a9c4...",
    "scope": "user:read user:write"
}
```

### Protected API Routes
```php
use Bone\OAuth2\Middleware\ResourceServerMiddleware;

// User API routes
$router->group('/api/users', function ($router) {
    $router->get('', [UserController::class, 'indexAction']);
    $router->post('', [UserController::class, 'createAction']);
})->middleware(ResourceServerMiddleware::class);

// Admin-only routes
$router->get('/api/users/{id}', [UserController::class, 'viewAction'])
    ->middleware(new \Bone\Passport\Middleware\PassportControlMiddleware('admin'));

// User-specific routes
$router->get('/api/users/me', [UserController::class, 'meAction']);
```

## Validation Rules

### User Creation
```json
{
    "email": {
        "required": true,
        "type": "email",
        "unique": true
    },
    "firstName": {
        "required": true,
        "minLength": 1,
        "maxLength": 50
    },
    "lastName": {
        "required": true,
        "minLength": 1,
        "maxLength": 50
    },
    "password": {
        "required": true,
        "minLength": 8
    }
}
```

### User Update
```json
{
    "firstName": {
        "required": false,
        "minLength": 1,
        "maxLength": 50
    },
    "lastName": {
        "required": false,
        "minLength": 1,
        "maxLength": 50
    },
    "email": {
        "required": false,
        "type": "email",
        "unique": true
    }
}
```

## API Documentation

### OpenAPI Specification
```yaml
paths:
  /api/users:
    get:
      summary: List all users
      security:
        - Bearer: [admin]
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 10 }
      responses:
        '200':
          description: Successful operation
    post:
      summary: Create user
      security:
        - Bearer: [admin]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string, format: email }
                password: { type: string }
  /api/users/me:
    get:
      summary: Get current user
      security:
        - Bearer: [user:read]
      responses:
        '200':
          description: Current user details
```

## Testing API

### Unit Tests
```php
public function testListUsers(): void
{
    // Get admin token
    $token = $this->getAdminToken();
    
    // List users
    $response = $this->get('/api/users', [
        'Authorization' => 'Bearer ' . $token,
    ]);
    
    $this->assertEquals(200, $response->getStatusCode());
    $data = json_decode($response->getBody(), true);
    
    $this->assertArrayHasKey('users', $data['data']);
    $this->assertArrayHasKey('meta', $data['data']);
}

public function testCreateUser(): void
{
    $token = $this->getAdminToken();
    
    $response = $this->post('/api/users', [
        'Authorization' => 'Bearer ' . $token,
        'Content-Type' => 'application/json',
    ], json_encode([
        'email' => 'test@example.com',
        'firstName' => 'John',
        'lastName' => 'Doe',
        'password' => 'password123',
    ]));
    
    $this->assertEquals(201, $response->getStatusCode());
    $data = json_decode($response->getBody(), true);
    
    $this->assertEquals('test@example.com', $data['data']['email']);
}
```

## Best Practices

1. **Use OAuth2 for authentication**: Never send credentials in API requests
2. **Validate all input**: Always validate request data
3. **Return clear errors**: Include error messages and codes
4. **Use proper status codes**: 200, 201, 400, 401, 403, 404, 500
5. **Paginate lists**: Always paginate large result sets
6. **Include metadata**: Add pagination, sorting info
7. **Version API**: Use versioned endpoints (/api/v1/)
8. **Secure sensitive data**: Never return passwords
9. **Log API activity**: Track API usage and errors
10. **Rate limit endpoints**: Protect from abuse

## Error Responses

```json
// 400 Bad Request
{
    "success": false,
    "message": "Validation failed",
    "errors": {
        "email": "Invalid email address",
        "password": "Password too short"
    },
    "code": 400
}

// 401 Unauthorized
{
    "success": false,
    "message": "Invalid or expired token",
    "code": 401
}

// 403 Forbidden
{
    "success": false,
    "message": "You do not have permission",
    "code": 403
}

// 404 Not Found
{
    "success": false,
    "message": "User not found",
    "code": 404
}

// 409 Conflict
{
    "success": false,
    "message": "Email already exists",
    "code": 409
}
```
