# pypi-database

*Word of warning: Some directories like /nix/store tend to get pretty
 big (millions of entries). Avoid hitting that autocomplete-key in bash at all costs!*

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

This generates a humongous file which is of course too large to build
with nix-build (command line passed to nix-store is too long). As as
workaround we instantiate all the individual derivations and build
them manually.

```sh
nix-instantiate  /var/fullpypi/extract_imports_expression.nix -A pkgs > /var/fullpypi/extract_import_intantiations.txt
cat /var/fullpypi/extract_import_intantiations.txt  | xargs nix-store -r -j 8 --keep-going --option use-binary-caches false
```
