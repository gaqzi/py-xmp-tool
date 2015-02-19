.PHONY : test clean default lint-rst upload-package clean-build clean-pyc

default: test

test:
	tox

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name __pycache__ -exec rm -rf {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean: clean-pyc clean-build

lint-rst:
	pip install restructuredtext_lint
	rst-lint README.rst

upload-package: test lint-rst clean
	pip install twine wheel
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*
