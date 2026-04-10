---
name: bone-server
description: "Handles server configuration, environment detection, and site configuration in Bone Framework applications using delboy1978uk/bone-server package with PSR-7 integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "server", "environment", "configuration", "site-config"]
trigger_patterns:
  - "server"
  - "environment"
  - "configuration"
  - "site-config"
  - "server-config"
  - "apache"
---

# Bone Server Skill

## When to Use
Activate this skill when working with server configuration, environment detection, or site configuration in a Bone Framework application using the `delboy1978uk/bone-server` package.

## Package Information
- **Package**: `delboy1978uk/bone-server`
- **Dependencies**: delboy1978uk/session
- **License**: MIT
- **PHP Version**: ^8.2

## Core Components

### Environment
Replaces `$_SERVER` superglobal with a cleaner interface:
```php
use Bone\Server\Environment;

$environment = new Environment($_SERVER);
$host = $environment->getHttpHost();
$method = $environment->getRequestMethod();
```

### SiteConfig
Contains site-wide configuration:
```php
use Bone\Server\SiteConfig;

$config = new SiteConfig($configArray, $environment);
$title = $config->getTitle();
$domain = $config->getDomain();
$email = $config->getContactEmail();
```

## Environment Class

### Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getApplicationEnv()` | string | APPLICATION_ENV value |
| `getPhpIniDir()` | string | PHP INI directory |
| `getPwd()` | string | Current working directory |
| `getUser()` | string | Current user |
| `getRequestUri()` | string | REQUEST_URI |
| `getQueryString()` | string | Query string |
| `getRequestMethod()` | string | HTTP method |
| `getScriptFilename()` | string | Script filename |
| `getServerAdmin()` | string | Server admin |
| `getRequestScheme()` | string | http/https |
| `getDocumentRoot()` | string | Document root |
| `getRemoteAddress()` | string | Client IP |
| `getServerPort()` | string | Server port |
| `getServerName()` | string | Server name |
| `getHttpHost()` | string | Host header |
| `getSiteURL()` | string | Full site URL |

### Usage Examples
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);

// Environment detection
if ($env->getApplicationEnv() === 'development') {
    // Development-specific code
}

// Get current URL
$scheme = $env->getRequestScheme();  // http or https
$host = $env->getHttpHost();
$uri = $env->getRequestUri();
$url = $scheme . '://' . $host . $uri;

// Check request method
if ($env->getRequestMethod() === 'POST') {
    // Handle POST request
}
```

## SiteConfig Class

### Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getTitle()` | string | Site title |
| `getDomain()` | string | Domain name |
| `getContactEmail()` | string | Contact email |
| `getServerEmail()` | string | Server email |
| `getBaseUrl()` | string | Base URL |
| `getCompany()` | string | Company name |
| `getAddress()` | string | Company address |
| `getLogo()` | string | Logo path |
| `getEmailLogo()` | string | Email logo path |
| `getEnvironment()` | Environment | Environment instance |

### Configuration Format
```php
// config/site.php
return [
    'site' => [
        'title' => 'My Website',
        'domain' => 'example.com',
        'baseUrl' => 'https://example.com',
        'contactEmail' => 'contact@example.com',
        'serverEmail' => 'noreply@example.com',
        'company' => 'My Company',
        'address' => '123 Main St, City',
        'logo' => '/img/logo.png',
        'emailLogo' => '/img/email-logo.png',
    ],
];
```

## Configuration Integration

