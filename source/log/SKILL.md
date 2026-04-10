---
name: bone-log
description: "Handles logging in Bone Framework applications using delboy1978uk/bone-log package with Monolog integration and multiple log channels support."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "logging", "monolog", "logger", "log channels"]
trigger_patterns:
  - "log"
  - "logging"
  - "logger"
  - "monolog"
  - "log channels"
  - "error log"
---

# Bone Log Skill

## When to Use
Activate this skill when implementing application logging in a Bone Framework application using the `delboy1978uk/bone-log` package.

## Package Information
- **Package**: `delboy1978uk/bone-log`
- **Dependencies**: monolog/monolog
- **License**: MIT
- **PHP Version**: ^8.2

## Core Components

### LogPackage
Main package class that configures and registers the logger:
```php
class LogPackage implements RegistrationInterface
{
    public function addToContainer(Container $c): void
    {
        // Configure error reporting, log file paths
        // Create logger factory
        $c[LoggerInterface::class] = $c->factory(function ($c) {
            $config = $c->get('log');
            $loggerFactory = new LoggerFactory();
            return $loggerFactory->createLoggers($config);
        });
    }
}
```

### LoggerFactory
Creates Monolog logger instances from configuration:
```php
class LoggerFactory
{
    public function createLoggers(array $config): LoggerInterface
    {
        // Creates logger with handlers based on config
    }
}
```

### LoggerAwareInterface
Interface for classes that need logger access:
```php
interface LoggerAwareInterface
{
    public function setLogger(LoggerInterface $logger): void;
    public function getLogger(): LoggerInterface;
}
```

## Configuration

### Basic Configuration
```php
// config/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => 'data/logs/default_log',
            'access' => 'data/logs/access_log',
            'error' => 'data/logs/error_log',
        ],
    ],
    'error_log' => 'data/logs/error_log',
    'error_reporting' => E_ERROR,
    'display_errors' => true,
];
```

### Advanced Configuration
```php
// config/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => 'data/logs/default_log',
            'auth' => 'data/logs/auth.log',
            'payment' => 'data/logs/payment.log',
        ],
        'processors' => [
            'process_id',    // Add process ID
            'uid' => true,   // Add user ID
        ],
        'handlers' => [
            'stream' => [
                'level' => 'debug',
                'bubble' => true,
            ],
            'rotating' => [
                'level' => 'error',
                'max_files' => 7,
            ],
        ],
    ],
    'error_log' => 'data/logs/php_errors.log',
    'error_reporting' => E_ALL,
    'display_errors' => false,
];
```

## Logging Levels

Monolog supports these log levels (in order):
1. `DEBUG` - Detailed debug information
2. `INFO` - Interesting events
3. `NOTICE` - Normal but significant events
4. `WARNING` - Exceptional occurrences
5. `ERROR` - Runtime errors
6. `CRITICAL` - Critical conditions
7. `ALERT` - Action must be taken immediately
8. `EMERGENCY` - System is unusable

## Common Tasks

### 1. Getting Logger from Container
```php
use Psr\Log\LoggerInterface;

$logger = $container->get(LoggerInterface::class);
```

### 2. Logging Messages
```php
$logger = $container->get(LoggerInterface::class);

$logger->debug('Debug message');
$logger->info('Info message');
$logger->notice('Notice message');
$logger->warning('Warning message');
$logger->error('Error message');
$logger->critical('Critical message');
$logger->alert('Alert message');
$logger->emergency('Emergency message');
```

### 3. Logging with Context
```php
$logger->error('Failed to process order', [
    'order_id' => 123,
    'user_id' => 456,
    'error' => $e->getMessage(),
]);

$logger->info('User logged in', [
    'user_id' => $user->getId(),
    'ip' => $request->getRemoteAddress(),
]);
```

### 4. Logging with Channels
```php
// Use specific channel from config
$logger = $container->get(LoggerInterface::class);

// Default channel
$logger->info('User logged in');

// With context (not separate channels in bone-log)
// For multiple channels, configure in LoggerFactory
```

### 5. Error Logging
```php
// Automatic error logging
error_log('Error message');

// Or using logger
$logger->error('Error occurred', [
    'exception' => $e,
    'trace' => debug_backtrace(),
]);
```

