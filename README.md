[![Build Status](https://github.com/MarcoGorelli/absolufy-imports/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/absolufy-imports/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/absolufy-imports/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/absolufy-imports)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/absolufy-imports/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/absolufy-imports/main)

## NOTE

This tool has been superseded by Ruff https://docs.astral.sh/ruff/rules/relative-imports/. Please use that instead.

R.I.P. `absolufy-imports`

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

### Run on directory

I'd suggest using [pre-commit](https://pre-commit.com/).

Either that, or
```
git ls-files | grep '\.py$' | xargs absolufy-imports
```

### Relative imports if some condition else absolute

naah...
