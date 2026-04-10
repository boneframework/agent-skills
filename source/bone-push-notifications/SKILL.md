---
name: bone-push-notifications
description: "Handles push notification services in Bone Framework applications using delboy1978uk/bone-push-notifications package for Expo-based push notification support."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "push", "notifications", "expo", "mobile", "bone-native"]
trigger_patterns:
  - "bone-push-notifications"
  - "push notifications"
  - "expo"
  - "mobile notifications"
  - "bone-native"
---

# Bone Push Notifications Skill

## When to Use
Activate this skill when implementing push notification services in Bone Framework applications using the delboy1978uk/bone-push-notifications package for Expo-based push notification support.

## Package Information
- **Package**: `delboy1978uk/bone-push-notifications`
- **License**: MIT
- **PHP Version**: ^8.1
- **Dependencies**: bone-oauth2, ext-json

## Installation

```bash
composer require delboy1978uk/bone-push-notifications
```

## Package Features

### Key Features
- Push notification service integration with Expo
- Token management for devices
- User-specific token storage
- Notification queuing and delivery

## Package Registration

```php
// config/packages.php
return [
    'packages' => [
        \Bone\PushNotifications\PushNotificationPackage::class,
        // ... other packages
    ]
];
```

## Entities

### PushToken Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'push_tokens')]
class PushToken
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\ManyToOne(targetEntity: User::class, inversedBy: 'pushTokens')]
    private User $user;

    #[ORM\Column(type: 'string', length: 255)]
    private string $token;  // Expo push token

    #[ORM\Column(type: 'string', length: 10, default: 'mobile')]
    private string $type = 'mobile';  // mobile, tablet, web

    #[ORM\Column(type: 'string', length: 50, nullable: true)]
    private ?string $deviceName;

    #[ORM\Column(type: 'datetime')]
    private \DateTimeInterface $createdAt;

    #[ORM\Column(type: 'boolean')]
    private bool $isActive = true;

    // Getters and setters...
}
```

### User Entity Integration
```php
#[ORM\Entity]
#[ORM\Table(name: 'users')]
class User
{
    // ... other properties

    #[ORM\OneToMany(targetEntity: PushToken::class, mappedBy: 'user')]
    private ArrayCollection $pushTokens;

    public function getPushTokens(): iterable
    {
        return $this->pushTokens;
    }

    public function addPushToken(PushToken $token): self
    {
        if (!$this->pushTokens->contains($token)) {
            $this->pushTokens->add($token);
        }
        return $this;
    }

    public function removePushToken(PushToken $token): self
    {
        $this->pushTokens->removeElement($token);
        return $this;
    }
}
```

## Usage Examples

### Registering Push Token

```php
use Bone\PushNotifications\PushNotificationManager;

class PushController extends Controller
{
    public function registerAction($request)
    {
        $data = json_decode($request->getBody()->getContents(), true);
        $userId = $this->currentUser->getId();
        
        $token = new PushToken();
        $token->setUser($this->currentUser);
        $token->setToken($data['token']);
        $token->setType($data['type'] ?? 'mobile');
        $token->setDeviceName($data['deviceName'] ?? null);
        $token->setCreatedAt(new DateTime());
        
        $em->persist($token);
        $em->flush();
        
        return $this->jsonResponse(['success' => true]);
    }
    
    public function unregisterAction($request)
    {
        $tokenValue = $request->getAttribute('token');
        $token = $em->getRepository(PushToken::class)
            ->findOneBy(['token' => $tokenValue, 'user' => $this->currentUser]);
        
        if ($token) {
            $em->remove($token);
            $em->flush();
        }
        
        return $this->jsonResponse(['success' => true]);
    }
}
```

### Sending Push Notifications

```php
use Bone\PushNotifications\PushNotificationManager;

class NotificationController extends Controller
{
    public function sendAction($request)
    {
        $title = $request->getPost('title');
        $body = $request->getPost('body');
        $data = json_decode($request->getPost('data'), true);
        
        $manager = $this->container->get(PushNotificationManager::class);
        
        // Send to all users
        $manager->sendToAll($title, $body, $data);
        
        // Or send to specific user
        $manager->sendToUser($userId, $title, $body, $data);
        
        return $this->jsonResponse(['success' => true]);
    }
    
    public function sendBatchAction($request)
    {
        $title = $request->getPost('title');
        $body = $request->getPost('body');
        $userIds = $request->getPost('userIds');  // Array of IDs
        
        $manager = $this->container->get(PushNotificationManager::class);
        $manager->sendToMany($userIds, $title, $body);
        
        return $this->jsonResponse(['success' => true]);
    }
}
```

### Using PushNotificationManager Service

```php
class PushNotificationManager
{
    public function sendToUser(int $userId, string $title, string $body, array $data = []): void
    {
        $tokens = $this->getUserTokens($userId);
        
        foreach ($tokens as $token) {
            if ($token->getIsActive()) {
                $this->sendPush($token->getToken(), $title, $body, $data);
            }
        }
    }
    
    public function sendToAll(string $title, string $body, array $data = []): void
    {
        $tokens = $this->getAllActiveTokens();
        
        foreach ($tokens as $token) {
            $this->sendPush($token->getToken(), $title, $body, $data);
        }
    }
    
