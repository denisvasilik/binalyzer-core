import pytest
import io

from binalyzer_core import (
    Binalyzer,
    BindingContext,
    SimpleDataProvider,
    ZeroDataProvider,
    SimpleTemplateProvider,
    EmptyTemplateProvider,
    ZeroDataProvider,
    Template,
)


def test_binalyzer_instantiation_with_default_parameters():
    binalyzer = Binalyzer()
    assert isinstance(binalyzer.template_provider, EmptyTemplateProvider)
    assert isinstance(binalyzer.data_provider, ZeroDataProvider)


def test_binalyzer_instantiation():
    template_provider = EmptyTemplateProvider()
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer(template_provider, data_provider)
    assert isinstance(binalyzer, Binalyzer)


def test_binalyzer_get_template_provider():
    template_provider = EmptyTemplateProvider()
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.template_provider == template_provider


def test_binalyzer_get_data_provider():
    template_provider = EmptyTemplateProvider()
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.data_provider == data_provider


def test_binalyzer_get_data():
    template_provider = EmptyTemplateProvider()
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer(template_provider, data_provider)
    assert binalyzer.data == data_provider.data


def test_binalyzer_get_template():
    template_provider = EmptyTemplateProvider()
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer(template_provider, data_provider)
    binalyzer.template


def test_binalyzer_set_template_provider():
    template_provider = EmptyTemplateProvider()
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    assert binalyzer.template_provider == template_provider


def test_binalyzer_set_template():
    template_mock1 = Template()
    template_mock2 = Template()
    template_provider = SimpleTemplateProvider(template_mock1)
    binalyzer = Binalyzer()
    binalyzer.template_provider = template_provider
    binalyzer.template = template_mock2
    assert binalyzer.template == template_mock2
    assert binalyzer.template != template_mock1


def test_binalyzer_set_data_provider():
    data_provider = ZeroDataProvider()
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    assert binalyzer.data_provider == data_provider


def test_binalyzer_set_data():
    data_mock1 = object()
    data_mock2 = object()
    data_provider = SimpleDataProvider(data_mock1)
    binalyzer = Binalyzer()
    binalyzer.data_provider = data_provider
    binalyzer.data = data_mock2
    assert binalyzer.data == data_mock2
    assert binalyzer.data != data_mock1
