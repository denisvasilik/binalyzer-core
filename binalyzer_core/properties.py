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

from .utils import (
    classproperty_support,
    classproperty,
)
from .value_provider import (
    ValueProvider,
    FunctionValueProvider,
    ReferenceValueProvider,
    AutoSizeValueProvider,
    RelativeOffsetValueProvider,
    IdentityValueConverter,
    IntegerValueConverter,
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
            template,
            ReferenceValueProvider(template, reference_name),
            IntegerValueConverter()
        )


class RelativeOffsetProperty(PropertyBase):

    def __init__(self, template):
        super(RelativeOffsetProperty, self).__init__(
            template, RelativeOffsetValueProvider(template))


class StretchedSizeProperty(PropertyBase):

    def __init__(self, template):
        super(Offset, self).__init__(
            template, StretchSizeValueProvider(template))


class AutoSizeProperty(PropertyBase):

    def __init__(self, template):
        super(AutoSizeProperty, self).__init__(
            template, AutoSizeValueProvider(template))


@classproperty_support
class AddressingMode(object):
    """Determines whether the addressing of the :class:`Template` is ``absolute``
    or ``relative``.
    """

    ABSOLUTE_VALUE = "absolute"
    RELATIVE_VALUE = "relative"
    DEFAULT_VALUE = ABSOLUTE_VALUE
    ADDRESSING_MODES = [ABSOLUTE_VALUE, RELATIVE_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'relative' or 'absolute'.")

    def _is_valid(self, value):
        return value in self.ADDRESSING_MODES

    @classproperty
    def Absolute(cls):
        return cls(cls.ABSOLUTE_VALUE)

    @classproperty
    def Relative(cls):
        return cls(cls.RELATIVE_VALUE)

    def __eq__(self, other):
        return self.value == other.value


@classproperty_support
class Sizing(object):
    """Determines whether the sizing of a :class:`Template` should be ``fix`` or
    dynamically calculated using ``auto`` or ``stretch``.
    """

    AUTO_VALUE = "auto"
    FIX_VALUE = "fix"
    STRETCH_VALUE = "stretch"
    DEFAULT_VALUE = AUTO_VALUE
    SIZING = [AUTO_VALUE, FIX_VALUE, STRETCH_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'auto', 'fix' or 'stretch'.")

    def _is_valid(self, value):
        return value in self.SIZING

    @classproperty
    def Auto(cls):
        return cls(cls.AUTO_VALUE)

    @classproperty
    def Fix(cls):
        return cls(cls.FIX_VALUE)

    @classproperty
    def Stretch(cls):
        return cls(cls.STRETCH_VALUE)

    def __eq__(self, other):
        return self.value == other.value


@classproperty_support
class ByteOrder(object):
    """Determines the endianess of the byte-sequence the :class:`Template` is
    bound to. Valid values are `LittleEndian` or `BigEndian`.
    """

    LITTLE_ENDIAN_VALUE = "LittleEndian"
    BIG_ENDIAN_VALUE = "BigEndian"
    DEFAULT_VALUE = LITTLE_ENDIAN_VALUE
    BYTE_ORDERS = [LITTLE_ENDIAN_VALUE, BIG_ENDIAN_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'LittleEndian' or 'BigEndian'.")

    def _is_valid(self, value):
        return value in self.BYTE_ORDERS

    @classproperty
    def LittleEndian(cls):
        return cls(cls.LITTLE_ENDIAN_VALUE)

    @classproperty
    def BigEndian(cls):
        return cls(cls.BIG_ENDIAN_VALUE)

    def __eq__(self, other):
        return self.value == other.value
