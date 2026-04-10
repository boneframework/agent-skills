---
name: skeleton
description: "Handles Bone Framework skeleton project setup and development using boneframework/skeleton for rapid application development."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "skeleton", "project-template", "boilerplate", "setup"]
trigger_patterns:
  - "skeleton"
  - "bone skeleton"
  - "project template"
  - "boilerplate"
  - "boneframework/skeleton"
---

# Skeleton Skill

## When to Use
Activate this skill when setting up a new Bone Framework project or working with the boneframework/skeleton project template for rapid application development.

## Package Information
- **Package**: `boneframework/skeleton`
- **Repository**: https://github.com/boneframework/skeleton
- **License**: MIT
- **PHP Version**: ^8.2

## Overview

The Bone Framework skeleton is a ready-to-use application template that provides:
- PSR standards compliance (PSR-7, PSR-11, PSR-15)
- Modular package architecture
- i18n support with Gettext
- Docker LAMP development environment
- CLI tooling for scaffolding
- Environment-based configuration

## Installation

### Method 1: Via Composer
```bash
composer create-project boneframework/skeleton your/project/path
```

### Method 2: Via Docker
```bash
# Clone LAMP stack
git clone https://github.com/boneframework/lamp myproject
cd myproject

# Clone skeleton into code directory
git clone https://github.com/boneframework/skeleton code

# Start Docker
cd bin && ./start && cd ..
docker-compose up -d
```

## Project Structure

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
├── src/              # Application packages (modular)
│   ├── AppPackage.php
│   └── Controller/
│       └── IndexController.php
├── tests/            # Test files
├── vendor/           # Composer dependencies
├── bin/              # Docker scripts (if using LAMP)
│   ├── start
│   ├── stop
│   ├── terminal
│   └── setdomain
└── .env              # Environment configuration
```

## Key Directories

### `/config`
Contains all configuration files. Each file configures a specific aspect:
- **bone-db.php**: Database credentials and settings
- **bone-firewall.php**: Security rules and route protection
- **bone-i18n.php**: Translation and i18n setup
- **bone-log.php**: Monolog configuration
- **middleware.php**: Global middleware stack
- **packages.php**: Package registration
- **site.php**: Site-wide configuration
- **views.php**: View engine configuration

### `/src`
Application packages live here. Each package is self-contained:
- Controllers
- Models
- Views
- Package configuration

### `/data`
Stores runtime data:
- **cache/**: Compiled templates and cached data
- **logs/**: Application logs (via Monolog)
- **translations/**: i18n translation files
- **uploads/**: User-uploaded files

### `/public`
The web root directory. Only this directory should be accessible via web server:
- **index.php**: Main entry point
- **css/**, **images/**, **js/**: Static assets

## Configuration

### Environment Variables (`.env`)

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

### Environment-Specific Config

Configuration files check `APPLICATION_ENV`:

```php
// config/site.php
return [
    'siteName' => 'My Application',
    'debug' => getenv('APP_DEBUG') === 'true',
    'environment' => getenv('APPLICATION_ENV') ?: 'production',
];
```

## Package Registration

Packages are registered in `config/packages.php`:

```php
// config/packages.php
return [
    'packages' => [
        \Bone\Server\ServerPackage::class,
        \Bone\Router\RouterPackage::class,
        \Bone\View\ViewPackage::class,
        \Bone\I18n\I18nPackage::class,
        \Bone\Log\LogPackage::class,
        \Bone\Db\DbPackage::class,
        \App\AppPackage::class,
        // Add your packages here
    ],
];
```

## Creating a New Package

### Step 1: Create Package Directory
```bash
mkdir -p src/MyPackage
mkdir -p src/MyPackage/Controller
mkdir -p src/MyPackage/Entity
mkdir -p src/MyPackage/Service
```

### Step 2: Create Package Class

```php
<?php
// src/MyPackage/MyPackage.php

namespace MyPackage;

use Bone\Server\SiteConfig;
use Barnacle\Container;
use Bone\Package\RegistrationInterface;

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

use Bone\Controller\Controller;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;

class MyController extends Controller
{
    public function __invoke(
        ServerRequestInterface $request,
        ResponseInterface $response
    ): ResponseInterface {
        $html = $this->view->render('my-template', [
            'title' => 'My Page',
        ]);
        
        $response->getBody()->write($html);
        return $response;
    }
}
```

### Step 4: Register Package

```php
// config/packages.php
return [
    'packages' => [
        // ... existing packages
        \MyPackage\MyPackage::class,
    ],
];
```

## Routing

### Basic Route Registration
In your package's `addToSiteConfig()`:

```php
public function addToSiteConfig(SiteConfig $config)
{
    $config->addRoute('/my-route', Controller\MyController::class);
}
```

### Route Groups
```php
public function addToSiteConfig(SiteConfig $config)
{
    $config->addRouteGroup('/admin', function ($group) {
        $group->get('', [AdminController::class, 'index']);
        $group->get('/users', [AdminController::class, 'users']);
    })->middleware(\Bone\Firewall\Middleware\AdminMiddleware::class);
}
```

## Middleware

### Site-wide Middleware
Configure in `config/middleware.php`:

```php
return [
    \Bone\Server\Middleware\SessionMiddleware::class,
    \Bone\Firewall\Middleware\FirewallMiddleware::class,
    \Bone\I18n\Middleware\LocaleMiddleware::class,
    // Add your middleware here
];
```

### Route-specific Middleware

```php
public function addToSiteConfig(SiteConfig $config)
{
    $config->addRoute(
        '/admin',
        Controller\AdminController::class,
        'GET',
        [\Bone\Firewall\Middleware\AdminMiddleware::class]
    );
}
```

## Views and Templates

### Basic View Rendering
```php
use Bone\View\ViewEngine;

