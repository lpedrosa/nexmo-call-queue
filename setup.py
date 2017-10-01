from setuptools import setup


install_requires = ['Flask']
tests_require = ['pytest']

setup(
    name='callqueue',
    version='0.1.0',
    packages=['callqueue'],
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={
        'tests': tests_require
    }
)
