# Python XMP tool

[![Travis CI](https://travis-ci.org/gaqzi/py-xmp-tool.png?branch=master)](https://travis-ci.org/gaqzi/py-xmp-tool)

This is a simple command line utility to read/write single value
fields in XMP files using the [python-xmp-toolkit].

## Usage:

```bash
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
```

Reading a field:

```bash
$ xmp-tool format test.jpg
test.jpg: format=image/jpeg
```

Reading the entire XMP contents of a file

```bash
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
```

Writing a field:

```bash
# First try to read the field when there's no data in it
$ xmp-tool PhysicalMedium test.jpg
test.jpeg: ERROR READING FIELD "PhysicalMedium"

# Then try to add the data and then read the field
$ xmp-tool PhysicalMedium --value lto01 test.jpg
$ xmp-tool PhysicalMedium test.jpg
test.jpg: PhysicalMedium=lto01
```

## Installation

A simple install from pip:

```bash
$ pip install xmp-tool
```

**Note**: [python-xmp-toolkit] depends on [Exempi] which needs to be
  built for XMP to be installed properly.

Use your systems package manager to install [Exempi], on Mac OS X with
homebrew:

```bash
$ brew install exempi
```

[python-xmp-toolkit]: https://github.com/python-xmp-toolkit/python-xmp-toolkit
[Exempi]: http://libopenraw.freedesktop.org/wiki/Exempi/
