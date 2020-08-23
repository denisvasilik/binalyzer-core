"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""

from binalyzer_core.context import BindingEngine, TemplateFactory
from binalyzer_template_provider import XMLTemplateParser

from binalyzer_core import Binalyzer

from anytree import findall

def test_template_factory():
    template_description = """
        <template name="root"></template>
    """
    prototype = XMLTemplateParser(template_description).parse()
    duplicate = TemplateFactory().clone(prototype)

    assert prototype.name == duplicate.name

def test_dom_expansion():
    template_description = """
        <template name="a">
            <template name="b" count="2">
                <template name="c" count="4">
                    <template name="d" count="3">
                    </template>
                </template>
            </template>
        </template>
    """
    tom = XMLTemplateParser(template_description).parse()

    binalyzer = Binalyzer()
    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 2
    assert len(list(dom.b.children)) == 4
    assert len(list(dom.b.c.children)) == 3


def test_partial_dom_expansion():
    pass