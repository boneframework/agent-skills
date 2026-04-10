# Agent Skills Project

## Project Overview

This is a knowledge repository for AI coding agents, specifically designed to provide expert-level expertise about the Bone Framework and related technologies. The project contains "skills" - modular documentation packages that teach AI agents how to work with specific frameworks, tools, and best practices.

**Key technologies:**
- Node.js (for tooling scripts)
- Markdown-based skill documentation
- Bone Framework (PHP) and related packages
- Docker LAMP stack for development

**Project type:** Documentation/Knowledge repository for AI agents

**Repository:** https://github.com/boneframework/agent-skills

## Directory Structure

```
agent-skills/
├── source/                  # Main skill modules
│   ├── address/            # Address-related skills
│   ├── barnacle/           # Barnacle (WordPress) skills
│   ├── bf-lamp/            # Docker LAMP stack management skill
│   ├── bone/               # Bone Framework core skills
│   ├── bone-doctrine/      # Doctrine ORM skills
│   ├── bone-oauth2/        # OAuth2 integration skills
│   ├── bone-open-api/      # OpenAPI/Swagger skills
│   ├── bone-passport/      # Passport authentication skills
│   ├── bone-push-notifications/  # Push notification skills
│   ├── bone-settings/      # Settings management skills
│   ├── bone-skeleton/      # Skeleton project skills
│   ├── bone-user/          # User management skills
│   ├── bone-user-api/      # User API skills
│   ├── console/            # Console command skills
│   ├── contracts/          # Contract definitions
│   ├── controller/         # Controller skills
│   ├── country/            # Country data skills
│   ├── db/                 # Database skills
│   ├── dev-tools/          # Development tools skills
│   ├── firewall/           # Firewall/security skills
│   ├── http/               # HTTP-related skills
│   ├── i18n/               # Internationalization skills
│   ├── icon/               # Icon handling skills
│   ├── image/              # Image processing skills
│   ├── js-pro/             # JavaScript advanced skills
│   ├── log/                # Logging skills
│   ├── model-switcher/     # Model switching skills
│   ├── person/             # Person entity skills
│   ├── php-pro/            # PHP advanced skills
│   ├── router/             # Routing skills
│   ├── server/             # Server management skills
│   ├── session/            # Session management skills
│   ├── skeleton/           # Skeleton project skills
│   ├── user/               # User-related skills
│   └── view/               # View/template skills
├── shared/
│   ├── references/         # Reference data (WordPress versions, etc.)
│   └── scripts/            # Development scripts
│       ├── ai-generate-updates.mjs
│       ├── scaffold-skill.mjs      # Create new skill templates
│       ├── skillpack-build.mjs
│       ├── skillpack-install.mjs
│       └── update-upstream-indices.mjs
├── model_settings.json     # AI model configuration (Ollama, Anthropic, Google)
├── package.json
├── README.md
└── .gitignore
```

## Skills Architecture

Each skill is contained in its own directory under `source/` with a `SKILL.md` file that follows a specific format:

```markdown
---
name: skill-name
description: Brief description of what the skill teaches
author: Author name
version: "1.0"
compatibility: Requirements/dependencies
---

# Skill Name

## When to Use
Conditions under which this skill should be invoked.

## Prerequisites
What must be installed or set up before using this skill.

## Step-by-Step Workflows
Detailed procedures for common tasks.

## Verification
How to confirm the task was completed successfully.
```

## Building and Running

### Development Scripts

The project uses Node.js scripts for maintenance tasks. Run them with:

```bash
node shared/scripts/<script-name>.mjs [arguments]
```

**Available scripts:**

| Script | Purpose |
|--------|---------|
| `scaffold-skill.mjs` | Create a new skill template |
| `skillpack-build.mjs` | Build skill packages |
| `skillpack-install.mjs` | Install skill packages |
| `ai-generate-updates.mjs` | Generate AI-related updates |
| `update-upstream-indices.mjs` | Update reference data indices |

**Example - Create a new skill:**
```bash
node shared/scripts/scaffold-skill.mjs "my-skill" "Description of what this skill does"
```

The script validates skill names (lowercase, hyphen-separated, no consecutive hyphens, max 64 chars) and creates:
- `skills/<skill-name>/SKILL.md` - The skill documentation template
- `eval/scenarios/<skill-name>.md` - Test scenario template

### Model Configuration

AI model settings are in `model_settings.json`. The project supports:
- **Ollama** local models (Qwen, Gemma, Phi3, Mistral, LLaMA3.1)
- **Anthropic** (Claude Sonnet)
- **Google** (Gemini Pro, Gemini Flash)

All local models are configured to use Ollama at `http://host.docker.internal:11434`.

## Development Conventions

### Skill Naming
- Must be lowercase letters and digits with hyphens
- Cannot start or end with a hyphen
- Cannot contain consecutive hyphens (`--`)
- Maximum 64 characters
- Examples: `bone-framework-core`, `bf-lamp`, `js-pro`

### Skill Content Structure
1. YAML frontmatter with metadata (name, description, author, version, compatibility)
2. Main heading matching the skill name
3. "When to Use" section - clear conditions for invocation
4. "Prerequisites" section - requirements and dependencies
5. "Step-by-Step Workflows" - detailed procedures
6. Additional sections as needed (Verification, Failure modes, etc.)

### Version Control
- The project uses Git for version control
- `.gitignore` excludes `node_modules/` and `pnpm-lock.yaml`
- `.a0proj` file present (likely a Bone Framework project marker)

## Key Skills Documentation

### bf-lamp Skill
Teaches AI agents how to operate within a Docker-based Bone Framework LAMP stack. Key points:
- Runs inside a container with access to sibling containers via Docker socket
- Must use `docker -H unix:///var/run/docker.sock exec [container] [command]` pattern
- Three main services: `lamp-php-1` (PHP/Composer), `lamp-node-1` (NPM), `lamp-mariadb-1` (MySQL)
- Shared volumes mean paths are consistent across containers

### Bone Framework Core Skill
Provides expert knowledge of the Bone Framework:
- Lightweight PHP framework using PSR standards
- Dependency injection, middleware, PSR-7/11/15
- Configuration via PHP arrays in `config/` directory
- Environment-specific configs via `APPLICATION_ENV`
- Related packages: bone-user, bone-doctrine, bone-oauth2

## Testing and Evaluation

The project includes an `eval/` directory with scenario files for testing skill performance. Each skill should have a corresponding scenario file that defines:
- Test prompts
- Expected behavior
- Verification criteria

## License

ISC
