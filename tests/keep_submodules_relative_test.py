import os
import shutil
from pathlib import Path

import pytest

from absolufy_imports import main


@pytest.fixture()
def copy_data(tmp_path):
    def _make_copy(src=''):
        base_path = Path(os.path.dirname(__file__))
        target_path = tmp_path
        if src:
            target_path = tmp_path / src
        (target_path / 'mypackage').mkdir(parents=True)
        shutil.copytree(
            base_path / 'data' / 'library1',
            target_path / 'mypackage' / 'library1',
        )
        shutil.copytree(
            base_path / 'data' / 'library2',
            target_path / 'mypackage' / 'library2',
        )
        return target_path

    return _make_copy


expected_never = (
    'from . import baz\n'
    'from . import foo2\n'
    'from .. import foo\n'
    'from mypackage.library1.othersubdirectory import quox\n'
    'from ...library2 import qux\n'
    'from ... import aaa\n'
    'from datetime import dt\n'
    'from otherpackage import A\n'
)


@pytest.mark.parametrize('src', ['', 'src'])
def test_main(tmp_path, copy_data, src):
    target_path = copy_data(src)
    with (target_path / 'otherpackage.py').open('w') as fd:
        fd.write('A = 3')

    cwd = os.getcwd()
    os.chdir(tmp_path)
    file_path = \
        target_path / 'mypackage' / 'library1' / 'subdirectory' / 'bar.py'
    try:
        main(
            (
                '--never',
                str(file_path),
            ),
        )
    finally:
        os.chdir(cwd)

    result = file_path.read_text()

    assert result == expected_never


expected_local = (
    'from . import baz\n'
    'from . import foo2\n'
    'from mypackage.library1 import foo\n'
    'from mypackage.library1.othersubdirectory import quox\n'
    'from mypackage.library2 import qux\n'
    'from mypackage import aaa\n'
    'from datetime import dt\n'
    'from otherpackage import A\n'
)


@pytest.mark.parametrize('src', ['', 'src'])
def test_main_local(tmp_path, copy_data, src):
    target_path = copy_data(src)
    with (target_path / 'otherpackage.py').open('w') as fd:
        fd.write('A = 3')

    cwd = os.getcwd()
    os.chdir(tmp_path)
    file_path = \
        target_path / 'mypackage' / 'library1' / 'subdirectory' / 'bar.py'
    try:
        main(
            (
                '--allow_local',
                str(file_path),
            ),
        )
    finally:
        os.chdir(cwd)

    result = file_path.read_text()

    assert result == expected_local
