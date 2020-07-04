# -*- coding: utf-8 -*-
"""
    binalyzer_core.engine
    ~~~~~~~~~~~~~~~~~~~~~

    This module implements .

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree.util import rightsibling


def get_total_size(template):
    if template.children:
        return get_total_size_of_children(template)
    else:
        return template.boundary


def get_max_size(template):
    next_sibling = rightsibling(template)
    if next_sibling:
        return next_sibling.offset - template.offset
    elif template.parent:
        return template.parent.size - template.offset
    elif template.binding_context.data:
        data = template.binding_context.data
        data.seek(0, 2)
        return data.tell()
    else:
        return 0


def get_relative_offset(template, ignore_boundary=False):
    relative_offset = template.padding_before

    if not ignore_boundary:
        relative_offset += get_boundary_offset_relative_to_parent(
            template)

    relative_offset += get_relative_offset_end_of_previous_sibling(
        template)

    if not ignore_boundary:
        relative_offset += get_boundary_offset_relative_to_sibling(
            template)

    return relative_offset


def get_total_size_of_children(template):
    return max(get_total_size_of_child(child) for child in template.children)


def get_total_size_of_child(child):
    # NOTE: child.offset already contains the value of padding-before!!!
    value = child.offset + child.size + child.padding_after
    return get_multiple_of_boundary(value, child.parent.boundary)


def get_multiple_of_boundary(value, boundary):
    if boundary == 0:
        return value
    boundary_multiplier = int(value / boundary)
    if value % boundary:
        boundary_multiplier += 1
    return boundary_multiplier * boundary


def get_boundary_offset_relative_to_parent(template):
    if template.boundary > 0:
        return template.parent.offset % template.boundary
    else:
        return 0


def get_boundary_offset_relative_to_sibling(template):
    sibling_relative_offset = get_relative_offset_end_of_previous_sibling(
        template)
    if (
        template.boundary
        and template.boundary > 0
        and sibling_relative_offset > 0
        and sibling_relative_offset % template.boundary
    ):
        return template.boundary - (sibling_relative_offset % template.boundary)
    else:
        return 0


def get_relative_offset_end_of_previous_sibling(template):
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
