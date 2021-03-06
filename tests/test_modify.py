"""
    test_transform
    ~~~~~~~~~~~~~~

    This module implements tests for Binalyzer's transformation module.
"""
import io
import pytest

from binalyzer_core import (
    Binalyzer,
    Template,
)


@pytest.fixture
def binalyzer():
    return Binalyzer()


def test_transform_identity():
    source_data = io.BytesIO(bytes([0x11] * 8) +
                             bytes([0x22] * 8) +
                             bytes([0x33] * 8) +
                             bytes([0x44] * 8))

    expected_bytes = (bytes([0x11] * 8) +
                      bytes([0x22] * 8) +
                      bytes([0x33] * 8) +
                      bytes([0x44] * 8))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)
    destination_e = Template(name='e', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 8
    destination_c.size = 8
    destination_d.size = 8
    destination_e.size = 8

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform():
    source_data = io.BytesIO(bytes([0x11] * 8) +
                             bytes([0x22] * 8) +
                             bytes([0x33] * 8) +
                             bytes([0x44] * 8))

    expected_bytes = (bytes([0x22] * 8) +
                      bytes([0x44] * 8) +
                      bytes([0x00] * 8) +
                      bytes([0x00] * 8))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='c', parent=destination_template)
    destination_c = Template(name='e', parent=destination_template)
    destination_d = Template(name='i', parent=destination_template)
    destination_e = Template(name='j', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 8
    destination_c.size = 8
    destination_d.size = 8
    destination_e.size = 8

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform_add_template():
    source_data = io.BytesIO(bytes([0x11] * 8) +
                             bytes([0x22] * 8) +
                             bytes([0x33] * 8) +
                             bytes([0x44] * 8))

    expected_bytes = (bytes([0x11] * 8) +
                      bytes([0x22] * 8) +
                      bytes([0x33] * 8) +
                      bytes([0x44] * 8) +
                      bytes([0x00] * 8))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)
    destination_e = Template(name='e', parent=destination_template)
    destination_f = Template(name='f', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 8
    destination_c.size = 8
    destination_d.size = 8
    destination_e.size = 8
    destination_f.size = 8

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform_remove_template():
    source_data = io.BytesIO(bytes([0x11] * 8) +
                             bytes([0x22] * 8) +
                             bytes([0x33] * 8) +
                             bytes([0x44] * 8))

    expected_bytes = (bytes([0x11] * 8) +
                      bytes([0x22] * 8) +
                      bytes([0x33] * 8))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 8
    destination_c.size = 8
    destination_d.size = 8

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform_shrink_template():
    source_data = io.BytesIO(bytes([0x01] * 8) +
                             bytes([0x02] * 8) +
                             bytes([0x03] * 8) +
                             bytes([0x04] * 8))

    expected_bytes = (bytes([0x01] * 4) +
                      bytes([0x02] * 5) +
                      bytes([0x03] * 6) +
                      bytes([0x04] * 7))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)
    destination_e = Template(name='e', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 4
    destination_c.size = 5
    destination_d.size = 6
    destination_e.size = 7

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform_grow_template():
    source_data = io.BytesIO(bytes([0x11] * 8) +
                             bytes([0x22] * 8) +
                             bytes([0x33] * 8) +
                             bytes([0x44] * 8))

    expected_bytes = (bytes([0x11] * 8) +
                      bytes([0x00] * 8) +
                      bytes([0x22] * 8) +
                      bytes([0x00] * 7) +
                      bytes([0x33] * 8) +
                      bytes([0x00] * 6) +
                      bytes([0x44] * 8) +
                      bytes([0x00] * 5))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)
    destination_e = Template(name='e', parent=destination_template)

    binalyzer.project(binalyzer.template, destination_template)

    destination_b.size = 16
    destination_c.size = 15
    destination_d.size = 14
    destination_e.size = 13

    binalyzer.aggregate(destination_template)

    assert destination_template.value == expected_bytes


def test_transform_property_override(binalyzer):
    source_data = io.BytesIO(bytes([0x01] * 8) +
                             bytes([0x02] * 8) +
                             bytes([0x03] * 8) +
                             bytes([0x04] * 8))

    expected_bytes = (bytes([0x01] * 4) +
                      bytes([0x02] * 5) +
                      bytes([0x03] * 6) +
                      bytes([0x04] * 7))

    source_template = Template(name='a')
    source_b = Template(name='b', parent=source_template)
    source_c = Template(name='c', parent=source_template)
    source_d = Template(name='d', parent=source_template)
    source_e = Template(name='e', parent=source_template)

    binalyzer = Binalyzer()
    binalyzer.data = source_data
    binalyzer.template = source_template

    source_b.size = 8
    source_c.size = 8
    source_d.size = 8
    source_e.size = 8

    destination_template = Template(name='a')
    destination_b = Template(name='b', parent=destination_template)
    destination_c = Template(name='c', parent=destination_template)
    destination_d = Template(name='d', parent=destination_template)
    destination_e = Template(name='e', parent=destination_template)

    destination_b.size = 4
    destination_c.size = 5
    destination_d.size = 6
    destination_e.size = 7

    binalyzer.transform(binalyzer.template, destination_template)

    assert destination_template.value == expected_bytes
