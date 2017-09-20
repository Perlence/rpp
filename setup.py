#!/usr/bin/python
#
# Copyright (c) 2013 Sviatoslav Abakumov
# 
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 
# 3. This notice may not be removed or altered from any source
#    distribution.

from distutils.core import setup
# rpp attempts to load ply via scanner.py which fails because ply hasn't been installed yet.
# from rpp import __version__

setup(name='rpp',
      # For now, we hardwire the version until we figure out how to avoid the circular reference to ply.
      # version=__version__,
      version='0.3',
      description='REAPER Project File Parser',
      author='Sviatoslav Abakumov',
      author_email='dust.harvesting@gmail.com',
      license='zlib',
      url='https://bitbucket.org/Perlence/rpp/src',
      packages=['rpp'],
      package_dir={'rpp': 'rpp'},
      install_requires=['ply==3.9']
      )
