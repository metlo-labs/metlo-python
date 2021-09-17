import argparse
from getpass import getpass
import os

from metlo.config import (
    DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FOLDER, API_KEY_NAME, HOST_KEY_NAME
)


def setup():
    host = input('Enter your Metlo Host: ')
    api_key = getpass(prompt='Enter your API Key: ')

    if not os.path.exists(DEFAULT_CONFIG_FOLDER):
        os.mkdir(DEFAULT_CONFIG_FOLDER)

    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        f.write(f'{HOST_KEY_NAME}={host}\n{API_KEY_NAME}={api_key}')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    setup_parser = subparsers.add_parser('setup')
    args = parser.parse_args()

    command = args.command 

    if command == 'setup':
        setup()


if __name__ == '__main__':
    main()
