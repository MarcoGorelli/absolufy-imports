import os
import shutil

from absolufy_imports import main


def test_main(tmpdir):
    os.mkdir(os.path.join(tmpdir, 'mypackage'))
    shutil.copytree(
        os.path.join('tests', 'data', 'library1'),
        os.path.join(tmpdir, 'mypackage', 'library1'),
    )
    shutil.copytree(
        os.path.join('tests', 'data', 'library2'),
        os.path.join(tmpdir, 'mypackage', 'library2'),
    )
    with open(os.path.join(tmpdir, 'otherpackage.py'), 'w') as fd:
        fd.write('A = 3')

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--never',
                os.path.join(
                    'mypackage', 'library1',
                    'subdirectory', 'bar.py',
                ),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(
        os.path.join(
            tmpdir, 'mypackage', 'library1',
            'subdirectory', 'bar.py',
        ),
    ) as fd:
        result = fd.read()

    expected = (
        'from . import baz\n'
        'from .. import foo\n'
        'from mypackage.library1.othersubdirectory import quox\n'
        'from ...library2 import qux\n'
        'from ... import aaa\n'
        'from datetime import dt\n'
        'from otherpackage import A\n'
    )
    assert result == expected


def test_main_src(tmpdir):
    os.mkdir(os.path.join(tmpdir, 'src'))
    os.mkdir(os.path.join(tmpdir, 'src', 'mypackage'))
    shutil.copytree(
        os.path.join('tests', 'data', 'library1'),
        os.path.join(tmpdir, 'src', 'mypackage', 'library1'),
    )
    shutil.copytree(
        os.path.join('tests', 'data', 'library2'),
        os.path.join(tmpdir, 'src', 'mypackage', 'library2'),
    )
    with open(os.path.join(tmpdir, 'src', 'otherpackage.py'), 'w') as fd:
        fd.write('A = 3')

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--never',
                os.path.join(
                    'src', 'mypackage', 'library1',
                    'subdirectory', 'bar.py',
                ),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(
        os.path.join(
            tmpdir, 'src', 'mypackage', 'library1',
            'subdirectory', 'bar.py',
        ),
    ) as fd:
        result = fd.read()

    expected = (
        'from . import baz\n'
        'from .. import foo\n'
        'from mypackage.library1.othersubdirectory import quox\n'
        'from ...library2 import qux\n'
        'from ... import aaa\n'
        'from datetime import dt\n'
        'from otherpackage import A\n'
    )
    assert result == expected
