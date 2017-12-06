from setuptools import setup

with open('README.rst') as fp:
    README = fp.read()

setup(
    name='rpp',
    version='0.4',
    description='REAPER Project File Parser',
    long_description=README,
    author='Sviatoslav Abakumov',
    author_email='dust.harvesting@gmail.com',
    license='BSD',
    url='https://github.com/Perlence/rpp',
    download_url='https://github.com/Perlence/rpp/archive/0.3.tar.gz',
    packages=['rpp'],
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'ply',
        'attrs',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing',
    ])
