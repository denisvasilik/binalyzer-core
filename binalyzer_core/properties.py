# -*- coding: utf-8 -*-
"""
    binalyzer_core.properties
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements template properties.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from .value_provider import (
    ValueProvider,
    FunctionValueProvider,
    ReferenceValueProvider,
    AutoSizeValueProvider,
    OffsetValueProvider,
    RelativeOffsetValueProvider,
    RelativeOffsetReferenceValueProvider,
    StretchSizeValueProvider,
)


class PropertyBase(object):

    def __init__(self, template, value_provider):
        self.template = template
        self.value_provider = value_provider

    @property
    def value(self):
        return self.value_provider.get_value()

    @value.setter
    def value(self, value):
        self.value_provider.set_value(value)


class ValueProperty(PropertyBase):

    def __init__(self, value=0, template=None):
        super(ValueProperty, self).__init__(
            template, ValueProvider(value))


class FunctionProperty(PropertyBase):

    def __init__(self, template):
        super(FunctionProperty, self).__init__(
            template, FunctionValueProvider())


class ReferenceProperty(PropertyBase):

    def __init__(self, template, reference_name):
        super(ReferenceProperty, self).__init__(
            template, ReferenceValueProvider(template, reference_name))


class OffsetValueProperty(PropertyBase):

    def __init__(self, template, value):
        super(OffsetValueProperty, self).__init__(
            template, OffsetValueProvider(template, value))


class RelativeOffsetValueProperty(PropertyBase):

    def __init__(self, template, ignore_boundary=False):
        super(RelativeOffsetValueProperty, self).__init__(
            template, RelativeOffsetValueProvider(template, ignore_boundary))


class RelativeOffsetReferenceProperty(PropertyBase):

    def __init__(self, template, reference_name):
        super(RelativeOffsetReferenceProperty, self).__init__(
            template, RelativeOffsetReferenceValueProvider(template, reference_name))


class StretchSizeProperty(PropertyBase):

    def __init__(self, template):
        super(StretchSizeProperty, self).__init__(
            template, StretchSizeValueProvider(template))


class AutoSizeValueProperty(PropertyBase):

    def __init__(self, template):
        super(AutoSizeValueProperty, self).__init__(
            template, AutoSizeValueProvider(template))


class AutoSizeReferenceProperty(PropertyBase):

    def __init__(self, template):
        super(AutoSizeReferenceProperty, self).__init__(
            template, AutoSizeReferenceProvider(template))
