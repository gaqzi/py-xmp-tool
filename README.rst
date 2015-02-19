===============
Python XMP tool
===============

.. image:: https://travis-ci.org/gaqzi/py-xmp-tool.png?branch=master
           :target: https://travis-ci.org/gaqzi/py-xmp-tool

.. image:: https://pypip.in/version/xmp-tool/badge.png
           :target: https://pypi.python.org/pypi/xmp-tool/
           :alt: Latest Version

.. image:: https://pypip.in/download/xmp-tool/badge.png
           :target: https://pypi.python.org/pypi/xmp-tool/
           :alt: Downloads

This is a simple command line utility to read/write single value
fields in XMP files using the `python-xmp-toolkit`_.

Installation
------------

A simple install from pip:

.. code-block:: shell

      $ pip install xmp-tool

**Note**: `python-xmp-toolkit`_ depends on `Exempi`_ which needs to be
  built for XMP to be installed properly.

Use your systems package manager to install `Exempi`_, on Mac OS X with
homebrew:

.. code-block:: shell

      $ brew install exempi

On a Debian based Linux system do:

.. code-block:: shell

      # apt-get install libexempi-dev

Usage:
------

.. code-block:: shell

      $ xmp-tool -h
      usage: xmp-tool [-h] [--value VALUE] [--no-sidecar] [field] file [file ...]

      Read or write XMP fields in a file

      positional arguments:
        field          The field to read/write. If no field specified entire XMP
                       document printed.
        file           A file to work on

      optional arguments:
        -h, --help     show this help message and exit
        --value VALUE  A value to write to the field specified
        --no-sidecar   Never write to sidecar files.

Reading a field:

.. code-block:: shell

      $ xmp-tool format test.jpg
      test.jpg: format=image/jpeg

Reading the entire XMP contents of a file:

.. code-block:: shell

      $ xmp-tool test.jpg
      test.jpg: None=<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
      <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Exempi + XMP Core 5.1.2">
       <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about=""
          xmlns:dc="http://purl.org/dc/elements/1.1/">
         <dc:PhysicalMedium>lto01</dc:PhysicalMedium>
        </rdf:Description>
       </rdf:RDF>
      </x:xmpmeta>
      <?xpacket end="w"?>

Writing a field:

.. code-block:: shell

      # First try to read the field when there's no data in it
      $ xmp-tool PhysicalMedium test.jpg
      test.jpeg: ERROR READING FIELD "PhysicalMedium"

      # Then try to add the data and then read the field
      $ xmp-tool PhysicalMedium --value lto01 test.jpg
      $ xmp-tool PhysicalMedium test.jpg
      test.jpg: PhysicalMedium=lto01

.. _python-xmp-toolkit: https://github.com/python-xmp-toolkit/python-xmp-toolkit
.. _Exempi: http://libopenraw.freedesktop.org/wiki/Exempi/
