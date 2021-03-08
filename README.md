[![Build Status](https://github.com/MarcoGorelli/absolufy-imports/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/absolufy-imports/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/absolufy-imports/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/absolufy-imports)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/absolufy-imports/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/absolufy-imports/main)

absolufy-imports
===========

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

## Usage as a pre-commit hook (recommended)

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/absolufy-imports
    rev: v0.3.0
    hooks:
    -   id: absolufy-imports
```

## Command-line example

```console
$ cat mypackage/myfile.py
from . import __version__
$ absolufy-imports mypackage/myfile.py
$ cat mypackage/myfile.py
from mypackage import __version__
```

## Configuration

### Application directories

If your package follows the popular `./src` layout, you can pass your application directories via `--application-directories`, e.g.

```console
$ cat src/mypackage/myfile.py
from . import __version__
$ absolufy-imports src/mypackage/myfile.py --application-directories src
$ cat src/mypackage/myfile.py
from mypackage import __version__
```

Multiple application directories should be comma-separated, e.g. `--application-directories .:src`. This is the same as in [reorder-python-imports](https://github.com/asottile/reorder_python_imports).

### Only use relative imports

Use the `--never` flag, e.g.

```console
$ cat mypackage/myfile.py
from mypackage import __version__
$ absolufy-imports mypackage/myfile.py --never
$ cat mypackage/myfile.py
from . import __version__
```

### Keep submodules relative

Use the `--keep-submodules-relative` flag. By default, submodules are considered to be the first level of the directory. E.g. if you have

```
├── mypackage
│   ├── library1
│   │   ├── foo.py
│   │   └── subdirectory
│   │       ├── bar.py
│   │       └── baz.py
│   └── library2
│       └── qux.py
```

and

```console
$ cat mypackage/library1/subdirectory/bar.py
from mypackage.library1.subdirectory import baz
from mypackage.library1 import foo
from mypackage.library2 import qux
```

then you will get

```console
$ absolufy-imports mypackage/library1/subdirectory/bar.py --keep-submodules-relative
$ cat mypackage/library1/subdirectory/bar.py
from . import baz
from .. import foo
from mypackage.library2 import qux
```

To specify a custom list of submodules, you can use the `--submodules` flag, e.g.

```console
$ absolufy-imports mypackage/library1/subdirectory/bar.py \
  --keep-submodules-relative \
  --submodules '{".": ["mypackage.library1", "mypackage.library2"]}'
```

Note that they need to be in json format, and the keys should be the application directories.

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
