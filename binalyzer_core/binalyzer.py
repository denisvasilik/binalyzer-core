# -*- coding: utf-8 -*-
"""
    binalyzer.binalyzer
    ~~~~~~~~~~~~~~~~~~~

    This module implements the central Binalyzer object.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import io

from .provider import BufferedIODataProvider


class Binalyzer(object):
    """:class:`Binalyzer` is the central object and provides a high-level API
    for binding templates to binary data.

    :param template: a template that should be bound to a binary data stream
    :param stream: a binary data stream that sould be bound to the template
    """

    def __init__(self, template=None, stream=None):
        self._binding_context = BindingContext(template, stream)

        if template:
            self.template = template

        if stream:
            self.stream = stream

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
        self._binding_context.template.binding_context = self._binding_context
        self._binding_context.template.propagate()
        if self.stream is None:
            self.stream = io.BytesIO(bytes([0] * value.size.value))

    @property
    def stream(self):
        """A buffered IO stream that is bound to the corresponding
        :attr:`~binalyzer.binalyzer.Binalyzer.template`.
        In case a new stream is assigned it gets rebound to the template.
        """
        return self._binding_context.stream

    @stream.setter
    def stream(self, value):
        self._binding_context.stream = value
        self._binding_context.provider.stream = value


class BindingContext(object):
    """The :class:`BindingContext` is a data container that holds contextual
    information about the binding between a template and binary data. It is
    mainly an interface that is used to decouple the :class:`~binalyzer.template.Template`
    from the :class:`Binalyzer` and :class:`~binalyzer.provider.DataProvider`.

    :param template: the template to provide by the context
    :param stream: the stream to provide by the context
    """

    def __init__(self, template=None, stream=None):
        #: The template to provide by the context. It usually is the *top-most*
        #: or *root* template.
        self.template = template

        #: The stream to provide by the context
        self.stream = stream

        #: The data provider to use.
        #: Defaults to :class:`~binalyzer.provider.BufferedIODataProvider`.
        self.provider = BufferedIODataProvider(self)
