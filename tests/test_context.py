"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""

from binalyzer_core.context import BindingEngine, TemplateFactory
from binalyzer_template_provider import XMLTemplateParser

from anytree import findall

def test_template_factory():
    template_description = """
        <template name="root"></template>
    """
    prototype = XMLTemplateParser(template_description).parse()
    duplicate = TemplateFactory().clone(prototype)

    assert prototype.name == duplicate.name

def test_binding_engine_copy():
    binding_engine = BindingEngine()
    template_description = """
        <template name="root"></template>
    """
    tom = XMLTemplateParser(template_description).parse()
    dom = binding_engine.copy_tree(tom)

    assert dom.name == "root"
    assert tom.name == "root"
    assert id(dom) != id(tom)


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

    binding_engine = BindingEngine()
    dom = binding_engine.create_dom(tom, tom.binding_context)

    dom

    # assert nodes[0].name == "a"
    # assert nodes[1].name == "d"