import os
from shutil import copyfile

import pytest

import xmp

FILES_FOLDER = os.path.join(os.path.dirname(__file__), 'files')
BUBBA_JPG = os.path.join(FILES_FOLDER, 'bubba.jpg')
HELLO_TXT = os.path.join(FILES_FOLDER, 'hello.txt')


@pytest.fixture
def clean_file(request):
    filename = os.tmpnam()
    copyfile(BUBBA_JPG, filename)

    request.addfinalizer(lambda: os.unlink(filename))

    return filename


@pytest.fixture
def clean_file_text(request):
    filename = os.tmpnam()
    copyfile(HELLO_TXT, filename)

    def remove_files():
        os.unlink(filename)
        try:
            os.unlink('{0}.xmp'.format(filename))
        except OSError:
            pass

    request.addfinalizer(remove_files)

    return filename


def test_write_physical_medium(clean_file):
    assert xmp.read_xmp(clean_file, 'PhysicalMedium') is False
    assert xmp.write_xmp(clean_file, 'PhysicalMedium', 'lto01')
    assert xmp.read_xmp(clean_file, 'PhysicalMedium') == 'lto01'


def test_write_physical_medium_to_text_file_should_fail(clean_file_text):
    assert xmp.read_xmp(clean_file_text, 'PhysicalMedium') is False
    assert xmp.write_xmp(clean_file_text, 'PhysicalMedium', 'lto01') is False


def test_write_physical_medium_to_text_with_sidecar(clean_file_text):
    assert xmp.read_xmp(clean_file_text, 'PhysicalMedium') is False

    sidecar_file = xmp.write_xmp(clean_file_text, 'PhysicalMedium', 'lto01',
                                 sidecar=True)

    assert sidecar_file == '{0}.xmp'.format(clean_file_text)
    assert os.path.exists(sidecar_file)

    assert xmp.read_xmp(clean_file_text, 'PhysicalMedium') == 'lto01'
    assert xmp.read_xmp(clean_file_text, 'Test') is False


def test_read_back_entire_xmp_data_from_sidecar(clean_file_text):
    xmp.write_xmp(clean_file_text, 'PhysicalMedium', 'lto01', sidecar=True)

    assert 'lto01' in xmp.read_xmp(clean_file_text)


def test_read_back_entire_xmp_data(clean_file):
    xmp.write_xmp(clean_file, 'PhysicalMedium', 'lto01')

    assert 'lto01' in xmp.read_xmp(clean_file)


def test_write_to_sidecar_file_again(clean_file_text):
    xmp.write_xmp(clean_file_text, 'PhysicalMedium', 'lto01', sidecar=True)
    xmp.write_xmp(clean_file_text, 'format', 'text/plain', sidecar=True)

    assert xmp.read_xmp(clean_file_text, 'PhysicalMedium') == 'lto01'
    assert xmp.read_xmp(clean_file_text, 'format') == 'text/plain'
