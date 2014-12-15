# Building a full nix inventory of pypi (very WIP)

**Current status: fetching pypi packages. **

Packaging is traditionally a tricky business. Python has a long
history of packaging solutions that I am going to skip. I'm only going
to mention that the latest iteration is a [merge of setuptools and
distutils](https://pythonhosted.org/setuptools/merge.html).

This latest iteration still uses executable code to specify
dependencies. As much as I dislike nodejs for its choice of javascript
their packaging solutions is relatively sane. It's a [json file,
packages.json](http://browsenpm.org/package.json) that's declarative.
I.e. no if-statements that influence dependencies.

`packages.json` contains one section for runtime-dependencies and one
for development-dependencies. That allows e.g. omitting the test tools
from the released version.

Specifying dependencies is only half the battle though: Almost all
packaging systems can set constraints, e.g. "liba > 2.0.1" and "libz =
2.2.2". Installing one package in isolation usually works fine. If you
combine all the constraints of all installed packges things tend to
get more tricky. Package A requires "liba > 2.0.1" and package b
requires "liba > 2.2.0". This one is easy, just pick "liba >
2.2.0". In the most general case this is a satisfiablity problem, so
the common solution is to plug all constraints into a SAT solver and
hope that it returns a solution before the universe ends.

In some cases there is no solution (e.g. Package depends on "liba ==
2.0.1" and package b depends on "liba == 2.2.0"), we're going to skip
these for now.

I'm going to move on despite having omitted a whole lot of problems
such as optional dependencies or python3.

## Enter Nix

Nix is a packaging system that defines each package with a
purely functional language. A side-effect (hah) of that is that
*every* package depends on *all* its build inputs. The creators have a
[better, longer description here](http://nixos.org/nixos/about.html).

I'm really interested in this because it allows me to build and test
each package with all its dependencies in total isolation. There is no
chance that a random system package will sneak in and provide an
import that I didn't expect to be there.

Nix also comes with a large repository of existing packages that are
not python, e.g. gcc, or libblas. A lot of python packages are
actually bindings to c libraries. It's useful to be able to rely on
nix's existing packages.

## The sorry state of pypi

There is a large number of packages that don't specify their imports
correctly. There is no way of knowing how many without explicitly
checking. Some low-N sampling makes me think at least half.

## The plan

This project plans to build a nix expression for all versions of all
python packages. There are some easy and some hard parts, but there
are parts, i.e. we can divide and conquer. Here's the plan.

1. Get a copy of pypi's metadata (done, ~1d)
2. Build a large nix-derivation with all packages (tdb).
3. Fetch all packages and extract their metadata (20%).
  1. Extract dependencies where provided (e.g. from `.egg/requires.txt`).
  2. Write a second, hand-curated datastore of dependencies that
     maps (pypi-name, version) -> build-dependencies.
  3. Write "smoke tests" that test some of the most basic imports etc.
     These wouldn't replace full unit testing, but they are a good
     indicator for whether the project has a chance to run.
4. Build everything / update store accordingly.
5. Extend nix to provide a sat-solver.

## And then happily ever after

I would of course love to merge all that dependency data back into the
actual python packages but I have no community involvement. Maybe I
can provide the database?
