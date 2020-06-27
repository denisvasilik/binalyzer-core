# -*- coding: utf-8 -*-
"""
    binalyzer.template
    ~~~~~~~~~~~~~~~~~~

    This module implements the concepts of the template mechanism.

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
    """This class implements the concept described in :ref:`template`. It is
    used to establish the template object model that makes binary data
    accessible.
    """

    def __init__(self, name=None, parent=None, children=None, **kwargs):
        self._value = bytes([0])

        self._binding_context = BackedBindingContext(self)

        #: The unique identifier of the template
        self.name = name

        #: Children of the template
        if children:
            self.children = children

        #: Parent of the template (optional)
        self.parent = parent

        #: :class:`~binalyzer.template.AddressingMode` of the template
        self.addressing_mode = AddressingMode.Relative

        #: :class:`~binalyzer.template.Offset` of the template
        self.offset = Offset(template=self)

        #: :class:`~binalyzer.template.Size` of the template
        self.size = Size(template=self)

        #: :class:`~binalyzer.template.Sizing` of the template
        self.sizing = Sizing.Auto

        #: :class:`~binalyzer.template.PaddingBefore` of the template
        self.padding_before = PaddingBefore(template=self)

        #: :class:`~binalyzer.template.PaddingAfter` of the template
        self.padding_after = PaddingAfter(template=self)

        #: :class:`~binalyzer.template.Boundary` of the template
        self.boundary = Boundary(template=self)

    @property
    def absolute_address(self):
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
        bound to. It uses the :attr:`~binalyzer.binalyzer.BindingContext.provider`
        of the :class:`~binalyzer.binalyzer.BindingContext`.

        Reading from the property provides a buffered IO stream of the area the
        template is bound to. Likewise, writing to the property writes a buffered
        IO stream to the area the template is bound to.

        .. note:: The size of the buffered IO stream must match the
                  :py:attr:`~binalyzer.template.Template.size` of the template.
        """
        if self.binding_context:
            return self.binding_context.data_provider.read(self)
        else:
            return self._value

    @value.setter
    def value(self, value):
        if self.binding_context:
            self.binding_context.data_provider.write(self, value)
        else:
            self._value = value

    @property
    def binding_context(self):
        """The :class:`~binalyzer.binalyzer.BindingContext` of the template
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
        """Propagates the binding context top-down from this element to its
        children.
        """
        for child in self.children:
            child.binding_context = self.binding_context
            child._propagate_binding_context()
