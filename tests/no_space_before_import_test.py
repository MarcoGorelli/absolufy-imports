import os
import shutil
from pathlib import Path

from absolufy_imports import main


def test_main(tmpdir):
    source_file: Path = Path(__file__).parent / 'data/baf.py'
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    tmp_file = os.path.join(
        str(tmpdir), 'mypackage', 'mysubpackage', 'baf.py',
    )
    shutil.copy(source_file, tmp_file)

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                os.path.join('mypackage', 'mysubpackage', 'baf.py'),
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        'from mypackage.mysubpackage import O\n'
        '\n'
        'print(T)\n'
        'print(D)\n'
    )
    assert result == expected
