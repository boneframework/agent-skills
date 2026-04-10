---
name: bone-http
description: "Handles HTTP operations, middleware stack, and HTTP response types in Bone Framework applications using delboy1978uk/bone-http package with PSR-7/15 integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "http", "middleware", "psr-7", "psr-15"]
trigger_patterns:
  - "http"
  - "http message"
  - "psr-7"
  - "psr-15"
  - "middleware"
  - "stack"
---

# Bone HTTP Skill

## When to Use
Activate this skill when working with HTTP messages, middleware stack, or HTTP-specific operations in a Bone Framework application using the `delboy1978uk/bone-http` package.

## Package Information
- **Package**: `delboy1978uk/bone-http`
- **Dependencies**: laminas/laminas-diactoros (PSR-7), delboy1978uk/router, bone-server
- **License**: MIT
- **PHP Version**: ^8.2
- **PSR Compliance**: PSR-7 HTTP messages, PSR-15 middleware

## Core Components

### Response Classes

#### Response
Extended HTML response with layout support:
```php
use Bone\Http\Response;

$response = new Response('<html>...</html>', 200);
$response->withHeader('layout', 'admin');
$response->withAttribute('user', $user);
```

#### LayoutResponse
Response with explicit layout setting:
```php
use Bone\Http\Response\LayoutResponse;

$response = new LayoutResponse($body, 'admin');
```

#### HtmlResponse
Standard HTML response:
```php
use Laminas\Diactoros\Response\HtmlResponse;

$response = new HtmlResponse($body, 200);
```

### Middleware Interfaces

#### MiddlewareRegistrationInterface
For per-package middleware:

```php
interface MiddlewareRegistrationInterface
{
    public function getMiddleware(Container $c): array;
}
```

#### GlobalMiddlewareRegistrationInterface
For global stack middleware:

```php
interface GlobalMiddlewareRegistrationInterface
{
    public function getGlobalMiddleware(Container $c): array;
}
```

### Stream
Custom stream wrapper:
```php
use Bone\Http\Stream;

$stream = new Stream('php://memory', 'r+');
$stream->write($content);
```

## Response Methods

### Response Class Methods
```php
$response = new Response($body, $status);

// Header management
$response->withHeader($name, $value);
$response->withoutHeader($name);
$response->getHeader($name);
$response->getHeaderLine($name);

// Attribute management (for passing data through middleware)
$response->withAttribute($name, $value);
$response->getAttribute($name);
$response->hasAttribute($name);
$response->withoutAttribute($name);

// Layout management
$response->withLayout($layout);
$response->getLayout();
```

### Layout Response
```php
// Set layout via header
$response->headers->set('layout', 'admin');

// Or use LayoutResponse
$response = new LayoutResponse($body, 'admin');
```

## Middleware Stack

### Adding Middleware to Stack
```php
// Via GlobalMiddlewareRegistrationInterface
public function getGlobalMiddleware(Container $c): array
{
    return [MiddlewareClass::class];
}

// Via MiddlewareRegistrationInterface
public function getMiddleware(Container $c): array
{
    return [$middlewareInstance];
}
```

### Middleware Registration Process
1. `addToContainer()` - Creates middleware instances
2. `getMiddleware()` - Returns instances for container
3. `getGlobalMiddleware()` - Returns class names for stack

## Router Interface

### RouterInterface
Extension of League Router for Bone Framework:

```php
interface RouterInterface extends RequestHandlerInterface
{
    // Route management methods
    public function getRoutes(): array;
    public function getGroups(): array;
    public function removeRoute(Route $route);
    
    // API methods
    public function apiResource($urlSlug, $controllerClass, $c);
    public function adminResource($urlSlug, $controllerClass, $c, $role = 'admin');
    
    // Request handling
    public function handle($request): ResponseInterface;
}
```

### API Resource Routes
Generates RESTful API routes:
```php
$router->apiResource('/api/users', UserController::class, $container);
// Generates: GET /api/users, POST /api/users, GET /api/users/{id}, etc.
```

