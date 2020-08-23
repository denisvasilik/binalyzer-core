# -*- coding: utf-8 -*-
"""
    binalyzer_core.factory
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements factories used for cloning types.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import copy

from .properties import ReferenceProperty

class PropertyFactory(object):

    def __init__(self):
        pass

    def clone(self, prototype, template):
        duplicate = copy.deepcopy(prototype)
        duplicate.template = template
        if isinstance(duplicate, ReferenceProperty):
            duplicate.value_provider.template = template
        return duplicate


class TemplateFactory(object):

    def __init__(self):
        self.property_factory = PropertyFactory()

    def clone(self, prototype):
        duplicate = copy.deepcopy(prototype)
        duplicate.prototype = prototype
        return duplicate

    def clone2(self, prototype):
        duplicate = type(prototype)()
        duplicate.name = prototype.name
        duplicate.size_property = self.property_factory.clone(
            prototype.size_property,
            duplicate
        )
        return duplicate