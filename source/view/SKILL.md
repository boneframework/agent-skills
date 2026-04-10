---
name: bone-view
description: "Handles view rendering, templates, layout management, and view helpers in Bone Framework applications using league/plates and Bone View package."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "view", "templates", "plates", "layout", "helpers"]
trigger_patterns:
  - "view"
  - "template"
  - "render"
  - "plates"
  - "layout"
  - "alert"
  - "paginator"
---

# Bone View Skill

## When to Use
Activate this skill when working with view rendering, templates, layout management, or view helpers in a Bone Framework application using the `delboy1978uk/bone-view` package.

## Package Information
- **Package**: `delboy1978uk/bone-view`
- **Dependencies**: league/plates (templating engine), boneframework/contracts, delboy1978uk/bone-http
- **License**: MIT

## Core Components

### ViewEngine
The primary interface for template rendering, extending `League\Plates\Engine`:
- Implements `ViewEngineInterface`
- Methods: `render($view, $vars = [])`, `addFolder($name, $directory, $fallback = false)`
- Automatically loaded with extensions: AlertBox and AdminLinks

### ViewPackage
The main package class that registers view components:
- Implements `RegistrationInterface` and `GlobalMiddlewareRegistrationInterface`
- Registers `ViewEngine` and `ViewEngineInterface` in the container
- Adds `AlertBox` and `AdminLinks` extensions by default
- Registers middleware: `LayoutMiddleware` and `ExceptionMiddleware`

## Middlewares

### LayoutMiddleware
Wraps HTML responses with a layout template:
- Constructor: `__construct(ViewEngineInterface $viewEngine, string $defaultLayout, SiteConfig $config)`
- Checks for `LayoutResponse` or `layout` header to determine layout
- Renders the layout with content, config, user, and vars
- Skips layout if response is not HTML or layout is disabled ('none')

### ExceptionMiddleware
Catches exceptions and renders error pages:
- Constructor: `__construct(ViewEngineInterface $viewEngine, array $errorPages)`
- Returns default 500 error page for unknown exceptions
- Uses status code to select error page from configured errorPages
- Logs exception message and trace to PHP error log

## View Helpers and Extensions

### AlertBox Helper
Renders Bootstrap-style alert messages:

**Template function**: `alert($message, $closeButton = true)`

```php
<?php
// Usage in template
echo $this->alert(['User created successfully', 'success']);
echo $this->alert(['Error saving data', 'danger']);
?>
```

**Helper class**: `Bone\View\Helper\AlertBox`
- `alertBox(array $message, bool $closeButton = true): string`
- Automatically detects alert class (alert-success, alert-danger, etc.)
- Supports multiple lines with `<br>` separation

### AdminLinks Extension
Generates admin navigation menu:
- Uses `AdminLinksHelper` to collect links from packages implementing `AdminPanelProviderInterface`
- Renders as Bootstrap pills sidebar with FontAwesome icons
- Supports custom classes for ul, li, a, and icon elements
- Links are sorted alphabetically by name

**Template function**: `adminLinks()`

```php
<?php
// Usage in admin layout template
echo $this->adminLinks();
?>
```

### Paginator Helper
Renders pagination navigation:
- Uses `Del\Icon` for navigation arrows (backward, fast-backward, forward, fast-forward)
- Supports configurable page size, URL patterns, and current page
- Renders with Bootstrap pagination classes

**Configuration methods**:
- `setPageCount(int $pageCount)`
- `setPageCountByTotalRecords(int $rowCount, int $numPerPage)`
- `setCurrentPage(int $pageNo)`
- `setUrl(string $url)` - URL must contain `:page` placeholder
- `setPagerSize(int $numBoxes)` - Number of page links to show (must be odd)
- `setLimit(?int $limit)` - Optional limit parameter for URL

**Template function**: Available via Plates template engine

### AdminLink Utility
Represents a single admin navigation link:
- Properties: name, url, iconClass, aClass, liClass
- Used by packages to define admin menu items via `getAdminLinks()`

## Common Tasks

### 1. Configuring Views
In `config/views.php`:
```php
return [
    'views' => [
        'boneuser' => 'src/App/View/bone-user',
        'email.user' => 'src/App/View/email',
        'contact' => 'src/App/View/contact',
    ],
];
```

### 2. Setting Default Layout
In `config/layouts.php`:
```php
return [
    'default_layout' => 'layout',
    'error_pages' => [
        403 => 'not-allowed',
        404 => 'not-found',
        500 => 'error',
    ],
];
```

### 3. Creating a Controller with View
```php
use Bone\View\Traits\HasViewTrait;
use Bone\View\ViewEngineInterface;

class MyController
{
    use HasViewTrait;
    
    public function __construct(ViewEngineInterface $view)
    {
        $this->setView($view);
    }
    
    public function indexAction()
    {
        $body = $this->view->render('my-template', [
            'title' => 'My Page',
            'items' => $items
        ]);
        return new HtmlResponse($body);
    }
}
```

### 4. Rendering with Layout
```php
use Bone\Http\Response\LayoutResponse;

// Option 1: Set layout header
$response = new HtmlResponse($body);
$response->headers->set('layout', 'admin');

// Option 2: Use LayoutResponse
$response = new LayoutResponse($body, 'admin');
```

### 5. Using View Helpers in Templates
```php
<!-- Alert Box -->
<?php echo $this->alert(['Operation completed', 'success']); ?>

<!-- Admin Links Navigation -->
<?php echo $this->adminLinks(); ?>

<!-- Pagination -->
<?php
$pager = new Bone\View\Helper\Paginator();
$pager->setUrl('/page/:page');
$pager->setPageCountByTotalRecords($total, 10);
$pager->setCurrentPage($currentPage);
echo $pager->render();
?>
```

### 6. Creating Admin Panel Links
Packages implementing `AdminPanelProviderInterface` return links:

```php
use Bone\Contracts\Container\AdminPanelProviderInterface;
use Bone\View\Util\AdminLink;

class MyPackage implements AdminPanelProviderInterface
{
    public function getAdminLinks(): array
    {
        return [
            new AdminLink('My Settings', '/admin/settings', 'fa fa-cog'),
            new AdminLink('Manage Users', '/admin/users', 'fa fa-users'),
        ];
    }
}
```

## Configuration Files

### layouts.php
```php
return [
    'default_layout' => 'layout',           // Default layout template
    'error_pages' => [                      // Error page templates
        403 => 'not-allowed',
        404 => 'not-found',
        500 => 'error',
    ],
];
```

### views.php
```php
return [
    'views' => [
        // Map view names to folder paths
        'view-name' => 'path/to/view/folder',
    ],
];
```

## Error Pages
Default error pages in tests/_data/error/:
- `error.php` - General error page (500)
- `not-allowed.php` - Forbidden (403)
- `not-authorised.php` - Unauthorised (401)
- `not-found.php` - Not found (404)

## Best Practices
1. Always use `HasViewTrait` in controllers that need view rendering
2. Use `LayoutResponse` or set `layout` header for pages with layouts
3. Set `layout` to `none` to disable layout wrapping
4. Use AlertBox helper for user feedback messages
5. Use Paginator helper for consistent pagination across the app
6. Implement `AdminPanelProviderInterface` for admin packages
7. Organize view templates by module (e.g., `boneuser`, `email`)
8. Use Plates `e()` function for escaping: `<?php echo $this->e($var); ?>`
9. Register custom view folders via `addFolder()` method
10. Keep view logic in helpers, not templates
