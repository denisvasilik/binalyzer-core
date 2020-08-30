"""
    test_context
    ~~~~~~~~~~~~

    This module implements tests for the context module.
"""
import io
import pytest

from anytree import findall

from binalyzer_core import (
    Binalyzer,
    Template,
    TemplateFactory,
)


@pytest.fixture
def binalyzer():
    return Binalyzer()


def test_template_factory():
    prototype = Template(name='root')
    duplicate = TemplateFactory().clone(prototype)

    assert prototype.name == duplicate.name


def test_template_expansion(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)

    b.count = 2

    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 2


def test_template_expansion_nested(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)
    c = Template(name='c', parent=b)
    d = Template(name='d', parent=c)

    b.count = 2
    c.count = 4
    d.count = 3

    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 2
    assert len(list(dom.children[0].children)) == 4
    assert len(list(dom.children[0].children[0].children)) == 3


def test_template_reduction(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)

    b.count = 0

    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 0


def test_template_reduction_nested(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)
    c = Template(name='c', parent=b)
    d = Template(name='d', parent=c)

    b.count = 2
    c.count = 4
    d.count = 0

    binalyzer.template = tom
    dom = binalyzer.template

    assert dom.name == tom.name
    assert id(dom) != id(tom)
    assert len(list(dom.children)) == 2
    assert len(list(dom.children[0].children)) == 4
    assert len(list(dom.children[0].children[0].children)) == 0


def test_template_validation(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)
    b.size = 1
    b.signature = bytes([0x01])

    binalyzer.template = tom
    binalyzer.data = io.BytesIO(bytes([0x01]))
    dom = binalyzer.template

    assert len(list(dom.children[0].value)) == 0x01


def test_template_validation_failed(binalyzer):
    tom = Template(name='a')
    b = Template(name='b', parent=tom)
    b.size = 1
    b.signature = bytes([0x01])

    binalyzer.template = tom
    binalyzer.data = io.BytesIO(bytes([0x02]))

    with pytest.raises(RuntimeError):
        binalyzer.template


def test_template_validation_nested(binalyzer):
    template = Template(name='a')
    b = Template(name='b', parent=template)
    c = Template(name='c', parent=b)
    d = Template(name='d', parent=b)

    b.size = 2
    b.signature = bytes([0x01, 0x02])
    c.size = 1
    c.signature = bytes([0x01])
    d.size = 1
    d.signature = bytes([0x02])

    binalyzer.template = template
    binalyzer.data = io.BytesIO(bytes([0x01, 0x02]))

    assert binalyzer.template.children[0].value == bytes([0x01, 0x02])
    assert binalyzer.template.children[0].children[0].value == bytes([0x01])
    assert binalyzer.template.children[0].children[1].value == bytes([0x02])


def test_template_validation_failed_nested(binalyzer):
    template = Template(name='a')
    b = Template(name='b', parent=template)
    c = Template(name='c', parent=b)
    d = Template(name='d', parent=b)

    b.size = 2
    b.signature = bytes([0x01, 0x02])
    c.size = 1
    c.signature = bytes([0x01])
    d.size = 1
    d.signature = bytes([0x02])

    binalyzer.template = template
    binalyzer.data = io.BytesIO(bytes([0x01, 0x03]))

    with pytest.raises(RuntimeError):
        binalyzer.template
