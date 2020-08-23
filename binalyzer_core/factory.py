# -*- coding: utf-8 -*-
"""
    binalyzer_core.factory
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements factories used for cloning types.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import copy

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
        duplicate = factory.clone(prototype)
        return duplicate


class PropertyBaseFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)
        #duplicate.template = template
        # duplicate.value_provider = type(prototype.value_provider)(

        # )
        # duplicate.value_converter = type(prototype.value_converter)(

        # )
        # return duplicate

    def is_clonable(self, obj):
        return isinstance(obj, PropertyBase)


class ValuePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, ValueProperty)


class FunctionPropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, FunctionProperty)


class ReferencePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)
        # if isinstance(duplicate, ReferenceProperty):
        #    duplicate.value_provider.template = template

    def is_clonable(self, obj):
        return isinstance(obj, ReferenceProperty)


class RelativeOffsetValuePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, RelativeOffsetValueProperty)


class RelativeOffsetReferencePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, RelativeOffsetReferenceProperty)


class StretchSizePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, StretchSizeProperty)


class AutoSizeValuePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, AutoSizeValueProperty)


class AutoSizeReferencePropertyFactory(object):

    def clone(self, prototype):
        return copy.copy(prototype)

    def is_clonable(self, obj):
        return isinstance(obj, AutoSizeReferenceProperty)


class TemplateFactory(object):

    def __init__(self):
        self.property_factory = PropertyFactory()

    def clone(self, prototype, parent=None):
        duplicate = type(prototype)()
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

        for child in prototype.children:
            self.clone(child, duplicate)

        return duplicate

    def clone3(self, prototype):
        duplicate = copy.deepcopy(prototype)
        duplicate.prototype = prototype
        return duplicate
