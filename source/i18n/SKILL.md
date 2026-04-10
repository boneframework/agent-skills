---
name: bone-i18n
description: "Handles internationalization and translation in Bone Framework applications using delboy1978uk/bone-i18n package with Gettext support and Symfony Translation integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "i18n", "internationalization", "translation", "gettext"]
trigger_patterns:
  - "i18n"
  - "internationalization"
  - "translation"
  - "translate"
  - "gettext"
  - "locale"
  - "multi-language"
---

# Bone I18n Skill

## When to Use
Activate this skill when implementing internationalization and translation in a Bone Framework application using the `delboy1978uk/bone-i18n` package.

## Package Information
- **Package**: `delboy1978uk/bone-i18n`
- **Dependencies**: symfony/translation, delboy1978uk/form, bone-view, bone-http
- **License**: MIT
- **PHP Version**: ^8.2
- **Requirements**: ext-intl PHP extension

## Core Components

### I18nPackage
Main package class that registers translation services:
```php
class I18nPackage implements RegistrationInterface, GlobalMiddlewareRegistrationInterface
{
    public function addToContainer(Container $c): void
    {
        // Setup translator, load extensions
    }
    
    public function getMiddleware(Container $c): array
    {
        return [new I18nMiddleware(...)];
    }
    
    public function getGlobalMiddleware(Container $c): array
    {
        return [I18nMiddleware::class];
    }
}
```

### TranslatorInterface
The translation service interface:
```php
interface TranslatorInterface
{
    public function translate(string $message, ?string $textDomain = null, ?string $locale = null): string;
    public function getLocale(): string;
    public function setLocale(string $locale): void;
}
```

### I18nMiddleware
Handles locale detection and switching:
```php
class I18nMiddleware implements MiddlewareInterface
{
    public function process($request, $handler): ResponseInterface
    {
        // Detect locale from request
        // Set translator locale
        return $handler->handle($request);
    }
}
```

## Configuration

### Basic Configuration
```php
// config/bone-i18n.php
return [
    'i18n' => [
        'enabled' => true,
        'translations_dir' => 'data/translations',
        'type' => Gettext::class,  // Or another loader class
        'default_locale' => 'en_GB',
        'supported_locales' => ['en_GB', 'fr_FR', 'de_DE'],
        'date_format' => 'd/m/Y',
    ]
];
```

### Available Loader Types
- `Laminas\I18n\Translator\Loader\Gettext` - .po/.mo files
- `Laminas\I18n\Translator\Loader\Ini` - INI files
- `Laminas\I18n\Translator\Loader\PhpArray` - PHP arrays
- `Laminas\I18n\Translator\Loader\Sql` - Database

## Translation Methods

### Using Translator Service
```php
use Bone\Contracts\Service\TranslatorInterface;

// Get translator from container
$translator = $container->get(TranslatorInterface::class);

// Simple translation
echo $translator->translate('Welcome');

// Translation with placeholders
echo $translator->translate('Hello {name}', ['name' => 'John']);

// Specific locale
echo $translator->translate('Hello', null, 'fr_FR');
```

### In Controllers
```php
class MyController
{
    use HasTranslatorTrait;
    
    public function indexAction()
    {
        $title = $this->translator->translate('Welcome');
        $message = $this->translator->translate('Hello {name}', ['name' => 'John']);
    }
}
```

### In Views (Plates Template Engine)
```php
// Plates extension registered automatically
echo $this->translate('Welcome');
echo $this->translate('Hello {name}', ['name' => 'John']);
```

### Using Translate Extension
```php
// In Plates templates
<?php echo $this->translate('Hello World'); ?>
<?php echo $this->translate('Count: {count}', ['count' => 5]); ?>
```

### Using LocaleLink Extension
```php
// In Plates templates
// Generate locale switcher links
echo $this->localeLink('fr_FR');
echo $this->localeLink('de_DE');
```

## Translation File Format

### Gettext Format (.po/.mo)
```po
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"

msgid "Welcome"
msgstr "Bienvenue"

msgid "Hello {name}"
msgstr "Bonjour {name}"

msgid "There are {count} items"
msgstr "Il y a {count} articles"
```

