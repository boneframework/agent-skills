---
name: bf-lamp
description: Dockerised LAMP stack (Linux, Apache, MariaDB, PHP 8.3) for PHP web development. Includes self-signed SSL, MailHog for email testing, and NodeJs 18. Use when setting up PHP development environments, testing PHP applications, or working with Apache/MySQL/PHP projects.
license: MIT
metadata:
  author: boneframework
  version: "1.0"
  repository: https://github.com/boneframework/lamp
compatibility: Requires Docker and Docker Compose
---

# LAMP Stack Skill

A Dockerised LAMP (Linux, Apache, MariaDB, PHP) stack for PHP web development with modern tooling.

## Overview

This skill provides a complete Docker-based development environment including:

- **Linux**: Docker-based Linux server
- **Apache**: Web server with self-signed SSL certificate
- **MariaDB**: MySQL-compatible database server
- **PHP 8.3**: Latest PHP with common modules
- **MailHog**: Email testing (SMTP on port 1025, web UI on port 8025)
- **NodeJs 18**: For frontend tooling

## When to Use This Skill

Use this skill when you need to:

- Set up a PHP development environment
- Test PHP web applications locally
- Develop with Apache, MySQL/MariaDB, and PHP
- Test email functionality without sending real emails
- Work on projects requiring both PHP and Node.js
- Create isolated development environments with SSL

The instructions below are for the host machine. You are running inside an agent zero container, so use `/var/run/docker.sock` to access the services.

## Initial Setup

### 1. Configure Domain Name

The default domain is `boneframework.docker`. Change it to your preferred domain:

```bash
bin/setdomain dev.mycoolsite.com
```

### 2. SSL Certificate

A self-signed SSL certificate is automatically generated. To use your own certificate:

1. Copy your certificate to `build/certificates/server.crt`
2. Copy your private key to `build/certificates/server.key`
3. Run `bin/rebuild` to apply changes

### 3. Add Your Code

Place your PHP application in the `code` directory. Apache serves from `code/public/index.php` by default.

- Delete the placeholder `public/index.php`
- Add your project files or create a symlink to your existing project

### 4. Configure Virtual Host

Edit your system's hosts file to access the site by domain name:

**Linux/Mac**: `/etc/hosts`
**Windows**: `C:\Windows\system32\drivers\etc\hosts`

Add this line:
```
127.0.0.1 boneframework.docker
```
(Replace with your custom domain if you changed it)

## Starting and Stopping

### Start the Server

```bash
bin/start
```

This starts all services and displays logs. Keep this terminal open while working.

Access your site at:
- `https://localhost`
- `https://boneframework.docker` (or your custom domain)

### Stop the Server

Press `CTRL-C` in the terminal running the server, then:

```bash
bin/stop
```

## Running Commands

### Execute Commands in PHP Container

Run commands like Composer, PHP CLI, etc.:

```bash
bin/run composer install
bin/run bone router:list
bin/run composer require vendor/package
```

### Execute Node.js Commands

Run npm or npx commands:

```bash
bin/runnode npm ci --save-all
bin/runnode npx webpack
bin/runnode npm run build
```

### Interactive Terminal Access

Enter a container for interactive work:

```bash
bin/terminal [service]
```

Available services: `php`, `mariadb`, `node`

Example:
```bash
bin/terminal php
# Now you're inside the PHP container
```

### Restart Services

Restart individual services:

```bash
bin/restart [service]
```

### Rebuild Configuration

After changing Docker configuration:

```bash
bin/rebuild
```

### Initial Setup Script

Run custom initialization tasks (edit `bin/init` first):

```bash
bin/init
```

Typical uses:
- Run `composer install`
- Execute database migrations 
- Populate fixtures
- Warm up caches

## Database Configuration

### Connection Settings

When connecting from PHP code:

- **Host**: `mariadb` (NOT `127.0.0.1` or `localhost`)
- **Port**: `3306`
- **Username**: Check `.env` file
- **Password**: Check `.env` file
- **Database**: Check `.env` file

### External Database Access

To connect from your host machine (e.g., using a GUI tool):

