"""ConfigLoader - A flexible configuration loader for Python applications.

This package provides a simple way to load and manage configuration from various
sources like files, environment variables, and CLI arguments.
"""

from configloader.core import ConfigLoader
from configloader.sources import ConfigSource, FileConfigSource, EnvConfigSource, CLIConfigSource
from configloader.parsers.base import BaseParser
from configloader.parsers.json_parser import JSONParser
from configloader.parsers.toml_parser import TOMLParser
from configloader.parsers.yaml_parser import YAMLParser

__version__ = "0.1.0"
__all__ = [
    "ConfigLoader",
    "ConfigSource",
    "FileConfigSource",
    "EnvConfigSource",
    "CLIConfigSource",
    "BaseParser",
    "JSONParser",
    "TOMLParser",
    "YAMLParser",
]
