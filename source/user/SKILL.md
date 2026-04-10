---
name: user
description: "Handles user management in Bone Framework applications including authentication, registration, and session management."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "user", "authentication", "session", "login", "registration"]
trigger_patterns:
  - "user"
  - "authentication"
  - "login"
  - "registration"
  - "session"
---

# User Skill

## When to Use
Activate this skill when working with user management in Bone Framework applications including authentication, registration, and session management.

## Overview

User management includes:
- User registration and login
- Session-based authentication
- Password hashing and validation
- User profile management
- Role and permission management

## User Entity Structure

### Basic User Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'users')]
class User
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\Column(type: 'string', length: 100, unique: true)]
    private string $email;

    #[ORM\Column(type: 'string', length: 255)]
    private string $password;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $firstName;

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $lastName;

    #[ORM\Column(type: 'boolean')]
    private bool $isActive = true;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;

    #[ORM\OneToOne(targetEntity: Person::class)]
    private ?Person $person;

    // Getters and setters...
}
```

## Authentication Flow

### Registration
```php
public function registerAction($request)
{
    $email = $request->getPost('email');
    $password = $request->getPost('password');
    
    // Validate email
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $this->flash('error', 'Invalid email address');
        return $this->redirect('/register');
    }
    
    // Check if user exists
    $existing = $em->getRepository(User::class)->findOneBy([
        'email' => $email
    ]);
    
    if ($existing) {
        $this->flash('error', 'Email already registered');
        return $this->redirect('/register');
    }
    
    // Create user
    $user = new User();
    $user->setEmail($email);
    $user->setPassword(password_hash($password, PASSWORD_DEFAULT));
    $user->setFirstName($request->getPost('firstName'));
    $user->setLastName($request->getPost('lastName'));
    $user->setCreatedAt(new DateTime());
    
    $em->persist($user);
    $em->flush();
    
    // Login user
    $session->set('user_id', $user->getId());
    
    $this->flash('success', 'Registration successful!');
    return $this->redirect('/dashboard');
}
```

### Login
```php
public function loginAction($request)
{
    $email = $request->getPost('email');
    $password = $request->getPost('password');
    
    $user = $em->getRepository(User::class)->findOneBy([
        'email' => $email
    ]);
    
    if (!$user || !password_verify($password, $user->getPassword())) {
        $this->flash('error', 'Invalid email or password');
        return $this->redirect('/login');
    }
    
    if (!$user->getIsActive()) {
        $this->flash('error', 'Account is not active');
        return $this->redirect('/login');
    }
    
    // Store user ID in session
    $session->set('user_id', $user->getId());
    
    $this->flash('success', 'Welcome back!');
    return $this->redirect('/dashboard');
}
```

### Logout
```php
public function logoutAction()
{
    // Clear session
    $session->destroy();
    
    $this->flash('success', 'You have been logged out');
    return $this->redirect('/login');
}
```

## Session Management

### Session Handling
```php
use Bone\SessionManager;

// Start session
$session = SessionManager::getInstance();

// Set session data
$session->set('user_id', $userId);
$session->set('user_email', $email);
$session->set('roles', ['admin', 'user']);

// Get session data
$userId = $session->get('user_id');
$userEmail = $session->get('user_email');

// Check if logged in
if ($session->has('user_id')) {
    $user = $em->find(User::class, $session->get('user_id'));
}

// Clear session data
$session->clear('user_id');
$session->destroy();  // Destroy entire session
```

### Authenticated Routes
```php
// Middleware to protect routes
class AuthMiddleware
{
    public function __invoke($request, $handler)
    {
        $session = SessionManager::getInstance();
        
        if (!$session->has('user_id')) {
            $session->set('redirect_after_login', $request->getUri()->getPath());
            return $this->redirect('/login');
        }
        
        return $handler($request);
    }
}
```

## Password Management

### Hashing Passwords
```php
// Hash password
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);

// Verify password
if (password_verify($password, $hashedPassword)) {
    // Password is correct
}

// Rehash if needed (algorithm changed)
if (password_needs_rehash($hashedPassword, PASSWORD_DEFAULT)) {
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
}
```

### Change Password
```php
public function changePasswordAction($request)
{
    $currentPassword = $request->getPost('current_password');
    $newPassword = $request->getPost('new_password');
    
    $user = $this->currentUser;
    
    if (!password_verify($currentPassword, $user->getPassword())) {
        $this->flash('error', 'Current password is incorrect');
        return $this->redirect('/profile/password');
    }
    
    if (strlen($newPassword) < 8) {
        $this->flash('error', 'Password must be at least 8 characters');
        return $this->redirect('/profile/password');
    }
    
    $user->setPassword(password_hash($newPassword, PASSWORD_DEFAULT));
    $em->flush();
    
    $this->flash('success', 'Password changed successfully');
    return $this->redirect('/profile');
}
```

## User Profile

### Profile View
```php
public function profileAction()
{
    $user = $this->currentUser;
    
    return $this->view->render('user/profile', [
        'user' => $user,
    ]);
}
```

### Profile Edit
```php
public function editProfileAction($request)
{
    $user = $this->currentUser;
    $form = new ProfileForm();
    
    if ($_POST) {
        $form->populate($_POST);
        
        if ($form->isValid()) {
            $data = $form->getValues();
            
            $user->setFirstName($data['firstName']);
            $user->setLastName($data['lastName']);
            $user->setEmail($data['email']);
            
            if (!empty($data['password'])) {
                $user->setPassword(password_hash($data['password'], PASSWORD_DEFAULT));
            }
            
            $em->flush();
            
            return $this->redirect('/profile');
        }
    }
    
    return $this->view->render('user/edit-profile', [
        'user' => $user,
        'form' => $form,
    ]);
}
```

## User Repository

### Custom Repository
```php
class UserRepository extends ServiceEntityRepository
{
    public function findOneByEmail(string $email): ?User
    {
        return $this->createQueryBuilder('u')
            ->where('u.email = :email')
            ->setParameter('email', $email)
            ->getQuery()
            ->getOneOrNullResult();
    }
    
    public function findActiveUsers(): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.isActive = true')
            ->orderBy('u.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }
    
    public function searchUsers(string $search): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.firstName LIKE :search OR u.lastName LIKE :search OR u.email LIKE :search')
            ->setParameter('search', '%' . $search . '%')
            ->orderBy('u.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }
}
```

## Best Practices

1. **Hash passwords**: Use `password_hash()` and `password_verify()`
2. **Validate input**: Always validate email, password strength
3. **Secure sessions**: Regenerate session ID on login
4. **Track activity**: Store last login, IP address
5. **Rate limiting**: Limit login attempts
6. **Account lockout**: Temporarily lock after failed attempts
7. **Password requirements**: Enforce minimum length
8. **Email verification**: Verify email on registration
9. **Audit logging**: Log authentication events
10. **Session timeout**: Set appropriate session lifetime

## Common Use Cases

### Protected Dashboard
```php
public function dashboardAction()
{
    $session = SessionManager::getInstance();
    
    if (!$session->has('user_id')) {
        return $this->redirect('/login');
    }
    
    $user = $em->find(User::class, $session->get('user_id'));
    
    return $this->view->render('dashboard', [
        'user' => $user,
    ]);
}
```

### User Dashboard
```php
public function userDashboardAction($request)
{
    $userId = $this->currentUser->getId();
    
    // Get user-specific data
    $userOrders = $em->getRepository(Order::class)
        ->findBy(['user' => $userId]);
    
    return $this->view->render('user/dashboard', [
        'orders' => $userOrders,
    ]);
}
```

### Admin User List
```php
public function adminUsersAction()
{
    $users = $em->getRepository(User::class)
        ->findAll();
    
    return $this->view->render('admin/users', [
        'users' => $users,
    ]);
}
```