###INI Format
```ini
[en]
Welcome = Welcome
Hello {name} = Hello {name}
There are {count} items = There are {count} items

[fr]
Welcome = Bienvenue
Hello {name} = Bonjour {name}
There are {count} items = Il y a {count} articles
```

## Form Translation

### Using Form with Translation
```php
use Bone\I18n\Form;

$form = new Form($translator);

// Labels are automatically translated
$form->add([
    'name' => 'username',
    'label' => 'Username',  // Will be translated
    'type' => 'text',
]);
```

### I18nAwareInterface
Forms can implement this to receive translator:
```php
interface I18nAwareInterface
{
    public function setTranslator(TranslatorInterface $translator): void;
    public function getTranslator(): ?TranslatorInterface;
}
```

## Common Tasks

### 1. Setting Default Locale
```php
// In config/bone-i18n.php
return [
    'i18n' => [
        'default_locale' => 'en_GB',
        'supported_locales' => ['en_GB', 'fr_FR', 'de_DE'],
    ]
];
```

### 2. Changing Locale at Runtime
```php
$translator = $container->get(TranslatorInterface::class);
$translator->setLocale('fr_FR');

// Or in controller
$this->translator->setLocale('fr_FR');
```

### 3. Detecting User Locale
```php
use Bone\I18n\Http\Middleware\I18nMiddleware;

// Middleware handles detection from:
// 1. URL parameter (?locale=fr_FR)
// 2. Session variable
// 3. Cookie
// 4. Accept-Language header
```

### 4. Creating Translation Files
```bash
# Using xgettext or poEdit to create .po files
# Then compile to .mo files for performance
msgfmt data/translations/fr_FR/messages.po -o data/translations/fr_FR/messages.mo
```

### 5. Date/Time Localization
```php
use Bone\I18n\Service\DateFormatter;

// In config/bone-i18n.php
return [
    'i18n' => [
        'date_format' => 'd/m/Y',  // French format
    ]
];

// In controller
echo date('d/m/Y', $timestamp);
```

## Locale Switching

### URL-Based Switching
```
/?locale=fr_FR
/admin?locale=de_DE
```

### Cookie-Based Switching
```php
// User's preference stored in cookie
setcookie('locale', 'fr_FR', time() + 3600 * 24 * 30);
```

### Session-Based Switching
```php
$session->set('locale', 'fr_FR');
```

## Middleware Configuration

### I18nMiddleware Options
```php
// In I18nPackage
$i18nMiddleware = new I18nMiddleware(
    $translator,
    $i18n['supported_locales'],    // Available locales
    $i18n['default_locale'],       // Default locale
    $i18n['enabled']                // Whether enabled
);
```

## Best Practices

1. **Enable i18n early**: Add I18nPackage early in packages.php
2. **Use Gettext for performance**: Compile .po to .mo files
3. **Set default locale**: Always define default_locale
4. **Provide locale options**: Allow users to switch locales
5. **Use placeholders**: Don't concatenate translated strings
6. **Context matters**: Use different messages for different contexts
7. **Test all locales**: Verify translation works in all supported locales
8. **Handle pluralization**: Use proper plural forms for each language
9. **Cache translations**: Compile .po to .mo for production
10. **Document translations**: Keep translation keys consistent

## Configuration File Examples

### Full I18n Configuration
```php
// config/bone-i18n.php
return [
    'i18n' => [
        'enabled' => true,
        'translations_dir' => 'data/translations',
        'type' => \Laminas\I18n\Translator\Loader\Gettext::class,
        'default_locale' => 'en_GB',
        'supported_locales' => ['en_GB', 'fr_FR', 'de_DE', 'es_ES'],
        'date_format' => 'd/m/Y',
    ]
];
```

### Multi-Module Translations
```php
// config/bone-i18n.php
return [
    'i18n' => [
        'enabled' => true,
        'translations_dir' => 'data/translations',
        'type' => Gettext::class,
        'default_locale' => 'en_GB',
        'supported_locales' => ['en_GB', 'fr_FR'],
    ]
];

// For module-specific translations
// Load additional files via TranslatorFactory
$factory->addPackageTranslations($translator, $package, $locale);
```
