---
name: dev-tools
description: "Handles development tools and testing in Bone Framework applications using delboy1978uk/dev-tools package with Codeception, PHPStan, and GrumPHP integration."
version: "1.0.0"
author: "Bone Framework Team"
tags: ["php", "bone-framework", "dev-tools", "testing", "codeception", "phpstan", "grumphp"]
trigger_patterns:
  - "dev-tools"
  - "testing"
  - "codeception"
  - "phpstan"
  - "grumphp"
  - "quality"
  - "ci"
---

# Dev Tools Skill

## When to Use
Activate this skill when working with development tools, testing, and code quality in Bone Framework applications using the `delboy1978uk/dev-tools` package.

## Package Information
- **Package**: `delboy1978uk/dev-tools`
- **Includes**: Codeception, PHPStan, GrumPHP
- **License**: MIT
- **PHP Version**: ^8.2

## Components

### Codeception
Full-featured testing framework:
- Unit tests
- Functional tests
- Acceptance tests
- API tests

### PHPStan
Static analysis tool:
- Type checking
- Code quality analysis
- Error detection

### GrumPHP
Git hooks integration:
- Pre-commit checks
- Code style enforcement

## Running Tests

```bash
# Run all tests
vendor/bin/codecept run

# Run specific suite
vendor/bin/codecept run unit

# Run with coverage
vendor/bin/codecept run --coverage

# PHPStan
vendor/bin/phpstan analyse src/

# GrumPHP
vendor/bin/grumphp run
```

## Testing Best Practices

1. Write unit tests first (TDD)
2. Use data providers
3. Mock external dependencies
4. Test edge cases
5. Name tests descriptively
6. Keep tests fast
7. Test behavior, not implementation
8. Use fixtures
9. Mock interfaces
10. Clean up after tests

## CI/CD Integration

```yaml
# .github/workflows/tests.yml
- name: Run PHPStan
  run: vendor/bin/phpstan analyse src/
- name: Run tests
  run: vendor/bin/codecept run
```
