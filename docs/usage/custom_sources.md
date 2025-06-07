# Custom Sources

This guide explains how to create and use custom configuration sources with ConfigLoader.

## Creating a Custom Source

To create a custom configuration source, you need to implement the `ConfigSource` interface:

```python
from configloader import ConfigLoader, ConfigSource
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

## Using a Custom Source

Add your custom source to the ConfigLoader:

```python
from configloader import ConfigLoader

# Create a custom source
custom_source = CustomSource(some_param="value")

# Add it to the loader
loader = ConfigLoader(
    config_file_path="config.yaml",
    custom_sources=[custom_source]
)

# Load configuration
config = loader.load_config()
```

## Example: Database Configuration Source

Here's an example of a custom source that loads configuration from a database:

```python
from configloader import ConfigLoader, ConfigSource
from typing import Dict, Any
import sqlite3

class DatabaseSource(ConfigSource):
    def __init__(self, db_path: str, table: str):
        self.db_path = db_path
        self.table = table

    def load(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT key, value FROM {self.table}")
            return dict(cursor.fetchall())

    def get_source_name(self) -> str:
        return "database"

# Usage
db_source = DatabaseSource("config.db", "settings")
loader = ConfigLoader(
    config_file_path="config.yaml",
    custom_sources=[db_source]
)
config = loader.load_config()
```

## Example: API Configuration Source

Here's an example of a custom source that loads configuration from an API:

```python
from configloader import ConfigLoader, ConfigSource
from typing import Dict, Any
import requests

class APISource(ConfigSource):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def load(self) -> Dict[str, Any]:
        response = requests.get(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()

    def get_source_name(self) -> str:
        return "api"

# Usage
api_source = APISource(
    api_url="https://api.example.com/config",
    api_key="your-api-key"
)
loader = ConfigLoader(
    config_file_path="config.yaml",
    custom_sources=[api_source]
)
config = loader.load_config()
```

## Source Priority

Custom sources are loaded in the order they are provided, after environment variables but before the configuration file:

```python
from configloader import ConfigLoader

# Sources will be loaded in this order:
# 1. Environment variables
# 2. Custom sources (in order)
# 3. Configuration file
loader = ConfigLoader(
    config_file_path="config.yaml",
    env_prefix="APP_",
    custom_sources=[
        DatabaseSource("config.db", "settings"),
        APISource("https://api.example.com/config", "your-api-key")
    ]
)
config = loader.load_config()
```

## Error Handling

Handle errors in your custom sources:

```python
from configloader import ConfigLoader, ConfigSource, ConfigSourceError
from typing import Dict, Any

class CustomSource(ConfigSource):
    def load(self) -> Dict[str, Any]:
        try:
            # Your loading logic here
            return {"key": "value"}
        except Exception as e:
            raise ConfigSourceError(f"Failed to load from custom source: {e}")

    def get_source_name(self) -> str:
        return "custom_source"
```

## Next Steps

- Check the [API Reference](../api/configloader.md) for detailed information
- See [Basic Usage](basic.md) for simpler scenarios
- Learn about [Advanced Usage](advanced.md) for more complex scenarios