### Admin Resource Routes
Generates admin CRUD routes with auth:
```php
$router->adminResource('/admin/users', UserController::class, $container, 'admin');
// Generates: GET /admin/users, GET /admin/users/create, POST /admin/users/create, etc.
```

## Common Tasks

### 1. Creating JSON Response
```php
use Laminas\Diactoros\Response\JsonResponse;

$data = ['users' => $users];
$response = new JsonResponse($data);
return $response->withStatus(200);
```

### 2. Creating HTML Response
```php
use Laminas\Diactoros\Response\HtmlResponse;
use Bone\Http\Response;

$body = $this->view->render('template', $vars);

// With layout
$response = new Response($body, 200);
$response = $response->withHeader('layout', 'admin');

// Or with LayoutResponse
$response = new LayoutResponse($body, 'admin');

return $response;
```

### 3. Setting Response Headers
```php
$response = new HtmlResponse($body);
$response = $response->withHeader('Content-Type', 'application/json');
$response = $response->withHeader('X-Custom-Header', 'value');

return $response;
```

### 4. Passing Data Through Middleware
```php
// Set attribute
$response = $response->withAttribute('user', $user);
$response = $response->withAttribute('flash', $message);

// Get attribute
if ($response->hasAttribute('user')) {
    $user = $response->getAttribute('user');
}
```

### 5. Router with JSON Strategy
```php
use Laminas\Diactoros\ResponseFactory;
use League\Route\Strategy\JsonStrategy;

$factory = new ResponseFactory();
$strategy = new JsonStrategy($factory);
$strategy->setContainer($container);

$group = $router->group('/api', function ($route) {
    $route->map('GET', '/users', [UserController::class, 'index']);
})->setStrategy($strategy);
```

## Middleware Interface

### Request/Response Flow
```php
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;

class CustomMiddleware implements MiddlewareInterface
{
    public function process($request, $handler)
    {
        // Do something before
        $response = $handler->handle($request);
        // Do something after
        return $response;
    }
}
```

## Session Integration

### Accessing Session in Middleware
```php
use Del\SessionManager;

class AuthMiddleware implements MiddlewareInterface
{
    public function process($request, $handler)
    {
        $session = SessionManager::getInstance();
        
        if (!$session->has('user_id')) {
            return new HtmlResponse('Unauthorized', 401);
        }
        
        return $handler->handle($request);
    }
}
```

## Configuration

### Setting Response Status
```php
$response = new HtmlResponse($body);
$response = $response->withStatus(404);  // Not Found
$response = $response->withStatus(403);  // Forbidden
$response = $response->withStatus(302);  // Redirect
```

### Redirect Response
```php
use Laminas\Diactoros\Response\RedirectResponse;

$response = new RedirectResponse('/new-url', 302);
return $response->withHeader('Location', '/new-url');
```

## PSR-7 Compliance

All responses implement `Psr\Http\Message\ResponseInterface`:
- `getStatusCode()` - Get status code
- `getHeaders()` - Get all headers
- `hasHeader($name)` - Check header existence
- `getHeader($name)` - Get header value(s)
- `getBody()` - Get response body
- `withHeader($name, $value)` - Set header
- `withoutHeader($name)` - Remove header

## PSR-15 Compliance

All middleware implements `Psr\Http\Server\MiddlewareInterface`:
- `process($request, $handler)` - Process request

All handlers implement `Psr\Http\Server\RequestHandlerInterface`:
- `handle($request)` - Handle request

## Best Practices

1. **Use PSR-7 responses**: Always return ResponseInterface implementations
2. **Set proper status codes**: Use 200, 201, 400, 401, 403, 404, 500 appropriately
3. **Use LayoutResponse for layouts**: Cleaner than header manipulation
4. **Pass data via attributes**: Use attributes to pass data through middleware
5. **Keep middleware light**: Fast processing, minimal dependencies
6. **Use JSON for APIs**: Set Content-Type header appropriately
7. **Validate inputs**: Check request data before processing
8. **Handle errors gracefully**: Return proper error responses
9. **Log responses**: Track status codes and response times
10. **Cache appropriately**: Set cache headers for public responses
