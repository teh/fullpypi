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

        # Note that we have to replace spaces with dashes because of
        # restrictions in nix-derivation
        # names. E.g. `django-swingtime-0.3 beta 0' doesn't work.

        # More to sanitize:
        # egrep "name =" /var/fullpypi/extract.nix | egrep "\"[-_0-9a-zA-Z\.]+\";$"  -v
        #     name = "pyscons-1.0.42+";
        #     name = "fabricate-(latest-release)";
        #     name = "pyscons-1.0.30+";
        #     name = "keysync-(latest-release)";
        #     name = "pyscons-1.0.50+";
        #     name = "croc-1.1.21+";
        #     name = "croc-1.1.25+";
        #     name = "i2p.i2cp-(latest-release)";
        #     name = "pyscons-1.0.69+";
        #     name = "ipkiss24ce-(latest-release)";
        #     name = "pyscons-1.0.67+";
        #     name = "openelectrons-i2c-(latest-release)";

        out_name = '{}-{}'.format(meta.pypi_name, meta.version)\
            .replace(' ', '-')\
            .replace('(', '_')\
            .replace(')', '_')\
            .replace('+', '_plus')
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
