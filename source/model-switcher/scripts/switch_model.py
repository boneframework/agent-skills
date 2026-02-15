#!/usr/bin/env python3
"""
Model Switcher Script for Agent Zero
Switches chat, utility, or browser models by reading from model_settings.json
and updating /a0/usr/settings.json
"""

import json
import sys
import os
from pathlib import Path

def load_json(filepath):
    """Load and parse a JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)

def save_json(filepath, data):
    """Save data to JSON file with pretty formatting"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error: Failed to save {filepath}: {e}")
        return False

def find_model(model_settings, model_name):
    """Find a model configuration by name"""
    for model in model_settings:
        if model.get('name') == model_name:
            return model
    return None

def update_model_settings(settings, model_config, model_type):
    """Update settings.json with new model configuration"""
    prefix = f"{model_type}_model"

    # Map model_settings fields to settings.json fields
    settings[f"{prefix}_name"] = model_config.get('name', '')
    settings[f"{prefix}_provider"] = model_config.get('provider', '')
    settings[f"{prefix}_api_base"] = model_config.get('base_url', '')
    settings[f"{prefix}_ctx_length"] = model_config.get('context_length', 32768)
    settings[f"{prefix}_rl_input"] = model_config.get('input_rate_limit', 0)
    settings[f"{prefix}_rl_output"] = model_config.get('output_rate_limit', 0)

    # Handle additional_parameters -> kwargs
    if 'additional_parameters' in model_config:
        settings[f"{prefix}_kwargs"] = model_config['additional_parameters']

    return settings

def list_available_models(model_settings):
    """List all available models"""
    print("\nAvailable models:")
    print("-" * 60)
    for model in model_settings:
        name = model.get('name', 'Unknown')
        provider = model.get('provider', 'Unknown')
        ctx = model.get('context_length', 'Unknown')
        print(f"  • {name:30} ({provider}, {ctx:,} ctx)")
    print("-" * 60)

def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python switch_model.py <model_type> [model_name]")
        print("\nModel types: chat, util, browser")
        print("\nExamples:")
        print("  python switch_model.py list")
        print("  python switch_model.py chat qwen2.5:7b-q4_K_M")
        print("  python switch_model.py util mistral:7b-q4_K_M")
        print("  python switch_model.py browser claude-sonnet-4-5")
        sys.exit(1)

    # Paths
    project_dir = Path('/a0/usr/projects/agent-skills')
    model_settings_path = project_dir / 'model_settings.json'
    settings_path = Path('/a0/usr/settings.json')

    # Load model settings
    model_settings = load_json(model_settings_path)

    # Handle 'list' command
    if sys.argv[1].lower() == 'list':
        list_available_models(model_settings)
        sys.exit(0)

    # Validate model type
    model_type = sys.argv[1].lower()
    valid_types = ['chat', 'util', 'browser']
    if model_type not in valid_types:
        print(f"Error: Invalid model type '{model_type}'")
        print(f"Valid types: {', '.join(valid_types)}")
        sys.exit(1)

    # Get model name
    if len(sys.argv) < 3:
        print(f"Error: Please specify a model name")
        list_available_models(model_settings)
        sys.exit(1)

    model_name = sys.argv[2]

    # Find model configuration
    model_config = find_model(model_settings, model_name)
    if not model_config:
        print(f"Error: Model '{model_name}' not found in model_settings.json")
        list_available_models(model_settings)
        sys.exit(1)

    # Load current settings
    settings = load_json(settings_path)

    # Update settings
    print(f"\nSwitching {model_type} model to: {model_name}")
    print(f"Provider: {model_config.get('provider')}")
    print(f"Context length: {model_config.get('context_length'):,}")

    settings = update_model_settings(settings, model_config, model_type)

    # Save updated settings
    if save_json(settings_path, settings):
        print(f"\n✅ Successfully switched {model_type} model to {model_name}")
        print(f"\n⚠️  Note: You may need to restart Agent Zero for changes to take effect.")
    else:
        print(f"\n❌ Failed to update settings.json")
        sys.exit(1)

if __name__ == '__main__':
    main()
