import logging
from pathlib import Path
from typing import Any, Dict

import toml

from configloader.exceptions import ConfigParserError
from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class TOMLParser(BaseParser):
    def load(self, file_path: Path) -> Dict[str, Any]:
        try:
            toml_config = toml.load(file_path)
            if isinstance(toml_config, dict):
                logger.info(f"Config file loaded successfully: {toml_config}")
                return toml_config
            else:
                logger.error("Config file is not a valid TOML file.")
                raise ValueError("Config file is not a valid TOML file.")
        except toml.TomlDecodeError as e:
            raise ConfigParserError(f"Failed to parse TOML file {file_path}: {e}") from e