"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""
import pytest

from anytree import findall

from binalyzer_core import Binalyzer, Template, TemplateFactory


def test_template_factory():
    prototype = Template(name='root')
    duplicate = TemplateFactory().clone(prototype)

    assert prototype.name == duplicate.name


def test_dom_expansion():
    tom = Template(name='a')
    b = Template(name='b', parent=tom)
    b.count = 2
    c = Template(name='c', parent=b)
    c.count = 4
    d = Template(name='d', parent=c)
    d.count = 3

    binalyzer = Binalyzer()
    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 2
    assert len(list(dom.b.children)) == 4
    assert len(list(dom.b.c.children)) == 3


@pytest.mark.skip()
def test_partial_dom_expansion():
    pass
