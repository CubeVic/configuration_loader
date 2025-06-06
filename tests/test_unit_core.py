import json
from pathlib import Path
import tempfile
from hypothesis import given
import pytest
import toml
import yaml
from pydantic import BaseModel
from configloader.core import ConfigLoader
from configloader.sources import ConfigSource
from configloader.exceptions import (
    ConfigValidationError,
    ConfigSourceError,
    ConfigFileError,
    ConfigParserError,
    ConfigMergeError
)
from tests.conftest import config_strategy, config_strategy_with_sections


class TestConfig(BaseModel):
    """Test configuration model for validation."""
    name: str
    version: str
    debug: bool = False


class CustomTestSource(ConfigSource):
    """Custom configuration source for testing."""
    def load(self) -> dict:
        return {
            "name": "test_app",
            "version": "1.0.0",
            "debug": True
        }


class FailingSource(ConfigSource):
    """Source that always fails for testing error handling."""
    def load(self) -> dict:
        raise Exception("Source failed to load")


class MutableTestSource(ConfigSource):
    """Source with mutable configuration for testing cache invalidation."""
    def __init__(self):
        self.config = {
            "name": "mutable_app",
            "version": "1.0.0",
            "debug": True
        }

    def load(self) -> dict:
        return self.config.copy()

    def update_config(self, new_config: dict):
        """Update the configuration for testing cache invalidation."""
        self.config = new_config.copy()


@given(testing_data=config_strategy)
def test_load_yaml_config(testing_data):
    """
    Test the load_yaml_config function with a sample YAML configuration.
    """
    with tempfile.TemporaryDirectory() as tmpdirnamse:
        config_path = Path(tmpdirnamse) / "config.yaml"

        with open(config_path, "w") as f:
            yaml.dump(testing_data, f)

        config_loader = ConfigLoader(config_file_name=config_path)
        assert config_loader.config_file_path == config_path
        assert config_loader.config_file_path.suffix == ".yaml"
        assert config_loader.load_config() == testing_data


@given(testing_data=config_strategy)
def test_load_json_config(testing_data):
    """
    Test the load_json_config function with a sample JSON configuration.
    """
    with tempfile.TemporaryDirectory() as tmpdirnamse:
        config_path = Path(tmpdirnamse) / "config.json"

        with open(config_path, "w") as f:
            json.dump(testing_data, f)

        config_loader = ConfigLoader(config_file_name=config_path)
        assert config_loader.config_file_path == config_path
        assert config_loader.config_file_path.suffix == ".json"
        assert config_loader.load_config() == testing_data


@given(testing_data=config_strategy_with_sections)
def test_load_toml_config(testing_data):
    """
    Test the load_toml_config function with a sample TOML configuration.
    """
    with tempfile.TemporaryDirectory() as tmpdirnamse:
        config_path = Path(tmpdirnamse) / "config.toml"

        with open(config_path, "w") as f:
            toml.dump(testing_data, f)

        config_loader = ConfigLoader(config_file_name=config_path)
        assert config_loader.config_file_path == config_path
        assert config_loader.config_file_path.suffix == ".toml"
        assert config_loader.load_config() == testing_data


def test_custom_source():
    """
    Test loading configuration from a custom source.
    """
    config_loader = ConfigLoader(custom_sources=[CustomTestSource()], config_model=TestConfig)
    config = config_loader.load_config()

    assert config["name"] == "test_app"
    assert config["version"] == "1.0.0"
    assert config["debug"] is True


