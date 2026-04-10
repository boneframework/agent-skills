---
name: bone-passport
description: "Handles role-based access control (ACL) and permissions in Bone Framework applications using delboy1978uk/bone-passport package for securing routes based on user roles and entity-specific permissions."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "acl", "roles", "permissions", "passport", "authorization"]
trigger_patterns:
  - "bone-passport"
  - "acl"
  - "roles"
  - "permissions"
  - "authorization"
  - "passport"
---

# Bone Passport Skill

## When to Use
Activate this skill when implementing role-based access control (ACL) and permissions in Bone Framework applications using the delboy1978uk/bone-passport package for securing routes based on user roles and entity-specific permissions.

## Package Information
- **Package**: `delboy1978uk/bone-passport`
- **License**: MIT
- **PHP Version**: ^8.4
- **Dependencies**: bone-doctrine, barnacle, passport

## Installation

```bash
composer require delboy1978uk/bone-passport
```

## Package Features

### Key Features
- Role management (create/remove roles via CLI)
- Role assignment to users (grant/revoke via CLI)
- Middleware for securing routes based on required roles
- Entity-specific role control (granular access with entity ID)
- Admin panel integration (`/admin/roles`)

### Routes (when package registered)
- `/admin/roles` - Role management
- `/admin/permissions` - Permission management

## Package Registration

```php
// config/packages.php
return [
    'packages' => [
        \Bone\Passport\PassportPackage::class,
        // ... other packages
    ]
];
```

## Key Classes

### PassportPackage
Main package class that registers routes and services.

```php
use Bone\Passport\PassportPackage;

$package = new PassportPackage();
$package->addToContainer($container);
$package->addToSiteConfig($siteConfig);
```

### PassportControl
Service for role and permission management.

```php
// Get from container
$passport = $container->get(\Bone\Passport\PassportControl::class);

// Create role
$passport->createRole('admin', 'Admin role with full access');

// Check if user has role
$hasRole = $passport->hasRole($userId, 'admin');

// Grant role to user
$passport->grantRole($userId, 'admin');

// Revoke role from user
$passport->revokeRole($userId, 'admin');

// Check entity-specific permission
$hasPermission = $passport->can($userId, 'edit', $entityId);
```

### PassportControlMiddleware
Middleware for securing routes based on roles.

```php
use Bone\Passport\Middleware\PassportControlMiddleware;

// In routes
$router->group('/admin', function ($router) {
    $router->get('', [AdminController::class, 'index']);
})->middleware(new PassportControlMiddleware('admin'));
```

## Entities

### Role Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'roles')]
class Role
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 50, unique: true)]
    private string $name;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $description;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;
}
```

### Permission Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'permissions')]
class Permission
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 50)]
    private string $name;

    #[ORM\ManyToOne(targetEntity: Role::class)]
    private Role $role;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $entityId;

    #[ORM\Column(type: 'string', length: 50)]
    private string $action;
}
```

### UserRole Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'user_roles')]
class UserRole
{
    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: User::class)]
    private User $user;

    #[ORM\Id]
    #[ORM\ManyToOne(targetEntity: Role::class)]
    private Role $role;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $assignedAt;
}
```

## CLI Commands

### Role Management
```bash
# Create a role
bone passport:role add admin

# Remove a role
bone passport:role remove moderator

# List roles
bone passport:role list
```

### User Permission Management
```bash
# Grant role to user
bone passport:admin grant admin 123

# Revoke role from user
bone passport:admin revoke admin 123

# Grant entity-specific permission
bone passport:admin grant edit article 456
```

## Usage Examples

### Creating Roles

```php
use Bone\Passport\PassportControl;

// In a controller or service
public function createRoles()
{
    $passport = $this->container->get(PassportControl::class);
    
    // Create basic roles
    $passport->createRole('admin', 'Full administrative access');
    $passport->createRole('moderator', 'Content moderation access');
    $passport->createRole('editor', 'Content editing access');
    $passport->createRole('user', 'Basic user access');
}
```

### Checking User Permissions

```php
public function editAction($request)
{
    $passport = $this->container->get(PassportControl::class);
    $userId = $this->currentUser->getId();
    $entityId = $request->getAttribute('id');
    
    // Check if user has permission to edit this entity
    if (!$passport->can($userId, 'edit', $entityId)) {
        // Check if user has admin role (can edit any entity)
        if (!$passport->hasRole($userId, 'admin')) {
            return $this->jsonResponse(['error' => 'Permission denied'], 403);
        }
    }
    
    // User has permission
    // ... proceed with edit
}
```

### Securing Routes with Middleware

```php
// In routes
use Bone\Passport\Middleware\PassportControlMiddleware;

