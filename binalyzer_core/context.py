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

from .properties import (
    PropertyBase,
    ValueProperty,
    RelativeOffsetValueProperty,
    RelativeOffsetReferenceProperty,
    AutoSizeValueProperty,
    AutoSizeReferenceProperty,
)
from .utils import (
    leftsiblings,
    rightsiblings,
)


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
        # (3) Process DOM
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

    def reduce(self, dom):
        for t in findall(dom, filter_=lambda t: t.count == 0):
            t.parent = None

    def validate(self, dom):
        for t in findall(dom, filter_=lambda t: t.signature):
            size = len(t.signature)
            t.binding_context.data_provider.data.seek(t.absolute_address)
            value = t.binding_context.data_provider.data.read(size)
            if t.hint is None and t.signature != value:
                raise RuntimeError("Signature validation failed.")
            elif t.hint and t.signature != value:
                t.parent = None

    def validate_template(self, template):
        size = len(template.signature)
        template.binding_context.data_provider.data.seek(
            template.absolute_address)
        value = template.binding_context.data_provider.data.read(size)
        if template.hint is None and template.signature != value:
            raise RuntimeError("Signature validation failed.")
        elif template.hint and template.signature != value:
            template.parent = None
        template.signature = None  # Tree could be annotated instead

    def find_next(self, template, condition):
        if condition(template):
            return template
        for child in template.children:
            template = self.find_next(child, condition)
            if template:
                return template
        return None

    def expand_dom(self, dom):
        """ Precondition: DOM slice has not been expanded yet.
        """
        while True:
            template = self.find_next(dom, lambda t:
                                      (t.count > 1 or t.count == 0 or t.signature)
                                      )
            if template is None:
                break
            elif template.count > 1:
                self.expand_template(template)
            elif template.count == 0:
                self.reduce_template(template)
            elif template.signature:
                self.validate_template(template)
            else:
                raise RuntimeError()

    def reduce_template(self, template):
        template.parent = None

    def expand_template(self, expandable):
        # Set count to 1 for duplicates
        count = expandable.count
        expandable.count_property = ValueProperty(1)

        left = leftsiblings(expandable)
        right = rightsiblings(expandable)

        # remove expandable from DOM
        parent = expandable.parent
        expandable.parent = None

        # add duplicates to expandable's parent
        duplicates = []
        for i in range(count):
            duplicates.append(self.template_factory.clone(expandable, id=i))

        parent_children = []
        parent_children.extend(left)
        parent_children.extend(duplicates)
        parent_children.extend(right)

        parent.children = parent_children


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

        self._binding_engine = BindingEngine()

        #: The template provider to get the template from.
        self.template_provider = template_provider
        self.template_provider.template.binding_context = self

        self._dom = None

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        if self._dom is None:
            self._dom = self._binding_engine.create_dom(
                self.template_provider.template,
                self
            )
        return self._dom

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self
        self._dom = self._binding_engine.create_dom(
            self.template_provider.template,
            self
        )

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
