---
name: "bone-doctrine"
description: "Handles database operations, entities, migrations, and fixtures in Bone Framework applications using delboy1978uk/bone-doctrine."
version: "1.0.0"
author: "Agent Zero"
tags: ["php", "bone-framework", "doctrine", "orm", "database", "migrations", "fixtures"]
trigger_patterns:
  - "database"
  - "entity"
  - "migrations"
  - "fixtures"
  - "db"
  - "orm"
  - "doctrine"
  - "entities"
---

# Bone Doctrine Skill

## When to Use
Activate this skill when working with databases, creating or modifying entities, running database migrations, or generating fixtures in a Bone Framework application using the `delboy1978uk/bone-doctrine` package.

## Package Information
- **Package**: `delboy1978uk/bone-doctrine`
- **Purpose**: Integrates Doctrine ORM into Bone Framework.

## General Guidelines
1. **Entities**: Doctrine entities should be plain PHP objects with Doctrine mapping attributes or annotations. Prefer PHP 8 attributes.
2. **Entity Manager**: The `EntityManager` is the primary interface for database interactions (`persist`, `flush`, `find`, etc.).
3. **Repositories**: Use custom repository classes for complex queries using `QueryBuilder`.
4. **Migrations**: Database schema changes should be handled via Doctrine Migrations. Never modify the database schema manually.
5. **Fixtures**: Use Doctrine Data Fixtures for populating the database with test or initial data.

## Common Tasks

### 1. Creating an Entity
When creating an entity, ensure it has a primary key, appropriate fields, and getter/setter methods.

```php
<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: 'users')]
class User
{
    #[ORM\Id]
    #[ORM\Column(type: 'integer')]
    #[ORM\GeneratedValue]
    private int $id;

    #[ORM\Column(type: 'string', length: 255)]
    private string $name;

    public function getId(): int
    {
        return $this->id;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function setName(string $name): void
    {
        $this->name = $name;
    }
}
```

### 2. Using the EntityManager
In Bone framework, the `EntityManagerInterface` is typically registered in the dependency injection container.

```php
use Doctrine\ORM\EntityManagerInterface;

$em = $container->get(EntityManagerInterface::class);
$em->persist($user);
$em->flush();
```

### 3. creating abd dropping the database
Typically used in development environments. Use the command line to create the DB schema.
- **Create**: `vendor/bin/bone migrant:create`
- **Drop**: `vendor/bin/bone migrant:drop --force`

### 4. Migrations
Use the command line to generate and apply schema changes.
- **Generate**: `vendor/bin/bone migrant:diff`
- **Migrate**: `vendor/bin/bone migrant:migrate`

### 5. Proxies
After creating the DB (or migrating), proxy classes should be generated
- **Generate**: `vendor/bin/bone migrant:generate-proxies`

### 6. Fixtures
Fixtures can either be provided by the app, or a Bone Framework vendor package. To populate vendor and app fixtures:
- **Vendor Fixtures**: `vendor/bin/bone migrant:vendor-fixtures`
- **App Fixtures**: `vendor/bin/bone migrant:fixtures`

### 7. Using Convenience Traits (src/Traits)
The `delboy1978uk/bone-doctrine` package provides several convenience traits in the `src/Traits` folder. Use these traits to quickly add standard properties and their corresponding getter/setter methods to your entities (such as ID, Timestampable behaviors, UUIDs, etc.).

**Example Usage:**
```php
<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;
use Bone\Doctrine\Traits\HasIdTrait; // Include the appropriate trait namespace

#[ORM\Entity]
class Article
{
    // Use the trait to inject properties (like $id) and methods (like getId(), setId())
    use HasIdTrait;

    #[ORM\Column(type: 'string')]
    private string $title;

    // ...
}
```
