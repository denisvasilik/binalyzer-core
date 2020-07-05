# -*- coding: utf-8 -*-
"""
    binalyzer_core.context
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements the binding context that is used to bind templates to
    binary streams.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from .template_provider import (
    TemplateProviderBase,
    TemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    ZeroedDataProvider,
)


class BindingContext(object):
    """The :class:`BindingContext` stores information about the binding between a
    template and binary stream. It uses a :class:`~binalyzer.TemplateProvider` and
    a :class:`~binalyzer.DataProvider` to get templates and binary streams from
    various different sources.

    The :class:`~binalyzer.BackedBindingContext` for instance uses a
    :class:`~binalyzer.ZeroedDataProvider` to bind a given template to zeroed data.

    :param template_provider: a :class:`~binalyzer.TemplateProvider`
    :param data_provider: a :class:`~binalyzer.DataProvider`
    """

    def __init__(
        self, template_provider: TemplateProviderBase, data_provider: DataProviderBase
    ):
        #: The data provider to get the binary stream from.
        self.data_provider = data_provider

        #: The template provider to get the template from.
        self.template_provider = template_provider
        self.template_provider.template.binding_context = self

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        return self.template_provider.template

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self

    @property
    def data(self):
        """A buffered or unbuffered binary stream that inherits :class:`~io.IOBase`.
        It is bound to the corresponding :attr:`~binalyzer.Binalyzer.template`.
        """
        return self.data_provider.data

    @data.setter
    def data(self, value):
        self.data_provider.data = value


class BackedBindingContext(BindingContext):
    """ The :class:`~binalyzer.BackedBindingContext` uses a
    :class:`~binalyzer.ZeroedDataProvider` to bind a given template to zeroed
    data.
    """

    def __init__(self, template):
        super(BackedBindingContext, self).__init__(
            TemplateProvider(template), ZeroedDataProvider())
