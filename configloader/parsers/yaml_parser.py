import logging

import yaml

from configloader.exceptions import ConfigParserError
from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class YAMLParser(BaseParser):
    def load(self, config_file_path: str) -> dict:
        try:
            with open(config_file_path, "r") as file:
                yaml_config = yaml.safe_load(file)
                if isinstance(yaml_config, dict):
                    logger.info(f"Config file loaded successfully: {yaml_config}")
                    return yaml_config
                else:
                    logger.error("Config file is not a valid YAML file.")
                    raise ValueError("Config file is not a valid YAML file.")
        except yaml.YAMLError as e:
            raise ConfigParserError(f"Failed to parse YAML file {config_file_path}: {e}") from e
