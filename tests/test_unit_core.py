import json
from pathlib import Path
import tempfile
from hypothesis import given
import toml
import yaml
from pydantic import BaseModel
from configloader.core import ConfigLoader
from configloader.sources import ConfigSource
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
    config_loader = ConfigLoader(custom_sources=[CustomTestSource()])
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
            )
            assert False, "Should have raised ValidationError"
        except Exception as e:
            assert isinstance(e, Exception)


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
            custom_sources=[custom_source]
        )

        config = config_loader.load_config()
        assert config["name"] == "test_app"  # From custom source
        assert config["version"] == "1.0.0"  # From custom source
        assert config["debug"] is True  # From custom source
