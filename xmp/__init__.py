#!/usr/bin/env python
import os

from libxmp import XMPFiles, consts, XMPError
from libxmp.core import XMPMeta


def write_xmp_sidecar(filename, field, value):
    """Writes field to a XMP sidecar file

    Args:
      filename (str): The full path to the base file to write
         (without .xmp extension)
      field (str)
      value (str)

    Returns:
      The path to the newly written sidecar .xmp file
    """
    sidecar_path = '{0}.xmp'.format(filename)
    xmp = XMPMeta()

    if os.path.exists(sidecar_path):
        with open(sidecar_path, 'r') as f:
            xmp.parse_from_str(f.read())

    xmp.set_property(consts.XMP_NS_DC, field, value)

    with open(sidecar_path, 'w+') as f:
        f.write(str(xmp))

    return sidecar_path


def read_xmp_sidecar(filename, field=None):
    """Reads a field, or the entire XMP file, and returns it

    Args:
      filename (str): The full path to the base file to read
          (without .xmp extension)
      field (str|None)

    Returns:
      If ``field`` is None return the entire XMP content, else the
      value of the field specified or False if no value found.
    """
    xmp = XMPMeta()
    with open(filename, 'r') as f:
        if field is None:
            return f.read()
        else:
            xmp.parse_from_str(f.read())

    try:
        return xmp.get_property(consts.XMP_NS_DC, field)
    except XMPError:
        return False


def write_xmp(filename, field, value, sidecar=False):
    """Write a field into a files XMP store, if sidecar is True and the
    file format doesn't support writing inline a sidecar .xmp file
    will be created.

    Args:
      filename (str): The full path to file read to write XMP data into
      field (str|None)
      sidecar (bool): If True and the file doesn't support XMP inline a
          .xmp file with the same name as the ``filename`` will be
          created with an .xmp extension. Example: test.txt -> test.txt.xmp

    Returns:
      On success: The path to the file written
      On failure: False

    """
    xmpfile = XMPFiles(file_path=filename, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    if xmp is None and sidecar:
        return write_xmp_sidecar(filename, field, value)
    elif xmp is None:
        return False

    xmp.set_property(consts.XMP_NS_DC, field, value)

    if xmpfile.can_put_xmp(xmp):
        xmpfile.put_xmp(xmp)
        xmpfile.close_file()
        return filename
    else:
        return False


def read_xmp(filename, field=None):
    """Reads a field, or the entire XMP file, and returns it. If the field
    cannot be found inside the file and there exists a sidecar file
    then the sidecar file will also be searched for the field.

    Args:
      filename (str): The full path to the base file to read
          (without .xmp extension)
      field (str|None)

    Returns:
      If ``field`` is None return the entire XMP content, else the
      value of the field specified or False if no value found.

    """
    xmpfile = XMPFiles(file_path=filename, open_onlyxmp=True)
    xmp = xmpfile.get_xmp()
    sidecar = '{0}.xmp'.format(filename)

    if field is None and xmp:
        return str(xmp)
    elif field is None and xmp is None:
        if os.path.exists(sidecar):
            return read_xmp_sidecar(sidecar, field=None)
        else:
            return False

    try:
        return xmp.get_property(consts.XMP_NS_DC, field)
    except (AttributeError, XMPError):
        if os.path.exists(sidecar):
            return read_xmp_sidecar(sidecar, field)
        else:
            return False


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Read or write XMP fields in a file'
    )
    parser.add_argument('--value', dest='value', type=str, action='store',
                        help='A value to write to the field specified')
    parser.add_argument('--no-sidecar', dest='sidecar',
                        action='store_false', default=True,
                        help='Never write to sidecar files.')
    parser.add_argument('field', metavar='field', type=str, action='store',
                        help=('The field to read/write. If no field '
                              'specified entire XMP document printed.'),
                        nargs='?')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='A file to work on')

    args = parser.parse_args()
    field_reading_error = False
    for filename in args.files:
        if args.value:
            if not write_xmp(filename, args.field, args.value,
                             sidecar=args.sidecar):
                sys.stderr.write('error writing file: "{0}"'.format(filename))
                exit(1)
        else:
            val = read_xmp(filename, args.field)
            if val:
                print '{0}: {1}={2}'.format(filename, args.field, val)
            else:
                sys.stderr.write('{0}: ERROR READING FIELD "{1}"\n'.format(
                    filename,
                    args.field
                ))
                field_reading_error = True

    if field_reading_error:
        exit(2)


if __name__ == '__main__':
    main()
