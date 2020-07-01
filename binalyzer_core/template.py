# -*- coding: utf-8 -*-
"""
    binalyzer.template
    ~~~~~~~~~~~~~~~~~~

    This module implements the template.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import NodeMixin, find_by_attr
from anytree.util import leftsibling, rightsibling

from .properties import (
    AddressingMode,
    Boundary,
    Offset,
    PaddingBefore,
    PaddingAfter,
    ResolvableValue,
    Size,
    Sizing,
)
from .context import BackedBindingContext


class Template(NodeMixin, object):
    """This class implements the template mechanism as described in :ref:`template`.
    In addition, it inherits :class:`~anytree.node.nodemixin.NodeMixin` of the
    `anytree`_ library making it possible to create template trees.

    .. _anytree: https://anytree.readthedocs.io/en/latest/
    """

    def __init__(self, name=None, parent=None, children=None, **kwargs):
        self._binding_context = BackedBindingContext(self)

        #: The name of the template
        self.name = name

        #: Children of the template
        if children:
            self.children = children

        #: Parent of the template
        self.parent = parent

        #: :class:`~binalyzer.AddressingMode` of the template
        self.addressing_mode = AddressingMode.Relative

        #: :class:`~binalyzer.Offset` of the template
        self.offset = Offset(template=self)

        #: :class:`~binalyzer.Size` of the template
        self.size = Size(template=self)

        #: :class:`~binalyzer.Sizing` of the template
        self.sizing = Sizing.Auto

        #: :class:`~binalyzer.PaddingBefore` of the template
        self.padding_before = PaddingBefore(template=self)

        #: :class:`~binalyzer.PaddingAfter` of the template
        self.padding_after = PaddingAfter(template=self)

        #: :class:`~binalyzer.Boundary` of the template
        self.boundary = Boundary(template=self)

    @property
    def absolute_address(self):
        """Provides the absolue address of the template within the binary stream.
        """
        if self.addressing_mode == AddressingMode.Absolute:
            return self.offset
        elif self.parent:
            return ResolvableValue(
                self.offset.value + self.parent.absolute_address.value
            )
        else:
            return ResolvableValue(self.offset.value)

    @property
    def value(self):
        """The :attr:`value` provides direct access to the data the template is
        bound to. It uses the :attr:`~binalyzer.BindingContext.data_provider`
        of the :class:`~binalyzer.BindingContext`.

        Reading from the property provides a binary stream of the area the
        template is bound to. Likewise, writing to the property writes a binary
        stream to the same area.
        """
        return self.binding_context.data_provider.read(self)

    @value.setter
    def value(self, value):
        self.binding_context.data_provider.write(self, value)

    @property
    def binding_context(self):
        """The :class:`~binalyzer.BindingContext` of the template
        """
        return self._binding_context

    @binding_context.setter
    def binding_context(self, value):
        self._binding_context = value
        self._propagate_binding_context()

    def _post_attach(self, parent):
        if self.name:
            parent.__dict__[self.name.replace("-", "_")] = self
        self.binding_context = parent.binding_context

    def _propagate_binding_context(self):
        for child in self.children:
            child.binding_context = self.binding_context
            child._propagate_binding_context()
