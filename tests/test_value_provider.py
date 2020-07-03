import io
import pytest

from binalyzer_core import (
    ValueProvider,
    FunctionValueProvider,
    ReferenceValueProvider,
    RelativeOffsetValueProvider,
    RelativeOffsetReferenceProvider,
    Template,
)


def test_value_provider_default_instantiation():
    value_provider = ValueProvider()
    assert value_provider.get_value() == 0


def test_value_provider_instantiation():
    value_provider = ValueProvider(42)
    assert value_provider.get_value() == 42


def test_value_provider_set_value():
    value_provider = ValueProvider(47)
    value_provider.set_value(23)
    assert value_provider.get_value() == 23


def test_function_value_provider_default_instantiation():
    value_provider = FunctionValueProvider()
    with pytest.raises(TypeError):
        value_provider.get_value()


def test_function_value_provider_instantiation():
    def value_func(): return 17
    value_provider = FunctionValueProvider(value_func)
    assert value_provider.get_value() == 17
    assert value_provider.func == value_func


def test_function_value_provider_set_value():
    value_provider = FunctionValueProvider()
    value_provider.func = lambda: 78
    with pytest.raises(RuntimeError):
        value_provider.set_value(lambda: 1)
    assert value_provider.get_value() == 78


def test_reference_value_provider_get_value():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_c.size = 4
    template_c.value = bytes([0x01, 0x02, 0x03, 0x04])
    value_provider = ReferenceValueProvider(template_b, 'c')
    assert value_provider.get_value() == bytes([0x01, 0x02, 0x03, 0x04])


def test_reference_value_provider_set_value():
    template_a = Template(name='a')
    template_b = Template(name='b', parent=template_a)
    template_c = Template(name='c', parent=template_a)
    template_c.size = 4
    value_provider = ReferenceValueProvider(template_b, 'c')
    value_provider.set_value(bytes([0x01, 0x02, 0x03, 0x04]))
    assert value_provider.get_value() == bytes([0x01, 0x02, 0x03, 0x04])


def test_relative_offset_value_provider_instantiation():
    template = Template()
    value_provider = RelativeOffsetValueProvider(template)
    assert value_provider.get_value() == 0


def test_relative_offset_value_provider_set_value():
    template = Template()
    value_provider = RelativeOffsetValueProvider(template)
    value_provider.set_value(123)
    assert value_provider.get_value() == 123