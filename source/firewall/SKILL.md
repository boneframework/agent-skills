---
name: bone-firewall
description: "Handles route-based firewall and middleware management in Bone Framework applications using delboy1978uk/bone-firewall package with route blocking and per-route middleware support."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "firewall", "security", "middleware", "acl"]
trigger_patterns:
  - "firewall"
  - "route firewall"
  - "security"
  - "middleware"
  - "blocked routes"
  - "access control"
---

# Bone Firewall Skill

## When to Use
Activate this skill when implementing route-based security, access control, or per-route middleware in a Bone Framework application using the `delboy1978uk/bone-firewall` package.

## Package Information
- **Package**: `delboy1978uk/bone-firewall`
- **Dependencies**: bone-router, bone-http, PSR interfaces
- **License**: MIT
- **PHP Version**: ^8.2

## Architecture

### FirewallPackage
The main package class implementing registration interfaces:
- `RegistrationInterface` - Adds package to container
- `GlobalMiddlewareRegistrationInterface` - Registers global middleware

### RouteFirewall
The core middleware that inspects routes and applies blocking/mediation:
- Implements `MiddlewareInterface`
- Checks routes against blocked list
- Applies per-route middleware

## Core Components

### FirewallPackage
```php
class FirewallPackage implements RegistrationInterface, GlobalMiddlewareRegistrationInterface
{
    public function addToContainer(Container $c): void
    {
        // Package initialization
    }
    
    public function getMiddleware(Container $c): array
    {
        return [new RouteFirewall($c)];
    }
    
    public function getGlobalMiddleware(Container $c): array
    {
        return [RouteFirewall::class];
    }
}
```

### RouteFirewall
```php
class RouteFirewall implements MiddlewareInterface
{
    private $router;
    private $blockedRoutes;
    private $middlewares;
    private $container;
    
    public function __construct(Container $c)
    {
        $router = $c->get(Router::class);
        $blockedRoutes = $c->has('blockedRoutes') ? $c->get('blockedRoutes') : [];
        $middlewares = $c->has('routeMiddleware') ? $c->get('routeMiddleware') : [];
        // ...
    }
    
    public function process($request, $handler): ResponseInterface
    {
        // Inspect routes, block or add middleware
    }
}
```

## Configuration

### blockedRoutes Configuration
Block specific routes from being accessible:

```php
// config/bone-firewall.php
return [
    'blockedRoutes' => [
        '/admin/backup',           // Single route
        '/admin/settings',         // Another route
        'POST' => [
            '/api/dangerous',       // POST-only block
        ],
        'DELETE' => [
            '/admin/delete-all',    // DELETE-only block
        ],
    ],
];
```

### routeMiddleware Configuration
Apply middleware to specific routes:

```php
// config/bone-firewall.php
return [
    'routeMiddleware' => [
        // Per-path middleware
        '/admin' => [
            AdminMiddleware::class,
            AuthMiddleware::class,
        ],
        
        // Per-method middleware
        'POST' => [
            '/api/upload' => [UploadValidationMiddleware::class],
        ],
        'GET' => [
            '/api/cache' => [CacheMiddleware::class],
        ],
    ],
];
```

## Route Blocking

### Block All Methods
```php
// Block entire route for all methods
'blockedRoutes' => ['/admin/backup']
```

### Block Specific Methods
```php
// Block only POST requests
'blockedRoutes' => ['POST' => ['/api/delete-all']]

// Block only DELETE requests
'blockedRoutes' => ['DELETE' => ['/admin/users/*']]
```

### Block Multiple Methods
```php
'blockedRoutes' => [
    'POST' => ['/api/create', '/api/update'],
    'DELETE' => ['/api/remove'],
    '/admin/secret'  // All methods blocked
]
```

## Per-Route Middleware

### Apply Middleware to Path
```php
'routeMiddleware' => [
    '/admin' => [AdminMiddleware::class],
    '/api' => [ApiMiddleware::class],
]
```

