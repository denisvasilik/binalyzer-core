# -*- coding: utf-8 -*-
"""
    binalyzer_core.value_provider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value providers.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from . import engine

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


class RelativeOffsetValueProvider(ValueProvider):

    def __init__(self, template, ignore_boundary=False):
        self.template = template
        self.ignore_boundary = ignore_boundary
        super(RelativeOffsetValueProvider, self).__init__()

    def get_value(self):
        return (engine.get_relative_offset(self.template, self.ignore_boundary) +
                self._value)

    def set_value(self, value):
        self._value = value


class RelativeOffsetReferenceValueProvider(ReferenceValueProvider):

    def __init__(self, template, reference_name):
        super(RelativeOffsetCalculator, self).__init__(
            template, reference_name)

    def get_value(self):
        return (engine.get_relative_offset(self.template) +
                find_by_attr(self.template.root, self.reference_name).value)

    def set_value(self, value):
        find_by_attr(self.template.root, self.reference_name).value = value


class AutoSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        return engine.get_total_size(self.template)

    def set_value(self, value):
        raise RuntimeError('Not supported')


class StretchSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self.template = template

    def get_value(self):
        return engine.get_max_size(self.template)

    def set_value(self, value):
        raise RuntimeError('Not supported')
