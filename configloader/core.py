import argparse
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Type

from pydantic import BaseModel, ValidationError

from configloader.exceptions import (
    ConfigFileError,
    ConfigParserError,
    ConfigSourceError,
    ConfigValidationError,
)
from configloader.parsers.json_parser import JSONParser
from configloader.parsers.toml_parser import TOMLParser
from configloader.parsers.yaml_parser import YAMLParser
from configloader.sources import (
    CLIConfigSource,
    ConfigSource,
    EnvConfigSource,
    FileConfigSource,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ConfigLoader:
    """A flexible configuration loader that supports multiple sources and formats.

    This class implements a configuration loader that can load configuration from
    multiple sources (files, environment variables, CLI arguments) and merge them
    according to a priority order. It also supports validation through Pydantic models.

    Attributes:
        config_file_path (Optional[Path]): Path to the configuration file, or None if not using file source
        config_model (Optional[Type[BaseModel]]): Optional Pydantic model for validation
        sources (List[ConfigSource]): List of configuration sources
        _config (Optional[Dict[str, Any]]): Cached configuration
    """

    def __init__(
        self,
        config_file_path: Optional[str] = None,
        config_file_name: str = "config.toml",
        cli_args: Optional[argparse.Namespace] = None,
        env_prefix: Optional[str] = None,
        config_model: Optional[Type[BaseModel]] = None,
        custom_sources: Optional[Sequence[ConfigSource]] = None
    ):
        """Initialize the configuration loader.

        Args:
            config_file_path: Optional path to the configuration file
            config_file_name: Name of the configuration file
            cli_args: Optional CLI arguments
            env_prefix: Optional prefix for environment variables
            config_model: Optional Pydantic model for configuration validation
            custom_sources: Optional sequence of custom configuration sources

        Raises:
            ConfigFileError: If the configuration file cannot be found or accessed
        """

        self.config_file_path: Optional[Path] = self._get_file(config_file_path, config_file_name)
        self.config_model = config_model
        self.sources = self._get_sources(env_prefix, cli_args, custom_sources)
        self._config: Optional[Dict[str, Any]] = None

    @staticmethod
    def _get_file(config_file_path: Optional[str], config_file_name: str) -> Optional[Path]:
        """Get the configuration file path.

        Returns None if no file path is configured (allows custom-source-only usage).

        Args:
            config_file_path: Optional path to the configuration file
            config_file_name: Name of the configuration file

        Returns:
            Optional[Path]: Path to the configuration file, or None if no file configured
        """
        if config_file_path is None:
            # Use default: repo root / config_file_name
            default_path = Path(__file__).parent.parent / config_file_name
            if default_path.exists():
                logger.info(f"Using default config file: {default_path}")
                return default_path
            # No default file exists - return None (file source will be skipped)
            return None

        path = Path(config_file_path)

        # If path is a file (has extension), use it directly
        if path.suffix:
            return path

        # If path is a directory, append config_file_name
        return path / config_file_name

    def _get_sources(
        self,
        env_prefix: Optional[str],
        cli_args: Optional[argparse.Namespace],
        custom_sources: Optional[Sequence[ConfigSource]]
    ) -> List[ConfigSource]:
        """Get the sources for the configuration loader.

        Args:
            env_prefix: Optional prefix for environment variables
            cli_args: Optional CLI arguments
            custom_sources: Optional sequence of custom configuration sources

        Returns:
            List[ConfigSource]: List of configuration sources
        """
        sources: List[ConfigSource] = [
            FileConfigSource(self.config_file_path, self._get_parser()),
            EnvConfigSource(env_prefix),
            CLIConfigSource(cli_args)
        ]
        if custom_sources:
            sources.extend(custom_sources)
        return sources

    def _get_parser(self) -> Any:
        """Get the appropriate parser for the configuration file.

        Returns:
            Any: The appropriate parser for the file format

        Raises:
            ConfigParserError: If the file format is not supported
        """
        try:
            ext = self.config_file_path.suffix.lstrip(".").lower()
            parser_dispatcher = {
                "toml": TOMLParser(),
                "yaml": YAMLParser(),
                "yml": YAMLParser(),
                "json": JSONParser(),
            }

            if ext in parser_dispatcher:
                logger.info(f"Using parser for extension: {ext}")
                return parser_dispatcher[ext]
            else:
                raise ConfigParserError(f"Unsupported config file format: {ext}")
        except Exception as e:
            raise ConfigParserError(f"Failed to get parser: {str(e)}") from e

    def _load_and_merge_configs(self) -> Dict[str, Any]:
        """Load and merge configurations from all sources.

        Returns:
            Dict[str, Any]: The merged configuration

        Raises:
            ConfigSourceError: If a source fails to load
            ConfigMergeError: If configurations cannot be merged
        """

        final_config = {}
        for source in self.sources:
            try:
                config = source.load()
                final_config.update(config)
                logger.info(f"Loaded configuration from {source.__class__.__name__}")
            except Exception as e:
                raise ConfigSourceError(
                    f"Error loading configuration from {source.__class__.__name__}: {str(e)}"
                ) from e
        return final_config

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate the configuration against the provided Pydantic model.

        Args:
            config: The configuration to validate

        Raises:
            ConfigValidationError: If validation fails
        """
        if not self.config_model:
            return

        try:
            self.config_model(**config)
            logger.info("Configuration validation successful")
        except ValidationError as e:
            errors = e.errors()
            raise ConfigValidationError(
                "Configuration validation failed",
                errors=errors
            ) from e

    def load_config(self) -> Dict[str, Any]:
        """Load and return the configuration.

        This method implements a simple singleton pattern - it loads the configuration
        only once and returns the cached version on subsequent calls.

        Returns:
            Dict[str, Any]: The merged configuration from all sources

        Raises:
            ConfigSourceError: If a source fails to load
            ConfigValidationError: If validation fails
            ConfigMergeError: If configurations cannot be merged
        """
        if self._config is None:
            config = self._load_and_merge_configs()
            self._validate_config(config)
            self._config = config
            logger.info("Configuration loaded and cached")
        else:
            logger.info("Returning cached configuration")
        return self._config
