# -*- coding: utf-8 -*-
"""
    binalyzer_core.engine
    ~~~~~~~~~~~~~~~~~~~~~

    This module implements the mechanics of the template concept.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree.util import rightsibling


def get_offset(template, ignore_boundary=False):
    """Returns the offset relative to a parent or predecessor taking a given
    boundary into account. It is possible to ignore the boundary by setting
    `ìgnore_boundary` to `True`.
    """
    offset = template.padding_before

    if not ignore_boundary:
        offset += _get_boundary_offset_relative_to_parent(template)

    offset += _get_offset_at_end_of_predecessor(template)

    if not ignore_boundary:
        offset += _get_boundary_offset_at_end_of_predecessor(template)

    return offset


def get_size(template):
    """Returns the actual size of the given template taking a given boundary
    into account.
    """
    if template.children:
        return max(_get_size_of_child(child) for child in template.children)
    else:
        return template.boundary


def get_max_size(template):
    """Returns a template's maximum possible size depending on the offset of
    its successor or size of it's parent.
    """
    from .properties import AutoSizeValueProperty

    next_sibling = rightsibling(template)
    if next_sibling:
        return next_sibling.offset - template.offset
    elif template.parent and not isinstance(template.parent.size_property, AutoSizeValueProperty):
        return template.parent.size - template.offset
    elif template.parent and template.parent.boundary > 0:
        return template.parent.boundary - template.offset
    elif template.binding_context.data:
        data = template.binding_context.data
        data.seek(0, 2)
        return data.tell()
    else:
        return 0


def _get_size_of_child(child):
    # NOTE: child.offset already contains the value of padding-before!!!
    value = child.offset + child.size + child.padding_after
    return _get_multiple_of_boundary(value, child.parent.boundary)


def _get_multiple_of_boundary(value, boundary):
    if boundary == 0:
        return value
    boundary_multiplier = int(value / boundary)
    if value % boundary:
        boundary_multiplier += 1
    return boundary_multiplier * boundary


def _get_offset_at_end_of_predecessor(template):
    # Need at least two children to grab previous sibling
    if template.parent and len(template.parent.children) >= 2:
        index = 0
        for (count, value) in enumerate(template.parent.children):
            if value == template:
                index = count
                break
        if index == 0:
            return 0
        else:
            previous_sibling = template.parent.children[index - 1]
            return (
                previous_sibling.offset
                + previous_sibling.size
                + previous_sibling.padding_after
            )
    else:
        return 0


def _get_boundary_offset_relative_to_parent(template):
    if template.parent:
        return _get_boundary_offset(template.parent.offset, template.boundary)
    else:
        return 0


def _get_boundary_offset_at_end_of_predecessor(template):
    offset = _get_offset_at_end_of_predecessor(template)
    return _get_boundary_offset(offset, template.boundary)


def _get_boundary_offset(offset, boundary):
    if (boundary and offset % boundary):
        return boundary - (offset % boundary)
    else:
        return 0
