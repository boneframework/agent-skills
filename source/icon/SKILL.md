---
name: icon
description: "Handles icon rendering and Font Awesome integration in Bone Framework applications using delboy1978uk/icon package for generating Font Awesome icons."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "icon", "font-awesome", "icons", "ui"]
trigger_patterns:
  - "icon"
  - "font awesome"
  - "fa"
  - "icons"
  - "glyph"
---

# Icon Skill

## When to Use
Activate this skill when working with icons and Font Awesome in Bone Framework applications using the `delboy1978uk/icon` package.

## Package Information
- **Package**: `delboy1978uk/icon`
- **License**: GPL-2.0
- **Type**: PHP class library for Font Awesome icons
- **Version**: Font Awesome 4.3.0

## Overview

The Icon class provides:
- Static constants for all Font Awesome icons
- Helper methods for generating icon HTML
- Support for custom icon classes
- FontAwesome CDN link generation

## Basic Usage

### Using Icon Class
```php
use Del\Icon;

echo Icon::ADD;    // <i class="fa fa-plus"></i>
echo Icon::HOME;   // <i class="fa fa-home"></i>
echo Icon::EDIT;   // <i class="fa fa-edit"></i>
echo Icon::DELETE; // <i class="fa fa-times"></i>
```

### Custom Icon Classes
```php
echo Icon::custom('fa-user', 'text-primary');
// <i class="fa fa-user text-primary"></i>

echo Icon::custom('fa-edit', 'text-success', true);
// <i class="fa fa-edit text-success">&nbsp;</i>
```

## Icon Constants

### Form Icons
- `Icon::ADD` - Plus icon
- `Icon::EDIT` - Edit/pencil icon
- `Icon::DELETE` - Times/X icon
- `Icon::CHECK` - Checkmark icon
- `Icon::REMOVE` - Remove icon
- `Icon::CLOSE` - Close icon

### Navigation Icons
- `Icon::HOME` - Home icon
- `Icon::ARROWS` - Arrows icon
- `Icon::UP` - Up arrow
- `Icon::DOWN` - Down arrow
- `Icon::LEFT` - Left arrow
- `Icon::RIGHT` - Right arrow

### User Icons
- `Icon::USER` - Single user
- `Icon::USERS` - Multiple users
- `Icon::USER_MD` - Doctor/medical
- `Icon::KEY` - Key/lock
- `Icon::LOCK` - Lock
- `Icon::UNLOCK` - Unlock

### File Icons
- `Icon::FILE` - Generic file
- `Icon::FILE_TEXT` - Document file
- `Icon::FILE_IMAGE` - Image file
- `Icon::DOWNLOAD` - Download
- `Icon::UPLOAD` - Upload

### Social Icons
- `Icon::FACEBOOK` - Facebook
- `Icon::TWITTER` - Twitter
- `Icon::GOOGLE` - Google
- `Icon::GITHUB` - GitHub
- `Icon::LINKEDIN` - LinkedIn
- `Icon::YOUTUBE` - YouTube

## Admin Panel Usage

### Sidebar Navigation
```php
<ul class="nav nav-pills nav-sidebar">
    <li class="nav-item">
        <a href="/dashboard" class="nav-link">
            <?= Icon::custom('fa-th-large', 'nav-icon') ?>
            <p>Dashboard</p>
        </a>
    </li>
    <li class="nav-item">
        <a href="/users" class="nav-link">
            <?= Icon::custom('fa-users', 'nav-icon') ?>
            <p>Users</p>
        </a>
    </li>
</ul>
```

### Admin Links
```php
use Bone\View\Util\AdminLink;
use Del\Icon;

public function getAdminLinks(): array
{
    return [
        new AdminLink(
            'Users', 
            '/admin/users', 
            Icon::custom('fa-users', 'nav-icon')
        ),
        new AdminLink(
            'Settings', 
            '/admin/settings', 
            Icon::custom('fa-cog', 'nav-icon')
        ),
    ];
}
```

## Template Examples

### Button with Icon
```php
<button type="submit">
    <?= Icon::CHECK ?> Save
</button>

<a href="/users/add">
    <?= Icon::ADD ?> Add User
</a>
```

### Navigation Item
```php
<li class="nav-item">
    <a href="/settings" class="nav-link">
        <i class="<?= Icon::custom('fa-cog', 'nav-icon') ?>"></i>
        <p>Settings</p>
    </a>
</li>
```

### Card Header
```php
<div class="card">
    <div class="card-header">
        <h3 class="card-title">
            <i class="<?= Icon::custom('fa-users') ?>"></i> User Management
        </h3>
    </div>
</div>
```

## CDN Integration

### Font Awesome CSS Link
```php
echo Icon::fontAwesomeHeadCssLink('4.7.1');
// <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
```

## Best Practices

1. Use specific icons for their purpose
2. Keep consistent sizing
3. Add labels alongside icons
4. Test against backgrounds
5. Use semantic naming
6. Ensure browser compatibility
7. Consider accessibility
8. Keep it simple
9. Document icon usage
10. Stay consistent
