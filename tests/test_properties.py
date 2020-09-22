"""
    test_properties
    ~~~~~~~~~~~~~~~

    This module implements tests for the properties module.
"""
import pytest

from binalyzer_core import (
    ValueProperty,
    ReferenceProperty,
    StretchSizeProperty,
    Template,
)


def test_reference_property_is_read_only():
    property = ReferenceProperty(Template(), 'invalid_name')
    with pytest.raises(RuntimeError):
        property.value = 0


def test_value_property():
    value_property0 = ValueProperty()
    value_property1 = ValueProperty(42)

    assert value_property0.value == 0
    assert value_property1.value == 42


def test_sizing_stretch_without_predecessors():
    template_a = Template(name='a')
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_a.size = 10
    template_c.size_property = StretchSizeProperty(template_c)
    template_d.size = 4
    assert template_c.size == 6


def test_sizing_stretch_without_successors():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_a.size = 10
    template_b.size = 1
    template_c.size_property = StretchSizeProperty(template_c)
    assert template_c.size == 9


def test_sizing_stretch_with_siblings():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_a.size = 10
    template_b.size = 1
    template_c.size_property = StretchSizeProperty(template_c)
    template_d.size = 4
    assert template_c.size == 5


def test_sizing_stretch_without_siblings():
    template_a = Template(name='a')
    template_c = Template(name='c', parent=template_a)
    template_a.size = 10
    template_c.size_property = StretchSizeProperty(template_c)
    assert template_c.size == 10