    public function sendToMany(array $userIds, string $title, string $body): void
    {
        foreach ($userIds as $userId) {
            $this->sendToUser($userId, $title, $body);
        }
    }
    
    private function sendPush(string $token, string $title, string $body, array $data = []): void
    {
        $url = 'https://exp.host/--/api/v2/push/send';
        
        $payload = [
            'to' => $token,
            'title' => $title,
            'body' => $body,
            'data' => $data,
        ];
        
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Accept: application/json',
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        curl_exec($ch);
        curl_close($ch);
    }
}
```

## Push Notification Data

### Notification Payload
```php
$data = [
    'title' => 'New Message',
    'body' => 'You have a new message from John',
    'icon' => '/icons/notification.png',
    'sound' => 'default',
    'badge' => 1,
    'color' => '#4A90E2',
    'click_action' => '/messages/123',
];

// Additional Expo fields
$payload = [
    'to' => $token,
    'title' => $data['title'],
    'body' => $data['body'],
    'data' => [
        'type' => 'message',
        'message_id' => '123',
        'redirect' => '/messages/123',
    ],
    'priority' => 'high',
    'ttl' => 86400,  // 24 hours
];
```

### Sound Options
```php
$sounds = [
    'default',    // Default system sound
    'success',    // Success tone
    'error',      // Error tone
    'warning',    // Warning tone
];
```

## Queueing Notifications

### Notification Queue Entity
```php
#[ORM\Entity]
#[ORM\Table(name: 'notification_queue')]
class NotificationQueue
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private int $id;

    #[ORM\ManyToOne(targetEntity: User::class)]
    private User $user;

    #[ORM\Column(type: 'string', length: 255)]
    private string $title;

    #[ORM\Column(type: 'string', length: 1000)]
    private string $body;

    #[ORM\Column(type: 'json', nullable: true)]
    private ?array $data = null;

    #[ORM\Column(type: 'string', length: 20, default: 'pending')]
    private string $status = 'pending';

    #[ORM\Column(type: 'datetime', nullable: true)]
    private ?\DateTimeInterface $sentAt = null;

    #[ORM\Column(type: 'string', length: 255, nullable: true)]
    private ?string $errorMessage = null;
}
```

### Queue Processor
```php
class NotificationProcessor
{
    public function processQueue(int $batchSize = 50): int
    {
        $queued = $em->getRepository(NotificationQueue::class)
            ->findBy(['status' => 'pending'], ['id' => 'ASC'], $batchSize);
        
        $processed = 0;
        
        foreach ($queued as $notification) {
            try {
                $this->sendNotification($notification);
                $notification->setStatus('sent');
                $notification->setSentAt(new DateTime());
                $notification->setErrorMessage(null);
            } catch (\Exception $e) {
                $notification->setStatus('failed');
                $notification->setErrorMessage($e->getMessage());
            }
            
            $em->flush();
            $processed++;
        }
        
        return $processed;
    }
    
    private function sendNotification(NotificationQueue $notification): void
    {
        $tokens = $notification->getUser()->getPushTokens();
        
        foreach ($tokens as $token) {
            if ($token->getIsActive()) {
                // Send to this token
                // (Implementation as above)
            }
        }
    }
}
```

## API Endpoints

### Push Token Management
```php
// Register token
$router->post('/api/push/token', [PushController::class, 'registerAction']);

// Unregister token
$router->delete('/api/push/token/{token}', [PushController::class, 'unregisterAction']);

// List tokens
$router->get('/api/push/tokens', [PushController::class, 'listAction']);

// Send notification
$router->post('/api/push/send', [NotificationController::class, 'sendAction']);
```

## Expo Configuration

### Expo Server URL
```php
// Production
define('EXPO_API_URL', 'https://exp.host/--/api/v2/push/send');

// Development/Testing
// define('EXPO_API_URL', 'https://exp.host/--/api/v2/push/send');
```

### Expo Credentials
No additional credentials required - Expo uses token-based authentication.

## Best Practices

1. **Store tokens securely**: Encrypt tokens in database
2. **Validate tokens**: Validate token format before saving
3. **Handle expiration**: Check token validity before sending
4. **Rate limit notifications**: Avoid sending too many too quickly
5. **Use batching**: Batch notifications for efficiency
6. **Track delivery**: Monitor notification status
7. **Test with Expo**: Use Expo Go app for testing
8. **Handle errors gracefully**: Retry failed notifications
9. **Use quiet times**: Send notifications during user-active hours
10. **Respect user preferences**: Let users control notification frequency

## Testing

### Local Testing
```bash
# Use Expo Go app for testing
# Install from App Store or Google Play
# Enter project URL in Expo Go
```

### Manual Testing
```php
// Send test notification
$manager->sendToUser($testUserId, 'Test', 'This is a test notification');
```

### Error Handling
```php
try {
    $manager->sendToUser($userId, $title, $body);
} catch (\Exception $e) {
    $logger->error('Push notification failed: ' . $e->getMessage());
    
    // Mark token as invalid if needed
    if (strpos($e->getMessage(), 'Expo token') !== false) {
        $token->setIsActive(false);
        $em->flush();
    }
}
```
