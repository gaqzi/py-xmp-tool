# encoding: utf-8
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='xmp-tool',
    version='0.9.0',
    packages=['xmp'],
    license='BSD License',
    description='CLI utility to read/write XMP fields in files',
    long_description=README,
    url='https://github.com/gaqzi/py-xmp-tool',
    author='Björn Andersson',
    author_email='ba@sanitarium.se',
    entry_points={
        'console_scripts': (
            'xmp-tool = xmp:main'
        ),
    },
    install_requires=(
        'python-xmp-toolkit>=2.0.1',
    ),
    tests_require=(
        'pytest',
        'pytest-xdist'
    ),
    cmdclass = {'test': PyTest},
    classifiers=(
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ),
)
