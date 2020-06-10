import pytest
import io

from binalyzer_core import (
    Binalyzer,
    BindingContext,
    DataProvider,
    TemplateProvider,
    Template,
)


class TemplateProviderMock(TemplateProvider):
    def __init__(self, template):
        self._template = template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value


class DataProviderMock(DataProvider):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class ZeroDataProvider(DataProvider):
    def __init__(self, size):
        self._stream = io.BytesIO(bytes([0] * size))

    @property
    def data(self):
        return self._stream

    @data.setter
    def data(self, value):
        raise NotImplementedError()


def test_binalyzer_instantiation_with_default_parameters():
    binalyzer = Binalyzer()
    assert binalyzer.template_provider == None
    assert binalyzer.data_provider == None
    with pytest.raises(AttributeError):
        binalyzer.data
    with pytest.raises(AttributeError):
        binalyzer.template


def test_binalyzer_instantiation():
    template_provider = TemplateProvider()
    data_provider = ZeroDataProvider(0)
    binalyzer = Binalyzer(template_provider, data_provider)
    assert isinstance(binalyzer, Binalyzer)


def test_binalyzer_get_template_provider():
    template_provider = TemplateProvider()
    data_provider = ZeroDataProvider(0)
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.template_provider == template_provider


def test_binalyzer_get_data_provider():
    template_provider = TemplateProvider()
    data_provider = ZeroDataProvider(0)
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.data_provider == data_provider


def test_binalyzer_get_data():
    template_provider = TemplateProvider()
    data_provider = ZeroDataProvider(0)
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.data == data_provider.data


def test_binalyzer_get_template():
    template_provider = TemplateProvider()
    data_provider = ZeroDataProvider(0)
    binalyzer = Binalyzer(template_provider, data_provider)
    binalyzer.template


def test_binalyzer_set_template_provider():
    template_provider = TemplateProvider()
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    assert binalyzer.template_provider == template_provider


def test_binalyzer_set_template():
    template_mock1 = Template()
    template_mock2 = Template()
    template_provider = TemplateProviderMock(template_mock1)
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    binalyzer.template = template_mock2
    assert binalyzer.template == template_mock2
    assert binalyzer.template != template_mock1


def test_binalyzer_set_data_provider():
    data_provider = DataProvider()
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    assert binalyzer.data_provider == data_provider


def test_binalyzer_set_data():
    data_mock1 = object()
    data_mock2 = object()
    data_provider = DataProviderMock(data_mock1)
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    binalyzer.data = data_mock2
    assert binalyzer.data == data_mock2
    assert binalyzer.data != data_mock1
