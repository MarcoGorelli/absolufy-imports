import os
import shutil

from absolufy_imports import main


def test_depth(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'depth.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'depth.py'), tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join('mypackage', 'mysubpackage', 'depth.py'),
                '--depth',
                '1',
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()
    expected = (
        'from mypackage.mysubpackage import already_absolute\n'
        'from mypackage.mysubpackage import already_absolute as f\n'
        'from mypackage.mysubpackage.foo.bar import baz\n'
        'from mypackage.mysubpackage.foo.bar.baz import baz\n'
        'from mypackage.foo import T\n'
        'from .bar import D\n'
        'from . import O\n'
        'from datetime import datetime\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected
