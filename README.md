[![Build Status](https://github.com/MarcoGorelli/abs-imports/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/abs-imports/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/abs-imports/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/abs-imports)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/abs-imports/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/abs-imports/main)

abs-imports
===========

A pre-commit hook to automatically convert relative imports to absolute.

## Installation

```
pip install abs-imports
```

## Usage as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/abs-imports
    rev: v0.2.1
    hooks:
    -   id: abs-imports
```

## Command-line example

```console
$ cat mypackage/myfile.py
from . import __version__
$ abs-imports mypackage/myfile.py
$ cat mypackage/myfile.py
from mypackage import __version__
```

If your package follows the popular `./src` layout, you can pass your application directories via `--application-directories`, e.g.

```console
$ cat src/mypackage/myfile.py
from . import __version__
$ abs-imports src/mypackage/myfile.py --application-directories src
$ cat src/mypackage/myfile.py
from mypackage import __version__
```

Multiple application directories should be comma-separated, e.g. `--application-directories .:src`. This is the same as in [reorder-python-imports](https://github.com/asottile/reorder_python_imports).

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
