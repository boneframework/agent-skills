---
name: bone-open-api
description: "Handles OpenAPI/Swagger documentation and API specification in Bone Framework applications using delboy1978uk/bone-open-api package for TypeSpec-based API documentation."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "openapi", "swagger", "api", "documentation", "typespec"]
trigger_patterns:
  - "bone-open-api"
  - "openapi"
  - "swagger"
  - "api documentation"
  - "typespec"
---

# Bone Open API Skill

## When to Use
Activate this skill when creating and managing OpenAPI (Swagger) documentation for REST APIs in Bone Framework applications using the delboy1978uk/bone-open-api package with TypeSpec.

## Package Information
- **Package**: `delboy1978uk/bone-open-api`
- **License**: MIT
- **PHP Version**: ^8.2
- **Dependencies**: bone-oauth2, laminas-diactoros
- **TypeSpec**: TypeScript-based API specification language

## Installation

```bash
composer require delboy1978uk/bone-open-api
```

## Setup Steps

### Step 1: Register Package
```php
// config/packages.php
return [
    'packages' => [
        \Bone\OpenApi\OpenApiPackage::class,
        // ... other packages
    ]
];
```

### Step 2: Create Configuration
```php
// config/openapi.php
return [
    'docs' => 'data/docs/api.json',
    'swaggerClient' => [
        'clientId' => '',      // For OAuth2
        'clientSecret' => ''   // For OAuth2
    ]
];
```

### Step 3: Deploy Assets
```bash
# Deploy assets to public directory
vendor/bin/bone assets:deploy
```

### Step 4: Setup TypeSpec
```bash
# If no npm project exists
vendor/bin/bone docs:setup

# Update package.json with TypeSpec dependencies
pnpm add -D \
  @typespec/compiler@^1.5.0 \
  @typespec/http@^1.5.0 \
  @typespec/openapi3@^1.5.0 \
  @typespec/rest@^0.75.0 \
  @typespec/versioning@^0.75.0
```

### Step 5: Generate Documentation
```bash
# Run TypeSpec compiler
pnpm run docs

# View documentation
# Open http://localhost:8080/api/docs
```

## TypeSpec API Definition

### Basic API Specification
```typespec
// docs/api.tspec

@swaggerEnabled
@server("https://api.example.com", "Production Server")
@service({
    title: "My Application API",
    description: "API for managing users and resources",
    version: "1.0.0"
})
namespace MyApi;

// Define models
model User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    createdAt: datetime;
}

model UserInput {
    email: string;
    firstName: string;
    lastName: string;
}

model ErrorResponse {
    error: string;
    message: string;
}

// Define operations
op listUsers is ApiCall<{}, User[]>;

op getUser @{
    path: "/users/{id}"
}:
    Input<{id: string}>,
    User;

op createUser @{
    path: "/users";
    method: "POST"
}:
    Input<UserInput>,
    User;

op updateUser @{
    path: "/users/{id}";
    method: "PUT"
}:
    Input<{id: string, body: UserInput}>,
    User;

op deleteUser @{
    path: "/users/{id}";
    method: "DELETE"
}:
    Input<{id: string}>,
    void;
```

### OAuth2 Integration
```typespec
@oauth2({
    authorizationUrl: "https://example.com/oauth/authorize",
    tokenUrl: "https://example.com/oauth/token",
    scopes: {
        read: "Read access",
        write: "Write access",
        admin: "Admin access"
    }
})
namespace MyApi;

@op
@tag("Users")
op listUsers is ApiCall<{}, User[]>;
```

### Path Parameters
```typespec
op getUser @{
    path: "/users/{userId}"
}:
    Input<{userId: string}>,
    User;

op listUserOrders @{
    path: "/users/{userId}/orders"
}:
    Input<{userId: string}>,
    Order[];
```

### Query Parameters
```typespec
op listUsers @{
    path: "/users";
    parameters: {
        page?: int32;
        limit?: int32;
        status?: string;
        search?: string;
    }
}:
    {}, User[];
```

### Request Body
```typespec
op createUser @{
    path: "/users";
    method: "POST";
    parameters: {
        body: {
            email: string;
            firstName: string;
            lastName: string;
            password: string;
        }
    }
}:
    {}, User;
```

### Response Codes
```typespec
op createUser @{
    path: "/users";
    method: "POST";
    responses: {
        201: User;
        400: ErrorResponse;
        409: ErrorResponse;  // Conflict (email already exists)
    }
}:
    Input<UserInput>,
    User;
```

## API Documentation Endpoint

