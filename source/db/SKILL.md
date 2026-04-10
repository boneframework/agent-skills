---
name: bone-db
description: "Handles database connections using PDO in Bone Framework applications using delboy1978uk/bone-db package with automatic PDO configuration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "database", "pdo", "mysql", "db"]
trigger_patterns:
  - "db"
  - "database"
  - "pdo"
  - "mysql"
  - "connection"
  - "database connection"
---

# Bone DB Skill

## When to Use
Activate this skill when working with database connections in Bone Framework applications using the `delboy1978uk/bone-db` package for PDO setup.

## Package Information
- **Package**: `delboy1978uk/bone-db`
- **Dependencies**: None (uses PHP's built-in PDO)
- **License**: MIT
- **PHP Version**: ^8.2
- **Purpose**: Automatic PDO configuration and container registration

## Core Components

### DbPackage
Main package that configures and registers PDO:
```php
class DbPackage implements RegistrationInterface
{
    public function addToContainer(ContainerInterface $c): void
    {
        $c[PDO::class] = $c->factory(function ($c) {
            $credentials = $c->get('db');
            // Create PDO connection
        });
    }
}
```

### DbProviderInterface
Interface for classes that need database access:
```php
interface DbProviderInterface
{
    public function getDbConnection(): PDO;
}
```

### HasDbTrait
Trait for classes that need database access:
```php
trait HasDbTrait
{
    private PDO $pdo;
    
    public function setPdo(PDO $pdo): void
    {
        $this->pdo = $pdo;
    }
    
    public function getPdo(): PDO
    {
        return $this->pdo;
    }
}
```

## Configuration

### Database Configuration
```php
// config/bone-db.php
return [
    'db' => [
        'driver' => 'pdo_mysql',
        'host' => $_ENV['DB_HOST'],
        'dbname' => $_ENV['DB_NAME'],
        'user' => $_ENV['DB_USERNAME'],
        'password' => $_ENV['DB_PASSWORD'],
    ],
];
```

### Environment Variables
```bash
# .env
DB_HOST=localhost
DB_NAME=app_db
DB_USERNAME=db_user
DB_PASSWORD=db_password
```

### MySQL PDO Options
The package automatically sets:
- `PDO::ATTR_EMULATE_PREPARES => false` - Use native prepared statements
- `PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION` - Throw exceptions

## Usage Examples

### 1. Getting PDO from Container
```php
use Bone\Application;
use PDO;

$app = Application::ahoy();
$container = $app->getContainer();
$pdo = $container->get(PDO::class);

// Use PDO
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
$stmt->execute(['id' => 123]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
```

### 2. In Controllers
```php
use Bone\Controller\Controller;
use PDO;

class UserController extends Controller
{
    use HasDbTrait;
    
    public function indexAction()
    {
        $pdo = $this->pdo;
        $stmt = $pdo->query('SELECT * FROM users');
        $users = $stmt->fetchAll();
        
        return $this->view->render('index', ['users' => $users]);
    }
}
```

### 3. In Services
```php
use Bone\Db\DbProviderInterface;
use PDO;

class UserRepository implements DbProviderInterface
{
    private PDO $pdo;
    
    public function __construct(PDO $pdo)
    {
        $this->pdo = $pdo;
    }
    
    public function getAll(): array
    {
        $stmt = $this->pdo->query('SELECT * FROM users');
        return $stmt->fetchAll();
    }
    
    public function getById(int $id): ?array
    {
        $stmt = $this->pdo->prepare('SELECT * FROM users WHERE id = :id');
        $stmt->execute(['id' => $id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}
```

### 4. Error Handling
```php
try {
    $pdo = $container->get(PDO::class);
    $stmt = $pdo->prepare('INSERT INTO users (name, email) VALUES (?, ?)');
    $stmt->execute([$name, $email]);
} catch (PDOException $e) {
    $logger->error('Database error', [
        'message' => $e->getMessage(),
        'code' => $e->getCode(),
    ]);
    throw new Exception('Failed to create user');
}
```

### 5. Transaction Handling
```php
try {
    $pdo = $container->get(PDO::class);
    $pdo->beginTransaction();
    
    $stmt = $pdo->prepare('INSERT INTO users (name) VALUES (?)');
    $stmt->execute([$name]);
    
    $stmt = $pdo->prepare('INSERT INTO profiles (user_id, bio) VALUES (?, ?)');
    $stmt->execute([$userId, $bio]);
    
    $pdo->commit();
} catch (Exception $e) {
    $pdo->rollBack();
    throw $e;
}
```

### 6. Prepared Statements
```php
$pdo = $container->get(PDO::class);

// Named parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
$stmt->execute(['id' => $id]);

// Positional parameters
$stmt = $pdo->prepare('SELECT * FROM users WHERE name = ?');
$stmt->execute([$name]);

// Fetch modes
$user = $stmt->fetch(PDO::FETCH_ASSOC);
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);
$count = $stmt->fetchColumn();
```

### 7. Last Insert ID
```php
$pdo = $container->get(PDO::class);

$stmt = $pdo->prepare('INSERT INTO users (name) VALUES (?)');
$stmt->execute([$name]);
$userId = $pdo->lastInsertId();
```

### 8. Row Count
```php
$pdo = $container->get(PDO::class);

$stmt = $pdo->prepare('DELETE FROM users WHERE id = :id');
$stmt->execute(['id' => $id]);
$deleted = $stmt->rowCount();
```

### 9. Multiple Statements
```php
$pdo = $container->get(PDO::class);

$pdo->beginTransaction();

try {
    $stmt = $pdo->prepare('INSERT INTO orders (user_id, total) VALUES (?, ?)');
    $stmt->execute([$userId, $total]);
    $orderId = $pdo->lastInsertId();
    
    $stmt = $pdo->prepare('INSERT INTO order_items (order_id, product_id) VALUES (?, ?)');
    foreach ($items as $item) {
        $stmt->execute([$orderId, $item['product_id']]);
    }
    
    $pdo->commit();
} catch (Exception $e) {
    $pdo->rollBack();
    throw $e;
}
```

### 10. Query Builder Alternative
For simple queries, use PDO directly:
```php
$pdo = $container->get(PDO::class);

// Select
$stmt = $pdo->query('SELECT * FROM users LIMIT 10');
$users = $stmt->fetchAll();

// Count
$count = $pdo->query('SELECT COUNT(*) FROM users')->fetchColumn();

// Check existence
$exists = $pdo->query('SELECT EXISTS(SELECT 1 FROM users WHERE email = ?)')
    ->fetchColumn();
```

## PDO Connection Settings

The package sets these PDO attributes:
- `ATTR_EMULATE_PREPARES` = false - Use native prepared statements (more secure)
- `ATTR_ERRMODE` = `ERRMODE_EXCEPTION` - Throw exceptions on errors

You can extend or modify these:
```php
// In config/bone-db.php
return [
    'db' => [
        'driver' => 'pdo_mysql',
        'host' => $_ENV['DB_HOST'],
        'dbname' => $_ENV['DB_NAME'],
        'user' => $_ENV['DB_USERNAME'],
        'password' => $_ENV['DB_PASSWORD'],
        'charset' => 'utf8mb4',
        'collation' => 'utf8mb4_unicode_ci',
        'options' => [
            PDO::ATTR_PERSISTENT => false,
        ],
    ],
];
```

## Error Handling

### PDOException
```php
try {
    $pdo = $container->get(PDO::class);
    $stmt = $pdo->query('INVALID SQL');
} catch (PDOException $e) {
    echo "SQL Error: " . $e->getMessage();
    echo "Error Code: " . $e->getCode();
}
```

### Error Log Integration
```php
use Psr\Log\LoggerInterface;

$logger = $container->get(LoggerInterface::class);

try {
    $pdo = $container->get(PDO::class);
    $stmt = $pdo->prepare('SELECT * FROM users WHERE id = :id');
    $stmt->execute(['id' => $id]);
} catch (PDOException $e) {
    $logger->error('Database query failed', [
        'error' => $e->getMessage(),
        'code' => $e->getCode(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
    ]);
}
```

## Best Practices

1. **Use PDO::ATTR_EMULATE_PREPARES = false**: Native prepared statements are more secure
2. **Enable error mode**: Use `PDO::ERRMODE_EXCEPTION` for exception handling
3. **Use transactions**: For multiple related queries
4. **Prefer prepared statements**: Always use for user input
5. **Close statements**: Call `closeCursor()` when done
6. **Handle errors gracefully**: Catch PDOException
7. **Use proper fetch modes**: `FETCH_ASSOC`, `FETCH_OBJ`, etc.
8. **Don't store PDO in static properties**: Get from container each time
9. **Use PDO constants**: Use `PDO::FETCH_*` constants
10. **Close database links**: Let PHP handle connection cleanup

## Configuration File Examples

### Full Database Configuration
```php
// config/bone-db.php
return [
    'db' => [
        'driver' => 'pdo_mysql',
        'host' => $_ENV['DB_HOST'] ?? 'localhost',
        'port' => $_ENV['DB_PORT'] ?? 3306,
        'dbname' => $_ENV['DB_NAME'],
        'user' => $_ENV['DB_USERNAME'],
        'password' => $_ENV['DB_PASSWORD'],
        'charset' => 'utf8mb4',
        'collation' => 'utf8mb4_unicode_ci',
        'options' => [
            PDO::ATTR_PERSISTENT => false,
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ],
    ],
];
```

### Environment-Specific Config
```php
// config/development/bone-db.php
return [
    'db' => [
        'host' => 'localhost',
        'dbname' => 'app_dev',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        ],
    ],
];

// config/production/bone-db.php
return [
    'db' => [
        'host' => 'prod-db.example.com',
        'dbname' => 'app_prod',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_PERSISTENT => false,
        ],
    ],
];
```
