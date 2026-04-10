---
name: bone-router
description: "Handles routing and URL generation in Bone Framework applications using delboy1978uk/bone-router package with League Router integration and route management features."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "routing", "router", "routes", "urls"]
trigger_patterns:
  - "router"
  - "route"
  - "routing"
  - "url"
  - "path"
  - "dispatch"
---

# Bone Router Skill

## When to Use
Activate this skill when defining routes, URL generation, or route management in a Bone Framework application using the `delboy1978uk/bone-router` package.

## Package Information
- **Package**: `delboy1978uk/bone-router`
- **Dependencies**: League Router, laminas/laminas-diactoros, bone-view
- **License**: MIT
- **PHP Version**: ^8.2

## Core Components

### Router
Extends `League\Router\Router` with Bone Framework integration:
```php
class Router extends LeagueRouter implements RequestHandlerInterface, RouterInterface
{
    public function getRoutes(): array;
    public function getGroups(): array;
    public function apiResource($urlSlug, $controllerClass, $c);
    public function adminResource($urlSlug, $controllerClass, $c, $role = 'admin');
    public function removeRoute(Route $routeToRemove);
}
```

### RouterPackage
Registers router in container:
```php
class RouterPackage implements RegistrationInterface
{
    public function addToContainer(Container $c): void;
}
```

### RouterConfigInterface
Interface for packages that register routes:
```php
interface RouterConfigInterface
{
    public function addRoutes(Container $c, Router $router);
}
```

## Route Definition

### Basic Routes
```php
// In package implementing RouterConfigInterface
public function addRoutes(Container $c, Router $router): void
{
    $router->get('/home', [HomeController::class, 'index']);
    $router->post('/submit', [FormController::class, 'submit']);
    $router->map(['GET', 'POST'], '/mixed', [Controller::class, 'action']);
}
```

### Named Routes
```php
$router->get('/users/{id}', [UserController::class, 'view'])->setName('user.view');
```

### Route Groups
```php
$router->group('/admin', function (Router $router) {
    $router->get('/dashboard', [AdminDashboard::class, 'index']);
    $router->get('/users', [AdminUser::class, 'index']);
});
```

### Group with Middleware
```php
$router->group('/admin', function (Router $router) {
    $router->get('/dashboard', [AdminDashboard::class, 'index']);
})->middleware(AuthMiddleware::class);
```

### Group with Strategy
```php
$factory = new ResponseFactory();
$strategy = new JsonStrategy($factory);
$strategy->setContainer($c);

$router->group('/api', function (Router $router) {
    $router->get('/users', [UserController::class, 'index']);
})->setStrategy($strategy);
```

## Built-in Route Generators

### API Resource Routes
Generates full CRUD API for a resource:
```php
$group = $router->apiResource('/api/users', UserController::class, $c);
// Generates:
// GET    /api/users       -> index
// POST   /api/users       -> create
// GET    /api/users/{id}  -> read
// PATCH  /api/users/{id} -> update
// DELETE /api/users/{id} -> delete
```

### Admin Resource Routes
Generates admin CRUD with authentication:
```php
$router->adminResource('/admin/users', UserController::class, $c, 'admin');
// Generates:
// GET    /admin/users              -> index
// GET    /admin/users/create       -> create
// GET    /admin/users/{id}         -> view
// GET    /admin/users/{id}/delete  -> delete
// GET    /admin/users/{id}/edit    -> edit
// POST   /admin/users/create       -> create
// POST   /admin/users/{id}/delete  -> delete
// POST   /admin/users/{id}/edit    -> edit
```

## Route Management

### Getting All Routes
```php
$routes = $router->getRoutes();
foreach ($routes as $route) {
    echo $route->getPath();
    echo $route->getMethod();
}
```

### Getting Route Groups
```php
$groups = $router->getGroups();
foreach ($groups as $group) {
    // Access group information
}
```

### Removing Routes
```php
// Remove specific route
$router->removeRoute($routeToRemove);

// Remove by path (requires iterating)
foreach ($router->getRoutes() as $route) {
    if ($route->getPath() === '/admin/backup') {
        $router->removeRoute($route);
        break;
    }
}
```

## Route Parameters

### Required Parameters
```php
$router->get('/users/{id}', [UserController::class, 'view']);
// Matches: /users/123
```

### Optional Parameters
```php
$router->get('/users[{/id}]', [UserController::class, 'indexOrView']);
// Matches: /users and /users/123
```

