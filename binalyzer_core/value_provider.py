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

    def __init__(self, template, reference_name, byteorder='little'):
        self.template = template
        self.reference_name = reference_name
        self.byteorder = byteorder
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        referenced_template = find_by_scope(self.template, self.reference_name)
        self._cached_value = int.from_bytes(
            referenced_template.value,
            self.byteorder,
        )
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError(
            'Unable to assign a value to a reference. Consider setting the '
            'value of the referenced template instead.'
        )


class OffsetValueProvider(ValueProvider):

    def __init__(self, template, value):
        self.template = template
        self._engine = TemplateEngine()
        self._cached_value = None
        super(OffsetValueProvider, self).__init__(value)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        absolute_address = 0
        if self.template.parent:
            absolute_address += self.template.parent.absolute_address
        absolute_address += self._value
        absolute_address += self._engine._get_boundary_offset(
            absolute_address, self.template.boundary
        )
        if self.template.parent:
            relative_offset = absolute_address - self.template.parent.absolute_address
        else:
            relative_offset = absolute_address
        self._cached_value = relative_offset
        return self._cached_value

    def set_value(self, value):
        self._value = value


class RelativeOffsetValueProvider(ValueProvider):

    def __init__(self, template, ignore_boundary=False):
        self.template = template
        self.ignore_boundary = ignore_boundary
        self._engine = TemplateEngine()
        self._cached_value = None
        super(RelativeOffsetValueProvider, self).__init__()

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = (self._engine.get_offset(self.template,
                                                      self.ignore_boundary))
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError(
            'Assigning a value to a relative offset is not allowed.'
        )


class RelativeOffsetReferenceValueProvider(ReferenceValueProvider):

    def __init__(self, template, reference_name):
        self._engine = TemplateEngine()
        self._cached_value = None
        super(RelativeOffsetReferenceValueProvider, self).__init__(
            template, reference_name)

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = (self._engine.get_offset(self.template) +
                              find_by_scope(self.template, self.reference_name).value)
        return self._cached_value

    def set_value(self, value):
        self._cached_value = None
        find_by_scope(self.template, self.reference_name).value = value


class AutoSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self.template = template
        self._engine = TemplateEngine()
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        self._cached_value = self._engine.get_size(self.template)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not supported')


class StretchSizeValueProvider(ValueProvider):

    def __init__(self, template):
        self.template = template
        self._engine = TemplateEngine()
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        return self._engine.get_max_size(self.template)

    def set_value(self, value):
        raise RuntimeError('Not supported')


def find_by_scope(template, reference_name):
    while template.parent:
        result = findall_by_attr(template.parent, reference_name)
        if result:
            return result[0]
        template = template.parent
    raise RuntimeError(
        'Unable to find referenced template "' + reference_name + '".'
    )
