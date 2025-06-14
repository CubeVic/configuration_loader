# ConfigLoader

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A flexible and extensible configuration loader for Python applications that supports multiple sources and formats. This package provides a simple way to load and manage configuration from various sources like files, environment variables, and CLI arguments.

## Features

- Multiple file format support (TOML, YAML, JSON)
- Environment variable configuration
- CLI argument integration
- Custom configuration sources
- Optional Pydantic validation support
- Smart caching mechanism
- Extensible architecture

## Installation

```bash
pip install configloader
```

Or using Poetry:

```bash
poetry add configloader
```

## Basic Usage

### Simple Configuration Loading (Without Validation)

```python
from configloader import ConfigLoader

# Load from default config.toml without validation
config_loader = ConfigLoader()
config = config_loader.load_config()  # Returns raw dictionary

# Load from specific file without validation
config_loader = ConfigLoader(config_file_name="config.yaml")
config = config_loader.load_config()  # Returns raw dictionary
```

### With Environment Variables (Without Validation)

```python
import os
from configloader import ConfigLoader

# Set environment variables
os.environ["MYAPP_DATABASE_HOST"] = "localhost"
os.environ["MYAPP_DATABASE_PORT"] = "5432"

# Load configuration with environment variables (no validation)
config_loader = ConfigLoader(
    config_file_name="config.yaml",
    env_prefix="MYAPP_"
)
config = config_loader.load_config()  # Returns raw dictionary
```

### With CLI Arguments (Without Validation)

```python
import argparse
from configloader import ConfigLoader

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str)
parser.add_argument('--port', type=int)
args = parser.parse_args()

# Load configuration with CLI arguments (no validation)
config_loader = ConfigLoader(
    config_file_name="config.yaml",
    cli_args=args
)
config = config_loader.load_config()  # Returns raw dictionary
```

## Advanced Usage

### Custom Configuration Sources (Without Validation)

You can create custom configuration sources by implementing the `ConfigSource` interface:

```python
from configloader.sources import ConfigSource
from typing import Dict, Any

class DatabaseConfigSource(ConfigSource):
    def load(self) -> Dict[str, Any]:
        # Load configuration from a database
        return {
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }

# Use custom source without validation
config_loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[DatabaseConfigSource()]
)
config = config_loader.load_config()  # Returns raw dictionary
```

### Optional Configuration Validation

You can optionally use Pydantic models to validate your configuration. This is useful when you want to ensure your configuration matches a specific schema:

```python
from pydantic import BaseModel
from configloader import ConfigLoader
from configloader.exceptions import ConfigValidationError

# Define your configuration schema
class AppConfig(BaseModel):
    name: str
    version: str
    debug: bool = False
    database: dict = {
        "host": "localhost",
        "port": 5432
    }

# Load with validation
config_loader = ConfigLoader(
    config_file_name="config.yaml",
    config_model=AppConfig  # Optional: Add validation
)

# If validation fails, it will raise a ConfigValidationError
try:
    config = config_loader.load_config()
except ConfigValidationError as e:
    print(f"Configuration validation failed: {e}")
```

## Configuration File Examples

### TOML Configuration (Default)

```toml
[app]
name = "myapp"
version = "1.0.0"
debug = true

[database]
host = "localhost"
port = 5432
```

### YAML Configuration

```yaml
app:
  name: myapp
  version: 1.0.0
  debug: true

database:
  host: localhost
  port: 5432
```

## CLI

The CLI helps you:

- Verify the configuration before running the app.
- Debug configuration issues
- Validate against your models
- Convert between formats
- Check environment variable overrides
