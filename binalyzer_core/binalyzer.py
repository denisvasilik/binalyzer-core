# -*- coding: utf-8 -*-
"""
    binalyzer.binalyzer
    ~~~~~~~~~~~~~~~~~~~

    This module implements the central Binalyzer object.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import io


class TemplateProvider(object):
    @property
    def template(self):
        pass

    @template.setter
    def template(self, value):
        pass


class DataProvider(object):
    @property
    def data(self):
        pass

    @data.setter
    def data(self, value):
        pass

    def read(self, template):
        pass

    def write(self, template, value):
        pass


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


class BindingContext(object):
    """The :class:`BindingContext` is a data container that holds contextual
    information about the binding between a template and binary data. It is
    mainly an interface that is used to decouple the :class:`~binalyzer.template.Template`
    from the :class:`Binalyzer` and :class:`~binalyzer.provider.DataProvider`.

    :param template: the template to provide by the context
    :param stream: the stream to provide by the context
    """

    def __init__(
        self, template_provider: TemplateProvider, data_provider: DataProvider
    ):
        #: The template to provide by the context. It usually is the *top-most*
        #: or *root* template.
        self.template_provider = template_provider

        #: The data provider to use.
        #: Defaults to :class:`~binalyzer.provider.BufferedIODataProvider`.
        self.data_provider = data_provider

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding :attr:`~binalyzer.binalyzer.Binalyzer.stream`. In
        case a new template is assigned it gets rebound to the buffered IO
        stream.
        """
        return self.template_provider.template

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self
        # FIXME: Move propagate to template, it should be called if binding
        #        context changes.
        self.template_provider.template.propagate()

    @property
    def data(self):
        """A buffered IO stream that is bound to the corresponding
        :attr:`~binalyzer.binalyzer.Binalyzer.template`.
        In case a new stream is assigned it gets rebound to the template.
        """
        return self.data_provider.data

    @data.setter
    def data(self, value):
        self.data_provider.data = value
