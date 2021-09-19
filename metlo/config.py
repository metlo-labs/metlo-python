import os
from typing import Optional

from dotenv import dotenv_values
from pydantic.dataclasses import dataclass


DEFAULT_CONFIG_FOLDER = os.path.join(os.path.expanduser('~/.metlo'))
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_FOLDER, 'credentials')
API_KEY_NAME = 'METLO_API_KEY'
HOST_KEY_NAME = 'METLO_HOST'
DEFINITION_DIR_KEY_NAME = 'METLO_DEFINITION_DIR'


@dataclass
class MetloConfig:
    api_key: str
    host_name: str
    definition_dir: Optional[str]


def load_config_file() -> Optional[dict]:
    config_path = os.environ.get('METLO_CONFIG_PATH', DEFAULT_CONFIG_PATH)
    if not os.path.exists(config_path):
        return None
    return dotenv_values(config_path)


def get_config() -> Optional[MetloConfig]:
    conf_file_vals = load_config_file() or {}
    api_key = os.environ.get(API_KEY_NAME, conf_file_vals.get(API_KEY_NAME))
    host_name = os.environ.get(HOST_KEY_NAME, conf_file_vals.get(HOST_KEY_NAME))
    definition_dir = os.environ.get(DEFINITION_DIR_KEY_NAME, conf_file_vals.get(DEFINITION_DIR_KEY_NAME))

    if not api_key:
        print('No API Key Specified')
    if not host_name:
        print('No Host Name Specified')
    
    if not (api_key and host_name):
        return
    
    return MetloConfig(
        api_key=api_key,
        host_name=host_name,
        definition_dir=definition_dir
    )
