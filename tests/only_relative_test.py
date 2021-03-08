import os
import shutil

from absolufy_imports import main


def test_main(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                '--never',
                os.path.join('mypackage', 'mysubpackage', 'bar.py'),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        'from . import B\n'
        'from .bar import baz\n'
        'from ..foo import T\n'
        'from .bar import D\n'
        'from . import O\n'
        'from datetime import datetime\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected
