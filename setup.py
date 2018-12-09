import sys

from setuptools import find_packages, setup

# Depend on pytest_runner only when the tests are actually invoked
needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []

setup_requires = pytest_runner

setup(
    name='kombu-django',
    version='1.0.0',
    packages=find_packages(exclude=('tests',)),
    install_requires=['django', 'kombu'],
    setup_requires=setup_requires,
    tests_require=['pytest', 'case'],
)
