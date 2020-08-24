"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""
import pytest

from binalyzer_core.context import BindingEngine, TemplateFactory
from binalyzer_template_provider import XMLTemplateParser

from binalyzer_core.factory import TemplateFactory

from binalyzer_core import Binalyzer, Template

from anytree import findall


@pytest.fixture
def factory():
    return TemplateFactory()


def test_template_factory(factory):
    binalyzer = Binalyzer()
    template_a = Template('a', parent=binalyzer.template_provider.template)
    template_a.size = 4
    template_b = Template('b', parent=binalyzer.template_provider.template)
    template_b.size = 4
    assert binalyzer.template.size == 8


def test_template_factory2(factory):
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


# def test_template_factory():
#    template_description = """
#         <template name="a">
#             <template name="b" count="2">
#                 <template name="c" count="4">
#                     <template name="d" count="3">
#                     </template>
#                 </template>
#             </template>
#         </template>
#     """
#     prototype = XMLTemplateParser(template_description).parse()
#     duplicate = TemplateFactory().clone(prototype)

#     assert prototype.name == duplicate.name
