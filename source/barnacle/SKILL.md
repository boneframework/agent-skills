---
name: barnacle
description: "Handles the Barnacle dependency injection container with PSR-11 implementation for Bone Framework applications."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "barnacle", "dependency-injection", "container", "psr-11"]
trigger_patterns:
  - "barnacle"
  - "container"
  - "dependency injection"
  - "di"
  - "psr-11"
---

# Barnacle Skill

## When to Use
Activate this skill when working with dependency injection in Bone Framework applications using the Barnacle container library with PSR-11 compliance.

## Package Information
- **Package**: `delboy1978uk/barnacle`
- **License**: MIT
- **PSR Standard**: PSR-11 Container Interface
- **PHP Version**: Compatible with PHP 8.2+

## Overview

Barnacle is a PSR-11 compliant dependency injection container specifically designed for Bone Framework applications. It provides service container functionality with support for:
- Service registration
- Factory patterns
- Dependency injection
- Lazy loading

## Core Interface

### ContainerInterface (PSR-11)
```php
interface ContainerInterface
{
    public function get($id);
    public function has($id): bool;
}
```

## Container Features

### Getting Services
```php
$container = $app->getContainer();
$router = $container->get(Router::class);

if ($container->has(TranslatorInterface::class)) {
    $translator = $container->get(TranslatorInterface::class);
}
```

### Service Registration
```php
$container[MyService::class] = new MyService();
$container[MyService::class] = $container->factory(function ($c) {
    return new MyService();
});
```

## Common Patterns

### Repository Pattern
```php
$container[UserRepository::class] = $c->factory(function ($c) {
    $db = $c->get(PDO::class);
    return new UserRepository($db);
});
```

### Service Layer
```php
$container[UserService::class] = $c->factory(function ($c) {
    return new UserService(
        $c->get(UserRepository::class),
        $c->get(PasswordEncoder::class),
        $c->get(LoggerInterface::class)
    );
});
```

## Container Best Practices

1. Use class names as keys
2. Lazy loading with factories
3. Inject dependencies via constructor
4. Register against interfaces
5. Check service existence
6. Separate config from registration
7. Avoid circular dependencies
8. Consider service lifetime
9. Test with mocks
10. Clean up after tests
