# -*- coding: utf-8 -*-
"""
    binalyzer.binalyzer
    ~~~~~~~~~~~~~~~~~~~

    This module implements the central Binalyzer object.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import io

from .context import BindingContext


class Binalyzer(object):
    """:class:`Binalyzer` is the central object and provides a high-level API
    for binding templates to binary data.

    :param template: a template that should be bound to a binary data stream
    :param stream: a binary data stream that sould be bound to the template
    """

    def __init__(self, template_provider=None, data_provider=None):
        self._binding_context = BindingContext(template_provider, data_provider)

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding :attr:`~binalyzer.binalyzer.Binalyzer.stream`. In
        case a new template is assigned it gets rebound to the buffered IO
        stream.
        """
        return self._binding_context.template

    @template.setter
    def template(self, value):
        self._binding_context.template = value

    @property
    def template_provider(self):
        return self._binding_context.template_provider

    @template_provider.setter
    def template_provider(self, value):
        self._binding_context.template_provider = value

    @property
    def data(self):
        """A buffered IO stream that is bound to the corresponding
        :attr:`~binalyzer.binalyzer.Binalyzer.template`.
        In case a new stream is assigned it gets rebound to the template.
        """
        return self._binding_context.data

    @data.setter
    def data(self, value):
        self._binding_context.data = value

    @property
    def data_provider(self):
        return self._binding_context.data_provider

    @data_provider.setter
    def data_provider(self, value):
        self._binding_context.data_provider = value
