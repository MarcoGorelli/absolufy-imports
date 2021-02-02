[![Build Status](https://github.com/MarcoGorelli/abs-imports/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/abs-imports/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/abs-imports/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/abs-imports)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/abs-imports/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/abs-imports/main)

abs-imports
===========

A pre-commit hook to automatically convert relative absolute to absolute.

## Usage as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/abs-imports
    rev: v0.1.1
    hooks:
    -   id: abs-imports
```

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
