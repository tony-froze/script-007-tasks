#!/usr/bin/env python3
import argparse


def main(args: argparse.Namespace):
    return args.directory


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", required=True, help="Working directory")
    arguments = parser.parse_args()
    main(arguments)
