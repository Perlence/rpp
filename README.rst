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
   [('REAPER_PROJECT', Decimal(0.1), '4.32', 1372525904), ('RIPPLE', 0), ('GROUPOVERRIDE', 0, 0, 0), ('AUTOXFADE', 1)]

Transform lists into RPP:

.. code-block:: python

   >>> rpp.dumps(
   [('REAPER_PROJECT', 0.1, '4.32', 1372525904),
    ('RIPPLE', 0),
    ('GROUPOVERRIDE', 0, 0, 0),
    ('AUTOXFADE', 1)
   ])
   '<REAPER_PROJECT 0.1 "4.32" 1372525904\n  RIPPLE 0\n  GROUPOVERRIDE 0 0 0\n  AUTOXFADE 1\n>'

You can also perform some quering operations:

.. code-block:: python

   >>> rpp.find(r, 'GROUPOVERRIDE')
   ((2,), ('GROUPOVERRIDE', 0, 0, 0))

The result is a tuple with first element as tuple of tree indexes and second as the found value.

To change the value of an item, do the following:

.. code-block:: python

   >>> rpp.update(r, [1], ('RIPPLE', 1))
   >>> r
   [('REAPER_PROJECT', 0.1, '4.32', 1372525904), ('RIPPLE', 1), ('GROUPOVERRIDE', 0, 0, 0), ('AUTOXFADE', 1)]


Dependencies
------------

- ply


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