// Require specific role for entire group
$router->group('/admin', function ($router) {
    $router->get('', [AdminController::class, 'index']);
    $router->get('/users', [AdminController::class, 'users']);
})->middleware(new PassportControlMiddleware('admin'));

// Require role for specific route
$router->get('/dashboard', [DashboardController::class, 'index'])
    ->middleware(new PassportControlMiddleware('user'));

// Require specific permission
$router->post('/articles/{id}', [ArticleController::class, 'update'])
    ->middleware(new PassportControlMiddleware('edit', 'article'));
```

### Admin Panel Implementation

```php
// Admin roles controller
class AdminRoleController extends Controller
{
    public function indexAction()
    {
        $passport = $this->container->get(PassportControl::class);
        $roles = $passport->getAllRoles();
        
        return $this->view->render('admin/roles', [
            'roles' => $roles,
        ]);
    }
    
    public function createAction($request)
    {
        $name = $request->getPost('name');
        $description = $request->getPost('description');
        
        $passport = $this->container->get(PassportControl::class);
        $passport->createRole($name, $description);
        
        return $this->redirect('/admin/roles');
    }
    
    public function deleteAction($request)
    {
        $id = $request->getAttribute('id');
        $passport = $this->container->get(PassportControl::class);
        $passport->removeRole($id);
        
        return $this->redirect('/admin/roles');
    }
}
```

### Granting/Revoke Permissions

```php
// Grant role to user
public function grantRoleAction($request)
{
    $userId = $request->getAttribute('userId');
    $roleName = $request->getAttribute('role');
    
    $passport = $this->container->get(PassportControl::class);
    $passport->grantRole($userId, $roleName);
    
    return $this->jsonResponse(['success' => true]);
}

// Revoke role from user
public function revokeRoleAction($request)
{
    $userId = $request->getAttribute('userId');
    $roleName = $request->getAttribute('role');
    
    $passport = $this->container->get(PassportControl::class);
    $passport->revokeRole($userId, $roleName);
    
    return $this->jsonResponse(['success' => true]);
}

// Grant entity-specific permission
public function grantPermissionAction($request)
{
    $userId = $request->getAttribute('userId');
    $permission = $request->getPost('permission');  // e.g., 'edit:123'
    
    [$action, $entityId] = explode(':', $permission);
    
    $passport = $this->container->get(PassportControl::class);
    $passport->grantPermission($userId, $action, $entityId);
    
    return $this->jsonResponse(['success' => true]);
}
```

## Entity-Specific Permissions

Entity-specific permissions allow fine-grained access control:

```php
// Example: User can edit only their own articles
$passport->can($userId, 'edit', $articleId);
// Returns true only if user has edit permission for this specific article

// Admin can edit any article
if ($passport->hasRole($userId, 'admin')) {
    $passport->can($userId, 'edit', $articleId);  // Always true
}
```

## Best Practices

1. **Use roles for broad access**: Define roles like 'admin', 'moderator', 'user'
2. **Use entity permissions for granularity**: Allow specific actions on specific entities
3. **Check both role and entity permission**: Use both for layered security
4. **Fail fast**: Deny access by default, only allow explicitly
5. **Cache permission checks**: Use caching for repeated checks
6. **Audit permission changes**: Log role/permission changes
7. **Test thoroughly**: Ensure all access paths are tested
8. **Document permissions**: Keep documentation of what each role can do
9. **Use middleware for routes**: Don't check permissions in every action
10. **Separate authorization from authentication**: Authorization is about what you can do

## Common Use Cases

### Admin Panel Access
```php
// Only admins can access admin panel
$router->group('/admin', function ($router) {
    $router->get('', [AdminController::class, 'index']);
})->middleware(new PassportControlMiddleware('admin'));
```

### Content Editor Access
```php
// Editors can edit only their own content
$router->get('/edit/{id}', [EditorController::class, 'edit'])
    ->middleware(new PassportControlMiddleware('edit'));
```

### User Profile Access
```php
// Users can access their own profile
// Admins can access any profile
if ($passport->can($userId, 'view', $targetUserId) || 
    $passport->hasRole($userId, 'admin')) {
    // Allow access
}
```

### API Endpoints
```php
// API middleware for role-based access
$router->group('/api', function ($router) {
    $router->get('/users', [ApiUserController::class, 'index'])
        ->middleware(new PassportControlMiddleware('admin'));
    
    $router->get('/posts', [ApiPostController::class, 'index'])
        ->middleware(new PassportControlMiddleware('user'));
})->middleware(new PassportControlMiddleware('user'));
```

## Database Schema

### Tables Created by bone-passport

```sql
-- Roles table
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME NOT NULL
);

-- User roles table (many-to-many)
CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Permissions table
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    role_id INT NOT NULL,
    entity_id VARCHAR(255) DEFAULT NULL,
    action VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
```
