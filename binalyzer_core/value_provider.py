# -*- coding: utf-8 -*-
"""
    binalyzer_core.value_provider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value providers.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from . import engine

from anytree import findall_by_attr
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


class LEB128UnsignedBindingValueProvider(ValueProviderBase):

    def __init__(self, template=None):
        self.template = template
        self._cached_value = None

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        data = self.template.binding_context.data_provider.data
        absolute_address = self.template.absolute_address
        data.seek(absolute_address)
        size = 1
        byte_value = int.from_bytes(data.read(1), 'little')
        while ((byte_value & 0x80) == 0x80):
            size += 1
            byte_value = int.from_bytes(data.read(1), 'little')
        data.seek(absolute_address)
        self._cached_value = data.read(size)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not implemented, yet.')


class LEB128SizeBindingValueProvider(ValueProviderBase):

    def __init__(self, template=None):
        self.template = template
        self._cached_value = None

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        data = self.template.binding_context.data_provider.data
        absolute_address = self.template.absolute_address
        data.seek(absolute_address)
        size = 1
        byte_value = int.from_bytes(data.read(1), 'little')
        while ((byte_value & 0x80) == 0x80):
            size += 1
            byte_value = data.read(1)
        self._cached_value = size
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not implemented, yet.')


def find_by_scope(template, reference_name):
    while template.parent:
        result = findall_by_attr(template.parent, reference_name)
        if result:
            return result[0]
        template = template.parent
    raise RuntimeError(
        'Unable to find referenced template "' + reference_name + '".'
    )


class ReferenceValueProvider(ValueProviderBase):

    def __init__(self, template, reference_name):
        self.template = template
        self.reference_name = reference_name
        self._cached_value = None

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        self._cached_value = find_by_scope(
            self.template, self.reference_name).value
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError(
            'Unable to assign a value to a reference. Consider setting the '
            'value of the referenced template instead.'
        )


class RelativeOffsetValueProvider(ValueProvider):

    def __init__(self, template, ignore_boundary=False):
        self.template = template
        self.ignore_boundary = ignore_boundary
        self._cached_value = None
        super(RelativeOffsetValueProvider, self).__init__()

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        self._cached_value = (engine.get_relative_offset(self.template,
                                                         self.ignore_boundary) + self._value)
        return self._cached_value

    def set_value(self, value):
        self._cached_value = None
        self._value = value


class RelativeOffsetReferenceValueProvider(ReferenceValueProvider):

    def __init__(self, template, reference_name):
        self._cached_value = None
        super(RelativeOffsetCalculator, self).__init__(
            template, reference_name)

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        self._cached_value = (engine.get_relative_offset(self.template) +
                              find_by_scope(self.template, self.reference_name).value)
        return self._cached_value

    def set_value(self, value):
        self._cached_value = None
        find_by_scope(self.template, self.reference_name).value = value


class AutoSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self._cached_value = None
        self.template = template

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        self._cached_value = engine.get_total_size(self.template)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not supported')


class StretchSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self._cached_value = None
        self.template = template

    def get_value(self):
        if self._cached_value:
            return self._cached_value
        return engine.get_max_size(self.template)

    def set_value(self, value):
        raise RuntimeError('Not supported')
