---
name: bone-settings
description: "Handles settings management in Bone Framework applications using delboy1978uk/bone-settings package for generic settings storage with Doctrine ORM support."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "settings", "configuration", "database", "options"]
trigger_patterns:
  - "bone-settings"
  - "settings"
  - "configuration"
  - "options"
  - "database settings"
---

# Bone Settings Skill

## When to Use
Activate this skill when managing generic application settings and configuration storage in Bone Framework applications using the delboy1978uk/bone-settings package.

## Package Information
- **Package**: `delboy1978uk/bone-settings`
- **License**: MIT
- **PHP Version**: ^8.1
- **Dependencies**: bone-oauth2, bone-doctrine

## Installation

```bash
composer require delboy1978uk/bone-settings
```

## Package Features

### Key Features
- Generic settings entity with Doctrine ORM support
- Dual-primary-key structure (settingsGroup + owner)
- Supports custom settings classes via inheritance
- Includes UserSettings entity as reference implementation
- JSON-encoded values for flexibility

## Entities

### AbstractSettings (Base Class)
```php
#[ORM\Entity]
#[ORM\Table(name: 'settings')]
abstract class AbstractSettings
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 255)]
    private string $key;  // Setting key (e.g., 'email.from')

    #[ORM\Column(type: 'json', nullable: true)]
    private ?array $value = null;  // JSON-encoded value

    #[ORM\Column(type: 'integer', options: ['default' => 1])]
    private int $settingsGroupId = 1;  // Group ID (default: 1)

    #[ORM\Column(type: 'integer')]
    private int $ownerId;  // Owner entity ID (e.g., user_id)
}
```

### UserSettings (Concrete Implementation)
```php
#[ORM\Entity]
#[ORM\Table(name: 'user_settings')]
class UserSettings extends AbstractSettings
{
    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: User::class)]
    private User $owner;

    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: SettingsGroup::class)]
    private SettingsGroup $settingsGroup;

    #[ORM\Column(type: 'string', length: 255)]
    private string $key;

    #[ORM\Column(type: 'json', nullable: true)]
    private ?array $value = null;

    // Getters and setters...
}
```

## Package Registration

```php
// config/packages.php
return [
    'packages' => [
        \Bone\Settings\SettingsPackage::class,
        // ... other packages
    ]
];
```

## Settings Structure

### Key Naming Convention
- Use dot notation for nested settings
- Group related settings by prefix

```php
// Examples
'email.from'          // Basic setting
'email.reply_to'      // Related setting
'mailchimp.api_key'   // Grouped by service
'mailchimp.list_id'
'social.facebook_url' // Grouped by service
'social.twitter_url'
```

## Usage Examples

### Creating Settings

```php
use Bone\Settings\Manager\SettingsManager;

// Get settings manager from container
$settings = $container->get(SettingsManager::class);

// Set a simple value
$settings->set('site.title', 'My Website');

// Set with group
$settings->set('email.from', 'noreply@example.com', 'email');

// Set complex value (array/object)
$settings->set('mailchimp.config', [
    'api_key' => 'your-key',
    'list_id' => 'your-list-id',
]);

// Set with owner (user-specific settings)
$settings->set('theme', 'dark', null, $userId);
```

### Getting Settings

```php
// Get single setting
$title = $settings->get('site.title');

// Get with default
$title = $settings->get('site.title', 'Default Title');

// Get by group
$emailSettings = $settings->getGroup('email');
// Returns ['email.from' => '...', 'email.reply_to' => '...']

// Get all settings
$allSettings = $settings->getAll();

// Get user-specific settings
$userSettings = $settings->getByOwner($userId);
```

### Updating Settings

```php
// Get current value
$current = $settings->get('site.description');

// Update
$settings->set('site.description', 'New description');

// Update complex value
$config = $settings->get('mailchimp.config');
$config['api_key'] = 'new-key';
$settings->set('mailchimp.config', $config);
```

### Deleting Settings

```php
// Delete single setting
$settings->delete('site.title');

// Delete by group
$settings->deleteGroup('email');

// Delete by owner
$settings->deleteByOwner($userId);
```

## Settings Manager Service

### Complete SettingsManager Interface
```php
class SettingsManager
{
    // Basic operations
    public function set($key, $value, $groupId = 1, $ownerId = null): void;
    public function get($key, $default = null);
    public function has($key): bool;
    public function delete($key): void;
    
    // Group operations
    public function getGroup($groupId): array;
    public function deleteGroup($groupId): void;
    public function clearGroup($groupId): void;
    
    // Owner operations
    public function getByOwner($ownerId): array;
    public function deleteByOwner($ownerId): void;
    public function clearByOwner($ownerId): void;
    
    // Utility
    public function getAll(): array;
    public function getKeys(): array;
}
```

