"""
    test_engine
    ~~~~~~~~~~~

    This module implements tests for the engine module.
"""
import pytest

from binalyzer_core import Template, TemplateEngine


@pytest.fixture
def engine():
    return TemplateEngine()


def test_get_offset_of_template_without_boundary(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_offset(template_d) == 3


def test_get_offset_when_template_is_not_on_boundary(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_d.boundary = 5
    assert engine.get_offset(template_d) == 5


def test_get_offset_when_template_is_on_boundary(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_d.boundary = 3
    assert engine.get_offset(template_d) == 3


def test_get_size_without_children_and_boundary(engine):
    template = Template()
    assert engine.get_size(template) == 0


def test_get_size_without_children_but_with_boundary(engine):
    template = Template()
    template.boundary = 0x100
    assert engine.get_size(template) == 0


def test_get_size_with_children_and_without_boundary(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_size(template_a) == 7


def test_get_size_with_children_and_boundary(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_a.boundary = 0x10
    assert engine.get_size(template_a) == 0x10


def test_get_size_of_children(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_size(template_a) == 7


def test_get_size_of_children_without_children(engine):
    template = Template()
    assert engine.get_size(template) == 0


@pytest.mark.skip()
def test_get_size_of_child_using_offset_attribute(engine):
    pass


@pytest.mark.skip()
def test_get_size_of_child_using_size_attribute(engine):
    pass


@pytest.mark.skip()
def test_get_size_of_child_using_padding_after_attribute(engine):
    pass


@pytest.mark.skip()
def test_get_size_of_child_using_parent_boundary_attribute(engine):
    pass


@pytest.mark.skip()
def test_get_max_size(engine):
    pass


@pytest.mark.skip()
def test_boundary_offset_relative_to_parent(engine):
    pass


def test_relative_offset_end_of_previous_sibling(engine):
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine._get_offset_at_end_of_predecessor(template_d) == 3


def test_get_multiple_of_boundary_when_boundary_zero(engine):
    assert engine._get_multiple_of_boundary(123, 0) == 123


def test_get_multiple_of_boundary_when_value_on_boundary(engine):
    assert engine._get_multiple_of_boundary(0x400, 0x100) == 0x400


def test_get_multiple_of_boundary_when_value_off_boundary(engine):
    assert engine._get_multiple_of_boundary(0x470, 0x100) == 0x500
