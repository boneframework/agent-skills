---
name: bone-oauth2
description: "Handles OAuth2 integration in Bone Framework applications using delboy1978uk/bone-oauth2 package for OAuth2 server implementation including authorization and resource server functionality."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "oauth2", "authentication", "authorization", "tokens", "api"]
trigger_patterns:
  - "bone-oauth2"
  - "oauth2"
  - "oauth"
  - "tokens"
  - "api authentication"
---

# Bone OAuth2 Skill

## When to Use
Activate this skill when implementing OAuth2 authorization and resource server in Bone Framework applications using the delboy1978uk/bone-oauth2 package.

## Package Information
- **Package**: `delboy1978uk/bone-oauth2`
- **License**: MIT
- **PHP Version**: ^8.2
- **Dependencies**: bone-doctrine, bone-user, league/oauth2-server, laminas-diactoros

## Installation

```bash
composer require delboy1978uk/bone-oauth2
```

## Setup Requirements

### Generate OAuth2 Keys
```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate public key from private
openssl rsa -in private.key -pubout -out public.key

# Generate encryption key for tokens
vendor/bin/generate-defuse-key
```

### Configure Keys
```php
// config/oauth2.php
return [
    'oauth2' => [
        'clientCredentialsTokenTTL' => 'PT1H',      // 1 hour
        'authCodeTTL' => 'PT1M',                    // 1 minute
        'accessTokenTTL' => 'PT5M',                 // 5 minutes
        'refreshTokenTTL' => 'P1M',                 // 1 month
        'privateKeyPath' => '/path/to/private.key',
        'publicKeyPath' => '/path/to/public.key',
        'encryptionKey' => 'generated-key-string'
    ]
];
```

## Package Features

### Key Features
- OAuth2 Authorization Server implementation
- OAuth2 Resource Server implementation
- Client management (create, read, update, delete)
- Token management (access tokens, refresh tokens, auth codes)
- Scope management
- User API key management endpoint

### Routes (when package registered)
- `/oauth2/authorize` - Authorization endpoint
- `/oauth2/token` - Token endpoint
- `/oauth2/revoke` - Token revocation
- `/oauth2/info` - OAuth2 server information
- `/user/api-keys` - User API key management

## Key Classes

### BoneOAuth2Package
Main package class that registers OAuth2 routes and services.

```php
use Bone\OAuth2\BoneOAuth2Package;

$package = new BoneOAuth2Package();
$package->addToContainer($container);
$package->addToSiteConfig($siteConfig);
```

### ResourceServerMiddleware
Middleware for protecting API routes.

```php
use Bone\OAuth2\Middleware\ResourceServerMiddleware;

$router->group('/api', function ($router) {
    $router->get('/users', [UserController::class, 'index']);
})->middleware(ResourceServerMiddleware::class);
```

## Entities

### OAuth2 Entities
```php
// AccessToken
- id
- clientId
- userId
- accessToken
- refreshToken
- expiresAt
- scopes

// AuthCode
- id
- clientId
- userId
- code
- redirectUri
- expiresAt
- scopes

// Client
- id
- clientId
- clientSecret
- redirectUri
- grantTypes
- scopes

// RefreshToken
- id
- accessTokenId
- refreshToken
- expiresAt

// Scope
- id
- scope
- description
```

## OAuth2 Flows

### Authorization Code Flow

#### 1. Authorization Request
```php
use League\OAuth2\Server\AuthorizationServer;

$server = new AuthorizationServer(
    $clientRepository,
    $tokenRepository,
    $scopeRepository,
    $privateKey,
    $publicKey
);

$authRequest = $server->validateAuthorizationRequest($request);
$userId = $authRequest->getUserId();

// Store authorization code
$authorizationCode = new AuthorizationCodeEntity();
$authorizationCode->setAuthorizationId(uniqid());
$authorizationCode->setClientId($clientId);
$authorizationCode->setUserId($userId);
$authorizationCode->setRedirectUri($redirectUri);
$authorizationCode->setExpiresAt(new DateTime('+10 minutes'));

// Redirect user to authorization page
return $this->redirect($authRequest->getRedirectUri());
```

