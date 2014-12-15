#!/usr/bin/env python
"""Script to prefetch all the pypi packages and then write their
sha256 sums with some metadata into a datastore.

Note that the download tool computes the flat hash but it still works
if you do e.g. this:

nix-prefetch-url \
  https://pypi.python.org/packages/source/A/AWSpider/AWSpider-0.3.0.4.tar.gz \
  000fbj6511w7dyc3h61x2krblygdx1r3dislgk2zvb7m75zx1dm4
"""
import eventlet
from eventlet import wsgi
from eventlet.green import subprocess
import os
import argparse
import pandas
from dep_extraction import dep_meta_pb2 as dep_meta
import sys
import flask
import pkg_resources

CONCURRENCY = 3
STATS = dict(i=0, total=0, errors=0)


# Small stats server so we can run in background:
stats_app = flask.Flask(__name__)
@stats_app.route('/')
def stats():
    return '{}'.format(STATS)
eventlet.spawn(wsgi.server, eventlet.listen(('', 8005)), stats_app)


def fetch_and_store_one((index, row)):
    try:
        sha256 = subprocess.check_output([
            '/bin/sh', '-c',
            'source /etc/profile; nix-prefetch-url {}'.format(row['url']),
        ], stderr=open('/dev/null')).strip()

        meta = dep_meta.SDist(
            pypi_name=row['pypi_name'],
            version=row['version'],
            url=row['url'],
        )
        
        with open(os.path.join(row['store_root'], sha256), 'w') as f:
            f.write(meta.SerializeToString())
        
    except subprocess.CalledProcessError as e:
        STATS['errors'] += 1
        print "error fetching", e, row


def get_done(store_root):
    for path in os.listdir(store_root):
        try:
            with open(os.path.join(store_root, path)) as f:
                meta = dep_meta.SDist()
                meta.ParseFromString(f.read())
                yield meta.url
        except Exception as e:
            print "could not read {}: {}".format(path, e)

def main():
    parser = argparse.ArgumentParser(description='Prefetch all packages.')
    parser.add_argument(
        'store_root', type=str, help='directory to store all the metadata.')
    args = parser.parse_args()

    store = pandas.HDFStore(pkg_resources.resource_filename(
        'dep_extraction', 'pypi-sdists-2014-12-14.h5'))
    df = store['sdist_df']
    store.close()

    done = list(get_done(args.store_root))
    df = df.set_index('url')
    df = df.ix[df.index.difference(done), :]

    df['store_root'] = args.store_root
    gdf = df.reset_index().groupby(lambda x: x//1000)

    i = 0
    pool = eventlet.GreenPool(CONCURRENCY)
    STATS['total'] = len(df)
    for _, group in gdf:
        for _ in pool.imap(fetch_and_store_one, group.iterrows()):
            if sys.stdout.isatty():
                sys.stdout.write('{}/{}. {:.2f}\r'.format(i, len(df), 100.0 * i / len(df)))
                sys.stdout.flush()
            i += 1
            STATS['i'] += 1

if __name__ == '__main__':
    main()
