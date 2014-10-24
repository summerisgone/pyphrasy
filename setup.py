#!/usr/bin/env python
# coding: utf-8

import io
import os
import unittest

from setuptools import setup
from setuptools.command.test import test as TestCommand


with io.open(os.path.join(os.path.dirname(__file__), 'README.md'),
             encoding='utf') as f:
    readme = f.read()


class PyTest(TestCommand):
    # see http://pytest.org/latest/goodpractises.html#integration-with-setuptools-distribute-test-commands

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded

        x = unittest.defaultTestLoader.discover('.', 'test.py')
        return unittest.TextTestRunner().run(x)


def recursive(root):
    return ['%s/%s' % (dir, x) for dir, subdirs, files  in os.walk(root) for x in  files]

setup(
    # overview
    name='pyphrasy',
    description='Inflection russian collocations based on pymorphy2',
    long_description=readme,

    # technical info
    version='0.1',
    packages=['pyphrasy'],
    provides=['pyphrasy'],
    package_dir={'pyphrasy': '.'},
    package_data={'pyphrasy': recursive('./static')+recursive('./templates')},

    # testing
    cmdclass={'test': PyTest},

    # copyright
    license='GNU Lesser General Public License (LGPL), Version 3',

    # more info
    url='https://github.com/summerisgone/pyphrasy',

    # categorization
    keywords=('pyhprasy pymorphy inflection phrases'),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
