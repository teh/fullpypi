#!/usr/bin/env python
import os
from dep_extraction import dep_meta_pb2 as dep_meta
import argparse

TEMPLATE = """\
  "{name}" = extractImports {{
    name = "{name}";
    sha256 = "{sha256}";
    url = "{url}";
  }};
"""


def process(prefetch_root, out_stream):
    out_stream.write('{ extractImports }: {\n')

    for x in os.listdir(prefetch_root):
        meta = dep_meta.SDist()
        meta.ParseFromString(open(os.path.join(prefetch_root, x)).read())

        out_name = '{}-{}'.format(meta.pypi_name, meta.version)
        out_stream.write(TEMPLATE.format(sha256=x, name=out_name, url=meta.url))

    out_stream.write('}\n')


def main():
    parser = argparse.ArgumentParser(
        description='Transform prefetched packages into a nix expression.')
    parser.add_argument(
        'prefetch_root', type=str, help='Where the prefetched files life.')
    parser.add_argument(
        'output_path', type=str, help='Where to store the nix-expressions file.')
    args = parser.parse_args()

    with open(args.output_path, 'w') as f:
        process(args.prefetch_root, f)


if __name__ == '__main__':
    main()