def test_config_validation():
    """
    Test configuration validation with Pydantic model.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        test_config = {
            "name": "test_app",
            "version": "1.0.0",
            "debug": True
        }

        with open(config_path, "w") as f:
            yaml.dump(test_config, f)

        # Test valid configuration
        config_loader = ConfigLoader(
            config_file_name=config_path,
            config_model=TestConfig
        )
        assert config_loader.load_config() == test_config

        # Test invalid configuration
        invalid_config = {
            "name": "test_app",
            # Missing required 'version' field
            "debug": True
        }

        with open(config_path, "w") as f:
            yaml.dump(invalid_config, f)

        try:
            ConfigLoader(
                config_file_name=config_path,
                config_model=TestConfig
            ).load_config()
            assert False, "Should have raised ConfigValidationError"
        except ConfigValidationError as e:
            assert isinstance(e, ConfigValidationError)
            assert "version" in str(e.errors)


def test_source_priority():
    """
    Test that configuration sources are merged in the correct priority order.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        file_config = {
            "name": "file_config",
            "version": "1.0.0"
        }

        with open(config_path, "w") as f:
            yaml.dump(file_config, f)

        custom_source = CustomTestSource()  # Will override file config

        config_loader = ConfigLoader(
            config_file_name=config_path,
            custom_sources=[custom_source],
            config_model=TestConfig
        )

        config = config_loader.load_config()
        assert config["name"] == "test_app"  # From custom source
        assert config["version"] == "1.0.0"  # From custom source
        assert config["debug"] is True  # From custom source


def test_error_handling():
    """
    Test error handling for various failure scenarios.
    """
    # Test file not found
    # try:
    #     ConfigLoader(config_file_name="nonexistent.yaml").load_config()
    #     assert False, "Should have raised ConfigFileError"
    # except ConfigFileError:
    #     pass

    with pytest.raises(ConfigSourceError):
        ConfigLoader(config_file_name="nonexistent.yaml").load_config()

    # Test unsupported file format
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.xyz"
        config_path.touch()
        with pytest.raises(ConfigFileError):
            ConfigLoader(config_file_name=config_path).load_config()

    # Test failing source
    with pytest.raises(ConfigSourceError):
        ConfigLoader(custom_sources=[FailingSource()]).load_config()



def test_caching_mechanism():
    """
    Test the caching mechanism of the ConfigLoader.
    """
    # Create a mutable source for testing
    mutable_source = MutableTestSource()

    # Create config loader with the mutable source
    config_loader = ConfigLoader(
        custom_sources=[mutable_source],
        config_model=TestConfig
    )
    
    # First load - should load from source
    config1 = config_loader.load_config()
    assert config1["name"] == "mutable_app"
    assert config1["version"] == "1.0.0"
    assert config1["debug"] is True
    
    # Second load - should return cached config
    config2 = config_loader.load_config()
    assert config2 == config1  # Should be the same object
    
    # Update source configuration
    mutable_source.update_config({
        "name": "updated_app",
        "version": "2.0.0",
        "debug": False
    })
    
    # Third load - should still return cached config
    config3 = config_loader.load_config()
    assert config3 == config1  # Should still be the same as first load
    
    # Create new loader to test fresh load
    new_loader = ConfigLoader(
        custom_sources=[mutable_source],
        config_model=TestConfig
    )
    
    # Load with new loader - should get updated config
    config4 = new_loader.load_config()
    assert config4["name"] == "updated_app"
    assert config4["version"] == "2.0.0"
    assert config4["debug"] is False


def test_cache_invalidation():
    """
    Test cache invalidation when configuration changes.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yaml"
        initial_config = {
            "name": "test_app",
            "version": "1.0.0",
            "debug": True
        }
        
        # Write initial config
        with open(config_path, "w") as f:
            yaml.dump(initial_config, f)
        
        # Create loader
        config_loader = ConfigLoader(
            config_file_name=config_path,
            config_model=TestConfig
        )
        
        # First load
        config1 = config_loader.load_config()
        assert config1 == initial_config
        
        # Update config file
        updated_config = {
            "name": "updated_app",
            "version": "2.0.0",
            "debug": False
        }
        with open(config_path, "w") as f:
            yaml.dump(updated_config, f)
        
        # Create new loader to simulate application restart
        new_loader = ConfigLoader(
            config_file_name=config_path,
            config_model=TestConfig
        )
        
        # Load with new loader - should get updated config
        config2 = new_loader.load_config()
        assert config2 == updated_config
        assert config2 != config1
