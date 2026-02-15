---
name: "model-switcher"
description: "Switch between different AI models for chat, utility, or browser operations by reading from model_settings.json and updating Agent Zero settings. Use when user wants to change the active model for any of the three model types."
version: "1.0.0"
author: "Agent Zero User"
tags: ["configuration", "models", "settings", "llm"]
trigger_patterns:
  - "switch model"
  - "change model"
  - "use different model"
  - "switch to"
  - "change chat model"
  - "change utility model"
  - "change browser model"
  - "list models"
  - "available models"
---

# Model Switcher

This skill allows you to switch between different AI models for chat, utility, or browser operations in Agent Zero.

## When to Use

Activate this skill when the user wants to:
- Switch the chat model to a different LLM
- Change the utility model for background tasks
- Update the browser agent model
- List all available models
- See current model configuration

## How It Works

The skill reads model configurations from `/a0/usr/projects/agent-skills/model_settings.json` and updates the appropriate settings in `/a0/usr/settings.json`.

### Model Types

Agent Zero uses three types of models:

1. **Chat Model** - Main conversational model (you!)
2. **Utility Model** - Background tasks, memory operations, embeddings
3. **Browser Model** - Browser automation agent

### Available Models

The `model_settings.json` file contains configurations for:

**Small Models (4B parameters):**
- `qwen3:4b-q4_K_M` - Fast, efficient Qwen model
- `gemma3:4b-q4_K_M` - Google's Gemma with large context
- `phi3:3.8b-q4_K_M` - Microsoft's Phi-3

**Medium Models (7-8B parameters):**
- `mistral:7b-q4_K_M` - Mistral AI's efficient model
- `llama3.1:8b-q4_K_M` - Meta's Llama with large context
- `qwen2.5:7b-q4_K_M` - Latest Qwen with large context

**Cloud Models:**
- `claude-sonnet-4-5` - Anthropic's Claude (200K context)

## Usage Instructions

### Step 1: List Available Models

First, show the user what models are available:

```bash
python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py list
```

### Step 2: Switch a Model

Use the script with two arguments:
1. Model type: `chat`, `util`, or `browser`
2. Model name: exact name from model_settings.json

```bash
python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py <type> <model_name>
```

### Step 3: Inform User About Restart

After switching, remind the user that Agent Zero may need to be restarted for changes to take full effect.

## Examples

### Example 1: List Available Models

**User**: "What models are available?"

**Agent Action**:
```json
{
    "thoughts": [
        "User wants to see available models",
        "I'll use the model-switcher skill to list them"
    ],
    "headline": "Listing available AI models",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py list",
        "session": 0
    }
}
```

### Example 2: Switch Chat Model

**User**: "Switch the chat model to qwen2.5:7b-q4_K_M"

**Agent Action**:
```json
{
    "thoughts": [
        "User wants to switch the chat model",
        "I'll use the model-switcher skill with chat type and the specified model name"
    ],
    "headline": "Switching chat model to Qwen 2.5",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py chat qwen2.5:7b-q4_K_M",
        "session": 0
    }
}
```

**Agent Response**:
```markdown
✅ Successfully switched chat model to **qwen2.5:7b-q4_K_M**

**Model Details:**
- Provider: Ollama
- Context Length: 131,072 tokens
- Input Rate Limit: 6,000 tokens/min
- Output Rate Limit: 3,600 tokens/min

⚠️ **Note**: You may need to restart Agent Zero for the changes to take full effect.
```

### Example 3: Switch Utility Model

**User**: "Use mistral for utility tasks"

**Agent Action**:
```json
{
    "thoughts": [
        "User wants to switch the utility model to Mistral",
        "I'll use the model-switcher skill with util type"
    ],
    "headline": "Switching utility model to Mistral",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py util mistral:7b-q4_K_M",
        "session": 0
    }
}
```

### Example 4: Switch Browser Model

**User**: "Change the browser agent to use phi3"

**Agent Action**:
```json
{
    "thoughts": [
        "User wants to switch the browser model to Phi-3",
        "I'll use the model-switcher skill with browser type"
    ],
    "headline": "Switching browser model to Phi-3",
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "python /a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py browser phi3:3.8b-q4_K_M",
        "session": 0
    }
}
```

## Model Selection Guidelines

### When to Use Small Models (4B)
- Quick responses needed
- Simple tasks
- Limited resources
- High throughput required

### When to Use Medium Models (7-8B)
- Complex reasoning needed
- Better code generation
- More nuanced responses
- Balance of speed and quality

### When to Use Cloud Models
- Maximum quality needed
- Very large context required (200K tokens)
- Complex multi-step tasks
- When local resources are limited

## Important Notes

1. **Model Availability**: Ensure the model is pulled in Ollama before switching:
   ```bash
   ollama pull <model_name>
   ```

2. **Context Length**: Different models have different context windows:
   - Small models: typically 32K tokens
   - Medium models: up to 131K tokens
   - Cloud models: up to 200K tokens

3. **Performance**: Smaller models are faster but may be less capable for complex tasks

4. **Rate Limits**: Each model has different rate limits configured in model_settings.json

5. **Restart Required**: Changes take effect immediately for new conversations, but a full restart ensures all components use the new model

## Troubleshooting

### Model Not Found
If you get "Model not found" error:
1. Check the exact model name in model_settings.json
2. Ensure spelling matches exactly (case-sensitive)
3. Run `list` command to see available models

### Model Not Responding
If the model doesn't respond after switching:
1. Verify the model is pulled in Ollama: `ollama list`
2. Check Ollama is running: `ollama ps`
3. Restart Agent Zero

### Settings Not Updating
If settings don't seem to update:
1. Check file permissions on /a0/usr/settings.json
2. Verify model_settings.json is valid JSON
3. Look for error messages in the script output

## Script Location

The model switcher script is located at:
```
/a0/usr/projects/agent-skills/source/model-switcher/scripts/switch_model.py
```

## Configuration Files

**Model Definitions**: `/a0/usr/projects/agent-skills/model_settings.json`
**Agent Settings**: `/a0/usr/settings.json`
