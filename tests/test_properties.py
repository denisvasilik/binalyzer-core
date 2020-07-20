"""
    test_properties
    ~~~~~~~~~~~~~~~

    This module implements tests for the properties module.
"""
import pytest

from binalyzer_core import (
    ReferenceProperty,
    Template,
)


def test_reference_property_is_read_only():
    property = ReferenceProperty(Template(), 'invalid_name')
    with pytest.raises(RuntimeError):
        property.value = 0
