#!/usr/bin/env python
"""
Too to dump the import metadata in human readable form.
"""
import argparse
from dep_extraction import dep_meta_pb2 as dep_meta


def main():
    parser = argparse.ArgumentParser(description='Show import metadata.')
    parser.add_argument('path', type=str, help='File to show')
    args = parser.parse_args()

    meta = dep_meta.DepMeta()
    with open(args.path) as f:
        meta.ParseFromString(f.read())

    print str(meta)


if __name__ == '__main__':
    main()
