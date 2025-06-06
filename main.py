import os
import argparse
from typing import Dict, Any
from pydantic import BaseModel
from configloader.core import ConfigLoader
from configloader.sources import ConfigSource


# Example 1: Basic Usage (Without Validation)
def basic_usage_example():
    """Example of basic configuration loading without validation."""
    print("\n=== Basic Usage Example (Without Validation) ===")

    # Set some environment variables
    os.environ["APP_NAME"] = "myapp"
    os.environ["APP_DEBUG"] = "true"

    # Create config loader without validation
    config_loader = ConfigLoader(
        config_file_name="config.yaml",
        env_prefix="APP_"
    )

    # Load configuration (returns raw dictionary)
    config = config_loader.load_config()
    print(f"Loaded configuration: {config}")


# Example 2: Advanced Usage (With Validation)
class DatabaseConfig(BaseModel):
    """Database configuration model."""
    host: str
    port: int
    user: str = "default"
    password: str = "default"


class AppConfig(BaseModel):
    """Application configuration model."""
    name: str
    version: str
    debug: bool = False
    database: DatabaseConfig


# Custom configuration source example
class CustomConfigSource(ConfigSource):
    """Example of a custom configuration source."""
    def load(self) -> Dict[str, Any]:
        return {
            "name": "custom_app",
            "version": "2.0.0",
            "debug": True,
            "database": {
                "host": "custom_host",
                "port": 5433,
                "user": "custom_user"
            }
        }


def advanced_usage_example():
    """Example of advanced configuration loading with validation."""
    print("\n=== Advanced Usage Example (With Validation) ===")

    # Set environment variables
    os.environ["MYAPP_DATABASE_HOST"] = "localhost"
    os.environ["MYAPP_DATABASE_PORT"] = "5432"

    # Parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()

    # Create config loader with validation
    config_loader = ConfigLoader(
        config_file_name="config.yaml",
        env_prefix="MYAPP_",
        cli_args=args,
        config_model=AppConfig,
        custom_sources=[CustomConfigSource()]
    )

    try:
        # Load and validate configuration
        config = config_loader.load_config()
        print(f"Validated configuration: {config}")

        # Access validated configuration
        print("\nAccessing validated configuration:")
        print(f"App name: {config['name']}")
        print(f"Database host: {config['database']['host']}")
        print(f"Database port: {config['database']['port']}")

    except Exception as e:
        print(f"Configuration validation failed: {e}")


# Example 3: Error Handling
def error_handling_example():
    """Example of handling configuration errors."""
    print("\n=== Error Handling Example ===")

    # Create an invalid configuration
    class StrictConfig(BaseModel):
        """Strict configuration model that will fail validation."""
        required_field: str
        number: int

    try:
        # This will fail because required_field is missing
        config_loader = ConfigLoader(
            config_file_name="config.yaml",
            config_model=StrictConfig
        )
        config = config_loader.load_config()
        print(f"Unexpected success with invalid config: {config}")
    except Exception as e:
        print(f"Expected validation error: {e}")


if __name__ == "__main__":
    # Run all examples
    basic_usage_example()
    advanced_usage_example()
    error_handling_example()
