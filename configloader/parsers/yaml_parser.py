

import logging
import yaml
from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class YAMLParser(BaseParser):
    def load(self, config_file_path: str) -> dict:
        yaml_config = {}
        try:
            with open(config_file_path, "r") as file:
                yaml_config = yaml.safe_load(file)
                if isinstance(yaml_config, dict):
                    logger.info(f"Config file loaded successfully: {yaml_config}")
                else:
                    logger.error("Config file is not a valid YAML file.")
                    raise ValueError("Config file is not a valid YAML file.")
        except yaml.YAMLError as e:
            logger.error(f"Error decoding YAML file: {e}")
        return yaml_config
