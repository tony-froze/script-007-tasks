import argparse
import logging
import os

from dotmap import DotMap
import yaml


def parse_cli_args():
    """Parses arguments from command line.

    Returns: a dictionary that may contain the following keys:
        directory: path to working directory;
        loglevel: logging level;
        logfile: path to file for logging;
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Working directory")
    parser.add_argument('-l', '--loglevel',  type=str.upper, default='INFO',
                        choices=logging._nameToLevel.keys(), help="Logging level")
    parser.add_argument('-f', '--logfile',  type=str, help="Logging file")
    return {k: v for k, v in vars(parser.parse_args()).items() if v}


def parse_environ_args(prefix):
    """Parses arguments from environment variables.

    Returns: a dictionary from environment variables with keys that start with a specific prefix.
    """
    return {k.replace(prefix, '', 1): v for k, v in os.environ.items() if k.startswith(prefix)}


def parse_yaml_config():
    """Parses arguments from .yaml configuration file.

    Returns: a dictionary with all variables from config file.
    """
    with open('config.yaml', 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            conf = {}
            logging.info(str(exc))
    return conf


config = {'directory': os.getcwd()}
config.update(parse_yaml_config())
config.update(parse_environ_args(config.get('app_prefix', 'FS_')))
config.update(parse_cli_args())

config = DotMap(config)
