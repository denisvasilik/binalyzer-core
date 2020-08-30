# -*- coding: utf-8 -*-
"""
    binalyzer_core.binding
    ~~~~~~~~~~~~~~~~~~~~~~

    This module implements the binding engine that is used to bind templates to
    binary streams.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from .factory import TemplateFactory
from .properties import ValueProperty
from .template_provider import (
    TemplateProviderBase,
    TemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    ZeroedDataProvider,
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

    def bind(self, template, binding_context):
        template = self._clone(template, binding_context)
        template = self._rebind(template, binding_context)
        template = self._modify(template, binding_context)
        return template

    def _clone(self, template, binding_context):
        return self.template_factory.clone(template)

    def _rebind(self, template, binding_context):
        template.binding_context = binding_context
        return template

    def _modify(self, template, binding_context):
        while True:
            template_branch = self._find(template, lambda t:
                                                  (t.count > 1 or t.count ==
                                                   0 or t.signature)
                                                  )
            if template_branch is None:
                break
            elif template_branch.count > 1:
                self._expand(template_branch)
            elif template_branch.count == 0:
                self._reduce(template_branch)
            elif template_branch.signature:
                self._validate(template_branch)
            else:
                raise RuntimeError()
        return template

    def _find(self, template, condition):
        if condition(template):
            return template
        for child in template.children:
            template = self._find(child, condition)
            if template:
                return template
        return None

    def _validate(self, template):
        size = len(template.signature)
        template.binding_context.data_provider.data.seek(
            template.absolute_address)
        value = template.binding_context.data_provider.data.read(size)
        if template.hint is None and template.signature != value:
            raise RuntimeError("Signature validation failed.")
        elif template.hint and template.signature != value:
            template.parent = None
        template.signature = None  # Tree could be annotated instead

    def _reduce(self, template):
        template.parent = None

    def _expand(self, expandable):
        count = expandable.count
        parent = expandable.parent
        left = leftsiblings(expandable)
        right = rightsiblings(expandable)
        
        expandable.parent = None
        expandable.count_property = ValueProperty(1)

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

        self._cached_dom = None

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding binary :attr:`~binalyzer.Binalyzer.data`.
        """
        return self._create_dom()

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self
        self._invalidate_dom()

    @property
    def data(self):
        """A buffered or unbuffered binary stream that inherits :class:`~io.IOBase`.
        It is bound to the corresponding :attr:`~binalyzer.Binalyzer.template`.
        """
        return self.data_provider.data

    @data.setter
    def data(self, value):
        self.data_provider.data = value

    def _invalidate_dom(self):
        self._cached_dom = None

    def _create_dom(self):
        if self._cached_dom:
            return self._cached_dom
        self._cached_dom = self._binding_engine.bind(
            self.template_provider.template,
            self
        )
        return self._cached_dom


class BackedBindingContext(BindingContext):
    """ The :class:`~binalyzer.BackedBindingContext` uses a
    :class:`~binalyzer.ZeroedDataProvider` to bind a given template to zeroed
    data.
    """

    def __init__(self, template):
        super(BackedBindingContext, self).__init__(
            TemplateProvider(template), ZeroedDataProvider())
