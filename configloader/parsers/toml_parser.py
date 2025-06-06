
import logging
import toml
from configloader.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class TOMLParser(BaseParser):
    def load(self, config_file_path: str) -> dict:
        toml_config = {}
        try:
            toml_config = toml.load(config_file_path)
            if isinstance(toml_config, dict):
                logger.info(f"Config file loaded successfully: {toml_config}")
            else:
                logger.error("Config file is not a valid TOML file.")
                raise ValueError("Config file is not a valid TOML file.")
        except toml.TomlDecodeError as e:
            logger.error(f"Error decoding TOML file: {e}")
        return toml_config