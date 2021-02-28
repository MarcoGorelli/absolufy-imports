import os
import shutil

from abs_imports import main


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
                os.path.join('mypackage', 'mysubpackage', 'bar.py'),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        'from mypackage.mysubpackage import B\n'
        'from mypackage.mysubpackage.bar import baz\n'
        'from mypackage.foo import T\n'
        'from mypackage.mysubpackage.bar import D\n'
        'from mypackage.mysubpackage import O\n'
        'from datetime import datetime\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected


def test_main_src(tmpdir):
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
                '--application-directories',
                '.',
                tmp_file,
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        'from mypackage.mysubpackage import B\n'
        'from mypackage.mysubpackage.bar import baz\n'
        'from mypackage.foo import T\n'
        'from mypackage.mysubpackage.bar import D\n'
        'from mypackage.mysubpackage import O\n'
        'from datetime import datetime\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected


def test_noop(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'baz.py'), tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                '--application-directories',
                '.',
                tmp_file,
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 'baz.py')) as fd:
        expected = fd.read()

    assert result == expected
