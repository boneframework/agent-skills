---
name: bone-session
description: "Handles secure session management in Bone Framework applications using delboy1978uk/session package with IP checking, session rotation, and hijack prevention."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "session", "security", "authentication"]
trigger_patterns:
  - "session"
  - "login"
  - "authentication"
  - "secure session"
  - "hijack"
---

# Bone Session Skill

## When to Use
Activate this skill when working with secure session management in a Bone Framework application using the `delboy1978uk/session` package.

## Package Information
- **Package**: `delboy1978uk/session`
- **License**: MIT
- **PHP Version**: ^8.1
- **Singleton pattern**: Uses `SessionManager::getInstance()`

## Core Features

### Security Features
1. **IP Address Checking**: Validates session against IP address to prevent hijacking
2. **Session Rotation**: Randomly regenerates session ID on 5% of requests
3. **User Agent Validation**: Checks that user agent hasn't changed between requests
4. **Secure Session Start**: Configures session cookies with secure defaults

### Session Configuration
Controlled via environment variables:
- `SESSION_ROTATION` - Enable/disable session ID rotation (default: true)
- `SESSION_IP_CHECK` - Enable/disable IP address checking (default: true)

## SessionManager Class

### Singleton Pattern
```php
use Del\SessionManager;

// Get the singleton instance
$session = SessionManager::getInstance();

// Or use the static method
SessionManager::sessionStart('app_name');
```

### Session Management Methods

| Method | Description |
|--------|-------------|
| `sessionStart($name, $lifetime, $path, $domain, $secure)` | Creates a secure session with the given name |
| `getInstance()` | Returns the singleton instance |
| `set($key, $value)` | Sets a session value |
| `get($key)` | Gets a session value (returns null if not exists) |
| `has($key)` | Checks if a session key exists |
| `unset($key)` | Removes a session key |
| `destroy()` | Alias for `unset()` (deprecated) |
| `destroySession()` | Destroys and restarts the session |

### Session Start Parameters
```php
SessionManager::sessionStart(
    string $name,      // Session name prefix (e.g., 'app')
    int $lifetime = 0, // Session lifetime in seconds (0 = until browser closes)
    string $path = '/', // Cookie path
    string $domain = '', // Cookie domain (defaults to $_SERVER['SERVER_NAME'])
    ?bool $secure = null // HTTPS only (defaults to isset($_SERVER['HTTPS']))
): void
```

## Session Hijack Prevention

### IP Address Masking
Sessions use a /24 network mask for IP validation:
```
Original: 192.168.1.123
Masked: 192.168.1.x
```
This allows sessions to persist when behind load balancers or proxies (like Cloudflare).

### Session Regeneration
- Regenerates session ID with 5% probability on each request
- Prevents session fixation attacks
- 10-second overlap period allows AJAX requests to complete

### Validation Checks
1. **Hijack Attempt Detection**: Compares stored IP and user agent with current
2. **Session Rotation**: Random ID regeneration
3. **Obsolescence Handling**: Manages transition between old and new session IDs

## Common Tasks

### 1. Starting a Secure Session
```php
use Del\SessionManager;

// Start session with custom name
SessionManager::sessionStart('myapp', 3600, '/', '.example.com', true);
```

### 2. Setting Session Data
```php
$session = SessionManager::getInstance();
$session->set('user_id', 123);
$session->set('role', 'admin');

// Array access style
$_SESSION['custom_data'] = 'value';
```

### 3. Reading Session Data
```php
$session = SessionManager::getInstance();

// Safe reading with null coalescing
userId = $session->get('user_id');
$role = $session->get('role');

// Check existence
if ($session->has('user_id')) {
    // User is authenticated
}
```

### 4. Removing Session Data
```php
$session = SessionManager::getInstance();

// Remove specific key
$session->unset('user_id');

// Or use standard PHP
unset($_SESSION['user_id']);
```

### 5. Destroying Session
```php
use Del\SessionManager;

// Destroy current session and start fresh
SessionManager::destroySession();

// Or manually
session_destroy();
session_start();
```

### 6. Working with Session Expiration
The session system uses an "obsolescence" pattern:
```php
// Session marked as obsolete during regeneration
$session['OBSOLETE'] = true;
$session['EXPIRES'] = time() + 10; // 10 seconds to complete operations

// New session can be started immediately after
session_regenerate_id();
```

## Integration with Bone Framework

### Automatic Session Registration
In `Application::initSession()`:
```php
private function initSession(): void
{
    $session = SessionManager::getInstance();
    
    if (isset($_SERVER['SERVER_NAME'])) {
        SessionManager::sessionStart('app');
    }
    
    $this->container[SessionManager::class] = $session;
}
```

### Accessing Session in Controllers
```php
use Bone\Application;
use Del\SessionManager;

$app = Application::ahoy();
$container = $app->getContainer();
$session = $container->get(SessionManager::class);

// Store data
$session->set('flash_message', 'Operation successful');

// Retrieve data
$message = $session->get('flash_message');
```

## Environment Configuration Examples

### Development Environment
```bash
SESSION_ROTATION=0  # Disable rotation for easier debugging
SESSION_IP_CHECK=0 # Disable IP check for local development
```

### Production Environment
```bash
SESSION_ROTATION=1  # Enable session rotation
SESSION_IP_CHECK=1  # Enable IP checking
```

### With Load Balancer (Cloudflare)
```bash
# IP is already masked in code, no additional config needed
SESSION_ROTATION=1
SESSION_IP_CHECK=1
```

## Best Practices

1. **Always use SessionManager**: Never call `session_start()` directly
2. **Set session name early**: Use unique names per application
3. **Enable rotation in production**: Prevents session fixation
4. **Use secure cookies**: Set `secure=true` for HTTPS sites
5. **Check session validity**: Use `has()` before accessing keys
6. **Destroy on logout**: Call `destroySession()` when user logs out
7. **Configure expiration**: Set appropriate session lifetime for your use case
8. **Test session regeneration**: Verify session works after ID changes
9. **Log session events**: Track hijack attempts and rotations
10. **Use environment variables**: Configure via `.env` not hard-coded values