### Apply Multiple Middleware
```php
'routeMiddleware' => [
    '/admin' => [
        AdminMiddleware::class,
        RoleCheckMiddleware::class,
    ],
]
```

### Method-Specific Middleware
```php
'routeMiddleware' => [
    'POST' => [
        '/api/upload' => [FileUploadMiddleware::class],
    ],
]
```

## Usage Examples

### 1. Blocking Admin Routes
```php
// config/bone-firewall.php
return [
    'blockedRoutes' => [
        '/admin/backup',
        '/admin/settings/restore',
    ],
];
```

### 2. Securing Admin Area
```php
// config/bone-firewall.php
return [
    'routeMiddleware' => [
        '/admin' => [
            SessionAuth::class,
            RoleCheck::class,
            AdminMiddleware::class,
        ],
    ],
];
```

### 3. API Rate Limiting
```php
// config/bone-firewall.php
return [
    'routeMiddleware' => [
        'GET' => [
            '/api/users' => [RateLimitMiddleware::class],
            '/api/posts' => [RateLimitMiddleware::class],
        ],
        'POST' => [
            '/api/comments' => [RateLimitMiddleware::class],
        ],
    ],
];
```

### 4. Combined Blocking and Middleware
```php
// config/bone-firewall.php
return [
    'blockedRoutes' => [
        '/admin/secrets',
    ],
    'routeMiddleware' => [
        '/admin' => [AdminMiddleware::class],
        '/api' => [ApiMiddleware::class],
    ],
];
```

## Middleware Interface Implementation

The firewall supports both middleware instances and class names:

### By Instance
```php
'routeMiddleware' => [
    '/path' => [new CustomMiddleware()],
]
```

### By Class Name
```php
'routeMiddleware' => [
    '/path' => [CustomMiddleware::class],
]
```

The firewall resolves class names via the container:
```php
if ($middleware instanceof MiddlewareInterface) {
    $route->middleware($middleware);
} elseif ($this->container->has($middleware)) {
    $middleware = $this->container->get($middleware);
    $route->middleware($middleware);
} else {
    $route->middleware(new $middleware());
}
```

## Router Integration

The firewall modifies routes before dispatch:
```php
foreach ($routes as $route) {
    $path = $route->getPath();
    $method = $route->getMethod();
    
    // Block routes
    if (in_array($path, $this->blockedRoutes)) {
        $this->router->removeRoute($route);
        break;
    }
    
    // Add middleware
    if (array_key_exists($path, $this->middlewares)) {
        $this->handleMiddleware($path, $route, $method);
    }
}
```

## Best Practices

1. **Place firewall early**: Register FirewallPackage early in packages.php
2. **Use path patterns**: Group related routes with common prefixes
3. **Block dangerous methods**: Block DELETE/POST for sensitive routes
4. **Keep middleware light**: Firewalls should be fast
5. **Log blocked requests**: Track security events
6. **Test blocking**: Verify routes are properly blocked
7. **Order matters**: Package order affects middleware stack
8. **Environment-specific blocking**: Use APPLICATION_ENV for different blocking rules
9. **Don't overuse blocking**: Prefer middleware for complex logic
10. **Document blocked routes**: Keep list of blocked routes visible

## Configuration File Examples

### Simple Blocking Only
```php
// config/bone-firewall.php
return [
    'blockedRoutes' => [
        '/admin/backup',
        '/admin/restore',
    ],
];
```

### Full Configuration
```php
// config/bone-firewall.php
return [
    'blockedRoutes' => [
        '/admin/backup',
        '/admin/secrets',
        'DELETE' => ['/admin/delete-all'],
    ],
    'routeMiddleware' => [
        '/admin' => [AdminMiddleware::class, RoleCheck::class],
        '/api' => [ApiMiddleware::class, RateLimit::class],
        'POST' => [
            '/api/upload' => [UploadValidation::class],
        ],
    ],
];
```
