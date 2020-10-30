from setuptools import setup

setup(
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'ply',
        'attrs',
    ])
