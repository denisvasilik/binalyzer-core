# -*- coding: utf-8 -*-
"""
    binalyzer_core.binalyzer
    ~~~~~~~~~~~~~~~~~~~~~~~~

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
            data = io.BytesIO()

        self._binding_context = BindingContext(TemplateProvider(template),
                                               DataProvider(data))

        #: A list of registered Binalyzer extensions.
        self.extensions = {}

        self._register_extensions()

    @property
    def data(self):
        """A buffered or unbuffered binary stream that inherits :class:`~io.IOBase`.
        It is bound to the corresponding :attr:`~binalyzer.Binalyzer.template`.
        """
        return self._binding_context.data

    @data.setter
    def data(self, value: io.IOBase):
        self._binding_context.data = value

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        return self._binding_context.template

    @template.setter
    def template(self, value: Template):
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

    def add_extension(self, name, extension):
        """Adds a Binalyzer extension.

        :param name: a unique name of the Binalyzer extension to add
        :param extension: a Binalyzer extension object

        .. note:: The Binalyzer extension name `template` is reserved for
                  internal use.
        """
        if self.has_extension(name):
            raise RuntimeError('Unable to initialize {:s} extension more than once!'
                               .format(name))
        self.__dict__[name] = extension
        self.extensions[name] = extension

    def del_extension(self, name):
        """Removes a Binalyzer extension. Raises
        a :class:`RuntimeError` if the extension does not exist.

        :param name: name of the Binalyzer extension to remove
        """
        if self.has_extension(name):
            if 'dispose' in self.extensions[name].__class__.__dict__:
                self.extensions[name].dispose()
            del self.extensions[name]
            del self.__dict__[name]
        else:
            raise RuntimeError('Unable to delete non-existent extension!')

    def has_extension(self, name):
        """Returns :const:`True` if the the Binalyzer extension exists;
        otherwise :const:`False`.

        :param name: name of the Binalyzer extension
        """
        return not self.extension(name) is None

    def extension(self, name):
        """Returns the Binalyzer extension that relates to the given
        name. Raises a :class:`KeyError` in case the extension does not exist.

        :param name: name of the Binalyzer extension to return
        """
        if name in self.__dict__:
            return self.__dict__[name]
        return None

    def _register_extensions(self):
        pass
