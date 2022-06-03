import logging

import argparse
import os

from dotmap import DotMap
import yaml


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True, help="Working directory")
    parser.add_argument('-l', '--loglevel',  type=str, default='INFO',
                        choices=logging._nameToLevel.keys(), help="Logging level")
    parser.add_argument('-f', '--logfile',  type=str, help="Logging file")
    return {k: v for k, v in vars(parser.parse_args()).items() if v}


def parse_environ_args(prefix):
    return {k: v for k, v in os.environ.items() if k.startswith(prefix)}


def parse_yaml_config():
    with open('config.yaml', 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            conf = {}
            print(exc)
    return conf


config = {'directory': os.getcwd()}
config.update(parse_yaml_config())
config.update(parse_environ_args(config.get('app_prefix', 'FPS')))
config.update(parse_cli_args())

config = DotMap(config)
print(config)
