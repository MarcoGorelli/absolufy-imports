import os
import shutil

from absolufy_imports import main


def test_bom(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir),
        'mypackage',
        'mysubpackage',
        'bar.py',
    )
    # write file with a BOM at start
    with open(os.path.join('tests', 'data', 'bar.py'), 'rb') as src:
        with open(tmp_file, 'wb') as dst:
            dst.write('\ufeff'.encode())
            dst.write(src.read())

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (os.path.join('mypackage', 'mysubpackage', 'bar.py'),),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        '\ufeff'
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


def test_crlf(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir),
        'mypackage',
        'mysubpackage',
        'bar.py',
    )
    # re-write as CRLF
    with open(os.path.join('tests', 'data', 'bar.py')) as src:
        with open(tmp_file, 'w', newline='\r\n') as dst:
            dst.write(src.read())

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (os.path.join('mypackage', 'mysubpackage', 'bar.py'),),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file, newline='') as fd:
        result = fd.read()

    expected = (
        'from mypackage.mysubpackage import B\r\n'
        'from mypackage.mysubpackage.bar import baz\r\n'
        'from mypackage.foo import T\r\n'
        'from mypackage.mysubpackage.bar import D\r\n'
        'from mypackage.mysubpackage import O\r\n'
        'from datetime import datetime\r\n'
        '\r\n'
        'print(T)\r\n'
        'print(D)\r\n'
    )
    assert result == expected
