# -*- coding: utf-8 -*-
"""
    binalyzer_core.transform
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements transformations of templates.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""


def transform(source_template, destination_template, additional_data={}):
    _transfer(source_template, destination_template)
    _bind(_diff(source_template, destination_template), additional_data)


def _transfer(source_template, destination_template):
    existing_leaves = [(source_leave, destination_leave)
                       for source_leave in source_template.leaves
                       for destination_leave in destination_template.leaves
                       if source_leave.name == destination_leave.name]

    for (source_leave, destination_leave) in existing_leaves:
        extension_size = destination_leave.size - source_leave.size
        destination_leave.value = (source_leave.value +
                                   bytes([0] * extension_size))


def _diff(source_template, destination_template):
    return (destination_leave
            for destination_leave in destination_template.leaves
            if destination_leave.name not in
            (source_leave.name for source_leave in source_template.leaves))


def _bind(templates, data_template_map):
    for template in templates:
        if template.name in list(data_template_map.keys()):
            template.value = data_template_map[template.name]
        else:
            template.value = bytes([0] * template.size)
