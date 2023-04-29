RPP
===

RPP is a format used to describe `REAPER <http://reaper.fm>`_ projects. This package is designed to be an RPP
parser/emitter and uses `PLY <http://www.dabeaz.com/ply/>`_ as a parser framework.

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
   Element(tag='REAPER_PROJECT', attrib=['0.1', '4.32', '1372525904'], children=[
       ['RIPPLE', '0'],
       ['GROUPOVERRIDE', '0', '0', '0'],
       ['AUTOXFADE', '1'],
   ])

Transform elements into RPP:

.. code-block:: python

   >>> from rpp import Element
   >>> rpp.dumps(
   ...     Element(tag='REAPER_PROJECT', attrib=['0.1', '4.32', '1372525904'], children=[
   ...         ['RIPPLE', '0'],
   ...         ['GROUPOVERRIDE', '0', '0', '0'],
   ...         ['AUTOXFADE', '1'],
   ...     ]))
   '<REAPER_PROJECT 0.1 4.32 1372525904\n  RIPPLE 0\n  GROUPOVERRIDE 0 0 0\n  AUTOXFADE 1\n>\n'

``Element`` mimics the interface of xml.etree.ElementTree.Element_. You can perform querying operations with
``findall``, ``find``, ``iterfind``. Note that attribute and text predicates are not supported.

.. _xml.etree.ElementTree.Element: https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element

.. code-block:: python

   >>> groupoverride = r.find('.//GROUPOVERRIDE')
   >>> groupoverride
   ['GROUPOVERRIDE', '0', '0', '0']
   >>> groupoverride[1:] = ['9', '9', '9']
   >>> r
   Element(tag='REAPER_PROJECT', attrib=['0.1', '4.32', '1372525904'], children=[
       ['RIPPLE', '0'],
       ['GROUPOVERRIDE', '9', '9', '9'],
       ['AUTOXFADE', '1'],
   ])

Dependencies
------------

- `attrs <https://attrs.readthedocs.org/>`_
- `ply <http://www.dabeaz.com/ply/>`_
