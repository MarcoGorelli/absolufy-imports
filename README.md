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


### Absolute imports for specified package

Using the below command you just need to specify the package name on which: `absolufy-imports` - will `walk` and convert relative import paths to absolute import python paths.

```console
$ absolufy-imports --package your_package_name
```
