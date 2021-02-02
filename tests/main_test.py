import os
import shutil

import pytest

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
        'from mypackage.foo import T\n'
        'from mypackage.mysubpackage.bar import D\n'
        'from mypackage.mysubpackage import O\n'
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

    main(
        (
            '--application-directories',
            str(tmpdir),
            tmp_file,
        ),
    )

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        'from mypackage.mysubpackage import B\n'
        'from mypackage.foo import T\n'
        'from mypackage.mysubpackage.bar import D\n'
        'from mypackage.mysubpackage import O\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected


def test_non_existent_file(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    os.mkdir(os.path.join(str(tmpdir), 'otherdir'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'bar.py'), tmp_file,
    )

    msg = r'File .* cannot be resolved relative to .*'
    with pytest.raises(ValueError, match=msg):
        main(
            (
                '--application-directories',
                os.path.join(str(tmpdir), 'otherdir'),
                tmp_file,
            ),
        )


def test_noop(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py',
    )
    shutil.copy(
        os.path.join('tests', 'data', 'baz.py'), tmp_file,
    )

    main(
        (
            '--application-directories',
            str(tmpdir),
            tmp_file,
        ),
    )

    with open(tmp_file) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 'baz.py')) as fd:
        expected = fd.read()

    assert result == expected
