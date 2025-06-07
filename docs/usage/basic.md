# Basic Usage

This guide covers the basic usage of ConfigLoader for common configuration scenarios.

## Loading Configuration from a File

The simplest way to use ConfigLoader is to load configuration from a file:

```python
from configloader import ConfigLoader

# Load from a YAML file
loader = ConfigLoader(config_file_path="config.yaml")
config = loader.load_config()

# Access configuration values
app_name = config["name"]
debug_mode = config["debug"]
```

## Environment Variables

ConfigLoader can load configuration from environment variables. The prefix is removed and the remaining part is converted to lowercase:

```python
from configloader import ConfigLoader

# Load from environment variables with prefix
loader = ConfigLoader(env_prefix="APP_")
config = loader.load_config()

# Environment variables will be loaded as:
# APP_NAME -> config["name"]
# APP_DEBUG -> config["debug"]
```

## Combining Sources

You can combine multiple configuration sources:

```python
from configloader import ConfigLoader

loader = ConfigLoader(
    config_file_path="config.yaml",
    env_prefix="APP_"
)
config = loader.load_config()

# Values will be loaded in this order:
# 1. Environment variables (highest priority)
# 2. Configuration file
```

## Basic Validation

You can use Pydantic for basic configuration validation:

```python
from configloader import ConfigLoader
from pydantic import BaseModel

class Config(BaseModel):
    name: str
    version: str
    debug: bool = False

loader = ConfigLoader(
    config_file_path="config.yaml",
    config_model=Config
)
config = loader.load_config()

# config will be an instance of Config
print(config.name)  # Access as attributes
print(config.version)
print(config.debug)
```

## Configuration File Examples

### YAML

```yaml
name: myapp
version: 1.0.0
debug: true
```

### JSON

```json
{
  "name": "myapp",
  "version": "1.0.0",
  "debug": true
}
```

### TOML (Default)

```toml
name = "myapp"
version = "1.0.0"
debug = true
```

## Error Handling

ConfigLoader provides specific exceptions for different error cases:

```python
from configloader import ConfigLoader
from configloader.exceptions import (
    ConfigValidationError,
    ConfigSourceError,
    ConfigFileError,
    ConfigParserError
)

try:
    loader = ConfigLoader(config_file_path="missing.yaml")
    config = loader.load_config()
except ConfigValidationError as e:
    print(f"Configuration validation failed: {e}")
except ConfigSourceError as e:
    print(f"Error loading from source: {e}")
except ConfigFileError as e:
    print(f"Error accessing config file: {e}")
except ConfigParserError as e:
    print(f"Error parsing config file: {e}")
```

## Next Steps

- Learn about [Advanced Usage](advanced.md) for more complex scenarios
- See how to create [Custom Sources](custom_sources.md)
- Check the [API Reference](../api/configloader.md) for detailed information
