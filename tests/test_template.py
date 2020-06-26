import unittest
import pytest
import io

from binalyzer_core import (
    BindingContext,
    Template,
    ByteOrder,
    AddressingMode,
    ResolvableValue,
    SimpleTemplateProvider,
    SimpleDataProvider,
)


def test_default_instantiation():
    template = Template()
    assert template.name == None
    assert template.parent == None
    assert template.children == ()
    assert template.addressing_mode.value == AddressingMode.Relative.value
    assert template.offset.value == 0
    assert template.size.value == 0
    assert template.boundary.value == 0
    assert template.padding_before.value == 0
    assert template.padding_after.value == 0


def test_add_child():
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
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    layout = template_provider_mock.template
    layout.binding_context = binding_context
    layout.offset = ResolvableValue(2)
    area = Template(parent=layout)
    area.offset = ResolvableValue(1)
    field = Template(parent=area)
    field.offset = ResolvableValue(4)
    field.size = ResolvableValue(1)
    assert field.value == b"7"


def test_write_value():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    layout = template_provider_mock.template
    layout.offset = ResolvableValue(2)
    area = Template(parent=layout)
    area.offset = ResolvableValue(3)
    field = Template(parent=area)
    field.offset = ResolvableValue(2)
    field.size = ResolvableValue(1)
    field.binding_context = binding_context
    field.value = b"8"
    assert field.value == b"8"


def test_read_offset_lower_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    lower_boundary_area = template_provider_mock.template
    lower_boundary_area.offset = ResolvableValue(0)
    lower_boundary_field = Template(parent=lower_boundary_area)
    lower_boundary_field.offset = ResolvableValue(0)
    lower_boundary_field.size = ResolvableValue(1)
    lower_boundary_field.binding_context = binding_context
    assert lower_boundary_field.value == b"0"


def test_read_offset_upper_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    upper_boundary_area = template_provider_mock.template
    upper_boundary_area.offset = ResolvableValue(7)
    upper_boundary_field = Template(parent=upper_boundary_area)
    upper_boundary_field.offset = ResolvableValue(0)
    upper_boundary_field.size = ResolvableValue(1)
    upper_boundary_field.binding_context = binding_context
    assert upper_boundary_field.value == b"7"


# def test_nested_area():
#     pass


# def test_size_calculation():
#     pass


def test_read_at_offset_lower_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    lower_boundary_field = template_provider_mock.template
    lower_boundary_field.offset = ResolvableValue(0)
    lower_boundary_field.size = ResolvableValue(1)
    lower_boundary_field.binding_context = binding_context
    assert lower_boundary_field.value == b"0"


def test_read_at_offset_upper_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    upper_boundary_field = template_provider_mock.template
    upper_boundary_field = Template()
    upper_boundary_field.offset = ResolvableValue(7)
    upper_boundary_field.size = ResolvableValue(1)
    upper_boundary_field.binding_context = binding_context
    assert upper_boundary_field.value == b"7"


def test_read_size_min_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    min_boundary_field = template_provider_mock.template
    min_boundary_field.offset = ResolvableValue(0)
    min_boundary_field.size = ResolvableValue(1)
    min_boundary_field.binding_context = binding_context
    assert min_boundary_field.value == b"0"


def test_read_size_max_boundary():
    buffered_stream = io.BytesIO(b"01234567")
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    max_boundary_field = template_provider_mock.template
    max_boundary_field.offset = ResolvableValue(0)
    max_boundary_field.size = ResolvableValue(8)
    max_boundary_field.binding_context = binding_context
    assert max_boundary_field.value == b"01234567"


def test_read_walkthrough():
    byte_values = list(range(8))
    buffered_stream = io.BytesIO(bytes(byte_values))
    data_provider_mock = SimpleDataProvider(buffered_stream)
    template_provider_mock = SimpleTemplateProvider(Template())
    binding_context = BindingContext(
        template_provider_mock, data_provider_mock)
    for offset in byte_values:
        field = template_provider_mock.template
        field.offset = ResolvableValue(offset)
        field.size = ResolvableValue(1)
        field.binding_context = binding_context
        assert field.value == bytes([offset])
