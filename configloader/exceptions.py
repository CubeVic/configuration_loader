"""Custom exceptions for the ConfigLoader package."""


class ConfigLoaderError(Exception):
    """Base exception for all ConfigLoader errors."""
    pass


class ConfigValidationError(ConfigLoaderError):
    """Raised when configuration validation fails."""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.errors = errors or {}


class ConfigSourceError(ConfigLoaderError):
    """Raised when a configuration source fails to load."""
    pass


class ConfigFileError(ConfigSourceError):
    """Raised when a configuration file cannot be loaded."""
    pass


class ConfigParserError(ConfigLoaderError):
    """Raised when a configuration file cannot be parsed."""
    pass


class ConfigMergeError(ConfigLoaderError):
    """Raised when configuration sources cannot be merged."""
    pass