## Settings Form Implementation

### Settings Form
```php
use Del\Form\Form;
use Del\Form\Field\Text;
use Del\Form\Field\TextArea;
use Del\Form\Field\Select;

class SiteSettingsForm extends Form
{
    public function __construct(
        private SettingsManager $settings
    ) {
        $this->init();
    }
    
    public function init(): void
    {
        $this->addField((new Text('site.title'))
            ->setLabel('Site Title')
            ->setValue($this->settings->get('site.title', 'My Website')));
        
        $this->addField((new Text('site.subtitle'))
            ->setLabel('Site Subtitle')
            ->setValue($this->settings->get('site.subtitle', '')));
        
        $this->addField((new Text('email.from'))
            ->setLabel('From Email')
            ->setValue($this->settings->get('email.from', 'noreply@example.com'))
            ->setAttribute('type', 'email'));
        
        $this->addField((new TextArea('seo.description'))
            ->setLabel('SEO Description')
            ->setValue($this->settings->get('seo.description', '')));
        
        $this->addField((new Text('mailchimp.api_key'))
            ->setLabel('Mailchimp API Key')
            ->setValue($this->settings->get('mailchimp.api_key', '')));
    }
    
    public function save(): bool
    {
        $values = $this->getValues();
        
        foreach ($values as $key => $value) {
            $this->settings->set($key, $value);
        }
        
        return true;
    }
}
```

### Settings Controller
```php
class SettingsController extends Controller
{
    public function indexAction($request)
    {
        $group = $request->getAttribute('group') ?? 'site';
        $settings = $this->settings->getGroup($group);
        
        return $this->view->render('settings/index', [
            'group' => $group,
            'settings' => $settings,
        ]);
    }
    
    public function updateAction($request)
    {
        $group = $request->getAttribute('group');
        $form = new SiteSettingsForm($this->settings);
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $form->save();
                $this->flash('success', 'Settings updated successfully');
                return $this->redirect('/settings/' . $group);
            }
        }
        
        return $this->view->render('settings/edit', [
            'group' => $group,
            'form' => $form,
        ]);
    }
}
```

## Database Schema

### Settings Table
```sql
CREATE TABLE settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key VARCHAR(255) NOT NULL,
    value JSON DEFAULT NULL,
    settings_group_id INT NOT NULL DEFAULT 1,
    owner_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_key (key),
    INDEX idx_owner (owner_id),
    INDEX idx_group (settings_group_id)
);

-- Default settings group
INSERT INTO settings_groups (id, name, description) VALUES 
(1, 'default', 'Default settings group');
```

### UserSettings Table
```sql
CREATE TABLE user_settings (
    owner_id INT NOT NULL,
    settings_group_id INT NOT NULL DEFAULT 1,
    key VARCHAR(255) NOT NULL,
    value JSON DEFAULT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (owner_id, settings_group_id, key),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (settings_group_id) REFERENCES settings_groups(id) ON DELETE CASCADE
);
```

## Settings Best Practices

1. **Use dot notation for hierarchy**: `service.option.suboption`
2. **Group related settings**: Email, Mailchimp, Social
3. **Provide defaults**: Always have sensible defaults
4. **Validate input**: Validate settings before saving
5. **Cache settings**: Use caching for production performance
6. **Document settings**: Create documentation for each setting
7. **Use appropriate data types**: Store arrays as JSON, booleans as booleans
8. **Consider user-specific settings**: Use owner_id for per-user settings
9. **Keep settings simple**: Avoid deeply nested structures
10. **Version settings**: Track changes over time

## Common Use Cases

### Site Configuration
```php
// Site-wide settings
$settings->set('site.name', 'My Website');
$settings->set('site.description', 'A great website');
$settings->set('site.favicon', '/img/favicon.ico');

// Email configuration
$settings->set('email.from', 'noreply@example.com');
$settings->set('email.reply_to', 'support@example.com');

// SEO settings
$settings->set('seo.title_suffix', ' - My Website');
$settings->set('seo.meta_keywords', 'keyword1, keyword2');
```

### Service Integration
```php
// Mailchimp configuration
$settings->set('mailchimp.api_key', 'your-key');
$settings->set('mailchimp.list_id', 'your-list-id');

// Payment configuration
$settings->set('stripe.api_key', 'sk_live_xxx');
$settings->set('stripe.webhook_secret', 'whsec_xxx');
```

### User Preferences
```php
// User theme preference
$settings->set('theme', 'dark', null, $userId);

// User notification settings
$settings->set('notifications.email', true, null, $userId);
$settings->set('notifications.push', false, null, $userId);
```