- **Host**: `localhost` or `127.0.0.1`
- **Port**: Check `docker-compose.yml` for mapped port

## Email Testing with MailHog

MailHog captures all outgoing emails for testing:

### SMTP Configuration

- **Host**: `mailhog`
- **Port**: `1025`
- **No authentication required**

### View Captured Emails

Access the MailHog web interface:
```
http://boneframework.docker:8025
```

All emails sent by your application appear here instead of being delivered.

## File Structure

```
lamp/
├── bin/                    # Management scripts
│   ├── start              # Start the stack
│   ├── stop               # Stop the stack
│   ├── run                # Run commands in PHP container
│   ├── runnode            # Run commands in Node container
│   ├── terminal           # Interactive shell access
│   ├── restart            # Restart services
│   ├── rebuild            # Rebuild containers
│   ├── setdomain          # Change domain name
│   └── init               # Custom initialization script
├── build/                 # Docker build files
│   └── certificates/      # SSL certificates
├── code/                  # Your application code
│   └── public/           # Web root (Apache serves from here)
├── .env                   # Environment variables
├── docker-compose.yml     # Docker services configuration
└── README.md
```

## Customization

### Environment Variables

Edit `.env` file to configure:
- Database credentials
- PHP settings
- Port mappings
- Other service configurations

### Docker Configuration

Modify `docker-compose.yml` to:
- Change service versions
- Add new services
- Modify port mappings
- Adjust resource limits

After changes, run `bin/rebuild`.

### PHP Configuration

PHP and Apache Dockerfiles are in the `build/` directory. Customize as needed.

### SMTP Configuration

The stack uses MailHog via `ssmtp.conf` configuration. All emails are automatically captured.

## Common Tasks

### Install PHP Dependencies

```bash
bin/run composer install
```
### Create fresh database from schema
```bash
bin/run bone migrant:create
```

### Drop the database  schema
```bash
bin/run bone migrant:drop --force
```

### Run Database Migrations
```bash
bin/run bone migrant:migrate
```

### Populate DB with vendor package fixtures
```bash
bin/run bone migrant:vendor-fixtures
```

### Populate DB with fixtures
```bash
bin/run bone migrant:fixtures
```

### Create a new migration
```bash
bin/run bone migrant:diff
```

### Install Node Dependencies

```bash
bin/runnode npm install
```

### Build Frontend Assets

```bash
bin/runnode npm run build
```

### Clear Application Cache

```bash
bin/run php artisan cache:clear  # Laravel
bin/run php bin/console cache:clear  # Symfony
```

### Access Database CLI

```bash
bin/terminal mariadb
mysql -u root -p
```

## Productivity Tips

### Simplify Command Execution

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH=$PATH:bin:vendor/bin
```

This allows running commands without prefixes:

```bash
# Before
bin/start
vendor/bin/phpunit

# After
start
phpunit
```

### File Naming

Avoid spaces in filenames when working in the `code/` directory for better compatibility.

## Troubleshooting

### Port Conflicts

If ports 80, 443, 3306, or 8025 are already in use:
1. Edit `docker-compose.yml`
2. Change port mappings
3. Run `bin/rebuild`

### Permission Issues

If you encounter file permission errors:
```bash
bin/terminal php
chown -R www-data:www-data /var/www/html
```

### Database Connection Fails

Ensure you're using `mariadb` as the host, not `localhost` or `127.0.0.1`.

### SSL Certificate Warnings

Self-signed certificates trigger browser warnings. This is normal for development. Click "Advanced" and proceed.

## Technical Details

### PHP Modules

See the complete list of installed PHP modules:
<https://github.com/delboy1978uk/dockerhub/blob/master/php83/Dockerfile>

### Service Architecture

The stack uses Docker Compose to orchestrate multiple containers:
- PHP/Apache container (web server)
- MariaDB container (database)
- MailHog container (email testing)
- Node.js container (frontend tooling)

Containers communicate via Docker networking.

## License

MIT License - See LICENSE.md in the repository

## Repository

<https://github.com/boneframework/lamp>