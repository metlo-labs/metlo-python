from glob import glob
import os
from typing import List

import yaml

from metlo.types.definition import Definition


def load_single_def(yaml_path: str) -> Definition:
    contents = open(yaml_path).read()
    yaml_data = yaml.load(contents, Loader=yaml.FullLoader)
    if 'id' not in yaml_data:
        yaml_data['id'] = yaml_path
    return Definition(**yaml_data)


def get_yaml_paths(yaml_dir: str) -> List[str]:
    get_glob = lambda ext: glob(os.path.join(yaml_dir, f'**/*.{ext}'), recursive=True)
    return get_glob('yaml') + get_glob('yml')


def load_defs(yaml_dir: str) -> List[Definition]:
    yaml_paths = get_yaml_paths(yaml_dir)
    return [load_single_def(yaml_path) for yaml_path in yaml_paths]
