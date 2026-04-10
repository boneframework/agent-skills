---
name: bone-controller
description: "Provides base Controller class with common traits for dependency injection, translation, view rendering, and serialization in Bone Framework applications."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "controller", "mvc", "traits", "di"]
trigger_patterns:
  - "controller"
  - "controller base"
  - "mvc"
  - "action"
  - "dispatch"
---

# Bone Controller Skill

## When to Use
Activate this skill when creating controllers in a Bone Framework application that need common functionality like dependency injection, translation, view rendering, and JSON serialization.

## Package Information
- **Package**: `delboy1978uk/bone-controller`
- **Dependencies**: bone-view, bone-i18n, bone-server, bone-db, bone-log, session, serializer
- **License**: MIT
- **PHP Version**: ^8.2

## Core Component: Controller Class

### Available Traits

| Trait | Purpose |
|-------|---------|
| `HasSerializer` | JSON serializer support via JMS Serializer |
| `HasSiteConfigTrait` | Access to site configuration |
| `HasTranslatorTrait` | Internationalization support |
| `HasViewTrait` | View template rendering |
| `Controller` | Main controller class with all traits |

### Controller Class Hierarchy
```php
class Controller 
    implements 
        I18nAwareInterface,
        ViewAwareInterface, 
        SiteConfigAwareInterface, 
        SerializerAwareInterface
{
    use HasSerializer;
    use HasSiteConfigTrait;
    use HasTranslatorTrait;
    use HasViewTrait;
    
    // Additional helper methods
}
```

## Core Features

### 1. View Rendering
Access to Plates template engine:

```php
use Bone\View\ViewEngineInterface;
use Bone\Controller\Traits\HasViewTrait;

class MyController
{
    use HasViewTrait;
    
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

### 2. Translation
Access to translator service:

```php
use Bone\I18n\Traits\HasTranslatorTrait;

class MyController
{
    use HasTranslatorTrait;
    
    public function indexAction()
    {
        $translated = $this->translator->translate('Welcome');
        return $this->translator->translate('Hello {name}', ['name' => 'John']);
    }
}
```

### 3. Site Configuration
Access to site configuration:

```php
use Bone\Server\Traits\HasSiteConfigTrait;

class MyController
{
    use HasSiteConfigTrait;
    
    public function indexAction()
    {
        $title = $this->siteConfig->getTitle();
        $domain = $this->siteConfig->getDomain();
        $contactEmail = $this->siteConfig->getContactEmail();
    }
}
```

### 4. JSON Serialization
Access to JMS Serializer:

```php
use Bone\Controller\Traits\HasSerializer;

class MyController
{
    use HasSerializer;
    
    public function jsonAction()
    {
        $serializer = $this->serializer;
        $json = $serializer->serialize($entity, 'json');
        return new HtmlResponse($json);
    }
}
```

### 5. View with Layout
Set layout for responses:

```php
public function indexAction()
{
    $body = $this->view->render('my-template', $vars);
    $response = new HtmlResponse($body);
    
    // Set layout header
    return $this->responseWithLayout($response, 'admin');
}
```

## Controller Usage Examples

### Basic Controller
```php
<?php

namespace App\Controller;

use Bone\Controller\Controller;
use Laminas\Diactoros\Response\HtmlResponse;
use Psr\Http\Message\ServerRequestInterface;

class HomeController extends Controller
{
    public function indexAction(ServerRequestInterface $request)
    {
        // Get site config
        $title = $this->siteConfig->getTitle();
        
        // Render view
        $body = $this->view->render('home', [
            'title' => $title,
            'message' => $this->translator->translate('Welcome'),
        ]);
        
        return new HtmlResponse($body);
    }
}
```

### API Controller with Serialization
```php
<?php

namespace App\Controller;

use Bone\Controller\Controller;
use Laminas\Diactoros\Response\JsonResponse;

