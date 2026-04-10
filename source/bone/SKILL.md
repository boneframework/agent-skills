---
name: bone-framework-core
description: Provides expert-level knowledge and procedural guidance for working with the Bone Framework core in PHP, including setup, package registration, routing, configuration, and best practices for building web applications. Use this skill when tasked with building, maintaining, or extending PHP applications using Bone Framework, such as initializing projects, configuring components, or integrating packages.
metadata:
  author: Bone Framework Team
  version: "1.0"
compatibility: Requires PHP 8.2+ with Composer installed. Uses PSR standards and laminas/httphandlerrunner.
---

# Bone Framework Core Skill

This skill equips AI agents with comprehensive knowledge of the Bone Framework core, a lightweight PHP framework using PSR standards, dependency injection, and middleware.

## When to Use This Skill
- Initializing a new Bone Framework project.
- Configuring packages, routes, controllers, or middleware.
- Handling configuration for databases, i18n, logging, or sessions.
- Implementing PSR-compliant components like HTTP messaging or DI containers.
- Debugging or optimizing Bone Framework applications.
- Integrating recommended packages like bone-user, bone-doctrine, or bone-oauth2.

Do not use for unrelated frameworks (e.g., Laravel, Symfony) unless explicitly comparing.

## Prerequisites
- PHP 8.2+ with Composer installed.
- Docker optional for development environment.
- Familiarity with PSR standards (PSR-7 HTTP messages, PSR-11 container, PSR-15 middleware).
- Composer package: `delboy1978uk/barnacle` for dependency injection.

## Core Architecture

### Application Bootstrapping
Bone Framework uses a singleton `Application` class for bootstrapping:

```php
use Bone\Application;

$app = Application::ahoy();
$app->bootstrap();  // Initialize container and packages
$app->setSail();    // Dispatch request and emit response
```

**Key methods:**
- `ahoy()` - Static factory returning the singleton Application instance
- `bootstrap()` - Initializes the DI container, loads config, registers packages
- `setSail()` - Handles HTTP request dispatch and response emission

### ApplicationPackage Class
The main package class that registers all core components into the container:
- `setupViewEngine()` - Registers ViewPackage
- `setupRouter()` - Registers RouterPackage and initializes router
- `setupPackages()` - Iterates through configured packages
- `registerPackage()` - Registers individual packages (routes, views, translations, middleware)
- `initMiddlewareStack()` - Initializes middleware stack with CORS middleware
- `setupTranslator()` - Registers I18nPackage for translations
- `setupPdoConnection()` - Registers DbPackage for database

## Step-by-Step Workflows

### 1. Project Setup
To create a new Bone Framework project:

1. Install via Composer:
```bash
composer create-project boneframework/skeleton your/path/here
cp your/path/here/.env.example your/path/here/.env
```

2. Configure environment variables in `.env`:
```
DB_HOST=localhost
DB_NAME=your_database
DB_USERNAME=your_user
DB_PASSWORD=your_password
DOMAIN_NAME=yourdomain.com
APPLICATION_ENV=development
```

3. Verify installation by accessing the site; you should see the default Bone Framework page.

### 2. Configuration Management
- Config files in `config/` return PHP arrays (e.g., `bone-db.php`, `bone-i18n.php`).
- Environment-specific overrides via `APPLICATION_ENV` (e.g., `config/development/` or `config/production/`).
- Config files are loaded by `Bone\Server\Environment` class.

**Key configuration files:**

| File | Purpose |
|------|---------|
| `packages.php` | List of packages to register (order matters for dependencies) |
| `middleware.php` | Site-wide middleware stack |
| `bone-db.php` | Database credentials (driver, host, dbname, user, password) |
| `bone-i18n.php` | Translations config (dir, type, default_locale, supported_locales) |
| `bone-log.php` | Log channels and error handling settings |
| `site.php` | Site metadata (title, domain, contact email, company info) |
| `paths.php` | Directory paths (proxy_dir, uploads_dir, cache_dir, entity_paths) |
| `views.php` | View folder configuration and vendor overrides |

