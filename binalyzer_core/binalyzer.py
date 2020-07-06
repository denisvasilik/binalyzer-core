# -*- coding: utf-8 -*-
"""
    binalyzer_core.binalyzer
    ~~~~~~~~~~~~~~~~~~~

    This module implements the central Binalyzer object.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import io

from typing import Optional

from .context import BindingContext
from .template_provider import TemplateProvider
from .data_provider import DataProvider
from .template import Template


class Binalyzer(object):
    """:class:`Binalyzer` is the central object and provides a high-level API
    for binding templates to binary data.

    :param template: a :class:`Template` that should be bound to binary data
    :param data: a binary stream inheriting :class:`~io.IOBase`
    """

    def __init__(self, template: Optional[Template] = None, data: Optional[io.IOBase] = None):
        if template is None:
            template = Template()

        if data is None:
            self._binding_context = template.binding_context
        else:
            self._binding_context = BindingContext(TemplateProvider(template),
                                                   DataProvider(data))

    @property
    def data(self):
        """A buffered or unbuffered binary stream that inherits :class:`~io.IOBase`.
        It is bound to the corresponding :attr:`~binalyzer.Binalyzer.template`.
        """
        return self._binding_context.data

    @data.setter
    def data(self, value):
        self._binding_context.data = value

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        return self._binding_context.template

    @template.setter
    def template(self, value):
        self._binding_context.template = value

    @property
    def template_provider(self):
        """
        """
        return self._binding_context.template_provider

    @template_provider.setter
    def template_provider(self, value):
        self._binding_context.template_provider = value

    @property
    def data_provider(self):
        """
        """
        return self._binding_context.data_provider

    @data_provider.setter
    def data_provider(self, value):
        self._binding_context.data_provider = value
