# -*- coding: utf-8 -*-
"""
    binalyzer_core.value_provider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value providers.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import find_by_attr
from anytree.util import leftsibling, rightsibling


class ValueProviderBase(object):

    def get_value(self):
        pass

    def set_value(self, value):
        pass


class ValueProvider(ValueProviderBase):

    def __init__(self, value=0):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class FunctionValueProvider(ValueProviderBase):

    def __init__(self, func=None):
        self.func = func

    def get_value(self):
        return self.func()

    def set_value(self, func):
        raise RuntimeError('Not supported')


class ReferenceValueProvider(ValueProviderBase):

    def __init__(self, template, reference_name):
        self.template = template
        self.reference_name = reference_name

    def get_value(self):
        return find_by_attr(self.template.root, self.reference_name).value

    def set_value(self, value):
        find_by_attr(self.template.root, self.reference_name).value = value


class RelativeOffsetCalculator(object):

    def calculate(self, template, ignore_boundary=False):
        return self._get_relative_offset(template)

    def _get_relative_offset(self, template, ignore_boundary=False):
        relative_offset = template.padding_before

        if not self.ignore_boundary:
            relative_offset += self._get_boundary_offset_relative_to_parent(
                template)

        relative_offset += self._get_relative_offset_end_of_previous_sibling(
            template)

        if not self.ignore_boundary:
            relative_offset += self._get_boundary_offset_relative_to_sibling(
                template)

        return relative_offset

    def _get_boundary_offset_relative_to_parent(self, template):
        if template.boundary > 0:
            return template.parent.offset % template.boundary
        else:
            return 0

    def _get_boundary_offset_relative_to_sibling(self, template):
        sibling_relative_offset = self._get_relative_offset_end_of_previous_sibling(template)
        if (
            template.boundary
            and template.boundary > 0
            and sibling_relative_offset > 0
            and sibling_relative_offset % template.boundary
        ):
            return template.boundary - (sibling_relative_offset % template.boundary)
        else:
            return 0

    def _get_relative_offset_end_of_previous_sibling(self, template):
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


class RelativeOffsetValueProvider(RelativeOffsetCalculator, ValueProvider):

    def __init__(self, template, ignore_boundary=False):
        self.template = template
        self.ignore_boundary = ignore_boundary
        super(RelativeOffsetValueProvider, self).__init__()

    def get_value(self):
        return self.calculate(self.template, self.ignore_boundary) + self._value

    def set_value(self, value):
        self._value = value


class RelativeOffsetReferenceProvider(RelativeOffsetCalculator, ReferenceValueProvider):

    def __init__(self, template, reference_name):
        super(RelativeOffsetCalculator, self).__init__(
            template, reference_name)

    def get_value(self):
        return self.calculate(self.template) + find_by_attr(self.template.root, self.reference_name).value

    def set_value(self, value):
        find_by_attr(self.template.root, self.reference_name).value = value


class AutoSizeValueProvider(ValueProviderBase):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        if self.template.children:
            return self._get_total_size_of_children()
        else:
            return self.template.boundary

    def set_value(self, value):
        raise RuntimeError('Not supported')

    def _get_total_size_of_children(self):
        return max(
            self._get_total_size_of_child(child) for child in self.template.children
        )

    def _get_total_size_of_child(self, child):
        # NOTE: child.offset already contains the value of padding-before!!!
        value = child.offset + child.size + child.padding_after

        return self.multiple_of_boundary(value, child.parent.boundary)

    def multiple_of_boundary(self, value, boundary_attribute):
        if boundary_attribute == 0:
            return value
        boundary_multiplier = int(value / boundary_attribute)
        if value % boundary_attribute:
            boundary_multiplier += 1
        return boundary_multiplier * boundary_attribute


class StretchSizeValueProvider(ValueProviderBase):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        return self._calculate_stretched_size()

    def set_value(self, value):
        raise RuntimeError('Not supported')

    def _calculate_stretched_size(self):
        next_sibling = rightsibling(self.template)
        if next_sibling:
            return next_sibling.offset - self.template.offset
        elif self.template.parent:
            return self.template.parent.size - self.template.offset
        elif self.template.binding_context.data:
            data = self.template.binding_context.data
            data.seek(0, 2)
            return data.tell()
        else:
            return 0


class IdentityValueConverter(object):

    def convert(self, value, template):
        return value

    def convert_back(self, value, template):
        return value


class IntegerValueConverter(object):

    def convert(self, value, template):
        if template.byte_order == 'LittleEndian':
            return int.from_bytes(value, byteorder='little')
        else:
            return int.from_bytes(value, byteorder='big')

    def convert_back(self, value, template):
        if template.byte_order == 'LittleEndian':
            return value.to_bytes(template.size, 'little')
        else:
            return value.to_bytes(template.size, 'big')
