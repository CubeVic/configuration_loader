# Parsers API Reference

This document provides detailed information about the configuration parsers API.

## Built-in Parsers

### YAMLParser

Parser for YAML configuration files.

```python
class YAMLParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse YAML content.

        Args:
            content: YAML content to parse

        Returns:
            Parsed configuration as a dictionary

        Raises:
            ConfigError: If there is an error parsing the YAML
        """
```

### JSONParser

Parser for JSON configuration files.

```python
class JSONParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse JSON content.

        Args:
            content: JSON content to parse

        Returns:
            Parsed configuration as a dictionary

        Raises:
            ConfigError: If there is an error parsing the JSON
        """
```

### TOMLParser

Parser for TOML configuration files.

```python
class TOMLParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse TOML content.

        Args:
            content: TOML content to parse

        Returns:
            Parsed configuration as a dictionary

        Raises:
            ConfigError: If there is an error parsing the TOML
        """
```

## Custom Parsers

### Creating a Custom Parser

To create a custom parser, implement the `ConfigParser` interface:

```python
from configloader import ConfigParser
from typing import Dict, Any

class CustomParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        # Implement your parsing logic here
        return {
            "key": "value"
        }
```

### Parser Interface

The `ConfigParser` interface requires one method:

#### parse

```python
def parse(self, content: str) -> Dict[str, Any]:
    """
    Parse configuration content.

    Args:
        content: Content to parse

    Returns:
        Parsed configuration as a dictionary

    Raises:
        ConfigError: If there is an error parsing the content
    """
```

## Using Parsers

### With FileSource

```python
from configloader import ConfigLoader, FileSource, YAMLParser

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[FileSource("override.yaml", parser=YAMLParser())]
)
config = loader.load_config()
```

### With Custom Parser

```python
from configloader import ConfigLoader, FileSource, ConfigParser
from typing import Dict, Any

class CustomParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        # Your parsing logic here
        return {"key": "value"}

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[FileSource("custom.txt", parser=CustomParser())]
)
config = loader.load_config()
```

## Error Handling

Handle errors in your parsers:

```python
from configloader import ConfigParser, ConfigError
from typing import Dict, Any

class CustomParser(ConfigParser):
    def parse(self, content: str) -> Dict[str, Any]:
        try:
            # Your parsing logic here
            return {"key": "value"}
        except Exception as e:
            raise ConfigError(f"Failed to parse content: {e}")
```

## Examples

### YAML Parser

```python
from configloader import ConfigLoader, FileSource, YAMLParser

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[FileSource("override.yaml", parser=YAMLParser())]
)
config = loader.load_config()
```

### JSON Parser

```python
from configloader import ConfigLoader, FileSource, JSONParser

loader = ConfigLoader(
    config_file_name="config.json",
    custom_sources=[FileSource("override.json", parser=JSONParser())]
)
config = loader.load_config()
```

### TOML Parser

```python
from configloader import ConfigLoader, FileSource, TOMLParser

loader = ConfigLoader(
    config_file_name="config.toml",
    custom_sources=[FileSource("override.toml", parser=TOMLParser())]
)
config = loader.load_config()
```

### Multiple Parsers

```python
from configloader import ConfigLoader, FileSource, YAMLParser, JSONParser

loader = ConfigLoader(
    config_file_name="config.yaml",
    custom_sources=[
        FileSource("override.yaml", parser=YAMLParser()),
        FileSource("override.json", parser=JSONParser())
    ]
)
config = loader.load_config()
```

## Related Documentation

- [Basic Usage](../usage/basic.md)
- [Advanced Usage](../usage/advanced.md)
- [Custom Sources](../usage/custom_sources.md)
- [ConfigLoader API](configloader.md)
- [Sources API](sources.md)
