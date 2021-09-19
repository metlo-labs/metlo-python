import argparse
from getpass import getpass
from glob import glob
import os

from colorama import init as colorama_init
from termcolor import colored
from pydantic import ValidationError

from metlo.config import (
    DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FOLDER, API_KEY_NAME, HOST_KEY_NAME
)
from metlo.load_definitions import load_single_def


def setup():
    host = input('Enter your Metlo Host: ')
    api_key = getpass(prompt='Enter your API Key: ')

    if not os.path.exists(DEFAULT_CONFIG_FOLDER):
        os.mkdir(DEFAULT_CONFIG_FOLDER)

    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        f.write(f'{HOST_KEY_NAME}={host}\n{API_KEY_NAME}={api_key}')


def validate(directory: str):
    yaml_paths = glob(os.path.join(directory, '*.yaml'))
    for yaml_path in yaml_paths:
        try:
            print(f'Validating {yaml_path}')
            load_single_def(yaml_path)
            print(colored('PASSED', 'green'))
        except ValidationError as e:
            print(colored(str(e), 'red'))

def main():
    colorama_init()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    setup_parser = subparsers.add_parser('setup')
    validate_parser = subparsers.add_parser('validate')
    validate_parser.add_argument(
        '-d', '--directory', help='The definition directory to validate.', required=True
    )
    args = parser.parse_args()

    command = args.command 

    if command == 'setup':
        setup()
    if command == 'validate':
        validate(args.directory)


if __name__ == '__main__':
    main()
