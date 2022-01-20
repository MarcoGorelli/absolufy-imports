import os
import shutil

from absolufy_imports import main


def test_main(tmpdir):
    # make src/mypackage/mysubpackage/bar.py
    os.mkdir(os.path.join(str(tmpdir), 'src'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'src', 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file,
    )

    # make mypackage/mysubpackage/bar.py
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file_1 = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file_1,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join(
                    str(tmpdir), 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                os.path.join(
                    str(tmpdir), 'src', 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                '--application-directories',
                '.:src',
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

    with open(tmp_file_1) as fd:
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


def test_main_inverted_order(tmpdir):
    # make src/mypackage/mysubpackage/bar.py
    os.mkdir(os.path.join(str(tmpdir), 'src'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'src', 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file,
    )

    # make mypackage/mysubpackage/bar.py
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file_1 = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file_1,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join(
                    str(tmpdir), 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                os.path.join(
                    str(tmpdir), 'src', 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                '--application-directories',
                '.:src',
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

    with open(tmp_file_1) as fd:
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


def test_relative_imports(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'src'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'src', 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'src', 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join(
                    str(tmpdir), 'src', 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                '--application-directories',
                '.:src',
            ),
        )
    finally:
        os.chdir(cwd)
    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join(
                    str(tmpdir), 'src', 'mypackage',
                    'mysubpackage', 'bar.py',
                ),
                '--application-directories',
                '.:src',
                '--never',
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()
    expected = (
        'from . import B\n'
        'from .bar import baz\n'
        'from mypackage.foo import T\n'
        'from .bar import D\n'
        'from . import O\n'
        'from datetime import datetime\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected
