run-tests:
	pytest tests/*_test.py

install:
	pip3 uninstall -y absolufy_imports
	python3 setup.py bdist_wheel sdist
	pip3 install dist/absolufy_imports-0.3.1-py2.py3-none-any.whl



