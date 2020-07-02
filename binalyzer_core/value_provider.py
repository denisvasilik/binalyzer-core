# -*- coding: utf-8 -*-
"""
    binalyzer_core.value_provider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value providers.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import find_by_attr

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


class RelativeOffsetValueProvider(ValueProviderBase):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        return self._get_relative_offset()

    def set_value(self, value):
        raise RuntimeError('Not supported')

    def _get_relative_offset(self):
        boundary_offset_relative_to_parent = 0
        boundary_offset_relative_to_sibling = 0

        if self.template.boundary and self.template.boundary.value > 0:
            boundary_offset_relative_to_parent = (
                self.template.parent.offset.value % self.template.boundary.value
            )

        sibling_relative_offset = self._get_relative_offset_end_of_previous_sibling()

        if (
            self.template.boundary
            and self.template.boundary.value > 0
            and sibling_relative_offset > 0
            and sibling_relative_offset % self.template.boundary.value
        ):
            boundary_offset_relative_to_sibling = self.template.boundary.value - (
                sibling_relative_offset % self.template.boundary.value
            )

        return (
            self.template.padding_before.value
            + boundary_offset_relative_to_parent
            + sibling_relative_offset
            + boundary_offset_relative_to_sibling
        )

    def _get_relative_offset_end_of_previous_sibling(self):
        # Need at least two children to grab previous sibling
        if self.template.parent and len(self.template.parent.children) >= 2:
            index = 0
            for (count, value) in enumerate(self.template.parent.children):
                if value == self.template:
                    index = count
                    break
            if index == 0:
                return 0
            else:
                previous_sibling = self.template.parent.children[index - 1]
                return (
                    previous_sibling.offset.value
                    + previous_sibling.size.value
                    + previous_sibling.padding_after.value
                )
        else:
            return 0


class AutoSizeValueProvider(ValueProviderBase):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        return self._get_total_size_of_children()

    def set_value(self, value):
        raise RuntimeError('Not supported')

    def _get_total_size_of_children(self):
        return max(
            self._get_total_size_of_child(child) for child in self.template.children
        )

    def _get_total_size_of_child(self, child):
        # NOTE: child.offset already contains the value of padding-before!!!
        value = child.offset.value + child.size.value + child.padding_after.value

        return self.multiple_of_boundary(value, child.parent.boundary)

    def multiple_of_boundary(self, value, boundary_attribute):
        if boundary_attribute.value == 0:
            return value
        boundary_multiplier = int(value / boundary_attribute.value)
        if value % boundary_attribute.value:
            boundary_multiplier += 1
        return boundary_multiplier * boundary_attribute.value


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
            return next_sibling.offset.value - self.template.offset.value
        elif self.template.parent:
            return self.template.parent.size.value - self.template.offset.value
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

    def convert(self, value):
        if self.byte_order == ByteOrder.LittleEndian:
            return int.from_bytes(value, byteorder="LittleEndian")
        else:
            return int.from_bytes(value, byteorder="BigEndian")

    def convert_back(self, value, template):
        if self.byte_order == ByteOrder.LittleEndian:
            return value.to_bytes(template.size.value, 'little')
        else:
            return value.to_bytes(template.size.value, 'big')
