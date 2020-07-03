from binalyzer_core import (
    AddressingMode,
    ByteOrder,
)


def test_default_instantiation():
    byte_order = ByteOrder()
    assert isinstance(byte_order, ByteOrder)
    assert byte_order.value == ByteOrder.LITTLE_ENDIAN_VALUE


def test_instantiation_with_value():
    byte_order = ByteOrder(ByteOrder.BIG_ENDIAN_VALUE)
    assert isinstance(byte_order, ByteOrder)
    assert byte_order.value == ByteOrder.BIG_ENDIAN_VALUE
    byte_order = ByteOrder(ByteOrder.LITTLE_ENDIAN_VALUE)
    assert isinstance(byte_order, ByteOrder)
    assert byte_order.value == ByteOrder.LITTLE_ENDIAN_VALUE


def test_factory_method_for_byte_order_little_endian():
    byte_order = ByteOrder.LittleEndian
    assert isinstance(byte_order, ByteOrder)
    assert byte_order.value == ByteOrder.LITTLE_ENDIAN_VALUE


def test_factory_method_for_byte_order_big_endian():
    byte_order = ByteOrder.BigEndian
    assert isinstance(byte_order, ByteOrder)
    assert byte_order.value == ByteOrder.BIG_ENDIAN_VALUE


def test_default_instantiation():
    addressing_mode = AddressingMode()
    assert isinstance(addressing_mode, AddressingMode)
    assert addressing_mode.value == AddressingMode.ABSOLUTE_VALUE


def test_instantiation_with_value():
    addressing_mode = AddressingMode(AddressingMode.ABSOLUTE_VALUE)
    assert isinstance(addressing_mode, AddressingMode)
    assert addressing_mode.value == AddressingMode.ABSOLUTE_VALUE
    addressing_mode = AddressingMode(AddressingMode.RELATIVE_VALUE)
    assert isinstance(addressing_mode, AddressingMode)
    assert addressing_mode.value == AddressingMode.RELATIVE_VALUE


def test_factory_method_for_addressing_mode_absolute():
    addressing_mode = AddressingMode.Absolute
    assert isinstance(addressing_mode, AddressingMode)
    assert addressing_mode.value == AddressingMode.ABSOLUTE_VALUE


def test_factory_method_for_addressing_mode_relative():
    addressing_mode = AddressingMode.Relative
    assert isinstance(addressing_mode, AddressingMode)
    assert addressing_mode.value == AddressingMode.RELATIVE_VALUE