### Loading Config
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);
$config = $env->fetchConfig('config', $env->getApplicationEnv());
```

### Config Merging
- Base config loaded from `config/*.php`
- Environment-specific config from `config/{env}/*.php`
- Environment config overrides base config

### Full Bootstrapping
```php
use Bone\Server\Environment;
use Bone\Application;

$app = Application::ahoy();
$app->setEnvironment('development');
$container = $app->bootstrap();
```

## Common Tasks

### 1. Detecting Environment
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);
$environment = $env->getApplicationEnv();  // development, staging, production

if ($environment === 'development') {
    // Debug settings
} elseif ($environment === 'production') {
    // Production settings
}
```

### 2. Getting Request Information
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);

// Request details
$method = $env->getRequestMethod();
$uri = $env->getRequestUri();
$path = $env->getScriptFilename();

// Client info
$clientIP = $env->getRemoteAddress();
$host = $env->getHttpHost();

// Full URL
$url = $env->getSiteURL() . $env->getRequestUri();
```

### 3. Accessing Site Configuration
```php
use Bone\Application;

$app = Application::ahoy();
$container = $app->getContainer();
$siteConfig = $container->get(SiteConfig::class);

$title = $siteConfig->getTitle();
$domain = $siteConfig->getDomain();
$email = $siteConfig->getContactEmail();
$company = $siteConfig->getCompany();
```

### 4. Building URLs
```php
use Bone\Server\SiteConfig;

$siteConfig = $container->get(SiteConfig::class);

// Base URL
$baseUrl = $siteConfig->getBaseUrl();

// Full URL to resource
$logoUrl = $baseUrl . $siteConfig->getLogo();

// Email URLs
$emailLogo = $baseUrl . $siteConfig->getEmailLogo();
```

### 5. Environment-Specific Config
```php
// config/site.php
return [
    'site' => [
        'title' => 'My Site',
        'domain' => $_ENV['DOMAIN_NAME'],
        'baseUrl' => 'https://' . $_ENV['DOMAIN_NAME'],
    ],
];

// config/development/site.php
return [
    'site' => [
        'title' => 'My Site (Dev)',
        'debug' => true,
    ],
];

// config/production/site.php
return [
    'site' => [
        'title' => 'My Site',
        'debug' => false,
    ],
];
```

### 6. Using Environment in Controllers
```php
use Bone\Controller\Controller;
use Bone\Server\SiteConfig;
use Bone\Server\Environment;

class MyController extends Controller
{
    public function indexAction()
    {
        $environment = $this->siteConfig->getEnvironment();
        $env = $environment->getApplicationEnv();
        
        if ($env === 'development') {
            // Enable debug info
        }
        
        return $this->view->render('index', $vars);
    }
}
```

### 7. Detecting HTTPS
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);

// Check if HTTPS
if ($env->getRequestScheme() === 'https') {
    // Force HTTPS redirects, set secure cookies
}

// Or check SERVER['HTTPS']
$isHttps = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on';
```

### 8. Getting Query Parameters
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);

// Query string
$query = $env->getQueryString();  // "page=1&sort=name"

// Parse query
parse_str($query, $params);
$page = $params['page'] ?? 1;
```

### 9. Logging Environment Info
```php
use Bone\Server\Environment;

$env = new Environment($_SERVER);
$logger->info('Request received', [
    'method' => $env->getRequestMethod(),
    'uri' => $env->getRequestUri(),
    'ip' => $env->getRemoteAddress(),
    'user_agent' => $env->getAttribute('HTTP_USER_AGENT'),
    'env' => $env->getApplicationEnv(),
]);
```

### 10. Configuring Environment Variables
```php
// .env file
APPLICATION_ENV=development
DB_HOST=localhost
DB_NAME=app_dev
DOMAIN_NAME=localhost:8080

// config/bone-db.php
return [
    'db' => [
        'host' => $_ENV['DB_HOST'],
        'dbname' => $_ENV['DB_NAME'],
        'user' => $_ENV['DB_USERNAME'],
        'password' => $_ENV['DB_PASSWORD'],
    ],
];
```

## Configuration File Examples

### Development Environment
```php
// config/development/site.php
return [
    'site' => [
        'title' => 'My Site - Dev',
        'debug' => true,
        'error_reporting' => E_ALL,
    ],
];

// config/development/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => 'php://stdout',
        ],
    ],
];
```

### Production Environment
```php
// config/production/site.php
return [
    'site' => [
        'title' => 'My Site',
        'debug' => false,
        'error_reporting' => 0,
    ],
];

// config/production/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => '/var/log/app/app.log',
        ],
    ],
];
```

## Best Practices

1. **Use Environment class**: Avoid direct `$_SERVER` access
2. **Environment-specific configs**: Override configs per environment
3. **Validate environment values**: Check for expected environment names
4. **Use SiteConfig for site-wide settings**: Centralize configuration
5. **Get site config from container**: Don't instantiate manually
6. **Document environment variables**: List required .env variables
7. **Handle missing values**: Use null coalescing or defaults
8. **Test environment detection**: Verify ENV values are correct
9. **Secure sensitive data**: Never commit .env with secrets
10. **Use APPLICATION_ENV**: Standardize environment naming
