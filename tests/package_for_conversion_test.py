import os
import shutil

from absolufy_imports import get_module_paths
from absolufy_imports import main
from absolufy_imports import to_absolute_imports


# pytest -s -v tests/package_for_conversion_test.py


# pytest -s -v tests/package_for_conversion_test.py::test_get_module_paths
def test_get_module_paths():

    module_paths = get_module_paths(package_name='package')

    assert sorted(module_paths) == sorted(
        ['./package/n2/n2_module.py', './package/n2/n3/n3_module.py'],
    )

    for path in module_paths:
        assert os.path.exists(path)


# pytest -s -v tests/package_for_conversion_test.py::test_to_absolute_imports
def test_to_absolute_imports():

    shutil.copytree('./package', './pkg')

    to_absolute_imports('pkg')

    with open('./pkg/n2/n3/n3_module.py') as f:
        flines = f.readlines()

    assert 'from pkg.n2.n2_module import func3' == flines[0].strip()

    shutil.rmtree('./pkg')


# pytest -s -v tests/package_for_conversion_test.py::test_main_with_package_flag
def test_main_with_package_flag():

    shutil.copytree('./package', './pkg')

    main(
        (
            '--package',
            'pkg',
        ),
    )

    with open('./pkg/n2/n3/n3_module.py') as f:
        flines = f.readlines()

    assert 'from pkg.n2.n2_module import func3' == flines[0].strip()

    shutil.rmtree('./pkg')
