---
name: bone-user
description: "Handles user management in Bone Framework applications using delboy1978uk/bone-user package including authentication, authorization, registration, and profile management."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "user", "authentication", "authorization", "registration", "login", "profile"]
trigger_patterns:
  - "bone-user"
  - "user management"
  - "authentication"
  - "login"
  - "registration"
  - "user profile"
---

# Bone User Skill

## When to Use
Activate this skill when working with user management in Bone Framework applications using the delboy1978uk/bone-user package. This includes user registration, login, logout, authentication middleware, and profile management.

## Package Information
- **Package**: `delboy1978uk/bone-user`
- **License**: MIT
- **PHP Version**: ^8.2
- **Dependencies**: bone-doctrine, bone-passport, bone-oauth2, bone-mail, bone-paseto

## Installation

```bash
composer require delboy1978uk/bone-user
```

## Package Features

### Key Features
- User registration with email activation
- Login/logout functionality
- Session-based authorization middleware
- Remember Me cookie support
- Profile management
- Admin pages (`/admin/users`, `/admin/people`)
- REST API routes (when using bone-oauth2)
- Integration with Bone Framework packages

### Routes (when package registered)
- `/user/register` - User registration form
- `/user/login` - User login form
- `/user/logout` - User logout
- `/user/activate/{token}` - Email activation
- `/user/profile` - User profile page
- `/user/profile/edit` - Edit profile
- `/admin/users` - Admin user management
- `/admin/people` - Admin people management
- `/api/users` - REST API endpoints (when bone-oauth2 enabled)

## Package Registration

```php
// config/packages.php
return [
    'packages' => [
        \Bone\User\BoneUserPackage::class,
        // ... other packages
    ]
];
```

## Key Classes and Services

### BoneUserPackage
Main package class that registers routes and services.

```php
use Bone\User\BoneUserPackage;

$package = new BoneUserPackage();
$package->addToContainer($container);
$package->addToSiteConfig($siteConfig);
```

### UserService
Core service for user operations.

```php
// Get user service from container
$userService = $container->get(\Bone\User\Service\UserService::class);

// Create user
$user = $userService->createUser([
    'email' => 'user@example.com',
    'password' => 'password123',
    'firstName' => 'John',
    'lastName' => 'Doe',
]);

// Get user by ID
$user = $userService->findById($userId);

// Get user by email
$user = $userService->findByEmail($email);

// Login user
$user = $userService->login($email, $password);

// Logout user
$userService->logout();
```

### PersonService
Manages Person entity linked to users.

```php
$personService = $container->get(\Bone\User\Service\PersonService::class);

// Get person for user
$person = $personService->getPerson($userId);

// Create person
$person = $personService->createPerson([
    'firstName' => 'John',
    'lastName' => 'Doe',
    'email' => 'john@example.com',
]);

// Update person
$personService->updatePerson($personId, [
    'firstName' => 'John',
    'lastName' => 'Doe',
]);
```

## Entities

### User Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'users')]
class User
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 100)]
    private string $email;

    #[ORM\Column(type: 'string', length: 255)]
    private string $password;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $activationToken;

    #[ORM\Column(type: 'boolean')]
    private bool $isActive = false;

    #[ORM\OneToOne(targetEntity: Person::class)]
    private ?Person $person = null;

    #[ORM\Column(type: 'string', length: 100, nullable: true)]
    private ?string $rememberMeToken = null;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;

    #[ORM\Column(type: 'datetime', nullable: true)]
    private ?\DateTimeInterface $updatedAt = null;

    #[ORM\Column(type: 'datetime', nullable: true)]
    private ?\DateTimeInterface $lastLogin = null;

    // Getters and setters...
}
```

### Person Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'people')]
class Person
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $firstName;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $lastName;

    #[ORM\Column(type: 'string', length: 100, nullable: true)]
    private ?string $email;

    #[ORM\OneToOne(targetEntity: User::class, inversedBy: 'person')]
    private ?User $user = null;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $avatar;

    // Getters and setters...
}
```

## Authentication Middleware

### SessionAuth
Restricts access to logged-in users.

```php
use Bone\User\Http\Middleware\SessionAuth;

// In routes
$router->group('/dashboard', function ($router) {
    $router->get('', [DashboardController::class, 'index']);
})->middleware(SessionAuth::class);
```

