# ConfigLoader API Reference

This document provides detailed information about the ConfigLoader API.

## ConfigLoader

The main class for loading and managing configuration.

### Class Definition

```python
class ConfigLoader:
    def __init__(
        self,
        config_file_path: Optional[str] = None,
        config_file_name: str = "config.toml",
        cli_args: Optional[argparse.Namespace] = None,
        env_prefix: Optional[str] = None,
        config_model: Optional[Type[BaseModel]] = None,
        custom_sources: Optional[Sequence[ConfigSource]] = None
    ):
        """
        Initialize the configuration loader.

        Args:
            config_file_path: Optional path to the configuration file
            config_file_name: Name of the configuration file (default: "config.toml")
            cli_args: Optional CLI arguments
            env_prefix: Optional prefix for environment variables
            config_model: Optional Pydantic model for configuration validation
            custom_sources: Optional sequence of custom configuration sources

        Raises:
            ConfigFileError: If the configuration file cannot be found or accessed
        """
```

### Methods

#### load_config

```python
def load_config(self) -> Dict[str, Any]:
    """
    Load and return the configuration.

    This method implements a simple singleton pattern - it loads the configuration
    only once and returns the cached version on subsequent calls.

    Returns:
        Dict[str, Any]: The merged configuration from all sources

    Raises:
        ConfigSourceError: If a source fails to load
        ConfigValidationError: If validation fails
        ConfigMergeError: If configurations cannot be merged
    """
```

### Instance Attributes

#### config_file_path

```python
config_file_path: Path
"""
Path to the configuration file. Set during initialization.
"""
```

#### config_model

```python
config_model: Optional[Type[BaseModel]]
"""
Optional Pydantic model for configuration validation.
"""
```

#### sources

```python
sources: List[ConfigSource]
"""
List of configuration sources used by the loader.
"""
```

#### _config

```python
_config: Optional[Dict[str, Any]]
"""
Cached configuration. Set to None initially and populated on first load_config() call.
"""
```

### Private Methods

#### _get_file

```python
@staticmethod
def _get_file(config_file_path: Optional[str], config_file_name: str) -> Path:
    """
    Get the configuration file path.

    Args:
        config_file_path: Optional path to the configuration file
        config_file_name: Name of the configuration file

    Returns:
        Path: Path to the configuration file

    Raises:
        ConfigFileError: If the configuration file cannot be found or accessed
    """
```

#### _get_sources

```python
def _get_sources(
    self,
    env_prefix: Optional[str],
    cli_args: Optional[argparse.Namespace],
    custom_sources: Optional[Sequence[ConfigSource]]
) -> List[ConfigSource]:
    """
    Get the sources for the configuration loader.

    Args:
        env_prefix: Optional prefix for environment variables
        cli_args: Optional CLI arguments
        custom_sources: Optional sequence of custom configuration sources

    Returns:
        List[ConfigSource]: List of configuration sources
    """
```

#### _get_parser

```python
def _get_parser(self) -> Any:
    """
    Get the appropriate parser for the configuration file.

    Returns:
        Any: The appropriate parser for the file format

    Raises:
        ConfigParserError: If the file format is not supported
    """
```

#### _load_and_merge_configs

```python
def _load_and_merge_configs(self) -> Dict[str, Any]:
    """
    Load and merge configurations from all sources.

    Returns:
        Dict[str, Any]: The merged configuration

    Raises:
        ConfigSourceError: If a source fails to load
        ConfigMergeError: If configurations cannot be merged
    """
```

#### _validate_config

```python
def _validate_config(self, config: Dict[str, Any]) -> None:
    """
    Validate the configuration against the provided Pydantic model.

    Args:
        config: The configuration to validate

    Raises:
        ConfigValidationError: If validation fails
    """
```

## ConfigSource

Interface for custom configuration sources.

### Class Definition

```python
class ConfigSource(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from the source.
        
        Returns:
            Dictionary containing the configuration
        """
        pass
```

## Exceptions

### ConfigLoaderError

Base exception for all ConfigLoader errors.

```python
class ConfigLoaderError(Exception):
    """Base exception for all ConfigLoader errors."""
    pass
```

### ConfigValidationError

Exception for configuration validation errors.

```python
class ConfigValidationError(ConfigLoaderError):
    """Raised when configuration validation fails."""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.errors = errors or {}
```

### ConfigSourceError

Exception for configuration source errors.

```python
class ConfigSourceError(ConfigLoaderError):
    """Raised when a configuration source fails to load."""
    pass
```

### ConfigFileError

Exception for configuration file errors.

```python
class ConfigFileError(ConfigSourceError):
    """Raised when a configuration file cannot be loaded."""
    pass
```

### ConfigParserError

Exception for configuration parser errors.

```python
class ConfigParserError(ConfigLoaderError):
    """Raised when a configuration file cannot be parsed."""
    pass
```

### ConfigMergeError

Exception for configuration merge errors.

```python
class ConfigMergeError(ConfigLoaderError):
    """Raised when configuration sources cannot be merged."""
    pass
```

## Usage Examples

### Basic Usage

```python
from configloader import ConfigLoader

loader = ConfigLoader(config_file_path="config.yaml")
config = loader.load_config()
```

### With Pydantic Model

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
```

### With Environment Variables

```python
from configloader import ConfigLoader

loader = ConfigLoader(
    config_file_path="config.yaml",
    env_prefix="APP_"
)
config = loader.load_config()
```

### With Custom Sources

```python
from configloader import ConfigLoader, ConfigSource
from typing import Dict, Any

class CustomSource(ConfigSource):
    def load(self) -> Dict[str, Any]:
        return {"key": "value"}

loader = ConfigLoader(
    config_file_path="config.yaml",
    custom_sources=[CustomSource()]
)
config = loader.load_config()
```

## Related Documentation

- [Basic Usage](../usage/basic.md)
- [Advanced Usage](../usage/advanced.md)
- [Custom Sources](../usage/custom_sources.md)
