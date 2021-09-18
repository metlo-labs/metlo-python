from glob import glob
import os
from typing import List

import yaml

from metlo.types.definition import Definition


def load_defs(yaml_dir: str) -> List[Definition]:
    yaml_paths = glob(os.path.join(yaml_dir, '*.yaml'))

    definitions = []

    for yaml_path in yaml_paths:
        contents = open(yaml_path).read()
        yaml_data = yaml.load(contents, Loader=yaml.FullLoader)
        if 'id' not in yaml_data:
            yaml_data['id'] = yaml_path
        definitions.append(Definition(**yaml_data))

    return definitions
