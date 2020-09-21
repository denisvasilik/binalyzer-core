"""
    test_value_provider
    ~~~~~~~~~~~~~~~~~~~

    This module implements tests for the value provider module.
"""
import io
import pytest

from binalyzer_core import (
    ValueProvider,
    RelativeOffsetValueProvider,
    RelativeOffsetReferenceValueProvider,
    Template,
)


# def test_value_provider_default_instantiation():
#     value_provider = ValueProvider()
#     assert value_provider.get_value() == 0


# def test_value_provider_instantiation():
#     value_provider = ValueProvider(42)
#     assert value_provider.get_value() == 42


# def test_value_provider_set_value():
#     value_provider = ValueProvider(47)
#     value_provider.set_value(23)
#     assert value_provider.get_value() == 23


# def test_reference_value_provider_get_little_endian_value():
#     template_a = Template(name='a')
#     template_b = Template(name='b', parent=template_a)
#     template_c = Template(name='c', parent=template_a)
#     template_c.size = 4
#     template_c.value = bytes([0x01, 0x02, 0x03, 0x04])
#     value_provider = ReferenceValueProvider(template_b, 'c')
#     assert value_provider.get_value() == 67305985


# def test_reference_value_provider_get_big_endian_value():
#     template_a = Template(name='a')
#     template_b = Template(name='b', parent=template_a)
#     template_c = Template(name='c', parent=template_a)
#     template_c.size = 4
#     template_c.value = bytes([0x01, 0x02, 0x03, 0x04])
#     value_provider = ReferenceValueProvider(template_b, 'c', 'big')
#     assert value_provider.get_value() == 16909060


# def test_reference_value_provider_set_value():
#     template_a = Template(name='a')
#     template_b = Template(name='b', parent=template_a)
#     template_c = Template(name='c', parent=template_a)
#     template_c.size = 4
#     template_c.value = bytes([0x01, 0x02, 0x03, 0x04])
#     value_provider = ReferenceValueProvider(template_b, 'c')
#     with pytest.raises(RuntimeError):
#         value_provider.set_value(bytes([0x07, 0x08, 0x09, 0x0A]))
#     assert value_provider.get_value() == 67305985


# def test_relative_offset_value_provider_instantiation():
#     template = Template()
#     value_provider = RelativeOffsetValueProvider(template)
#     assert value_provider.get_value() == 0


# def test_relative_offset_value_provider_set_value():
#     template = Template()
#     value_provider = RelativeOffsetValueProvider(template)
#     with pytest.raises(RuntimeError):
#         value_provider.set_value(123)
#     assert value_provider.get_value() == 0
