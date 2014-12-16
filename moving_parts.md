# pypi-database

Scraped on 14th of December 2014 using [this
script](https://github.com/WeAreWizards/pypidata).

# Package prefetcher

Fetches all versions of all pypi packages it can get using
`nix-prefetch-url` and stores them in /nix/store with their
cryptographic hash. We also store some metadata in
`/var/fullpypi/prefetch_result/`.

Run with

```sh
systemd-run prefetch_all.py /var/fullpypi/prefetch_result/
```

# Nix-file generator for dependency builder.

This is generating a nix-file per python package with a special
builder: `extract_imports.py`. This build doesn't build a python
package but a protobuf file with import/package metadata (see
`dep_extraction/dep_meta.proto`).

```sh
write_extractor_builder.py /var/fullpypi/prefetch_result/ /var/fullpypi/extract.nix
```

This generates a humongous file that we can then build with nix-build:

```sh
nix-build ---no-out-link --keep-going -j 4 --attr all /var/fullpypi/extract_run.nix
```
