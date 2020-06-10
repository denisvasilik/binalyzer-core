import pytest

from binalyzer_core import (
    Binalyzer,
    BindingContext,
    TemplateProvider,
    ZeroDataProvider,
)

def test_binalyzer_default_instantiation():
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
    pass

def test_binalyzer_set_template():
    pass

def test_binalyzer_set_data_provider():
    pass

def test_binalyzer_set_data():
    pass
