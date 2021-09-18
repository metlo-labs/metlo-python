import argparse
from getpass import getpass
import os

from metlo.config import (
    DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FOLDER, API_KEY_NAME, HOST_KEY_NAME
)
from metlo.load_definitions import load_defs


def setup():
    host = input('Enter your Metlo Host: ')
    api_key = getpass(prompt='Enter your API Key: ')

    if not os.path.exists(DEFAULT_CONFIG_FOLDER):
        os.mkdir(DEFAULT_CONFIG_FOLDER)

    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        f.write(f'{HOST_KEY_NAME}={host}\n{API_KEY_NAME}={api_key}')


def validate(directory: str):
    load_defs(directory)


def main():
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
