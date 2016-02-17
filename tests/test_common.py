# coding=utf-8
"""
Module
"""
from __future__ import absolute_import

import pytest

from datacube.ui.common import get_metadata_path, _find_any_metadata_suffix
from . import util
from datacube.utils import attrs_all_equal


def test_find_metadata_path():
    files = util.write_files({
        'directory_dataset': {
            'file1.txt': '',
            'file2.txt': '',
            'agdc-metadata.yaml.gz': ''
        },
        'file_dataset.tif': '',
        'file_dataset.tif.agdc-md.yaml': '',
        'dataset_metadata.yaml': '',
        'no_metadata.tif': '',
    })

    # A metadata file can be specified directly.
    path = get_metadata_path(files.joinpath('dataset_metadata.yaml'))
    assert path.absolute() == files.joinpath('dataset_metadata.yaml').absolute()

    # A dataset directory will have an internal 'agdc-metadata' file.
    path = get_metadata_path(files.joinpath('directory_dataset'))
    assert path.absolute() == files.joinpath('directory_dataset', 'agdc-metadata.yaml.gz').absolute()

    # Other files can have a sibling file ending in 'agdc-md.yaml'
    path = get_metadata_path(files.joinpath('file_dataset.tif'))
    assert path.absolute() == files.joinpath('file_dataset.tif.agdc-md.yaml').absolute()

    # Lack of metadata raises an error.
    with pytest.raises(ValueError):
        get_metadata_path(files.joinpath('no_metadata.tif'))

    # Nonexistent dataset raises a ValueError.
    with pytest.raises(ValueError):
        get_metadata_path(files.joinpath('missing-dataset.tif'))


def test_find_any_metatadata_suffix():
    files = util.write_files({
        'directory_dataset': {
            'file1.txt': '',
            'file2.txt': '',
            'agdc-metadata.json.gz': ''
        },
        'file_dataset.tif.agdc-md.yaml': '',
        'dataset_metadata.YAML': '',
        'no_metadata.tif': '',
    })

    path = _find_any_metadata_suffix(files.joinpath('dataset_metadata'))
    assert path.absolute() == files.joinpath('dataset_metadata.YAML').absolute()

    path = _find_any_metadata_suffix(files.joinpath('directory_dataset', 'agdc-metadata'))
    assert path.absolute() == files.joinpath('directory_dataset', 'agdc-metadata.json.gz').absolute()

    path = _find_any_metadata_suffix(files.joinpath('file_dataset.tif.agdc-md'))
    assert path.absolute() == files.joinpath('file_dataset.tif.agdc-md.yaml').absolute()

    # Returns none if none exist
    path = _find_any_metadata_suffix(files.joinpath('no_metadata'))
    assert path is None


def test_attrs_all_equal():
    class Bunch:
        def __init__(self, **kwds):
            self.__dict__.update(kwds)

    all_equal = [Bunch(a=1), Bunch(a=1), Bunch(a=1)]
    assert attrs_all_equal(all_equal, 'a')

    not_all_equal = [Bunch(a=1), Bunch(a=2)]
    assert not attrs_all_equal(not_all_equal, 'a')

    missing = [Bunch(a=1), Bunch()]
    assert not attrs_all_equal(missing, 'a')
