"""
    test_engine
    ~~~~~~~~~~~

    This module implements tests for the engine module.
"""
import pytest

from binalyzer_core import Template, engine


def test_get_total_size_without_children_and_boundary():
    template = Template()
    assert engine.get_total_size(template) == 0


def test_get_max_size():
    pass


def test_get_relative_offset():
    pass


def test_get_total_size_without_children_but_with_boundary():
    template = Template()
    template.boundary = 0x100
    assert engine.get_total_size(template) == 0x100


def test_get_total_size_with_children_and_without_boundary():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_total_size(template_a) == 7


def test_get_total_size_with_children_and_boundary():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_a.boundary = 0x10
    assert engine.get_total_size(template_a) == 0x10


def test_get_total_size_of_children():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_total_size_of_children(template_a) == 7


def test_get_total_size_of_children_without_children():
    template = Template()
    with pytest.raises(ValueError):
        engine.get_total_size_of_children(template)


def get_total_size_of_child_using_offset_attribute():
    pass


def get_total_size_of_child_using_size_attribute():
    pass


def get_total_size_of_child_using_padding_after_attribute():
    pass


def get_total_size_of_child_using_parent_boundary_attribute():
    pass


def test_get_multiple_of_boundary_when_boundary_zero():
    assert engine.get_multiple_of_boundary(123, 0) == 123


def test_get_multiple_of_boundary_when_value_on_boundary():
    assert engine.get_multiple_of_boundary(0x400, 0x100) == 0x400


def test_get_multiple_of_boundary_when_value_off_boundary():
    assert engine.get_multiple_of_boundary(0x470, 0x100) == 0x500


def test_boundary_offset_relative_to_parent():
    pass


def test_relative_offset_end_of_previous_sibling():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_relative_offset_end_of_previous_sibling(template_d) == 3


def test_boundary_offset_relative_to_sibling_no_boundary():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    assert engine.get_boundary_offset_relative_to_sibling(template_d) == 0


def test_boundary_offset_relative_to_sibling_off_boundary():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_d.boundary = 5
    assert engine.get_boundary_offset_relative_to_sibling(template_d) == 2


def test_boundary_offset_relative_to_sibling_on_boundary():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_d = Template(name='d', parent=template_a)
    template_b.size = 1
    template_c.size = 2
    template_d.size = 4
    template_d.boundary = 3
    assert engine.get_boundary_offset_relative_to_sibling(template_d) == 0
