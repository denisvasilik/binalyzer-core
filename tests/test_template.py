import unittest
import pytest
import io

from binalyzer_core import (
    Binalyzer,
    Template,
    ByteOrder,
    AddressingMode,
    ValueProperty,
)


def test_default_instantiation():
    template = Template()
    assert template.name == None
    assert template.parent == None
    assert template.children == ()
    assert template.offset == 0
    assert template.size == 0
    assert template.boundary == 0
    assert template.padding_before == 0
    assert template.padding_after == 0


def test_dynamic_child_attribute_creation():
    node_parent = Template()
    node_child = Template()
    node_child.name = "child_node"
    node_parent.children = (node_child,)
    assert node_parent.child_node.name == "child_node"


def test_parent_instantiation():
    template = Template()
    layout = Template(parent=template)
    assert layout.parent == template


def test_read_value():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    layout = binalyzer.template
    layout.name = "layout"
    layout.offset = 2
    area = Template(name="area", parent=layout)
    area.offset = 1
    field = Template(parent=area)
    field.offset = 4
    field.size = 1
    assert field.value == b"7"


def test_write_value():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    layout = binalyzer.template
    layout.offset = 2
    area = Template(parent=layout)
    area.offset = 3
    field = Template(parent=area)
    field.offset = 2
    field.size = 1
    field.value = b"8"
    assert field.value == b"8"


def test_read_offset_lower_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    lower_boundary_area = binalyzer.template
    lower_boundary_area.offset = 0
    lower_boundary_field = Template(parent=lower_boundary_area)
    lower_boundary_field.offset = 0
    lower_boundary_field.size = 1
    assert lower_boundary_field.value == b"0"


def test_read_offset_upper_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    upper_boundary_area = binalyzer.template
    upper_boundary_area.offset = 7
    upper_boundary_field = Template(parent=upper_boundary_area)
    upper_boundary_field.offset = 0
    upper_boundary_field.size = 1
    assert upper_boundary_field.value == b"7"


def test_read_at_offset_lower_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    lower_boundary_field = binalyzer.template
    lower_boundary_field.offset = 0
    lower_boundary_field.size = 1
    assert lower_boundary_field.value == b"0"


def test_read_at_offset_upper_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    upper_boundary_field = binalyzer.template
    upper_boundary_field.offset = 7
    upper_boundary_field.size = 1
    assert upper_boundary_field.value == b"7"


def test_read_size_min_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    min_boundary_field = binalyzer.template
    min_boundary_field.offset = 0
    min_boundary_field.size = 1
    assert min_boundary_field.value == b"0"


def test_read_size_max_boundary():
    binalyzer = Binalyzer(Template(), io.BytesIO(b"01234567"))
    max_boundary_field = binalyzer.template
    max_boundary_field.offset = 0
    max_boundary_field.size = 8
    assert max_boundary_field.value == b"01234567"


def test_read_walkthrough():
    byte_values = list(range(8))
    binalyzer = Binalyzer(Template(), io.BytesIO(bytes(byte_values)))
    for offset in byte_values:
        field = binalyzer.template
        field.offset = offset
        field.size = 1
        assert field.value == bytes([offset])


def test_template_auto_size():
    binalyzer = Binalyzer()
    template_a = Template('a', parent=binalyzer.template)
    template_a.size = 4
    template_b = Template('b', parent=binalyzer.template)
    template_b.size = 4
    assert binalyzer.template.size == 8
