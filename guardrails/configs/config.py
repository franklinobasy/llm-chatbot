"""
Module: guardrails/configs/config.py

The `config.py` module provides functionality for loading and accessing configuration settings for guardrails.

Classes and Functions:
    - load_config(): Function to load guardrails configuration settings.
    - guardrail_app: Instance of LLMRails initialized with the loaded configuration settings.

Usage:
    from guardrails.configs import config

    # Load guardrails configuration settings
    config.load_config()

    # Access guardrails application instance
    guardrail_app = config.guardrail_app
"""

import os
from nemoguardrails import LLMRails, RailsConfig

# Load YAML and COlang content from files
with open(os.path.join(os.getcwd(), "guardrails", "configs", "files", "config.yaml")) as f:
    yaml_content = f.read()

with open(os.path.join(os.getcwd(), "guardrails", "configs", "files", "prompts.co")) as f:
    colang_content = f.read()

# Initialize RailsConfig instance with YAML and COlang content
config = RailsConfig.from_content(
    yaml_content=yaml_content,
    colang_content=colang_content
)

# Initialize LLMRails instance with the loaded configuration
guardrail_app = LLMRails(config=config)