### Parameter Constraints
```php
$router->get('/users/{id:[0-9]+}', [UserController::class, 'view']);
// Only matches numeric IDs
```

## Common Tasks

### 1. Defining Routes in a Package
```php
// config/packages.php
return [
    'packages' => [
        App\AppPackage::class,
    ]
];

// App/AppPackage.php
public function addToContainer(ContainerInterface $c): void
{
    // Register routes
    $this->registerRoutes($c);
}

private function registerRoutes(ContainerInterface $c): void
{
    $router = $c->get(Router::class);
    
    $router->get('/', [HomeController::class, 'index']);
    $router->get('/about', [PageController::class, 'about']);
}
```

### 2. Generating URLs
```php
use League\Route\Route;

$router = $container->get(Router::class);

// Get route by name
$route = $router->getRouteCollection()->get('user.view');
$url = $route->getGenerator()->generate(['id' => 123]);

// Or use named routes
$url = $router->pathFor('user.view', ['id' => 123]);
```

### 3. Setting Route Middleware
```php
$router->group('/admin', function (Router $router) {
    $router->get('/dashboard', [AdminDashboard::class, 'index']);
})->middleware([AuthMiddleware::class, RoleCheck::class]);
```

### 4. JSON API Routes
```php
use League\Route\Strategy\JsonStrategy;
use Laminas\Diactoros\ResponseFactory;

$factory = new ResponseFactory();
$strategy = new JsonStrategy($factory);
$strategy->setContainer($c);

$router->group('/api', function (Router $router) {
    $router->get('/users', [UserController::class, 'index']);
})->setStrategy($strategy);
```

### 5. Route with Constraints
```php
$router->get('/posts/{year:[0-9]{4}}/{month:[0-9]{2}}/{slug}', 
    [BlogController::class, 'view']);
// Matches: /posts/2024/01/my-post
```

### 6. Route Prefix
```php
$router->group('/api/v1', function (Router $router) {
    $router->get('/users', [UserController::class, 'index']);
});
// Matches: /api/v1/users
```

### 7. GET vs POST Routes
```php
$router->get('/form', [FormController::class, 'show']);
$router->post('/form', [FormController::class, 'submit']);
```

## Router Integration

### In Bone Framework
```php
// In ApplicationPackage
private function setupRouter(ContainerInterface $c): void
{
    $package = new RouterPackage();
    $package->addToContainer($c);
    $this->router = $c->get(Router::class);
}
```

### Accessing Router in Code
```php
$router = $container->get(Router::class);

// Get routes
$routes = $router->getRoutes();

// Dispatch request
$response = $router->dispatch($request);
```

## Route Order

Routes are matched in order of definition:
```php
// More specific routes first
$router->get('/users/{id}', [UserController::class, 'view']);
$router->get('/users', [UserController::class, 'index']);

// Don't put generic routes before specific ones
```

## Best Practices

1. **Define routes in packages**: Organize routes by feature
2. **Name routes**: Use `->setName()` for URL generation
3. **Group related routes**: Use `->group()` for common prefixes
4. **Add middleware to groups**: Apply auth/security at group level
5. **Use constraints**: Validate parameters with regex
6. **Order matters**: Put specific routes before generic ones
7. **Use strategies**: JSON strategy for API endpoints
8. **Document routes**: Keep route list documented
9. **Test routes**: Verify all routes work as expected
10. **Remove unused routes**: Clean up routes when features removed

## Route Configuration Examples

### Complete Router Setup
```php
// App/AppPackage.php
public function addRoutes(ContainerInterface $c, Router $router): void
{
    // Home
    $router->get('/', [HomeController::class, 'index'])->setName('home');
    
    // Auth
    $router->get('/login', [AuthController::class, 'login']);
    $router->post('/login', [AuthController::class, 'authenticate']);
    $router->get('/logout', [AuthController::class, 'logout']);
    
    // Admin with middleware
    $router->group('/admin', function (Router $router) {
        $router->get('/dashboard', [AdminDashboard::class, 'index']);
        $router->get('/users', [AdminUser::class, 'index']);
    })->middleware([AuthMiddleware::class, AdminMiddleware::class]);
    
    // API with JSON strategy
    $factory = new ResponseFactory();
    $strategy = new JsonStrategy($factory);
    $strategy->setContainer($c);
    
    $router->group('/api/v1', function (Router $router) use ($c) {
        $router->get('/users', [ApiUserController::class, 'index']);
    })->setStrategy($strategy);
}
```
