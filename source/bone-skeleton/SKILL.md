---
name: "bone-skeleton"
description: "Bone Framework skeleton application - a fresh, ready-to-use PHP framework installation with PSR-7/11/15 support, and modular package architecture. Use when setting up new Bone Framework projects or working with Bone Framework applications."
version: "1.0.0"
author: "Agent Zero Team"
tags: ["php", "framework", "bone", "psr", "docker", "lamp", "skeleton", "bone"]
trigger_patterns:
  - "bone framework"
  - "bone skeleton"
  - "boneframework"
  - "bone project"
---

# Bone Framework Skeleton

## Overview

The Bone Framework skeleton is a fresh, ready-to-use application installation that serves as a starting point for PHP development. It provides a pre-configured structure with all essential components for building modern PHP applications.

**GitHub Repository**: https://github.com/boneframework/skeleton

## Core Features

- **PSR-7** HTTP messaging
- **PSR-11** dependency injection container configuration
- **PSR-15** middleware routing
- **i18n translator** for internationalization
- **Self-contained package-based architecture**
- **Extendable Command Line Interface**
- **Session management**
- **Configuration system** with environment-based loading
- **Logging** using Monolog
- **View engine** support
- **Database connectivity** (MariaDB)
- **Mailhog integration** for development email testing

## Installation Methods

### Method 1: Via Composer

```bash
composer create-project boneframework/skeleton your/path/here
cp your/path/here/.env.example your/path/here/.env
```
### Post-Installation Setup

3. **Access the application**:
   - Main site: `https://boneframework.docker`
   - Mailhog: `http://boneframework.docker:8025`

## Directory Structure

```
project-root/
├── config/              # Configuration files
│   ├── bone-db.php     # Database configuration
│   ├── bone-firewall.php
│   ├── bone-i18n.php   # Internationalization
│   ├── bone-log.php    # Logging configuration
│   ├── layouts.php     # View layouts
│   ├── middleware.php  # Middleware configuration
│   ├── packages.php    # Package registration
│   ├── paginator.php
│   ├── paths.php       # Path definitions
│   ├── site.php        # Site-wide settings
│   └── views.php       # View configuration
├── data/               # Application data
│   ├── cache/         # Cache files
│   ├── logs/          # Log files
│   ├── translations/  # i18n files
│   └── uploads/       # User uploads
├── public/            # Web root
│   ├── index.php     # Application entry point
│   ├── css/          # Stylesheets
│   ├── images/       # Images
│   └── js/           # JavaScript files
├── src/              # Application packages
│   ├── AppPackage.php
│   └── Controller/
│       └── IndexController.php
├── tests/            # Test files
├── vendor/           # Composer dependencies (do not edit)
├── bin/              # Docker scripts
│   ├── start
│   ├── stop
│   ├── terminal
│   └── setdomain
└── .env              # Environment configuration
```

## Key Directories Explained

### `/config`
Contains all configuration files for the application. Each file configures a specific aspect:
- Database connections
- Middleware stack
- Package registration
- View rendering
- Logging
- Internationalization

