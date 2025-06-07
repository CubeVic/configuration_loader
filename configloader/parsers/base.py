from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseParser(ABC):
    """Base class for configuration parsers.
    
    This abstract base class defines the interface that all configuration parsers must implement.
    Each parser should be able to load configuration from a specific file format.
    """
 
    @abstractmethod
    def load(self, path: Path) -> Dict[str, Any]:
        """Load configuration from a file.
        
        Args:
            path: Path to the configuration file
            
        Returns:
            Dictionary containing the configuration
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        pass