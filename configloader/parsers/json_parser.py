import json
import logging

from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class JSONParser(BaseParser):

    def load(self, config_file_path: str) -> dict:
        json_config = {}
        try:
            with open(config_file_path, "r") as file:
                json_config = json.load(file)
                if isinstance(json_config, dict):
                    logger.info(f"Config file loaded successfully: {json_config}")
                else:
                    logger.error("Config file is not a valid JSON file.")
                    raise ValueError("Config file is not a valid JSON file.")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON file: {e}")
        return json_config