### SessionAuthRedirect
Auth middleware that redirects to login, then back to original page.

```php
use Bone\User\Http\Middleware\SessionAuthRedirect;

$router->group('/profile', function ($router) {
    $router->get('', [ProfileController::class, 'index']);
})->middleware(SessionAuthRedirect::class);
```

## Configuration

```php
// config/bone-user.php
return [
    'loginRedirect' => '/dashboard',
    'logoutRedirect' => '/',
    'registrationEnabled' => true,
    'profileRequired' => false,
    'rememberMeEnabled' => true,
    'activationRequired' => true,
    'fromEmail' => 'noreply@example.com',
    'fromName' => 'My Application',
];
```

## Registration Flow

### 1. Registration Form
```php
use Bone\User\Form\RegistrationForm;

class RegistrationController
{
    public function registerAction($request)
    {
        $form = new RegistrationForm();
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $data = $form->getValues();
                
                // Create user via service
                $userService = $this->container->get(\Bone\User\Service\UserService::class);
                $user = $userService->createUser([
                    'email' => $data['email'],
                    'password' => $data['password'],
                    'firstName' => $data['firstName'],
                    'lastName' => $data['lastName'],
                ]);
                
                // Send activation email
                $mailer = $this->container->get(\Bone\Mail\Service\MailService::class);
                $mailer->sendActivationEmail($user);
                
                return $this->redirect('/user/login?registered=1');
            }
        }
        
        return $this->view->render('user/register', ['form' => $form]);
    }
}
```

### 2. Email Activation
```php
class UserController
{
    public function activateAction($request)
    {
        $token = $request->getAttribute('token');
        
        $userService = $this->container->get(\Bone\User\Service\UserService::class);
        $user = $userService->activateUser($token);
        
        if ($user) {
            return $this->redirect('/user/login?activated=1');
        }
        
        return $this->redirect('/user/register?error=invalid_token');
    }
}
```

### 3. Login
```php
class AuthController
{
    public function loginAction($request)
    {
        $form = new \Del\Form\Form();
        $form->add([
            'name' => 'email',
            'type' => 'Email',
            'options' => ['label' => 'Email'],
        ])->add([
            'name' => 'password',
            'type' => 'Password',
            'options' => ['label' => 'Password'],
        ])->add([
            'name' => 'remember',
            'type' => 'Checkbox',
            'options' => ['label' => 'Remember Me'],
        ]);
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $data = $form->getValues();
                $userService = $this->container->get(\Bone\User\Service\UserService::class);
                $user = $userService->login($data['email'], $data['password']);
                
                if ($user) {
                    // Handle remember me
                    if ($data['remember']) {
                        $userService->createRememberMe($user);
                    }
                    
                    return $this->redirect('/dashboard');
                }
                
                $this->flash('error', 'Invalid email or password');
            }
        }
        
        return $this->view->render('user/login', ['form' => $form]);
    }
    
    public function logoutAction()
    {
        $userService = $this->container->get(\Bone\User\Service\UserService::class);
        $userService->logout();
        
        return $this->redirect('/');
    }
}
```

## Profile Management

### View Profile
```php
class ProfileController
{
    public function indexAction($request)
    {
        $userService = $this->container->get(\Bone\User\Service\UserService::class);
        $user = $userService->getCurrentUser();
        
        return $this->view->render('user/profile', [
            'user' => $user,
            'person' => $user->getPerson(),
        ]);
    }
}
```

### Edit Profile
```php
class ProfileController
{
    public function editAction($request)
    {
        $userService = $this->container->get(\Bone\User\Service\UserService::class);
        $user = $userService->getCurrentUser();
        
        $form = new \Del\Form\Form();
        $form->add([
            'name' => 'firstName',
            'type' => 'Text',
            'options' => ['label' => 'First Name'],
        ])->add([
            'name' => 'lastName',
            'type' => 'Text',
            'options' => ['label' => 'Last Name'],
        ]);
        
        if ($_POST) {
            $form->populate($_POST);
            
            if ($form->isValid()) {
                $person = $user->getPerson();
                $person->setFirstName($form->getValue('firstName'));
                $person->setLastName($form->getValue('lastName'));
                
                $em->flush();
                
                return $this->redirect('/profile');
            }
        }
        
        return $this->view->render('user/profile-edit', ['form' => $form]);
    }
}
```