### 6. Custom Logger Configuration
```php
// In config/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => 'data/logs/default.log',
        ],
        'processors' => [
            'process_id',
            'uid' => true,
        ],
        'handlers' => [
            'stream' => [
                'level' => 'debug',
                'bubble' => true,
            ],
        ],
    ],
];
```

### 7. Environment-Specific Logging
```php
// config/development/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => 'php://stdout',  // Log to stdout in dev
        ],
        'error_reporting' => E_ALL,
        'display_errors' => true,
    ],
];

// config/production/bone-log.php
return [
    'log' => [
        'channels' => [
            'default' => '/var/log/app/app.log',
        ],
        'error_reporting' => E_ERROR,
        'display_errors' => false,
    ],
];
```

### 8. Logging Exceptions
```php
try {
    // Some operation
} catch (\Exception $e) {
    $logger->error('Operation failed', [
        'exception' => get_class($e),
        'message' => $e->getMessage(),
        'code' => $e->getCode(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString(),
    ]);
    
    // Re-throw or handle
    throw $e;
}
```

### 9. Request/Response Logging
```php
// In middleware
public function process($request, $handler)
{
    $logger->info('Request started', [
        'method' => $request->getMethod(),
        'uri' => (string) $request->getUri(),
        'ip' => $request->getRemoteAddress(),
    ]);
    
    $response = $handler->handle($request);
    
    $logger->info('Response sent', [
        'status' => $response->getStatusCode(),
        'time' => microtime(true) - $startTime,
    ]);
    
    return $response;
}
```

### 10. Structured Logging
```php
$logger->info('User action', [
    'action' => 'password_changed',
    'user_id' => 123,
    'timestamp' => time(),
    'ip' => $request->getRemoteAddress(),
    'user_agent' => $request->getHeaderLine('User-Agent'),
]);
```

## LoggerFactory Features

### Stream Handler
Writes logs to files:
```php
new StreamHandler($path, $level, $bubble);
```

### Rotating File Handler
Auto-rotates log files:
```php
new RotatingFileHandler($path, $maxFiles, $level, $bubble);
```

### Processors
Add extra context to log entries:
- `ProcessIdProcessor` - Adds process ID
- `UidProcessor` - Adds unique ID
- `MemoryPeakUsageProcessor` - Memory usage
- `MemoryUsageProcessor` - Current memory

## Integration with Bone Framework

### In Controllers
```php
class MyController
{
    use HasLoggerTrait;
    
    public function indexAction()
    {
        $this->logger->info('Page accessed');
        $this->logger->debug('Variables', ['vars' => get_defined_vars()]);
    }
}
```

### In Middleware
```php
class LoggingMiddleware implements MiddlewareInterface
{
    public function process($request, $handler)
    {
        $container = $this->container;
        $logger = $container->get(LoggerInterface::class);
        
        $logger->info('Processing request');
        
        return $handler->handle($request);
    }
}
```

### In Services
```php
class MyService implements LoggerAwareInterface
{
    private LoggerInterface $logger;
    
    public function setLogger(LoggerInterface $logger): void
    {
        $this->logger = $logger;
    }
    
    public function doWork()
    {
        $this->logger->info('Service started');
        // ... work ...
        $this->logger->info('Service completed');
    }
}
```

## Best Practices

1. **Use appropriate log levels**: Choose the right level for each message
2. **Include context**: Always add relevant context data
3. **Log at appropriate level**: Debug for dev, Error for prod
4. **Use structured arrays**: Log context as associative arrays
5. **Don't log sensitive data**: Avoid passwords, credit cards
6. **Rotate logs**: Use RotatingFileHandler for production
7. **Set proper permissions**: Ensure log directory is writable
8. **Separate channels**: Use different channels for different log types
9. **Test logging**: Verify logs are being written
10. **Monitor logs**: Set up alerts for critical errors

## Configuration Examples

### Development Environment
```php
return [
    'log' => [
        'channels' => [
            'default' => 'php://stdout',  // Output to terminal
        ],
        'error_reporting' => E_ALL,
        'display_errors' => true,
    ],
];
```

### Production Environment
```php
return [
    'log' => [
        'channels' => [
            'default' => '/var/www/app/data/logs/app.log',
            'error' => '/var/www/app/data/logs/error.log',
        ],
        'processors' => ['process_id', 'uid'],
        'handlers' => [
            'rotating' => [
                'max_files' => 30,
            ],
        ],
    ],
    'error_reporting' => E_ERROR,
    'display_errors' => false,
];
```
