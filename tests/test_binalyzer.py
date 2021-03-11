"""
    test_binalyzer
    ~~~~~~~~~~~~~~

    This module implements tests for the Binalyzer object.
"""
import pytest
import io

from binalyzer_core import (
    Binalyzer,
    BinalyzerExtension,
    BindingContext,
    DataProvider,
    ZeroedDataProvider,
    TemplateProvider,
    PlainTemplateProvider,
    ZeroedDataProvider,
    Template,
)


def test_binalyzer_value_write_resets_data_stream_position():
    binalyzer = Binalyzer()
    binalyzer.template.size = 64
    binalyzer.template.value = bytes([0x01] * 64)
    assert binalyzer.data.tell() == 0


def test_binalyzer_value_read_resets_data_stream_position():
    binalyzer = Binalyzer()
    binalyzer.template.size = 64
    binalyzer.template.value = bytes([0x01] * 64)
    value = binalyzer.template.value
    assert binalyzer.data.tell() == 0
    assert value == bytes([0x01] * 64)


def test_binalyzer_instantiation_with_default_parameters():
    binalyzer = Binalyzer()
    assert isinstance(binalyzer.template_provider, TemplateProvider)
    assert isinstance(binalyzer.data_provider, DataProvider)


def test_binalyzer_instantiation():
    template_provider = PlainTemplateProvider()
    data_provider = ZeroedDataProvider()
    binalyzer = Binalyzer(template_provider.template, data_provider.data)
    assert isinstance(binalyzer, Binalyzer)


def test_binalyzer_get_template_provider():
    template_provider = PlainTemplateProvider()
    template = template_provider.template
    data_provider = ZeroedDataProvider()
    data = data_provider.data
    binalyzer = Binalyzer(template, data)
    assert binalyzer.template_provider != template_provider
    assert binalyzer.template_provider.template.name == template.name
    assert binalyzer.template.name == template.name


def test_binalyzer_get_data_provider():
    template = PlainTemplateProvider().template
    data_provider = ZeroedDataProvider()
    data = data_provider.data
    binalyzer = Binalyzer(template, data)
    assert binalyzer.data_provider != data_provider
    assert binalyzer.data_provider.data == data
    assert binalyzer.data == data


def test_binalyzer_get_data():
    template = PlainTemplateProvider().template
    data = ZeroedDataProvider().data
    binalyzer = Binalyzer(template, data)
    assert binalyzer.data == data


def test_binalyzer_get_template():
    binalyzer = Binalyzer()
    binalyzer.template_provider = PlainTemplateProvider()
    binalyzer.data_provider = ZeroedDataProvider()
    assert binalyzer.template


def test_binalyzer_set_template_provider():
    template_provider = PlainTemplateProvider()
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    assert binalyzer.template_provider == template_provider


def test_binalyzer_set_template():
    template_mock1 = Template(name="a")
    template_mock2 = Template(name="b")
    template_provider = TemplateProvider(template_mock1)
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    binalyzer.template = template_mock2
    assert binalyzer.template.name == template_mock2.name
    assert binalyzer.template.name != template_mock1.name


def test_binalyzer_set_data_provider():
    data_provider = ZeroedDataProvider()
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    assert binalyzer.data_provider == data_provider


def test_binalyzer_set_data():
    data_mock1 = object()
    data_mock2 = object()
    data_provider = DataProvider(data_mock1)
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    binalyzer.data = data_mock2
    assert binalyzer.data == data_mock2
    assert binalyzer.data != data_mock1


def test_add_extension_at_object_creation():
    binalyzer = Binalyzer()
    mock = MockExtension(binalyzer)
    assert binalyzer.has_extension("mock")
    assert len(binalyzer.extensions), 1
    assert isinstance(binalyzer.extensions["mock"], MockExtension)
    assert id(mock) == id(binalyzer.extension("mock"))
    assert id(mock) == id(binalyzer.mock)


def test_add_extension():
    mock = MockExtension(None)
    binalyzer = Binalyzer()
    binalyzer.extensions = {}
    binalyzer.add_extension("mock", mock)
    assert binalyzer.has_extension("mock")
    assert len(binalyzer.extensions) == 1
    assert isinstance(binalyzer.extensions["mock"], MockExtension)
    assert id(mock) == id(binalyzer.extension("mock"))
    assert id(mock) == id(binalyzer.mock)


def test_add_extension_twice():
    binalyzer = Binalyzer()
    mock = MockExtension(None)
    binalyzer.add_extension("mock", mock)
    with pytest.raises(RuntimeError):
        binalyzer.add_extension("mock", mock)


def test_del_non_existent_extension():
    binalyzer = Binalyzer()
    with pytest.raises(RuntimeError):
        binalyzer.del_extension("mock")


def test_del_extension():
    binalyzer = Binalyzer()
    binalyzer.extensions = {}
    mock = MockExtension(binalyzer)
    assert binalyzer.has_extension("mock")
    assert len(binalyzer.extensions) == 1
    assert isinstance(binalyzer.extensions["mock"], MockExtension)
    assert id(mock) == id(binalyzer.extension("mock"))
    assert id(mock) == id(binalyzer.mock)
    binalyzer.del_extension("mock")
    assert not binalyzer.has_extension("mock")
    assert len(binalyzer.extensions) == 0


def test_dispose_extension():
    binalyzer = Binalyzer()
    binalyzer.extensions = {}
    mock = MockExtension(binalyzer)
    assert binalyzer.has_extension("mock")
    assert len(binalyzer.extensions) == 1
    assert isinstance(binalyzer.extensions["mock"], MockExtension)
    assert id(mock) == id(binalyzer.extension("mock"))
    binalyzer.del_extension("mock")
    assert not binalyzer.has_extension("mock")
    assert len(binalyzer.extensions) == 0
    assert mock.disposed


def test_has_extension():
    binalyzer = Binalyzer()
    mock = MockExtension(binalyzer)
    assert binalyzer.has_extension("mock")
    assert len(binalyzer.extensions), 1
    assert isinstance(binalyzer.extensions["mock"], MockExtension)
    assert id(mock) == id(binalyzer.extension("mock"))


def test_count_array_access():
    a = Template(name="a")
    b = Template(name="b", parent=a)
    b.count = 3

    binalyzer = Binalyzer()
    binalyzer.template = a

    assert len(binalyzer.template.b) == 3
    assert binalyzer.template.b[0].name == "b-0"
    assert binalyzer.template.b[1].name == "b-1"
    assert binalyzer.template.b[2].name == "b-2"


class MockExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        self.disposed = False
        super(MockExtension, self).__init__(binalyzer, "mock")

    def init_extension(self):
        super(MockExtension, self).init_extension()

    def dispose(self):
        self.disposed = True