public function __invoke(
    ServerRequestInterface $request,
    ResponseInterface $response
): ResponseInterface {
    $html = $this->view->render('my-template', [
        'title' => 'My Page',
        'data' => $someData,
    ]);
    
    $response->getBody()->write($html);
    return $response;
}
```

### View Helpers
```php
// In templates
<a href="<?= $this->url('home') ?>">Home</a>
<img src="<?= $this->asset('img/logo.png') ?>" alt="Logo">
```

## Database Operations

### Using PDO
```php
$pdo = $this->container->get(\PDO::class);

// Select
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
$stmt->execute([$userId]);
$user = $stmt->fetch(\PDO::FETCH_ASSOC);

// Insert
$stmt = $pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
$stmt->execute([$name, $email]);
$newId = $pdo->lastInsertId();
```

### With Bone-Doctrine
```php
$em = $this->container->get(EntityManagerInterface::class);

$user = $em->getRepository(User::class)->find($userId);
$em->persist($newUser);
$em->flush();
```

## Email Testing with Mailhog

Mailhog captures all outgoing emails during development:

- **SMTP**: `mailhog:1025`
- **Web UI**: `http://boneframework.docker:8025`

## Docker LAMP Stack

When using the LAMP stack:

### Container Services
- `lamp-php-1`: PHP/Composer
- `lamp-node-1`: NPM
- `lamp-mariadb-1`: MySQL/MariaDB

### Running Commands
```bash
# In PHP container
docker -H unix:///var/run/docker.sock exec lamp-php-1 php bin/bone migrate:diff
docker -H unix:///var/run/docker.sock exec lamp-php-1 php bin/bone migrant:migrate

# In Node container
docker -H unix:///var/run/docker.sock exec lamp-node-1 npm install
docker -H unix:///var/run/docker.sock exec lamp-node-1 npm run build

# In MariaDB container
docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -p myapp
```

## CLI Commands

Bone Framework includes CLI commands via Bone Console:

```bash
# Database migrations
bone migrant:diff
bone migrant:migrate
bone migrant:status

# Package commands
bone package:register MyPackage

# Clear cache
bone cache:clear

# List routes
bone route:list
```

## Recommended Packages

### Commonly Used Packages
| Package | Purpose |
|---------|----------|
| `delboy1978uk/bone-form` | Form generation and handling |
| `delboy1978uk/bone-doctrine` | Doctrine ORM integration |
| `delboy1978uk/bone-user` | User registration and authentication |
| `delboy1978uk/bone-passport` | Role-based access control |
| `delboy1978uk/bone-oauth2` | OAuth2 server and API |
| `delboy1978uk/bone-open-api` | OpenAPI/Swagger documentation |
| `delboy1978uk/image` | Image manipulation |
| `delboy1978uk/bone-mail` | Email functionality |
| `delboy1978uk/bone-settings` | Settings management |
| `delboy1978uk/bone-push-notifications` | Push notifications |

### Installing Additional Packages

```bash
# Via Composer
composer require delboy1978uk/bone-form
composer require delboy1978uk/bone-user

# Register in config/packages.php
# Run migrations if needed
bone migrant:diff
bone migrant:migrate
```

## Development Best Practices

### 1. Use Dependency Injection
Inject dependencies through constructors and register in the container.

```php
class MyController extends Controller
{
    public function __construct(
        private MyService $myService
    ) {}
}
```

### 2. Keep Controllers Thin
Delegate business logic to services.

```php
// Bad
public function createAction($request)
{
    // Long business logic here
}

// Good
public function createAction($request)
{
    $this->myService->processData($data);
}
```

### 3. Use Environment Variables
Never hardcode configuration.

```env
# Good
DB_HOST=<?= getenv('DB_HOST') ?>

# Bad
DB_HOST=localhost
```

### 4. Validate Input
Always validate and sanitize user input.

```php
$form->add([
    'name' => 'email',
    'type' => 'Email',
    'validators' => [
        new \Laminas\Validator\EmailAddress(),
    ],
]);
```

### 5. Handle Errors Gracefully
Use try-catch blocks and log errors properly.

```php
try {
    $this->myService->process();
} catch (\Exception $e) {
    $this->logger->error($e->getMessage());
    $this->flash('error', 'An error occurred');
}
```

### 6. Follow PSR Standards
- PSR-7: HTTP messages
- PSR-11: Container interface
- PSR-15: HTTP middleware
- PSR-3: Logger interface

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

4. **Template Not Found**
   - Check template path in `config/views.php`
   - Verify template file exists

5. **Migration Errors**
   - Run `bone migrant:status` to see pending migrations
   - Check database structure matches migrations

## Resources

- **GitHub**: https://github.com/boneframework/skeleton
- **LAMP Stack**: https://github.com/boneframework/lamp
- **Bone Framework**: https://github.com/boneframework
- **Documentation**: Check individual package repositories

## License

MIT License - Free to use and modify.
