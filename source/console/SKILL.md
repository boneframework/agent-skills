---
name: bone-console
description: "Handles CLI commands and console operations in Bone Framework applications using delboy1978uk/bone-console package with Symfony Console integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "cli", "console", "commands", "artisan"]
trigger_patterns:
  - "console"
  - "cli"
  - "command"
  - "terminal"
  - "artisan"
  - "bone"
---

# Bone Console Skill

## When to Use
Activate this skill when working with command-line interface (CLI) commands in a Bone Framework application using the `delboy1978uk/bone-console` package.

## Package Information
- **Package**: `delboy1978uk/bone-console`
- **Dependencies**: Symfony Console, delboy1978uk/booty, delboy1978uk/barnacle
- **License**: MIT
- **PHP Version**: ^8.2
- **Entry Point**: `vendor/bin/bone` or `php bin/bone`

## Architecture

### ConsoleApplication
Extends `Symfony\Component\Console\Application` with Bone Framework integration:
- Returns custom version string with Bone ASCII art
- Integrates Bone Framework packages with console commands

### ConsolePackage
Registers default commands in the container:
- `DebugContainerCommand` - Shows container services
- `PackagesCommand` - Lists registered packages
- `PostInstallCommand` - Runs post-install tasks

## Core Components

### Command Registration Interface
```php
interface CommandRegistrationInterface
{
    public function registerConsoleCommands(Container $container): array;
}
```

Packages implementing this interface can register custom console commands.

### Console Command Base Class
```php
abstract class Command extends \Symfony\Component\Console\Command\Command
{
    // Provides access to Bone Framework services
}
```

## Built-in Commands

### 1. Debug Container
Lists all services registered in the container:
```bash
bone container:debug
```

### 2. List Packages
Shows all registered packages:
```bash
bone packages:list
```

### 3. Post Install
Runs post-install tasks:
```bash
bone post-install
```

## Creating Custom Commands

### 1. Create Command Class
```php
<?php

namespace App\Command;

use Bone\Console\Command;
use Barnacle\Container;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

class MyCommand extends Command
{
    protected function configure(): void
    {
        $this->setName('my:command')
            ->setDescription('My custom console command')
            ->addArgument('name', InputArgument::REQUIRED, 'Name parameter');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $name = $input->getArgument('name');
        $output->writeln(sprintf('Hello, %s!', $name));
        
        return self::SUCCESS;
    }
}
```

### 2. Register Command via Package
Create a package that implements `CommandRegistrationInterface`:

```php
<?php

namespace App;

use Bone\Console\CommandRegistrationInterface;
use Bone\Console\ConsoleApplication;
use Barnacle\Container;
use App\Command\MyCommand;

class AppPackage implements CommandRegistrationInterface
{
    public function registerConsoleCommands(Container $container): array
    {
        return [
            new MyCommand(),
        ];
    }
}
```

### 3. Register Package
Add to `config/packages.php`:
```php
return [
    'packages' => [
        App\AppPackage::class,
    ]
];
```

## Common Tasks

### 1. Running Commands
```bash
# List all available commands
bone list

# Get help for a command
bone my:command --help

# Run a command
bone my:command value
```

### 2. Accessing Container in Commands
```php
protected function execute(InputInterface $input, OutputInterface $output): int
{
    // Get container
    $container = $this->getContainer();
    
    // Get services
    $router = $container->get(Router::class);
    $entityManager = $container->get(EntityManagerInterface::class);
    
    // ...
}
```

### 3. Using IO Helper
```php
protected function execute(InputInterface $input, OutputInterface $output): int
{
    // Write output
    $output->writeln('<info>Success message</info>');
    $output->writeln('<error>Error message</error>');
    $output->writeln('<warning>Warning message</warning>');
    
    // Ask for input
    $helper = $this->getHelper('question');
    $question = new \Symfony\Component\Console\Question\Question('Enter name: ');
    $name = $helper->ask($input, $output, $question);
    
    return self::SUCCESS;
}
```

### 4. Configuring Command Options
```php
protected function configure(): void
{
    $this->setName('my:command')
        ->setDescription('My command')
        ->addArgument('name', InputArgument::REQUIRED, 'Name parameter')
        ->addOption('verbose', null, InputOption::VALUE_NONE, 'Enable verbose output')
        ->addOption('env', 'e', InputOption::VALUE_REQUIRED, 'Environment', 'production');
}
```

## Command Registration Patterns

### Package-Based Registration
```php
class AppPackage implements CommandRegistrationInterface
{
    public function registerConsoleCommands(Container $container): array
    {
        $commands = [];
        
        // Register multiple commands
        $commands[] = new MyFirstCommand();
        $commands[] = new MySecondCommand();
        
        return $commands;
    }
}
```

### Service-Based Registration
Commands can also be registered as container services:
```php
// In config/console.php
return [
    'consoleCommands' => [
        MyCommand::class,
    ]
];
```

## Integration with Bone Framework

### Application Bootstrapping
Commands can access the Bone Framework via the container:
```php
protected function execute(InputInterface $input, OutputInterface $output): int
{
    $container = $this->getContainer();
    
    // Access configuration
    $config = $container->get('site');
    $title = $config['site']['title'];
    
    // Access database
    $pdo = $container->get(PDO::class);
    
    // Access router
    $router = $container->get(Router::class);
    
    return self::SUCCESS;
}
```

### Environment-Aware Commands
```php
protected function execute(InputInterface $input, OutputInterface $output): int
{
    $env = getenv('APPLICATION_ENV');
    $output->writeln("Running in <info>{$env}</info> environment");
    
    return self::SUCCESS;
}
```

## Development Workflow

### 1. Create New Command
```bash
# Create command file
mkdir -p src/Command
touch src/Command/MyNewCommand.php
```

### 2. Implement Command
Follow the pattern in existing commands.

### 3. Register in Package
Add command to your package's `registerConsoleCommands()` method.

### 4. Register Package
Ensure package is listed in `config/packages.php`.

### 5. Test Command
```bash
bone list          # Verify command appears
bone my:command    # Test command execution
```

## Best Practices

1. **Use Symfony Console base class**: Extend `Bone\Console\Command` for Bone integration
2. **Name commands clearly**: Use `vendor:command:subcommand` format
3. **Provide helpful descriptions**: Describe what command does
4. **Add input validation**: Validate all inputs in configure()
5. **Use color output**: Help users understand status with colors
6. **Handle errors gracefully**: Return proper exit codes
7. **Document commands**: Add help text for options and arguments
8. **Test commands**: Create unit tests for command logic
9. **Keep commands focused**: Single responsibility principle
10. **Use environment variables**: Configure via .env, not hard-coded
