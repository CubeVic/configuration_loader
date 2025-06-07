# ConfigLoader

A flexible and extensible configuration loader for Python applications with support for multiple formats and sources.

## Features

- Multiple configuration formats (YAML, JSON, TOML)
- Environment variable support
- CLI argument integration
- Custom configuration sources
- Pydantic validation
- Caching mechanism
- Extensible architecture

## Quick Start

```python
from configloader import ConfigLoader

# Basic usage
loader = ConfigLoader(config_file_name="config.yaml")
config = loader.load_config()

# With environment variables
loader = ConfigLoader(
    config_file_name="config.yaml",
    env_prefix="APP_"
)

# With validation
from pydantic import BaseModel

class Config(BaseModel):
    name: str
    version: str
    debug: bool = False

loader = ConfigLoader(
    config_file_name="config.yaml",
    config_model=Config
)
```

## Installation

```bash
pip install configloader
```

## Why ConfigLoader?

ConfigLoader provides a simple yet powerful way to manage configuration in your Python applications:

- **Multiple Sources**: Load configuration from files, environment variables, and CLI arguments
- **Format Support**: Work with YAML, JSON, and TOML files
- **Type Safety**: Validate your configuration using Pydantic models
- **Extensible**: Create custom configuration sources
- **Caching**: Efficient configuration loading with caching

## Example Configuration Files

### YAML

```yaml
name: myapp
version: 1.0.0
debug: true
database:
  host: localhost
  port: 5432
```

### JSON

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "debug": true,
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

### TOML

```toml
name = "myapp"
version = "1.0.0"
debug = true

[database]
host = "localhost"
port = 5432
```

## Documentation

- [Installation](installation.md)
- [Basic Usage](usage/basic.md)
- [Advanced Usage](usage/advanced.md)
- [Custom Sources](usage/custom_sources.md)
- [API Reference](api/configloader.md)