### `/data`
Stores runtime data:
- **cache/**: Compiled templates and cached data
- **logs/**: Application logs (via Monolog)
- **translations/**: i18n translation files
- **uploads/**: User-uploaded files

### `/public`
The web root directory. Only this directory should be accessible via web server:
- **index.php**: Main entry point that bootstraps the application
- **css/**, **images/**, **js/**: Static assets

### `/src`
Application packages live here. Each package is self-contained:
- Controllers
- Models
- Views
- Package configuration

### `/vendor`
Composer dependencies. **Never edit files here** - they will be overwritten on `composer update`.

## Configuration

### Environment Variables (`.env`)

The `.env` file contains environment-specific configuration:

```env
# Database
DB_HOST=mariadb
DB_NAME=myapp
DB_USER=root
DB_PASS=secret

# Application
APP_ENV=development
APP_DEBUG=true
APP_URL=https://boneframework.docker

# Mail (Mailhog for development)
MAILER_DSN=smtp://mailhog:1025
```

### Package Registration

Packages are registered in `config/packages.php`:

```php
return [
    \Bone\Server\ServerPackage::class,
    \Bone\Router\RouterPackage::class,
    \Bone\View\ViewPackage::class,
    \App\AppPackage::class,
    // Add your packages here
];
```

## Creating a New Package

### Step 1: Create Package Directory

```bash
mkdir -p src/MyPackage/Controller
```

### Step 2: Create Package Class

```php
<?php
// src/MyPackage/MyPackage.php

namespace MyPackage;

use Bone\Server\SiteConfig;
use Barnacle\Container;
use Barnacle\RegistrationInterface;

class MyPackage implements RegistrationInterface
{
    public function addToContainer(Container $c)
    {
        // Register services
        $c[Controller\MyController::class] = $c->factory(function ($c) {
            return new Controller\MyController();
        });
    }

    public function addToSiteConfig(SiteConfig $config)
    {
        // Register routes
        $config->addRoute('/my-route', Controller\MyController::class);
    }
}
```

### Step 3: Create Controller

```php
<?php
// src/MyPackage/Controller/MyController.php

namespace MyPackage\Controller;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;

class MyController
{
    public function __invoke(
        ServerRequestInterface $request,
        ResponseInterface $response
    ): ResponseInterface {
        $response->getBody()->write('Hello from MyController!');
        return $response;
    }
}
```

### Step 4: Register Package

Add to `config/packages.php`:

```php
return [
    // ... existing packages
    \MyPackage\MyPackage::class,
];
```



## Available Bone Packages

The skeleton can be extended with additional Bone packages:

| Package | Purpose |
|---------|----------|
| `delboy1978uk/bone-form` | Form generation and handling |
| `delboy1978uk/bone-doctrine` | Doctrine ORM integration |
| `delboy1978uk/bone-mail` | Email functionality |
| `delboy1978uk/bone-user` | User registration system |
| `delboy1978uk/generator` | Package template generation |
| `delboy1978uk/bone-oauth2` | OAuth2 server |
| `delboy1978uk/bone-open-api` | Swagger documentation |
| `delboy1978uk/image` | Image manipulation |

See github.com/boneframework and github.com/deboy1978uk for more packages.

### Installing Additional Packages

```bash
# composer require delboy1978uk/bone-form
# Register in config/packages.php
```

## Routing

### Basic Route Registration

In your package's `addRoutes()` method:

```php
public function addRoutes(Container $c, Router $router): Router
{
    $router->map('GET', '/', [IndexController::class, 'index']);
    $router->map('GET', '/learn/{id}', [IndexController::class, 'learn']);

    return $router;
}
```

## Middleware

### Site-wide Middleware

Configure in `config/middleware.php`:

```php
return [
    \\Bone\\Server\\Middleware\\SessionMiddleware::class,
    \\Bone\\Firewall\\Middleware\\FirewallMiddleware::class,
    // Add your middleware here
];
```

### Route-specific Middleware

```php
public function addToSiteConfig(SiteConfig $config)
{
    $config->addRoute(
        '/admin',
        Controller\\AdminController::class,
        'GET',
        [Middleware\\AuthMiddleware::class]
    );
}
```

## Views and Templates

### Rendering Views

```php
use Bone\\View\\ViewEngine;

public function __invoke(
    ServerRequestInterface $request,
    ResponseInterface $response
): ResponseInterface {
    $view = $this->container->get(ViewEngine::class);
    
    $html = $view->render('my-template', [
        'title' => 'My Page',
        'data' => $someData,
    ]);
    
    $response->getBody()->write($html);
    return $response;
}
```

## Database Operations

### Using PDO

```php
$pdo = $this->container->get(\\PDO::class);

// Select
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
$stmt->execute([$userId]);
$user = $stmt->fetch(\\PDO::FETCH_ASSOC);

// Insert
$stmt = $pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
$stmt->execute([$name, $email]);
$newId = $pdo->lastInsertId();
```

## Email Testing with Mailhog

Mailhog captures all outgoing emails during development:

- **SMTP**: `mailhog:1025`
- **Web UI**: `http://boneframework.docker:8025`

## Best Practices

### 1. Use Dependency Injection

Inject dependencies through constructors and register in the container.

### 2. Keep Controllers Thin

Delegate business logic to services.

### 3. Use Environment Variables

Never hardcode configuration - use `.env` file.

### 4. Validate Input

Always validate and sanitize user input.

### 5. Handle Errors Gracefully

Use try-catch blocks and log errors properly.

### 6. Follow PSR Standards

- **PSR-7**: HTTP messages
- **PSR-11**: Container interface
- **PSR-15**: HTTP middleware
- **PSR-3**: Logger interface


## Troubleshooting

### Common Issues

1. **404 Not Found**
   - Check route registration
   - Verify package is registered in `config/packages.php`

2. **500 Internal Server Error**
   - Check `data/logs/app.log`
   - Enable debug mode: `APP_DEBUG=true`

3. **Database Connection Failed**
   - Verify credentials in `.env`
   - Check MariaDB is running

## Resources

- **GitHub**: https://github.com/boneframework/skeleton
- **LAMP Stack**: https://github.com/boneframework/lamp
- **Documentation**: Check individual package repositories

## License

MIT License - Free to use and modify.
