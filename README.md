[![Build Status](https://github.com/MarcoGorelli/absolufy-imports/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/absolufy-imports/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/absolufy-imports/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/absolufy-imports)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/absolufy-imports/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/absolufy-imports/main)

absolufy-imports
================

A tool and pre-commit hook to automatically convert relative imports to absolute.

<p align="center">
    <a href="#readme">
        <img alt="demo" src="https://raw.githubusercontent.com/nbQA-dev/nbQA-demo/master/abs-imports.gif">
    </a>
</p>

## Installation

```console
$ pip install absolufy-imports
```

## Usage as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/absolufy-imports
    rev: v0.3.1
    hooks:
    -   id: absolufy-imports
```

## Command-line example

```console
$ absolufy-imports mypackage/myfile.py
```

```diff
- from . import __version__
+ from mypackage import __version__
```

## Configuration

### Application directories

If your package follows the popular `./src` layout, you can pass your application directories via `--application-directories`, e.g.

```console
$ absolufy-imports src/mypackage/myfile.py --application-directories src
```

```diff
- from . import __version__
+ from mypackage import __version__
```

Multiple application directories should be colon-separated, e.g. `--application-directories .:src`. This is the same as in [reorder-python-imports](https://github.com/asottile/reorder_python_imports).

### Only use relative imports

Use the `--never` flag, e.g.

```console
$ absolufy-imports mypackage/myfile.py --never
```

```diff
- from mypackage import __version__
+ from . import __version__
```

### Depth (default: 0)

Don't absolufy (backward or forward) relative imports less or equal to the specified depth.

Usage: `--depth N` with `N` as integer.

* `--never` and `--depth N` are mutually exclusive

In other words, when choosing `--depth 1` you can only use relative
imports for files/folder in the same package. See above examples

Folder:
```
mypackage
 |-- mysubpackage
 |   |-- __init__.py
 |   |-- example.py
 |-- __init__.py
 |-- main.py
```

#### Examples (backward: `from ..X import A`) with `--depth 1`:
* `$ absolufy-imports mypackage/mysubpackage/__init__.py --depth 1`

```diff
  from .example import __file__
- from ..main import __file__
+ from mypackage.main import __file__
```
* `$ absolufy-imports mypackage/mysubpackage/__init__.py --depth 0 # default value`

```diff
- from .example import __file__
+ from mypackage.mysubpackage.example import __file__
- from ..main import __file__
+ from mypackage.main import __file__
```

With: `mypackage.mysubpackage.__init__.py` content:
```
from .example import __file__
from ..main import __file__
```

#### Example (forward: `from .X.Y.Z import A`) with `--depth 1`:

* `$ absolufy-imports mypackage/__init__.py --depth 1`
```diff
- from .mysubpackage.__init__ import __file__
+ from mypackage.mysubpackage.__init__ import __file__
  from .mysubpackage import __init__ as i
```

With `mypackage.__init__.py` content:
```
from .mysubpackage.__init__ import __file__
from .mysubpackage import __init__ as i
```