## Admin Features

### Admin Routes (requires bone-passport)
- `/admin/users` - List all users
- `/admin/users/create` - Create user
- `/admin/users/edit/{id}` - Edit user
- `/admin/users/delete/{id}` - Delete user
- `/admin/people` - List all people

### Admin Controller Example
```php
use Bone\User\Controller\AdminUserController;

// Admin user management
$router->get('/admin/users', [AdminUserController::class, 'indexAction']);
$router->get('/admin/users/create', [AdminUserController::class, 'createAction']);
$router->post('/admin/users', [AdminUserController::class, 'storeAction']);
$router->get('/admin/users/edit/{id}', [AdminUserController::class, 'editAction']);
$router->post('/admin/users/update/{id}', [AdminUserController::class, 'updateAction']);
$router->get('/admin/users/delete/{id}', [AdminUserController::class, 'deleteAction']);
```

## API Endpoints (requires bone-oauth2)

### User API Routes
- `/api/users` - GET: List users, POST: Create user
- `/api/users/{id}` - GET: Get user, PUT: Update user, DELETE: Delete user
- `/api/users/me` - GET: Get current user

## Command Line Interface

### User Commands (with bone-console)
```bash
# Create admin user
bone user:admin-create

# Activate user
bone user:activate <userId>

# Deactivate user
bone user:deactivate <userId>

# Change user password
bone user:password <userId> <newPassword>
```

## User Management Functions

### UserService Methods
```php
// User service from container
$userService = $container->get(\Bone\User\Service\UserService::class);

// Create user
$user = $userService->createUser([
    'email' => 'user@example.com',
    'password' => 'password123',
    'firstName' => 'John',
    'lastName' => 'Doe',
]);

// Find user
$user = $userService->findById(1);
$user = $userService->findByEmail('user@example.com');
$users = $userService->findAll();

// Login/logout
$user = $userService->login($email, $password);
$userService->logout();

// Activate user
$user = $userService->activateUser($token);

// Update user
$userService->updateUser($user, $data);

// Delete user
$userService->deleteUser($user);

// Remember me
$userService->createRememberMe($user);
$userService->verifyRememberMe($token);

// Current user
$user = $userService->getCurrentUser();
```

### PersonService Methods
```php
$personService = $container->get(\Bone\User\Service\PersonService::class);

// Get person
$person = $personService->getPerson($userId);
$person = $personService->findByEmail($email);

// Create person
$person = $personService->createPerson([
    'firstName' => 'John',
    'lastName' => 'Doe',
    'email' => 'john@example.com',
]);

// Update person
$personService->updatePerson($person, $data);

// Delete person
$personService->deletePerson($person);
```

## Best Practices

1. **Always check authentication**: Use middleware for protected routes
2. **Validate input**: Validate all user input before creating/updating
3. **Hash passwords**: Never store plain text passwords
4. **Email verification**: Enable email activation for security
5. **Session management**: Clear sessions on logout
6. **Remember Me security**: Use secure tokens, implement token rotation
7. **Audit logging**: Log user login/logout events
8. **Rate limiting**: Implement rate limiting on login/registration
9. **Password policies**: Enforce strong password requirements
10. **Data consistency**: Keep User and Person entities in sync

##常见 Use Cases

### Restrict Access to Dashboard
```php
// In routes
$router->group('/dashboard', function ($router) {
    $router->get('', [DashboardController::class, 'index']);
})->middleware(SessionAuth::class);
```

### Show User-Specific Content
```php
// In controller
public function dashboardAction()
{
    $userService = $this->container->get(\Bone\User\Service\UserService::class);
    $user = $userService->getCurrentUser();
    
    // User is authenticated
    $data = [
        'user' => $user,
        'person' => $user->getPerson(),
    ];
    
    return $this->view->render('dashboard', $data);
}
```

### User Profile Page
```php
// In template
<h1><?= $person->getFirstName() ?> <?= $person->getLastName() ?></h1>
<p><?= $user->getEmail() ?></p>
<?php if ($user->getLastLogin()): ?>
    <p>Last login: <?= $user->getLastLogin()->format('Y-m-d H:i:s') ?></p>
<?php endif; ?>
```