### 3. Dependency Injection Container
Bone uses `barnacle` container (PSR-11 compliant):

```php
$container = $app->getContainer();

// Get services
$em = $container->get(EntityManagerInterface::class);
$router = $container->get(Router::class);
$session = $container->get(SessionManager::class);

// Register services
$container[MyService::class] = new MyService();
```

### 4. Package Registration
Packages are registered in `config/packages.php`:

```php
return [
    'packages' => [
        Bone\BoneDoctrine\BoneDoctrinePackage::class,
        App\AppPackage::class,
    ]
];
```

**Package interfaces:**
- `RegistrationInterface` - Basic package registration
- `RouterConfigInterface` - Register routes via `addRoutes($c, $router)`
- `ViewRegistrationInterface` - Register views via `addViews()` and `addViewExtensions()`
- `MiddlewareRegistrationInterface` - Register middleware via `getMiddleware()`
- `GlobalMiddlewareRegistrationInterface` - Register global stack middleware
- `CommandRegistrationInterface` - Register console commands
- `FixtureProviderInterface` - Provide Doctrine fixtures
- `EntityRegistrationInterface` - Provide entity paths

### 5. Middleware Stack
Middleware is registered at two levels:

**Global stack** (applied to all requests):
- CORS middleware by default
- Added via `GlobalMiddlewareRegistrationInterface` or `middleware.php`

**Per-package stack:**
- Added via `MiddlewareRegistrationInterface::getMiddleware()`
- Registered as container services

### 6. Environment Setup
Environment-specific configuration:
```php
// In config/development/ - override settings for development
// In config/production/ - override settings for production

// Set environment in .env or server config
APPLICATION_ENV=development
```

## Package Dependencies

Bone Framework depends on these delboy1978uk packages:
- `bone-db` - Database/Doctrine integration
- `bone-console` - CLI commands
- `bone-controller` - Controller base class
- `bone-firewall` - Route firewall/ACL
- `bone-http` - HTTP utilities and middleware stack
- `bone-i18n` - Internationalization with Gettext
- `bone-log` - Logging
- `bone-router` - Router implementation
- `bone-server` - Server environment and config
- `bone-view` - Plates template engine integration

Third-party:
- `delboy1978uk/barnacle` - PSR-11 container
- `laminas/laminas-diactoros` - PSR-7 HTTP messages
- `laminas/laminas-httphandlerrunner` - Request dispatching
- `symfony/contracts` - Shared interfaces

## Common Tasks

### Creating a New Package
```php
<?php
namespace App;

use Bone\Contracts\Container\ContainerInterface;
use Bone\Contracts\Container\RegistrationInterface;

class AppPackage implements RegistrationInterface
{
    public function addToContainer(ContainerInterface $c): void
    {
        // Register services, routes, views, etc.
    }
}
```

### Accessing Config in Code
```php
$config = $container->get('site');
$title = $config['site']['title'];

$i18n = $container->get('i18n');
$defaultLocale = $i18n['default_locale'];
```

### Setting Environment-Specific Config
Create `config/production/` or `config/development/` with override files that merge with base config.

## Errors and Exceptions
- `Bone\Exception::SHIVER_ME_TIMBERS` - 'Application Error'
- `Bone\Exception::LOST_AT_SEA` - 'Page not found.'
- `Bone\Exception::GHOST_SHIP` - 'Record not found.'

Custom error handling via `ErrorHandler::getShutdownHandler()` which displays formatted errors in development or generic messages in production.

## Best Practices
1. Always use PSR standards (HTTP messages, container, middleware)
2. Register packages in correct dependency order in `packages.php`
3. Use environment-specific config folders for different environments
4. Implement appropriate interfaces when creating custom packages
5. Use Doctrine entities for database models
6. Register views via `ViewRegistrationInterface` for package view folders
7. Use `MiddlewareRegistrationInterface` for package-specific middleware
8. Use `GlobalMiddlewareRegistrationInterface` for site-wide middleware
