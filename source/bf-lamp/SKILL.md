---
name: "bf-lamp"
description: "Informs Agent Zero that it's running in a Bone Framework Docker container as part of a docker-compose LAMP stack with php, node, and mariadb services. Use when executing PHP (composer), Node (npm), or MariaDB (mysql) commands."
version: "1.0.0"
author: "Agent Zero User"
tags: ["docker", "lamp", "php", "node", "mariadb", "composer", "mysql", "bone"]
trigger_patterns:
  - "lamp"
  - "composer"
  - "php container"
  - "node container"
  - "mariadb"
  - "mysql container"
  - "docker compose"
  - "bone framework"
---

# LAMP Project Docker Environment

## Environment Overview

You (Agent Zero) are running inside a Docker container that is part of a docker-compose LAMP stack. This stack includes the following sibling containers:

- **php** - PHP runtime with Apache (for running PHP applications and composer)
- **node** - Node.js runtime (for running npm and node commands)
- **mariadb** - MariaDB database server (for MySQL operations)

## Important: You Are Inside a Container

Since you are running inside a container, you **cannot** directly execute commands like `composer`, `npm`, or `mysql` in your local environment. Instead, you must use the Docker socket to execute commands in the appropriate sibling containers.

## How to Execute Commands in Sibling Containers

### General Pattern

To execute a command in a sibling container, use this pattern:

```bash
docker -H unix:///var/run/docker.sock exec [container-name] [command]
```

**Key Components:**
- `-H unix:///var/run/docker.sock` - Connects to the Docker daemon via the socket
- `exec` - Executes a command in a running container
- `[container-name]` - The name of the target container
- `[command]` - The command to execute

### Finding Container Names

If you need to verify container names, list all running containers:

```bash
docker -H unix:///var/run/docker.sock ps
```

Container names typically follow the pattern: `[project-name]-[service-name]-[number]`

For example:
- `lamp-php-1`
- `lamp-node-1`
- `lamp-mariadb-1`

## Service-Specific Commands

### PHP Container (composer, php, bone)
The PHP container shares the same volumes as the AgentZero container, so the paths to the project files are the same.
**Running bone:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-php-1 bone --help
docker -H unix:///var/run/docker.sock exec lamp-php-1 bone migrant:migrate
docker -H unix:///var/run/docker.sock exec lamp-php-1 bone assets:deploy
```
**Running Composer:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-php-1 composer install
docker -H unix:///var/run/docker.sock exec lamp-php-1 composer require vendor/package
docker -H unix:///var/run/docker.sock exec lamp-php-1 composer update
```

**Running PHP:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-php-1 php -v
docker -H unix:///var/run/docker.sock exec lamp-php-1 php script.php
```

**Interactive Shell:**
```bash
docker -H unix:///var/run/docker.sock exec -it lamp-php-1 bash
```

### Node Container (npm, node)

**Running NPM:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-node-1 npm install
docker -H unix:///var/run/docker.sock exec lamp-node-1 npm run build
docker -H unix:///var/run/docker.sock exec lamp-node-1 npm install package-name
```

**Running Node:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-node-1 node -v
docker -H unix:///var/run/docker.sock exec lamp-node-1 node script.js
```

**Interactive Shell:**
```bash
docker -H unix:///var/run/docker.sock exec -it lamp-node-1 bash
```

### MariaDB Container (mysql)

**Running MySQL Client:**
```bash
docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -p
docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -ppassword -e "SHOW DATABASES;"
```

**Database Operations:**
```bash
# Create database
docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -ppassword -e "CREATE DATABASE mydb;"

# Import SQL file
docker -H unix:///var/run/docker.sock exec -i lamp-mariadb-1 mysql -u root -ppassword mydb < dump.sql

# Export database
docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysqldump -u root -ppassword mydb > backup.sql
```

**Interactive Shell:**
```bash
docker -H unix:///var/run/docker.sock exec -it lamp-mariadb-1 bash
```

## Working with Files

### Copying Files to Containers

```bash
docker -H unix:///var/run/docker.sock cp /local/path/file.txt lamp-php-1:/container/path/
```

### Copying Files from Containers

```bash
docker -H unix:///var/run/docker.sock cp lamp-php-1:/container/path/file.txt /local/path/
```

## Common Workflows

### Setting Up a New PHP Project

1. Create composer.json in your project directory
2. Install dependencies:
   ```bash
   docker -H unix:///var/run/docker.sock exec lamp-php-1 composer install
   ```

### Building Frontend Assets

1. Ensure package.json exists
2. Install dependencies:
   ```bash
   docker -H unix:///var/run/docker.sock exec lamp-node-1 npm install
   ```
3. Build assets:
   ```bash
   docker -H unix:///var/run/docker.sock exec lamp-node-1 npm run build
   ```

### Database Setup

1. Create database:
   ```bash
   docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -ppassword -e "CREATE DATABASE myapp;"
   ```
2. Import schema:
   ```bash
   docker -H unix:///var/run/docker.sock exec -i lamp-mariadb-1 mysql -u root -ppassword myapp < schema.sql
   ```

## Troubleshooting

### Container Not Found

If you get "No such container" error:
1. List running containers to verify names:
   ```bash
   docker -H unix:///var/run/docker.sock ps
   ```
2. Check if the container is running:
   ```bash
   docker -H unix:///var/run/docker.sock ps -a
   ```

### Permission Denied

If you get permission errors:
- Ensure the Docker socket is mounted and accessible
- Check socket permissions: `ls -la /var/run/docker.sock`

### Command Not Found in Container

If a command isn't available in the container:
- Verify you're using the correct container (php vs node vs mariadb)
- Check if the tool is installed in that container
- You may need to install it first

## Best Practices

1. **Always use the Docker socket** - Never try to run composer, npm, or mysql directly
2. **Verify container names** - Use `docker ps` if unsure about container names
3. **Use appropriate containers** - PHP commands in php container, Node in node container, etc.
4. **Handle paths carefully** - Remember that container paths may differ from your local paths
5. **Use -i flag for input** - When piping data into containers (like SQL imports)
6. **Use -it flags for interactive** - When you need an interactive shell or prompt

## Quick Reference

| Task | Container | Command |
|------|-----------|----------|
| Install PHP packages | php | `docker -H unix:///var/run/docker.sock exec lamp-php-1 composer install` |
| Install Node packages | node | `docker -H unix:///var/run/docker.sock exec lamp-node-1 npm install` |
| Run MySQL query | mariadb | `docker -H unix:///var/run/docker.sock exec lamp-mariadb-1 mysql -u root -ppassword -e "QUERY"` |
| PHP shell | php | `docker -H unix:///var/run/docker.sock exec -it lamp-php-1 bash` |
| Node shell | node | `docker -H unix:///var/run/docker.sock exec -it lamp-node-1 bash` |
| MySQL shell | mariadb | `docker -H unix:///var/run/docker.sock exec -it lamp-mariadb-1 mysql -u root -ppassword` |

