---
name: bone-contracts
description: "Provides interfaces and contracts for Bone Framework packages including container, service, and registration interfaces."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "contracts", "interfaces", "psr", "di"]
trigger_patterns:
  - "contracts"
  - "interface"
  - "container"
  - "registration"
  - "di"
  - "dependency injection"
---

# Bone Contracts Skill

## When to Use
Activate this skill when working with Bone Framework package interfaces, dependency injection contracts, or needing to understand the contract definitions for Bone Framework packages.

## Package Information
- **Package**: `boneframework/contracts`
- **Dependencies**: psr/container, psr/http-message, psr/http-server-middleware, symfony/contracts
- **License**: MIT
- **PHP Version**: Requires PSR compliant interfaces

## Core Interfaces

### Container Interfaces

#### ContainerInterface
PSR-11 compatible container interface:
```php
interface ContainerInterface
{
    public function get($id);
    public function has($id): bool;
}
```

#### RegistrationInterface
Base interface for all Bone Framework packages:
```php
interface RegistrationInterface
{
    public function addToContainer(ContainerInterface $c): void;
}
```

### Package Registration Interfaces

#### CommandRegistrationInterface
For packages that register console commands:
```php
interface CommandRegistrationInterface
{
    public function registerConsoleCommands(Container $container): array;
}
```

#### RouterConfigInterface
For packages that define routes:
```php
interface RouterConfigInterface
{
    public function addRoutes(Container $c, Router $router);
}
```

#### ViewRegistrationInterface
For packages that register view templates:
```php
interface ViewRegistrationInterface
{
    public function addViews(): array;
    public function addViewExtensions(ContainerInterface $c): array;
}
```

#### I18nRegistrationInterface
For packages that provide translations:
```php
interface I18nRegistrationInterface
{
    // Mark package as providing translations
}
```

#### MiddlewareRegistrationInterface
For packages that register middleware:
```php
interface MiddlewareRegistrationInterface
{
    public function getMiddleware(ContainerInterface $c): array;
}
```

#### GlobalMiddlewareRegistrationInterface
For packages that register global middleware:
```php
interface GlobalMiddlewareRegistrationInterface extends MiddlewareRegistrationInterface
{
    public function getGlobalMiddleware(ContainerInterface $c): array;
}
```

### Provider Interfaces

#### AdminPanelProviderInterface
For packages that provide admin menu links:
```php
interface AdminPanelProviderInterface
{
    public function getAdminLinks(): array;
}
```

#### ApiDocProviderInterface
For packages that provide API documentation:
```php
interface ApiDocProviderInterface
{
    public function getApiDocs(): array;
}
```

#### DefaultSettingsProviderInterface
For packages that provide default settings:
```php
interface DefaultSettingsProviderInterface
{
    public function getDefaultSettings(): array;
}
```

#### DependentPackagesProviderInterface
For packages with dependencies:
```php
interface DependentPackagesProviderInterface
{
    public function getDependentPackages(): array;
}
```

#### EntityRegistrationInterface
For packages that register Doctrine entities:
```php
interface EntityRegistrationInterface
{
    public function getEntityPath(): string;
}
```

#### FixtureProviderInterface
For packages that provide Doctrine fixtures:
```php
interface FixtureProviderInterface
{
    public function getFixtures(): array;
}
```

#### PostFixturesProviderInterface
For post-installation fixtures:
```php
interface PostFixturesProviderInterface
{
    public function getPostFixtures(): array;
}
```

#### PostInstallProviderInterface
For post-installation tasks:
```php
interface PostInstallProviderInterface
{
    public function runPostInstall(ContainerInterface $c): void;
}
```

### Service Interfaces

#### TranslatorInterface
Translation service interface:
```php
interface TranslatorInterface
{
    public function translate(string $message, ?string $textDomain = null, ?string $locale = null): string;
    public function getLocale(): string;
    public function setLocale(string $locale): void;
}
```

#### RestServiceInterface
REST service interface:
```php
interface RestServiceInterface
{
    // Methods for REST API services
}
```

#### ViewEngineInterface
View rendering interface:
```php
interface ViewEngineInterface
{
    public function render($view, array $vars = []);
    public function addFolder($name, $directory, $fallback = false);
}
```

## Usage Examples

