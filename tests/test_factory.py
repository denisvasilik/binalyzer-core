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

from anytree import findall


@pytest.fixture
def factory():
    return TemplateFactory()


def test_template_factory(factory):
    template = Template()
    template.name = 'a'
    template.size = 0x1
    template.offset = 0x2
    template.boundary = 0x3
    template.padding_before = 0x4
    template.padding_after = 0x5

    duplicate = factory.clone(template)

    assert duplicate.name == template.name
    assert duplicate.size == template.size
    assert duplicate.offset == template.offset
    assert duplicate.boundary == template.boundary
    assert duplicate.padding_before == template.padding_before
    assert duplicate.padding_after == template.padding_after
    assert duplicate.name == template.name