class ApiUserController extends Controller
{
    public function indexAction()
    {
        $users = $this->entityManager->findAll(User::class);
        $json = $this->serializer->serialize($users, 'json');
        return new JsonResponse($json);
    }
}
```

### Form Controller with Validation
```php
<?php

namespace App\Controller;

use Bone\Controller\Controller;
use Bone\View\Form;
use Laminas\Diactoros\Response\HtmlResponse;

class FormController extends Controller
{
    public function submitAction($request)
    {
        $form = new Form($this->translator);
        
        if ($form->isValid()) {
            // Process form
            $this->entityManager->persist($data);
            $this->entityManager->flush();
            
            // Set success message
            $this->session->set('flash', 'Data saved');
            
            // Redirect
            return $this->responseWithLayout(
                new HtmlResponse($body), 
                'none'
            );
        }
        
        // Render form
        $body = $this->view->render('form', ['form' => $form]);
        return new HtmlResponse($body);
    }
}
```

## Trait Details

### HasSerializerTrait
Provides access to JMS Serializer:
```php
trait HasSerializer
{
    protected SerializerInterface $serializer;
    
    public function setSerializer(SerializerInterface $serializer): void
    {
        $this->serializer = $serializer;
    }
    
    public function getSerializer(): SerializerInterface
    {
        return $this->serializer;
    }
}
```

### HasSiteConfigTrait
Provides access to SiteConfig:
```php
trait HasSiteConfigTrait
{
    protected SiteConfig $siteConfig;
    
    public function setSiteConfig(SiteConfig $siteConfig): void
    {
        $this->siteConfig = $siteConfig;
    }
    
    public function getSiteConfig(): SiteConfig
    {
        return $this->siteConfig;
    }
}
```

### HasTranslatorTrait
Provides access to translator:
```php
trait HasTranslatorTrait
{
    protected TranslatorInterface $translator;
    
    public function setTranslator(TranslatorInterface $translator): void
    {
        $this->translator = $translator;
    }
    
    public function getTranslator(): TranslatorInterface
    {
        return $this->translator;
    }
}
```

### HasViewTrait
Provides access to ViewEngine:
```php
trait HasViewTrait
{
    protected ViewEngineInterface $view;
    
    public function setView(ViewEngineInterface $view): void
    {
        $this->view = $view;
    }
    
    public function getView(): ViewEngineInterface
    {
        return $this->view;
    }
}
```

## Service Container Integration

The controller is typically instantiated via the container:
```php
// In config/packages.php
return [
    'packages' => [
        App\AppPackage::class,
    ]
];

// In AppPackage
public function addToContainer(ContainerInterface $c): void
{
    $c[Controller::class] = $c->factory(function ($c) {
        $controller = new Controller();
        $controller->setView($c->get(ViewEngineInterface::class));
        $controller->setTranslator($c->get(TranslatorInterface::class));
        $controller->setSiteConfig($c->get(SiteConfig::class));
        $controller->setSerializer($c->get(SerializerInterface::class));
        return $controller;
    });
}
```

## Best Practices

1. **Extend base Controller**: Always extend `Bone\Controller\Controller`
2. **Use traits for dependencies**: Leverage provided traits
3. **Access services via traits**: Use `$this->view`, `$this->translator`, etc.
4. **Return proper response types**: Use `HtmlResponse`, `JsonResponse`, etc.
5. **Use translation for UI**: Always translate user-facing strings
6. **Set layout for HTML responses**: Use `responseWithLayout()` method
7. **Handle exceptions gracefully**: Catch and log errors appropriately
8. **Validate input**: Always validate request data before processing
9. **Use container for dependencies**: Let container inject services
10. **Keep controllers thin**: Move business logic to service classes

## Controller Lifecycle

1. **Container instantiation**: Controller created via factory
2. **Service injection**: Traits receive required services
3. **Route dispatch**: Request routed to controller action
4. **Action execution**: Method processes request
5. **Response return**: Method returns response object
