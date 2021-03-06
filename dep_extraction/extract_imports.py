#!/usr/bin/env python
"""
compile proto:
protoc --python_out=. dep_extraction/dep_meta.proto

"""
import os
import argparse
from dep_extraction import extract_lib
from dep_extraction import heuristic_setup_deps
from dep_extraction import stdlib_modules_autogenerated
from dep_extraction import dep_meta_pb2 as dep_meta
import pkg_resources

SCRIPT_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_pkg_resources_path(x):
    if os.path.exists(pkg_resources.resource_filename('dep_extraction', x)):
        return pkg_resources.resource_filename('dep_extraction', x)
    return os.path.join(SCRIPT_ROOT, x)


def discover_egg_dir(root):
    _, dirs, _ = os.walk(root).next()
    egg_dirs = [x for x in dirs if x.endswith('.egg-info')]
    if not egg_dirs:
        return ''
    assert len(egg_dirs) == 1, "Found more than one .egg directory in {}: {}".format(root, egg_dirs)

    return egg_dirs[0]


def main():
    parser = argparse.ArgumentParser(description='Extract deps.')
    parser.add_argument(
        'root', type=str, help='root of a python package.')
    parser.add_argument(
        'out_path', type=str, help='File path for storing the metadata-protobuf.')
    args = parser.parse_args()

    tl_imports, provides = extract_lib.extract_tlis(args.root)

    # Read database of known names.
    with open(get_pkg_resources_path('known_names.protobuf')) as f:
        known_names = dep_meta.KnownNames()
        known_names.ParseFromString(f.read())
        known_names = set(known_names.names)

    log = []
    meta = dep_meta.DepMeta()
    meta.provides.extend(sorted(provides))
    meta.depends_full.extend(sorted(tl_imports))
    meta.depends_remove_py2_stdlib.extend(sorted(tl_imports - stdlib_modules_autogenerated.python2_modules))
    meta.depends_remove_py3_stdlib.extend(sorted(tl_imports - stdlib_modules_autogenerated.python3_modules))

    try:
        meta.heuristic_setup_deps.extend(
            heuristic_setup_deps.extract(
                open(os.path.join(args.root, 'setup.py')).read(),
                known_names,
            )
        )
    except IOError as e:
        log.append('setup.py IOError: {}'.format(e))
    except SyntaxError as e:
        log.append('setup.py SyntaxError: {}'.format(e))

    try:
        requires_txt = open(os.path.join(args.root, discover_egg_dir(args.root), 'requires.txt')).read()
        meta.requires_txt.extend(sorted(requires_txt.splitlines()))

    except IOError as e:
        log.append('No .egg/requires.txt.'.format(e))

    try:
        requirements_txt = open(os.path.join(args.root, 'requirements.txt')).read()
        meta.requirements_txt.extend(sorted(requirements_txt.splitlines()))

    except IOError as e:
        log.append('No requirements.txt.'.format(e))

    meta.log.extend(log)

    with open(args.out_path, 'w') as f:
        f.write(meta.SerializeToString())


if __name__ == '__main__':
    main()
