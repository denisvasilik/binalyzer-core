"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""
import pytest

from binalyzer_core import (
    Template,
    TemplateFactory,
)
from binalyzer_core.factory import (
    RelativeOffsetValuePropertyFactory,
)
from binalyzer_core.properties import (
    RelativeOffsetValueProperty,
)

from anytree import findall


@pytest.fixture
def factory():
    return TemplateFactory()


def test_relative_offset_value_property_factory():
    template0 = Template()
    template1 = Template()
    factory = RelativeOffsetValuePropertyFactory()
    offset_property = RelativeOffsetValueProperty(template0)
    duplicate = factory.clone(offset_property, template1)
    assert id(offset_property.value_converter) == id(duplicate.value_converter)
    assert id(offset_property.value_provider) != id(duplicate.value_provider)
    assert id(offset_property.template) == id(template0)
    assert id(duplicate.template) == id(template1)


# def test_template_factory_referencing_properties(factory):
#     template = Template()
#     template.name = 'a'
#     template.size = 0x1
#     template.offset = 0x2
#     template.boundary = 0x3
#     template.padding_before = 0x4
#     template.padding_after = 0x5

#     duplicate = factory.clone(template, copy=False)

#     assert id(duplicate.name) == id(template.name)
#     assert id(duplicate.size_property) == id(template.size_property)
#     assert id(duplicate.offset_property) == id(template.offset_property)
#     assert id(duplicate.boundary_property) == id(template.boundary_property)
#     assert id(duplicate.padding_before_property) == id(template.padding_before_property)
#     assert id(duplicate.padding_after_property) == id(template.padding_after_property)


def test_template_factory_copying_properties(factory):
    template = Template()
    template.name = 'a'
    template.size = 0x1
    template.offset = 0x2
    template.boundary = 0x3
    template.padding_before = 0x4
    template.padding_after = 0x5

    duplicate = factory.clone(template)

    assert id(duplicate.name) == id(template.name)
    assert id(duplicate.size_property) != id(template.size_property)
    assert id(duplicate.offset_property) != id(template.offset_property)
    assert id(duplicate.boundary_property) != id(template.boundary_property)
    assert id(duplicate.padding_before_property) != id(template.padding_before_property)
    assert id(duplicate.padding_after_property) != id(template.padding_after_property)
