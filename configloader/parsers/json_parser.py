import json
import logging
from pathlib import Path
from typing import Any, Dict

from configloader.exceptions import ConfigParserError
from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class JSONParser(BaseParser):

    def load(self, file_path: Path) -> Dict[str, Any]:
        try:
            with open(file_path, "r") as file:
                json_config = json.load(file)
                if isinstance(json_config, dict):
                    logger.info(f"Config file loaded successfully: {json_config}")
                    return json_config
                else:
                    logger.error("Config file is not a valid JSON file.")
                    raise ValueError("Config file is not a valid JSON file.")
        except json.JSONDecodeError as e:
            raise ConfigParserError(f"Failed to parse JSON file {file_path}: {e}") from e
