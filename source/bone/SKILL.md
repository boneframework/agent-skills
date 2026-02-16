---
name: bone-framework-core
description: Provides expert-level knowledge and procedural guidance for working with the Bone Framework core in PHP, including setup, package registration, routing, configuration, and best practices for building web applications. Use this skill when tasked with building, maintaining, or extending PHP applications using Bone Framework, such as initializing projects, configuring components, or integrating packages.
metadata:
  author: Bone Framework Team
  version: "1.0"
compatibility: Requires PHP 8.1+ with Composer installed. Optional Docker for development.
---

# Bone Framework Core Skill

This skill equips AI agents with comprehensive knowledge of the Bone Framework core, a lightweight PHP framework using PSR standards, dependency injection, and middleware.

## When to Use This Skill
- Initializing a new Bone Framework project.
- Configuring packages, routes, controllers, or middleware.
- Handling configuration for databases, i18n, logging, or sessions.
- Implementing PSR-compliant components like HTTP messaging or DI containers.
- Debugging or optimizing Bone Framework applications.
- Integrating recommended packages like bone-user, bone-doctrine, or bone-oauth2.

Do not use for unrelated frameworks (e.g., Laravel, Symfony) unless explicitly comparing.

## Prerequisites
- PHP 8.1+ with Composer installed.
- Optional: Docker for development environment.
- Familiarity with PSR standards (PSR-7, PSR-11, PSR-15).

## Step-by-Step Workflows

### 1. Project Setup
To create a new Bone Framework project:

1. Install via Composer:
```bash
composer create-project boneframework/skeleton your/path/here
cp your/path/here/.env.example your/path/here/.env
```
2. Verify installation by accessing the site; you should see the default Bone Framework page.

### 2. Configuration Management
- Config files in `config/` return arrays (e.g., `bone-db.php`, `bone-i18n.php`).
- Environment-specific overrides via `APPLICATION_ENV` (e.g., `config/production/`).
- Key configs:
  - `packages.php`: List of packages to register (order matters for dependencies).
  - `middleware.php`: Site-wide middleware.
  - `bone-db.php`: Database credentials (host, database, user, pass).
  - `bone-i18n.php`: Translations dir, type (Gettext), default_locale, supported_locales.
  - `bone-log.php`: Log channels (e.g., 'default' => 'data/logs/default_log').

Access config in code via DI container or traits.
