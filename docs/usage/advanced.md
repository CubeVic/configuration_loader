# Advanced Usage

This guide covers advanced usage scenarios of ConfigLoader.

## Complex Configuration Models

You can create complex Pydantic models for your configuration:

```python
from configloader import ConfigLoader
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Optional

class DatabaseConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    ssl: bool = False

class EmailConfig(BaseModel):
    smtp_server: str
    port: int
    username: EmailStr
    password: str
    use_tls: bool = True

class Config(BaseModel):
    name: str
    version: str
    debug: bool = False
    database: DatabaseConfig
    email: Optional[EmailConfig] = None
    allowed_hosts: List[str] = ["localhost"]

loader = ConfigLoader(
    config_file_path="config.yaml",
    config_model=Config
)
config = loader.load_config()
```

## Custom Validation

Add custom validation to your configuration models:

```python
from configloader import ConfigLoader
from pydantic import BaseModel, validator
from typing import List

class Config(BaseModel):
    name: str
    version: str
    ports: List[int]

    @validator("ports")
    def validate_ports(cls, v):
        if not all(1024 <= port <= 65535 for port in v):
            raise ValueError("Ports must be between 1024 and 65535")
        return v

loader = ConfigLoader(
    config_file_path="config.yaml",
    config_model=Config
)
config = loader.load_config()
```

## Nested Configuration

Handle nested configuration structures:

```python
from configloader import ConfigLoader
from pydantic import BaseModel
from typing import Dict

class ServiceConfig(BaseModel):
    host: str
    port: int
    timeout: int = 30

class Config(BaseModel):
    services: Dict[str, ServiceConfig]

loader = ConfigLoader(
    config_file_path="config.yaml",
    config_model=Config
)
config = loader.load_config()

# Access nested configuration
db_config = config.services["database"]
api_config = config.services["api"]
```

## Environment Variable Mapping

Environment variables are mapped using a prefix-based approach. The prefix is removed and the remaining part is converted to lowercase:

```python
from configloader import ConfigLoader
from pydantic import BaseModel

class Config(BaseModel):
    database_url: str
    api_key: str

loader = ConfigLoader(
    config_file_path="config.yaml",
    env_prefix="APP_",
    config_model=Config
)
config = loader.load_config()

# Environment variables will be mapped as:
# APP_DATABASE_URL -> database_url
# APP_API_KEY -> api_key
```

For example:
- `APP_DATABASE_URL` becomes `database_url`
- `APP_API_KEY` becomes `api_key`

## Configuration Inheritance

Create base configuration classes and extend them:

```python
from configloader import ConfigLoader
from pydantic import BaseModel

class BaseConfig(BaseModel):
    name: str
    version: str
    debug: bool = False

class DevelopmentConfig(BaseConfig):
    database_url: str = "sqlite:///dev.db"
    log_level: str = "DEBUG"

class ProductionConfig(BaseConfig):
    database_url: str
    log_level: str = "INFO"

# Use different config models based on environment
env = "development"
config_model = DevelopmentConfig if env == "development" else ProductionConfig

loader = ConfigLoader(
    config_file_path="config.yaml",
    config_model=config_model
)
config = loader.load_config()
```

## Configuration Caching

ConfigLoader implements a simple singleton-like caching mechanism. The configuration is cached per instance:

```python
from configloader import ConfigLoader

# First instance - loads and caches
loader1 = ConfigLoader(config_file_path="config.yaml")
config1 = loader1.load_config()  # Loads and caches
config2 = loader1.load_config()  # Returns cached config

# New instance - fresh load
loader2 = ConfigLoader(config_file_path="config.yaml")
config3 = loader2.load_config()  # Fresh load
```

To get a fresh configuration, create a new instance of ConfigLoader.

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
    loader = ConfigLoader(config_file_path="config.yaml")
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

- Learn how to create [Custom Sources](custom_sources.md)
- Check the [API Reference](../api/configloader.md) for detailed information
- See [Basic Usage](basic.md) for simpler scenarios
