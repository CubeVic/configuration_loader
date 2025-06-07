# Sources API Reference

This document provides detailed information about the configuration sources API.

## Built-in Sources

### FileSource

Loads configuration from a file.

```python
class FileSource(ConfigSource):
    def __init__(
        self,
        file_name: str,
        parser: Optional[ConfigParser] = None
    ):
        """
        Initialize the FileSource.

        Args:
            file_name: Name of the configuration file
            parser: Parser to use for the file (optional)
        """
```

### EnvironmentSource

Loads configuration from environment variables.

```python
class EnvironmentSource(ConfigSource):
    def __init__(
        self,
        prefix: Optional[str] = None,
        separator: str = "_"
    ):
        """
        Initialize the EnvironmentSource.

        Args:
            prefix: Prefix for environment variables
            separator: Separator for nested keys
        """
```

### CLISource

Loads configuration from command-line arguments.

```python
class CLISource(ConfigSource):
    def __init__(
        self,
        args: Optional[List[str]] = None,
        prefix: str = "--"
    ):
        """
        Initialize the CLISource.

        Args:
            args: Command-line arguments (optional)
            prefix: Prefix for configuration arguments
        """
```

## Custom Sources

### Creating a Custom Source

To create a custom source, implement the `ConfigSource` interface:

```python
from configloader import ConfigSource
from typing import Dict, Any

class CustomSource(ConfigSource):
    def __init__(self, some_param: str):
        self.some_param = some_param

    def load(self) -> Dict[str, Any]:
        # Implement your configuration loading logic here
        return {
            "custom_key": "custom_value",
            "param": self.some_param
        }

    def get_source_name(self) -> str:
        return "custom_source"
```

### Source Interface

The `ConfigSource` interface requires two methods:

#### load

```python
def load(self) -> Dict[str, Any]:
    """
    Load configuration from the source.

    Returns:
        The loaded configuration as a dictionary

    Raises:
        ConfigError: If there is an error loading the configuration
    """
```

#### get_source_name

```python
def get_source_name(self) -> str:
    """
    Get the name of the configuration source.

    Returns:
        The name of the configuration source
    """
```

## Source Priority

Sources are loaded in the following order:

1. Environment variables
2. Custom sources (in order)
3. Configuration file

Example:

```python
from configloader import ConfigLoader

loader = ConfigLoader(
    config_file_name="config.yaml",
    env_prefix="APP_",
    custom_sources=[
        DatabaseSource("config.db", "settings"),
        APISource("https://api.example.com/config", "your-api-key")
    ]
)
config = loader.load_config()
```

## Error Handling

Handle errors in your sources:

```python
from configloader import ConfigSource, ConfigError
from typing import Dict, Any

class CustomSource(ConfigSource):
    def load(self) -> Dict[str, Any]:
        try:
            # Your loading logic here
            return {"key": "value"}
        except Exception as e:
            raise ConfigError(f"Failed to load from custom source: {e}")

    def get_source_name(self) -> str:
        return "custom_source"
```

## Examples

### File Source

```python
from configloader import ConfigLoader, FileSource

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[FileSource("override.yaml")]
)
config = loader.load_config()
```

### Environment Source

```python
from configloader import ConfigLoader, EnvironmentSource

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[EnvironmentSource(prefix="APP_")]
)
config = loader.load_config()
```

### CLI Source

```python
from configloader import ConfigLoader, CLISource
import sys

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[CLISource(args=sys.argv[1:])]
)
config = loader.load_config()
```

### Multiple Sources

```python
from configloader import ConfigLoader, FileSource, EnvironmentSource, CLISource
import sys

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[
        FileSource("override.yaml"),
        EnvironmentSource(prefix="APP_"),
        CLISource(args=sys.argv[1:])
    ]
)
config = loader.load_config()
```

## Related Documentation

- [Basic Usage](../usage/basic.md)
- [Advanced Usage](../usage/advanced.md)
- [Custom Sources](../usage/custom_sources.md)
- [ConfigLoader API](configloader.md)
