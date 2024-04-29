# Package: guardrails

The `guardrails` package provides utilities for managing configuration files and settings related to guardrails.

## Structure

- `__init__.py`: Initialization script for the package.
- `config`: Module containing configuration-related utilities.
  - `rails`: Submodule for managing guardrails configurations.
- `configs`: Directory containing configuration files.
  - `__init__.py`: Initialization script for the `configs` module.
  - `config.py`: Module for loading and accessing configuration settings.
  - `files`: Directory containing actual configuration files.
    - `config.yaml`: YAML configuration file.
    - `prompts.co`: Configuration file for prompts.

## Modules

### `config`

The `config` module provides utilities for loading and accessing configuration settings.

#### Classes and Functions

- `load_config()`: Function to load configuration settings from file.
- `get_setting(setting_name)`: Function to retrieve a specific setting from the configuration.

### `rails`

The `rails` submodule provides functionality for managing guardrails configurations.

#### Classes and Functions

- `load_rails_config()`: Function to load guardrails configurations.
- `set_rails_config()`: Function to set guardrails configurations.

## Usage

```python
from guardrails.config import load_config

# Load configuration settings
config = load_config()
print(config)

from guardrails.configs import config

# Access specific settings
print(config.get_setting('setting_name'))
