# -*- coding: utf-8 -*-
"""
    binalyzer_core.factory
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements factories used for cloning types.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from .properties import (
    PropertyBase,
    ValueProperty,
    FunctionProperty,
    ReferenceProperty,
    RelativeOffsetValueProperty,
    RelativeOffsetReferenceProperty,
    StretchSizeProperty,
    AutoSizeValueProperty,
    AutoSizeReferenceProperty,
)
from .value_provider import (
    RelativeOffsetValueProvider,
    LEB128UnsignedBindingValueProvider,
    LEB128SizeBindingValueProvider,
)
from .converter import (
    IdentityValueConverter,
    LEB128UnsignedValueConverter,
)


class PropertyFactory(object):

    def __init__(self):
        self.property_factories = [
            ValuePropertyFactory(),
            FunctionPropertyFactory(),
            ReferencePropertyFactory(),
            RelativeOffsetValuePropertyFactory(),
            RelativeOffsetReferencePropertyFactory(),
            StretchSizePropertyFactory(),
            AutoSizeValuePropertyFactory(),
            AutoSizeReferencePropertyFactory(),
            PropertyBaseFactory(),
        ]

    def clone(self, prototype, template):
        factory = [f for f in self.property_factories
                   if f.is_clonable(prototype)][0]
        duplicate = factory.clone(prototype, template)
        return duplicate


class PropertyBaseFactory(object):

    def clone(self, prototype, template):
        if isinstance(prototype.value_provider, LEB128UnsignedBindingValueProvider):
            return PropertyBase(
                template=template,
                value_provider=LEB128UnsignedBindingValueProvider(template),
                value_converter=LEB128UnsignedValueConverter(),
            )
        if isinstance(prototype.value_provider, LEB128SizeBindingValueProvider):
            return PropertyBase(
                template=template,
                value_provider=LEB128SizeBindingValueProvider(template),
                value_converter=IdentityValueConverter(),
            )
        raise RuntimeError()

    def is_clonable(self, obj):
        return isinstance(obj, PropertyBase)


class ValuePropertyFactory(object):

    def clone(self, prototype, template):
        return ValueProperty(
            value=prototype.value_provider.get_value(),
            template=template,
            value_converter=prototype.value_converter,
        )

    def is_clonable(self, obj):
        return isinstance(obj, ValueProperty)


class FunctionPropertyFactory(object):

    def clone(self, prototype, template):
        return FunctionProperty(template)

    def is_clonable(self, obj):
        return isinstance(obj, FunctionProperty)


class ReferencePropertyFactory(object):

    def clone(self, prototype, template):
        return ReferenceProperty(
            template,
            prototype.value_provider.reference_name,
            prototype.value_converter,
        )

    def is_clonable(self, obj):
        return isinstance(obj, ReferenceProperty)


class RelativeOffsetValuePropertyFactory(object):

    def clone(self, prototype, template):
        offset_property = RelativeOffsetValueProperty(
            template,
            prototype.value_provider.ignore_boundary,
        )
        if prototype.value_provider.ignore_boundary:
            offset_property.value = prototype.value
        return offset_property

    def is_clonable(self, obj):
        return isinstance(obj, RelativeOffsetValueProperty)


class RelativeOffsetReferencePropertyFactory(object):

    def clone(self, prototype, template):
        return RelativeOffsetReferenceProperty(
            template,
            prototype.value_provider.reference_name,
        )

    def is_clonable(self, obj):
        return isinstance(obj, RelativeOffsetReferenceProperty)


class StretchSizePropertyFactory(object):

    def clone(self, prototype, template):
        return StretchSizeProperty(template)

    def is_clonable(self, obj):
        return isinstance(obj, StretchSizeProperty)


class AutoSizeValuePropertyFactory(object):

    def clone(self, prototype, template):
        return AutoSizeValueProperty(template)

    def is_clonable(self, obj):
        return isinstance(obj, AutoSizeValueProperty)


class AutoSizeReferencePropertyFactory(object):

    def clone(self, prototype, template):
        return AutoSizeReferenceProperty(template)

    def is_clonable(self, obj):
        return isinstance(obj, AutoSizeReferenceProperty)


class TemplateFactory(object):

    def __init__(self):
        self.property_factory = PropertyFactory()

    def clone(self, prototype, parent=None):
        duplicate = type(prototype)()
        duplicate._prototype = prototype
        duplicate.name = prototype.name
        duplicate.parent = parent

        duplicate.offset_property = self.property_factory.clone(
            prototype.offset_property,
            duplicate
        )
        duplicate.size_property = self.property_factory.clone(
            prototype.size_property,
            duplicate
        )
        duplicate.boundary_property = self.property_factory.clone(
            prototype.boundary_property,
            duplicate
        )
        duplicate.padding_before_property = self.property_factory.clone(
            prototype.padding_before_property,
            duplicate
        )
        duplicate.padding_after_property = self.property_factory.clone(
            prototype.padding_after_property,
            duplicate
        )
        duplicate.count_property = self.property_factory.clone(
            prototype.count_property,
            duplicate
        )

        duplicate.signature = prototype.signature
        duplicate.hint = prototype.hint

        for child in prototype.children:
            self.clone(child, duplicate)

        return duplicate