### Creating a Package
```php
use Bone\Contracts\Container\ContainerInterface;
use Bone\Contracts\Container\RegistrationInterface;

class MyPackage implements RegistrationInterface
{
    public function addToContainer(ContainerInterface $c): void
    {
        // Register services
        $c[MyService::class] = $c->factory(function ($c) {
            return new MyService();
        });
    }
}
```

### Registering Routes
```php
use Bone\Contracts\Container\ContainerInterface;
use Bone\Contracts\Container\RouterConfigInterface;
use Bone\Router\Router;

class MyRouterPackage implements RouterConfigInterface
{
    public function addRoutes(ContainerInterface $c, Router $router): void
    {
        $router->get('/my/route', [MyController::class, 'action']);
    }
}
```

### Providing Admin Links
```php
use Bone\Contracts\Container\AdminPanelProviderInterface;
use Bone\View\Util\AdminLink;

class AdminPackage implements AdminPanelProviderInterface
{
    public function getAdminLinks(): array
    {
        return [
            new AdminLink('My Link', '/admin/my-link', 'fa fa-cog'),
        ];
    }
}
```

### Providing Entities
```php
use Bone\Contracts\Container\EntityRegistrationInterface;

class EntityPackage implements EntityRegistrationInterface
{
    public function getEntityPath(): string
    {
        return 'src/Entity';
    }
}
```

### Providing Fixtures
```php
use Bone\Contracts\Container\FixtureProviderInterface;
use App\Fixtures\UserFixture;

class FixturePackage implements FixtureProviderInterface
{
    public function getFixtures(): array
    {
        return [
            UserFixture::class,
        ];
    }
}
```

## Interface Hierarchy

```
ContainerInterface (PSR-11)
    └── RegistrationInterface
        └── CommandRegistrationInterface
        └── RouterConfigInterface
        └── ViewRegistrationInterface
        └── I18nRegistrationInterface
        └── MiddlewareRegistrationInterface
            └── GlobalMiddlewareRegistrationInterface
        └── AdminPanelProviderInterface
        └── ApiDocProviderInterface
        └── DefaultSettingsProviderInterface
        └── EntityRegistrationInterface
        └── FixtureProviderInterface
        └── PostInstallProviderInterface
```

## Service Interfaces

```
ServiceInterfaces
    └── TranslatorInterface
    └── RestServiceInterface
    └── ViewEngineInterface
```

## Integration with Bone Framework

### Package Discovery
Bone Framework automatically discovers packages listed in `packages.php`:
```php
// config/packages.php
return [
    'packages' => [
        App\MyPackage::class,
        App\MyRouterPackage::class,
    ]
];
```

### Package Processing
The ApplicationPackage iterates through packages and:
1. Calls `addToContainer()` on each
2. Checks for `RouterConfigInterface` - adds routes
3. Checks for `ViewRegistrationInterface` - adds views
4. Checks for `MiddlewareRegistrationInterface` - adds middleware
5. Checks for `I18nRegistrationInterface` - loads translations

### Container Registration Flow
1. `ApplicationPackage::addToContainer()` is called
2. Each registered package has `addToContainer()` called
3. Package methods register services into container
4. Services become available via `$container->get()`

## Best Practices

1. **Implement appropriate interfaces**: Only implement what you need
2. **Return arrays from registration methods**: Consistent return types
3. **Use factories for complex objects**: `$c->factory()` for services
4. **Check interface existence**: `instanceof` checks in ApplicationPackage
5. **Keep interfaces focused**: Single responsibility per interface
6. **Document interface requirements**: What each interface expects
7. **Use PSR interfaces**: Leverage existing PSR standards
8. **Namespace properly**: Bone\Contracts\Container\*
9. **Test interfaces**: Verify package works with interface expectations
10. **Keep backward compatible**: Don't break interface signatures

## Interface Summary

| Interface | Purpose | When to Use |
|-----------|---------|-------------|
| `RegistrationInterface` | Base package interface | Every package |
| `RouterConfigInterface` | Define routes | Routes package |
| `ViewRegistrationInterface` | Register templates | View package |
| `MiddlewareRegistrationInterface` | Register middleware | Middleware package |
| `GlobalMiddlewareRegistrationInterface` | Global middleware | Site-wide middleware |
| `AdminPanelProviderInterface` | Admin menu links | Admin package |
| `EntityRegistrationInterface` | Entity paths | Doctrine package |
| `FixtureProviderInterface` | Fixtures | Data setup |
| `I18nRegistrationInterface` | Translations | Multi-language |
| `CommandRegistrationInterface` | CLI commands | Console package |
