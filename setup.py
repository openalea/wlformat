#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Objects descriptions for workflow related environments"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/openalea/wlformat/version.py
version = {}
with open("src/openalea/wlformat/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='openalea.wlformat',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="openalea, ",
    author_email="revesansparole@gmail.com, ",
    url='https://github.com/openalea/wlformat',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "jsonschema",
        "svgwrite",
        ],
    tests_require=[
        "coverage",
        "flake8",
        "mock",
        "nose",
        "sphinx",
        "coveralls",
        ],
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['wralea'] = ['openalea.wlformat = openalea.wlformat_wralea']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
