import os
import shutil
from pathlib import Path

import pytest

from absolufy_imports import main


def test_main(tmpdir):
    source_file: Path = Path(__file__).parent / 'data/bar.py'
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(source_file, tmp_file)

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
    source_file: Path = Path(__file__).parent / 'data/bar.py'
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py',
    )
    shutil.copy(
        source_file, tmp_file,
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
    source_file: Path = Path(__file__).parent / 'data/baz.py'
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py',
    )
    shutil.copy(
        source_file, tmp_file,
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

    with source_file.open() as fd:
        expected = fd.read()

    assert result == expected


def test_bom_file():
    test_file: Path = Path(__file__).parent / 'data/bom.py'
    main(
        (
            '--application-directories',
            '.',
            str(test_file),
        ),
    )


def test_non_utf8_file(capsys):
    path = Path(__file__).parent / 'data/non_utf8.py'
    assert main((str(path),)) == 1
    out, _ = capsys.readouterr()
    assert (out == f'{path} is non-utf-8 (not supported)\n')


def test_unresolvable_dir(tmpdir, capsys):
    f = tmpdir.join('f.py')
    f.write_binary('# -*- coding: cp1252 -*-\nx = €\n'.encode('cp1252'))
    with pytest.raises(ValueError):
        main(
            (
                f.strpath,
            ),
        )
