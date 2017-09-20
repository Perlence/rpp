from setuptools import setup

setup(
    name='rpp',
    version='0.1',
    description='REAPER Project File Parser',
    author='Sviatoslav Abakumov',
    author_email='dust.harvesting@gmail.com',
    license='BSD',
    url='https://github.com/Perlence/rpp',
    packages=['rpp'],
    install_requires=[
        'ply',
        'attrs',
    ])
