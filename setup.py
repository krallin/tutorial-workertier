#!/usr/bin/env python
#coding:utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
execfile('httpcache/version.py') # Load version

setup(
    name='httpcache',
    version=__version__,
    description='An utility package to locate the latest Ubuntu AMIs.',
    author='Thomas Orozco',
    author_email='thomas@scalr.com',
    url='https://github.com/scalr/tutorial-httpcache',
    packages=[
        'httpcache', 'httpcache.backends', 'httpcache.backends.cache', 'httpcache.backends.dispatcher'
    ],
    package_dir={'httpcache': 'httpcache'},
    include_package_data=True,
    install_requires=["gevent", "pymemcache", "haigha"],
    license="Apache 2",
    entry_points={
        'console_scripts': [
            'httpcache = httpcache.cli:cli',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
