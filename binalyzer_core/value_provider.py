# -*- coding: utf-8 -*-
"""
    binalyzer_core.value_provider
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value providers.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import findall_by_attr

from .template_engine import TemplateEngine


class ValueProviderBase(object):

    def __init__(self, property):
        self.property = property

    def get_value(self):
        pass

    def set_value(self, value):
        pass


class ValueProvider(ValueProviderBase):

    def __init__(self, property):
        self._value = 0
        super(ValueProvider, self).__init__(property)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class TemplateValueProvider(ValueProviderBase):

    def __init__(self, property):
        self.byteorder = 'little'
        self._cached_value = None
        super(TemplateValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = int.from_bytes(
            self.property.template.value,
            self.byteorder,
        )
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError(
            'Read-Only: Unable to assign a value to template using a value '
            'provider.'
        )


class OffsetValueProvider(ValueProvider):

    def __init__(self, property):
        self._engine = TemplateEngine()
        self._cached_value = None
        super(OffsetValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        absolute_address = 0
        template = self.property.template
        if template.parent:
            absolute_address += template.parent.absolute_address
        absolute_address += self._value
        absolute_address += self._engine._get_boundary_offset(
            absolute_address, template.boundary
        )
        if template.parent:
            relative_offset = absolute_address - template.parent.absolute_address
        else:
            relative_offset = absolute_address
        self._cached_value = relative_offset
        return self._cached_value

    def set_value(self, value):
        self._value = value


class RelativeOffsetValueProvider(ValueProviderBase):

    def __init__(self, property):
        self.ignore_boundary = False
        self._engine = TemplateEngine()
        self._cached_value = None
        super(RelativeOffsetValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = (self._engine.get_offset(self.property.template,
                                                      self.ignore_boundary))
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError(
            'Read-Only: Assigning a value to a relative offset is not allowed.'
        )


class RelativeOffsetReferenceValueProvider(ValueProviderBase):

    def __init__(self, property):
        self._engine = TemplateEngine()
        self._cached_value = None
        super(RelativeOffsetReferenceValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = (self._engine.get_offset(self.property.template) +
                              self.property.template.value)
        return self._cached_value

    def set_value(self, value):
        self._cached_value = None
        self.property.template.value = value


class AutoSizeValueProvider(ValueProviderBase):

    def __init__(self, property):
        self._engine = TemplateEngine()
        self._cached_value = None
        super(AutoSizeValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = self._engine.get_size(self.property.template)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not supported')


class StretchSizeValueProvider(ValueProvider):

    def __init__(self, property):
        self._engine = TemplateEngine()
        self._cached_value = None
        super(StretchSizeValueProvider, self).__init__(property)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        return self._engine.get_max_size(self.property.template)

    def set_value(self, value):
        raise RuntimeError('Not supported')