### Documentation Routes
```php
// api/docs - TypeSpec generated documentation
$router->get('/api/docs', [OpenApiController::class, 'indexAction']);

// api/documentation - OpenAPI JSON
$router->get('/api/documentation', [OpenApiController::class, 'jsonAction']);

// api/swagger - Swagger UI
$router->get('/api/swagger', [OpenApiController::class, 'swaggerAction']);
```

### OpenAPI Controller
```php
class OpenApiController extends Controller
{
    public function indexAction()
    {
        $docs = file_get_contents('data/docs/api.html');
        return $this->view->renderRaw($docs);
    }
    
    public function jsonAction()
    {
        $openapi = json_decode(file_get_contents('data/docs/api.json'), true);
        return $this->jsonResponse($openapi);
    }
    
    public function swaggerAction()
    {
        $html = file_get_contents('data/docs/swagger.html');
        return $this->view->renderRaw($html);
    }
}
```

## TypeSpec Features

### Models
```typespec
// Basic model
model User {
    id: string;
    email: string;
    name: string;
}

// With metadata
model User @{
    description: "User account"
} {
    id: string @{ description: "Unique identifier" };
    email: string @{ format: "email" };
    createdAt: datetime @{ description: "Account creation date" };
}

// Nested models
model Order {
    id: string;
    user: User;
    items: OrderItem[];
    total: number;
}

model OrderItem {
    productId: string;
    quantity: int32;
    price: number;
}
```

### Enums
```typespec
enum UserStatus {
    active: "Active",
    inactive: "Inactive",
    pending: "Pending"
}

model User {
    id: string;
    status: UserStatus;
}
```

### Inheritance
```typespec
model BaseResource {
    id: string;
    createdAt: datetime;
    updatedAt: datetime;
}

model User extends BaseResource {
    email: string;
    name: string;
}

model Product extends BaseResource {
    name: string;
    price: number;
}
```

### Generic Types
```typespec
model Paginated<T> {
    data: T[];
    meta: {
        page: int32;
        limit: int32;
        total: int32;
    };
}

op listUsers is ApiCall<{}, Paginated<User>>;
```

## OpenAPI JSON Output

### Generated Documentation
```json
{
    "openapi": "3.0.0",
    "info": {
        "title": "My Application API",
        "version": "1.0.0",
        "description": "API for managing users and resources"
    },
    "servers": [
        {
            "url": "https://api.example.com",
            "description": "Production Server"
        }
    ],
    "paths": {
        "/users": {
            "get": {
                "summary": "List all users",
                "tags": ["Users"],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create user",
                "tags": ["Users"],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/UserInput"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "User created",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/User"}
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "createdAt": {"type": "string", "format": "date-time"}
                }
            }
        },
        "securitySchemes": {
            "OAuth2": {
                "type": "oauth2",
                "flows": {
                    "clientCredentials": {
                        "tokenUrl": "https://example.com/oauth/token",
                        "scopes": {
                            "read": "Read access",
                            "write": "Write access"
                        }
                    }
                }
            }
        }
    }
}
```

## Security

### OAuth2 Protection
```typescript
@oauth2({
    authorizationUrl: "https://example.com/oauth/authorize",
    tokenUrl: "https://example.com/oauth/token"
})
namespace MyApi;

op protectedEndpoint is ApiCall<{}, Data>;
```

### API Key Protection
```typescript
@apiKey({
    name: "X-API-Key",
    in: "header"
})
namespace MyApi;

op apiEndpoint is ApiCall<{}, Data>;
```

## TypeSpec Best Practices

1. **Version your API**: Use `@version` decorator
2. **Document all parameters**: Add descriptions to all inputs
3. **Specify response codes**: Document all possible responses
4. **Use descriptive names**: Clear operation and model names
5. **Group operations**: Use `@tag` for organization
6. **Handle errors**: Document error responses
7. **Secure endpoints**: Apply authentication decorators
8. **Use types consistently**: Define reusable types
9. **Version compatibility**: Use `@deprecated` when needed
10. **Test documentation**: Verify generated docs are correct

## Troubleshooting

### Common Issues

1. **TypeSpec compilation errors**
   - Check syntax errors in .tspec file
   - Verify all imports are correct
   - Check TypeScript dependencies installed

2. **Empty documentation**
   - Verify TypeSpec files are in correct location
   - Check file permissions
   - Review TypeSpec compiler output

3. **Swagger UI not loading**
   - Check browser console for errors
   - Verify JSON file is accessible
   - Check CORS settings