#### 2. Token Exchange
```php
public function tokenAction($request)
{
    $client = $this->container->get(ClientRepository::class);
    $tokens = $this->container->get(TokenRepository::class);
    
    $clientId = $request->getPost('client_id');
    $clientSecret = $request->getPost('client_secret');
    $code = $request->getPost('code');
    $redirectUri = $request->getPost('redirect_uri');
    
    $client = $client->getClientById($clientId);
    
    if (!$client || $client->getSecret() !== $clientSecret) {
        return $this->jsonResponse(['error' => 'invalid_client'], 401);
    }
    
    $tokens->generateAccessToken($client, $code, $redirectUri);
}
```

### Client Credentials Flow
```php
public function tokenAction($request)
{
    $clientId = $request->getPost('client_id');
    $clientSecret = $request->getPost('client_secret');
    
    $client = $this->container->get(ClientRepository::class)
        ->getClientById($clientId);
    
    if (!$client || $client->getSecret() !== $clientSecret) {
        return $this->jsonResponse(['error' => 'invalid_client'], 401);
    }
    
    $token = $this->container->get(TokenGenerator::class)
        ->generateToken($client, [], 'client_credentials');
    
    return $this->jsonResponse([
        'access_token' => $token->getToken(),
        'expires_in' => $token->getExpires(),
        'token_type' => 'Bearer',
    ]);
}
```

### Refresh Token Flow
```php
public function refreshTokenAction($request)
{
    $refreshToken = $request->getPost('refresh_token');
    
    $tokens = $this->container->get(TokenRepository::class);
    $oldToken = $tokens->getRefreshToken($refreshToken);
    
    if (!$oldToken || $oldToken->isExpired()) {
        return $this->jsonResponse(['error' => 'invalid_grant'], 400);
    }
    
    $newToken = $tokens->refreshToken($oldToken);
    
    return $this->jsonResponse([
        'access_token' => $newToken->getToken(),
        'refresh_token' => $newToken->getRefreshToken(),
        'expires_in' => $newToken->getExpires(),
    ]);
}
```

## Client Management

### Creating a Client
```php
public function createClientAction($request)
{
    $client = new Client();
    $client->setName($request->getPost('name'));
    $client->setClientId(uniqid());
    $client->setClientSecret(bin2hex(random_bytes(32)));
    $client->setRedirectUri($request->getPost('redirect_uri'));
    $client->setGrantTypes(explode(',', $request->getPost('grant_types')));
    $client->setScopes(explode(',', $request->getPost('scopes')));
    
    $em->persist($client);
    $em->flush();
    
    return $this->jsonResponse([
        'client_id' => $client->getClientId(),
        'client_secret' => $client->getClientSecret(),
    ]);
}
```

### Client Configuration
```php
// Grant types
- authorization_code
- client_credentials
- refresh_token
- password (not recommended)
- implicit (not recommended)

// Scopes
- read
- write
- admin
- email
- profile
```

## Token Management

### Access Token Response
```php
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 300,
    "refresh_token": "def50200d51c28b8a9c4...",
    "scope": "read write"
}
```

### Token Expiration
```php
// Default TTLs (configurable)
- Client Credentials Token: 1 hour
- Authorization Code: 1 minute
- Access Token: 5 minutes
- Refresh Token: 1 month

// Check token expiration
$token->isExpired();  // Returns boolean
$token->getExpires(); // Returns DateTime
```

### Token Revocation
```php
public function revokeAction($request)
{
    $token = $request->getPost('token');
    $tokenType = $request->getPost('token_type');  // access or refresh
    
    $tokens = $this->container->get(TokenRepository::class);
    
    if ($tokenType === 'access') {
        $tokens->revokeAccessToken($token);
    } else {
        $tokens->revokeRefreshToken($token);
    }
    
    return $this->jsonResponse(['success' => true]);
}
```

## User API Keys

### User API Key Endpoint
```php
// GET /user/api-keys
$router->get('/user/api-keys', [UserApiKeyController::class, 'indexAction']);

// POST /user/api-keys
$router->post('/user/api-keys', [UserApiKeyController::class, 'createAction']);

// DELETE /user/api-keys/{id}
$router->delete('/user/api-keys/{id}', [UserApiKeyController::class, 'deleteAction']);
```

