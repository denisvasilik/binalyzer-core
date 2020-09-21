"""
    test_properties
    ~~~~~~~~~~~~~~~

    This module implements tests for the properties module.
"""
import pytest

from binalyzer_core import (
    ValueProperty,
    ReferenceProperty,
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