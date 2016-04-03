from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

version = "0.0.1"

TEST_DEPENDENCIES = ['nose',
                     'WebTest']


setup(
    name='tgext.utils',
    version=version,
    description="Collection of utilities for TurboGears2",
    long_description=README,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='turbogears2.extension',
    author='Alessandro Molina',
    author_email='amol@turbogears.org',
    url='https://github.com/amol-/tgext.utils',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages = ['tgext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "TurboGears2 >= 2.3.7",
    ],
    tests_require=TEST_DEPENDENCIES,
    extras_require={
        # Used by Travis and Coverage due to setup.py nosetests
        # causing a coredump when used with coverage
        'testing': TEST_DEPENDENCIES,
    },
    test_suite='nose.collector',
    entry_points="""
    # -*- Entry points: -*-
    """
)