### Create API Key
```php
public function createAction($request)
{
    $userId = $this->currentUser->getId();
    $name = $request->getPost('name');
    $scopes = $request->getPost('scopes');
    
    $apiKey = new ApiKey();
    $apiKey->setUserId($userId);
    $apiKey->setName($name);
    $apiKey->setToken(bin2hex(random_bytes(40)));
    $apiKey->setScopes($scopes);
    $apiKey->setExpiresAt(new DateTime('+1 year'));
    
    $em->persist($apiKey);
    $em->flush();
    
    return $this->jsonResponse(['token' => $apiKey->getToken()]);
}
```

## Resource Server Protection

### Protecting API Routes
```php
use Bone\OAuth2\Middleware\ResourceServerMiddleware;

$router->group('/api', function ($router) {
    $router->get('/users', [UserController::class, 'index']);
    $router->post('/users', [UserController::class, 'create']);
})->middleware(ResourceServerMiddleware::class);

// Or in middleware configuration
return [
    'routeMiddleware' => [
        'GET' => [
            '/api' => [ResourceServerMiddleware::class],
        ],
        'POST' => [
            '/api' => [ResourceServerMiddleware::class],
        ],
    ],
];
```

### Getting Current User from Token
```php
public function indexAction($request)
{
    $user = $request->getAttribute('user');
    
    if (!$user) {
        return $this->jsonResponse(['error' => 'Unauthorized'], 401);
    }
    
    // User is authenticated
    $userId = $user->getId();
    // ... proceed with query
}
```

## OAuth2 Configuration

### Complete Configuration
```php
// config/packages.php
return [
    'packages' => [
        \Bone\OAuth2\BoneOAuth2Package::class,
        // ... other packages
    ]
];

// config/oauth2.php
return [
    'oauth2' => [
        'clientCredentialsTokenTTL' => 'PT1H',
        'authCodeTTL' => 'PT1M',
        'accessTokenTTL' => 'PT5M',
        'refreshTokenTTL' => 'P1M',
        'privateKeyPath' => '/path/to/private.key',
        'publicKeyPath' => '/path/to/public.key',
        'encryptionKey' => 'generated-key-string'
    ]
];
```

## Testing OAuth2

### Unit Tests
```php
public function testAuthorizationCodeFlow(): void
{
    // 1. Create client
    $client = $this->createClient(['grant_types' => 'authorization_code']);
    
    // 2. Get authorization code
    $authUrl = $this->generateAuthorizationUrl($client);
    $this->get($authUrl);
    
    $authorizationCode = $this->getLastAuthorizationCode();
    
    // 3. Exchange for token
    $response = $this->post('/oauth2/token', [
        'client_id' => $client->getClientId(),
        'client_secret' => $client->getClientSecret(),
        'grant_type' => 'authorization_code',
        'code' => $authorizationCode,
        'redirect_uri' => $client->getRedirectUri(),
    ]);
    
    $this->assertEquals(200, $response->getStatusCode());
    $data = json_decode($response->getBody(), true);
    
    $this->assertArrayHasKey('access_token', $data);
    $this->assertArrayHasKey('refresh_token', $data);
}
```

### Integration Tests
```php
public function testProtectedResourceAccess(): void
{
    // 1. Get access token
    $token = $this->getAccessToken();
    
    // 2. Access protected resource
    $response = $this->get('/api/users', [
        'Authorization' => 'Bearer ' . $token,
    ]);
    
    $this->assertEquals(200, $response->getStatusCode());
}
```

## Best Practices

1. **Store keys securely**: Use environment variables or secure vault
2. **Use HTTPS**: Always use HTTPS in production
3. **Short token lifetimes**: 5-15 minutes for access tokens
4. **Validate redirect URIs**: Prevent open redirector attacks
5. **Use state parameter**: Prevent CSRF attacks
6. **Implement token revocation**: Allow users to revoke tokens
7. **Rate limit OAuth endpoints**: Prevent abuse
8. **Audit token usage**: Log token issuance and usage
9. **Support PKCE**: For public clients (mobile/apps)
10. **Scope minimization**: Request only necessary scopes

## Common Error Responses

```json
// Invalid client
{
    "error": "invalid_client",
    "error_description": "Client authentication failed"
}

// Invalid grant
{
    "error": "invalid_grant",
    "error_description": "The provided authorization grant is invalid"
}

// Invalid scope
{
    "error": "invalid_scope",
    "error_description": "The requested scope is invalid"
}

// Rate limited
{
    "error": "too_many_requests",
    "error_description": "Rate limit exceeded"
}
```
