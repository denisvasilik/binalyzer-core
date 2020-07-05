# -*- coding: utf-8 -*-
"""
    binalyzer_core.properties
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the properties of a template.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import find_by_attr
from anytree.util import rightsibling

from .value_provider import (
    ValueProvider,
    FunctionValueProvider,
    ReferenceValueProvider,
    AutoSizeValueProvider,
    RelativeOffsetValueProvider,
    RelativeOffsetReferenceValueProvider,
    StretchSizeValueProvider,
    LEB128UnsignedBindingValueProvider,
)
from .converter import (
    IdentityValueConverter,
    IntegerValueConverter,
    LEB128UnsignedValueConverter,
)


class PropertyBase(object):

    def __init__(
        self,
        template,
        value_provider,
        value_converter=IdentityValueConverter()
    ):
        self.template = template
        self.value_provider = value_provider
        self.value_converter = value_converter

    @property
    def value(self):
        return self.value_converter.convert(
            self.value_provider.get_value(), self.template)

    @value.setter
    def value(self, value):
        self.value_provider.set_value(
            self.value_converter.convert_back(value, self.template))


class ValueProperty(PropertyBase):

    def __init__(
        self,
        value=0,
        template=None,
        value_converter=IdentityValueConverter()
    ):
        super(ValueProperty, self).__init__(
            template,
            ValueProvider(value),
            value_converter,
        )


class FunctionProperty(PropertyBase):

    def __init__(self, template):
        super(FunctionProperty, self).__init__(
            template, FunctionValueProvider())


class LEB128UnsignedBindingProperty(PropertyBase):

    def __init__(self, template):
        super(LEB128UnsignedBindingProperty, self).__init(
            template=template,
            value_provider=LEB128UnsignedBindingValueProvider(template),
            value_converter=LEB128UnsignedValueConverter(),
        )


class ReferenceProperty(PropertyBase):

    def __init__(
        self,
        template,
        reference_name,
        value_converter=IntegerValueConverter()
    ):
        super(ReferenceProperty, self).__init__(
            template,
            ReferenceValueProvider(template, reference_name),
            value_converter,
        )


class RelativeOffsetValueProperty(PropertyBase):

    def __init__(self, template, ignore_boundary=False):
        super(RelativeOffsetValueProperty, self).__init__(
            template, RelativeOffsetValueProvider(template, ignore_boundary))


class RelativeOffsetReferenceProperty(PropertyBase):

    def __init__(self, template):
        super(RelativeOffsetValueProperty, self).__init__(
            template, RelativeOffsetReferenceValueProvider(template))


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
