from abs_imports import main
import os
import pytest
import shutil

def test_main(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    shutil.copy(os.path.join('tests', 'data', 'bar.py'), os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py'))

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    main(
        (
            os.path.join('mypackage', 'mysubpackage', 'bar.py'),
        )
    )
    os.chdir(cwd)

    with open(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py')) as fd:
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
    shutil.copy(os.path.join('tests', 'data', 'bar.py'), os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py'))

    main(
        (
            '--src',
            str(tmpdir),
            os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py'),
        )
    )

    with open(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py')) as fd:
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
    shutil.copy(os.path.join('tests', 'data', 'bar.py'), os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py'))

    with pytest.raises(ValueError, match=r'File .* cannot be resolved relative to .*'):
        main(
            (
                '--src',
                os.path.join(str(tmpdir), 'otherdir'),
                os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'bar.py'),
            )
        )

def test_noop(tmpdir):
    os.mkdir(os.path.join(str(tmpdir), 'mypackage'))
    os.mkdir(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage'))
    shutil.copy(os.path.join('tests', 'data', 'baz.py'), os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py'))

    main(
        (
            '--src',
            str(tmpdir),
            os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py'),
        )
    )

    with open(os.path.join(str(tmpdir), 'mypackage', 'mysubpackage', 'baz.py')) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 'baz.py')) as fd:
        expected = fd.read()

    assert result == expected
