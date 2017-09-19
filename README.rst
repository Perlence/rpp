RPP
===

Description
-----------

RPP is a format used to describe `REAPER <http://reaper.fm>`_ projects. This package is designed to be RPP
parser/emitter and uses PLY as parser framework. It understands the following RPP data types: integer, float, string,
uuid, symbolic data (base64).


Examples
--------

Import the package:

.. code-block:: python

   >>> import rpp

Decode RPP:

.. code-block:: python

   >>> r = rpp.loads("""\
   <REAPER_PROJECT 0.1 "4.32" 1372525904
     RIPPLE 0
     GROUPOVERRIDE 0 0 0
     AUTOXFADE 1
   >
   """)
   >>> r
   Element(tag='REAPER_PROJECT', attrib=(Decimal('0.1'), '4.32', 1372525904), children=[
       Element(tag='RIPPLE', attrib=(0,), children=None),
       Element(tag='GROUPOVERRIDE', attrib=(0, 0, 0), children=None),
       Element(tag='AUTOXFADE', attrib=(1,), children=None)
   ])

Transform elements into RPP:

.. code-block:: python

   >>> from decimal import Decimal
   >>> from rpp import Element
   >>> rpp.dumps(
   ...     Element(tag='REAPER_PROJECT', attrib=(Decimal('0.1'), '4.32', 1372525904), children=[
   ...         Element(tag='RIPPLE', attrib=(0,), children=None),
   ...         Element(tag='GROUPOVERRIDE', attrib=(0, 0, 0), children=None),
   ...         Element(tag='AUTOXFADE', attrib=(1,), children=None),
   ...     ]))
   '<REAPER_PROJECT 0.1 4.32 1372525904\n  RIPPLE 0\n  GROUPOVERRIDE 0 0 0\n  AUTOXFADE 1\n>\n'

``Element`` mimics the interface of ``xml.etree.ElementTree.Element``. You can perform quering operations with
``findall``, ``find``, ``iterfind``:

.. code-block:: python

   >>> r.find('.//GROUPOVERRIDE')
   Element(tag='GROUPOVERRIDE', attrib=(0, 0, 0), children=None)


Dependencies
------------

- `attrs <https://attrs.readthedocs.org/>`_
- `ply <http://www.dabeaz.com/ply/>`_


License
-------

Copyright (c) 2013-2017 Sviatoslav Abakumov

This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable
for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter it
and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If
   you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not
   required.

2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original
   software.

3. This notice may not be removed or altered from any source distribution.
