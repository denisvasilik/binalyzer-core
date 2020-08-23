# -*- coding: utf-8 -*-
"""
    binalyzer_core.context
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements the binding context that is used to bind templates to
    binary streams.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import copy

from .template_provider import (
    TemplateProviderBase,
    TemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    ZeroedDataProvider,
)
from .factory import TemplateFactory

from anytree import findall


class BindingEngine(object):

    def __init__(self, template_factory=None):
        self.template_factory = template_factory
        if self.template_factory is None:
            self.template_factory = TemplateFactory()

    def create_dom(self, tom, binding_context):
        # (1) Clone TOM
        dom = self.template_factory.clone(tom)
        # (2) Bind data to DOM
        self.bind(dom, binding_context)
        # (3) Expand DOM
        self.expand_dom(dom)
        # (4) Return DOM
        return dom

    def bind(self, template, binding_context):
        template.binding_context = binding_context
        self._bind_children(template, binding_context)

    def _bind_children(self, template, binding_context):
        if not template.children:
            return
        for child in template.children:
            child.binding_context = binding_context
            self._bind_children(child, binding_context)

    def expand_dom(self, dom):
        """ Precondition: DOM slice has not been expanded yet.
        """
        expandables = findall(dom, filter_=lambda t: t.count > 1)
        maxdepth = dom.leaves[0].depth

        for i in range(maxdepth, -1, -1):
            for expandable in expandables:
                if expandable.depth == i:
                    self.expand_template(expandable)

    def expand_template(self, expandable):
        # add duplicates to expandable's parent
        for i in range(expandable.count):
            duplicate = type(expandable)()
            duplicate.name = expandable.name + "-" + str(i)
            duplicate.parent = expandable.parent
            duplicate.binding_context = expandable.binding_context
            duplicate.children = copy.deepcopy(expandable.children)
        # remove expandable from DOM
        expandable.parent = None


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

        self._dom = None

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        return self._dom

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self
        # create DOM using BindingEngine (DOM is used internally only)
        self._dom = self.binding_engine.create_dom()

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
