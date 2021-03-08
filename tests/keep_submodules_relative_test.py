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

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--keep-submodules-relative',
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
        'from ..othersubdirectory import quox\n'
        'from mypackage.library2 import qux\n'
        'from mypackage import aaa\n'
        'from datetime import dt\n'
    )
    assert result == expected


def test_already_fixed(tmpdir):
    os.mkdir(os.path.join(tmpdir, 'mypackage'))
    shutil.copytree(
        os.path.join('tests', 'data', 'library1'),
        os.path.join(tmpdir, 'mypackage', 'library1'),
    )
    shutil.copytree(
        os.path.join('tests', 'data', 'library2'),
        os.path.join(tmpdir, 'mypackage', 'library2'),
    )

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--keep-submodules-relative',
                os.path.join(
                    'mypackage', 'library1',
                    'subdirectory', 'bar_fixed.py',
                ),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(
        os.path.join(
            tmpdir, 'mypackage', 'library1',
            'subdirectory', 'bar_fixed.py',
        ),
    ) as fd:
        result = fd.read()

    expected = (
        'from . import baz\n'
        'from .. import foo\n'
        'from mypackage.library2 import qux\n'
        'from mypackage import aaa\n'
    )
    assert result == expected


def test_custom_submodules(tmpdir):
    os.mkdir(os.path.join(tmpdir, 'mypackage'))
    shutil.copytree(
        os.path.join('tests', 'data', 'library1'),
        os.path.join(tmpdir, 'mypackage', 'library1'),
    )
    shutil.copytree(
        os.path.join('tests', 'data', 'library2'),
        os.path.join(tmpdir, 'mypackage', 'library2'),
    )

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--keep-submodules-relative',
                '--submodules',
                '{\".\":[\"mypackage.library1\",\"mypackage.library2\"]}',
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
        'from ..othersubdirectory import quox\n'
        'from mypackage.library2 import qux\n'
        'from mypackage import aaa\n'
        'from datetime import dt\n'
    )
    assert result == expected


def test_custom_submodules_one_missing(tmpdir):
    os.mkdir(os.path.join(tmpdir, 'mypackage'))
    shutil.copytree(
        os.path.join('tests', 'data', 'library1'),
        os.path.join(tmpdir, 'mypackage', 'library1'),
    )
    shutil.copytree(
        os.path.join('tests', 'data', 'library2'),
        os.path.join(tmpdir, 'mypackage', 'library2'),
    )

    cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        main(
            (
                '--keep-submodules-relative',
                '--submodules',
                '{\".\":[\"mypackage.library2\"]}',
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
        'from mypackage.library1.subdirectory import baz\n'
        'from mypackage.library1 import foo\n'
        'from mypackage.library1.othersubdirectory import quox\n'
        'from mypackage.library2 import qux\n'
        'from mypackage import aaa\n'
        'from datetime import dt\n'
    )
    assert result == expected
