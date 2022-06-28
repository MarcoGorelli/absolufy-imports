import os
import shutil

from absolufy_imports import get_module_paths
from absolufy_imports import main
from absolufy_imports import to_absolute_imports


# pytest -s -v tests/package_for_conversion_test.py


# pytest -s -v tests/package_for_conversion_test.py::test_get_module_paths
def test_get_module_paths(tmpdir):

    cwd = os.getcwd()
    assert os.path.isdir(tmpdir)

    srcpkgpath = os.path.join(cwd, "tests", "data", "package")
    assert os.path.isdir(srcpkgpath)
    pkgpath = os.path.join(tmpdir, "package")
    shutil.copytree(srcpkgpath, pkgpath)
    assert os.path.exists(pkgpath)

    os.chdir(str(tmpdir))

    module_paths = get_module_paths(package_name="package")

    assert len(module_paths) == 2

    for path in module_paths:
        assert os.path.exists(path)

    shutil.rmtree(pkgpath)
    os.chdir(cwd)


# pytest -s -v tests/package_for_conversion_test.py::test_to_absolute_imports
def test_to_absolute_imports(tmpdir):

    cwd = os.getcwd()
    srcpkgpath = os.path.join(cwd, "tests", "data", "package")
    pkgpath = os.path.join(tmpdir, "package")
    shutil.copytree(srcpkgpath, pkgpath)
    assert os.path.exists(pkgpath)

    os.chdir(str(tmpdir))

    module_paths = to_absolute_imports("package")

    assert len(module_paths) == 2

    for path in module_paths:
        assert os.path.exists(path)
        if path.endswith("n3_module.py"):
            with open(path, "r") as f:
                flines = f.readlines()
            assert "from package.n2.n2_module import func3" == flines[0].strip()

    shutil.rmtree(pkgpath)
    os.chdir(cwd)


# pytest -s -v tests/package_for_conversion_test.py::test_main_with_package_flag
def test_main_with_package_flag(tmpdir):

    cwd = os.getcwd()
    srcpkgpath = os.path.join(cwd, "tests", "data", "package")
    pkgpath = os.path.join(tmpdir, "package")
    shutil.copytree(srcpkgpath, pkgpath)
    assert os.path.exists(pkgpath)

    os.chdir(str(tmpdir))

    main(
        (
            "--package",
            "package",
        ),
    )

    module_paths = get_module_paths(package_name="package")

    for path in module_paths:
        assert os.path.exists(path)
        if path.endswith("n3_module.py"):
            with open(path, "r") as f:
                flines = f.readlines()
            assert "from package.n2.n2_module import func3" == flines[0].strip()

    shutil.rmtree(pkgpath)
    os.chdir(cwd)
