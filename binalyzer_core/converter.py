# -*- coding: utf-8 -*-
"""
    binalyzer_core.converter
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements value converters.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import leb128


class IdentityValueConverter(object):

    def convert(self, value, template):
        return value

    def convert_back(self, value, template):
        return value


class IntegerValueConverter(object):

    def __init__(self, byte_order='little'):
        self.byte_order = byte_order

    def convert(self, value, template):
        return int.from_bytes(value, self.byte_order)

    def convert_back(self, value, template):
        return value.to_bytes(template.size, self.byte_order)


class LEB128UnsignedValueConverter(object):

    def convert(self, value, template):
        return leb128.u.decode(value)

    def convert_back(self, value, template):
        return leb128.u.encode(value)
