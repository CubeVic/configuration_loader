import logging
import os
from abc import ABC, abstractmethod
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigSource(ABC):
    """Abstract base class for configuration sources.
    
    This class defines the interface that all configuration sources must implement.
    Each source should be able to load configuration from a specific source (file, env, CLI).
    """
    
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load configuration from the source.
        
        Returns:
            Dictionary containing the configuration
        """
        pass


class FileConfigSource(ConfigSource):
    """Configuration source that loads from a file."""
    
    def __init__(self, file_path: Path, parser: Any):
        self.file_path = file_path
        self.parser = parser
        
    def load(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.file_path}")
        return self.parser.load(self.file_path)


class EnvConfigSource(ConfigSource):
    """Configuration source that loads from environment variables."""
    
    def __init__(self, prefix: Optional[str] = None):
        self.prefix = prefix
        
    def load(self) -> Dict[str, Any]:
        if not self.prefix:
            return {}
            
        env_config = {}
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                config_key = key[len(self.prefix):].lower()
                env_config[config_key] = value
        return env_config


class CLIConfigSource(ConfigSource):
    """Configuration source that loads from CLI arguments."""
    
    def __init__(self, args: Optional[Namespace] = None):
        self.args = args
        
    def load(self) -> Dict[str, Any]:
        if not self.args:
            return {}
        return {k: v for k, v in vars(self.args).items() if v is not None} 