# -*- coding: utf-8 -*-
"""
    binalyzer_core.template
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the template.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from anytree import NodeMixin, find_by_attr
from anytree.util import leftsibling, rightsibling

import copy

from .properties import (
    ValueProperty,
    AutoSizeValueProperty,
    RelativeOffsetValueProperty,
    ReferenceProperty,
)
from .context import BackedBindingContext, BindingEngine

class Template(NodeMixin, object):
    """This class implements the template mechanism as described in :ref:`template`.
    In addition, it inherits :class:`~anytree.node.nodemixin.NodeMixin` of the
    `anytree`_ library making it possible to create template trees.

    .. _anytree: https://anytree.readthedocs.io/en/latest/
    """

    def __init__(self, name=None, parent=None, children=None, **kwargs):
        self._binding_context = BackedBindingContext(self)
        self._binding_engine = BindingEngine(self._binding_context)

        #: The name of the template
        self.name = name

        #: Children of the template
        if children:
            self.children = children

        #: Parent of the template
        self.parent = parent

        #: :class:`~binalyzer.Offset` of the template
        self._offset = RelativeOffsetValueProperty(self)

        #: :class:`~binalyzer.Size` of the template
        self._size = AutoSizeValueProperty(self)

        #: :class:`~binalyzer.PaddingBefore` of the template
        self._padding_before = ValueProperty()

        #: :class:`~binalyzer.PaddingAfter` of the template
        self._padding_after = ValueProperty()

        #: :class:`~binalyzer.Boundary` of the template
        self._boundary = ValueProperty()

        self._count = ValueProperty()
        self._signature = None
        self._hint = None

    @property
    def offset(self):
        return self._offset.value

    @offset.setter
    def offset(self, value):
        self._offset.value = value

    @property
    def offset_property(self):
        return self._offset

    @offset_property.setter
    def offset_property(self, value):
        self._offset = value

    @property
    def size(self):
        return self._size.value

    @size.setter
    def size(self, value):
        self._size = ValueProperty(value)

    @property
    def size_property(self):
        return self._size

    @size_property.setter
    def size_property(self, value):
        self._size = value

    @property
    def padding_before(self):
        return self._padding_before.value

    @padding_before.setter
    def padding_before(self, value):
        self._padding_before.value = value

    @property
    def padding_before_property(self):
        return self._padding_before

    @padding_before_property.setter
    def padding_before_property(self, value):
        self._padding_before = value

    @property
    def padding_after(self):
        return self._padding_after.value

    @padding_after.setter
    def padding_after(self, value):
        self._padding_after.value = value

    @property
    def padding_after_property(self):
        return self._padding_after

    @padding_after_property.setter
    def padding_after_property(self, value):
        self._padding_after = value

    @property
    def boundary(self):
        return self._boundary.value

    @boundary.setter
    def boundary(self, value):
        self._boundary.value = value

    @property
    def boundary_property(self):
        return self._boundary

    @boundary_property.setter
    def boundary_property(self, value):
        self._boundary = value

    @property
    def count(self):
        return self._count.value

    @count.setter
    def count(self, value):
        self._count.value = value

    @property
    def count_property(self):
        return self._count

    @count_property.setter
    def count_property(self, value):
        self._count = value

    @property
    def hint(self):
        return self._hint

    @hint.setter
    def hint(self, value):
        self._hint = value

    @property
    def hint_property(self):
        return self._hint

    @hint_property.setter
    def hint_property(self, value):
        self._hint = value

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, value):
        self._signature = value

    @property
    def signature_property(self):
        return self._signature

    @signature_property.setter
    def signature_property(self, value):
        self._signature = value

    @property
    def absolute_address(self):
        """Provides the absolue address of the template within the binary stream.
        """
        if isinstance(self.offset_property, ValueProperty):
            return self.offset

        if isinstance(self.offset_property, RelativeOffsetValueProperty):
            if self.parent:
                return self.offset + self.parent.absolute_address
            else:
                return self.offset

        raise TypeError()

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
        # FIX ME: Use event mechanism for decoupling (dependency inversion).
        if isinstance(self.size_property, AutoSizeValueProperty):
            self.size = len(value)
        self.binding_context.data_provider.write(self, value)

    @property
    def binding_context(self):
        """The :class:`~binalyzer.BindingContext` of the template
        """
        return self._binding_context

    @binding_context.setter
    def binding_context(self, value):
        self._binding_context = value
        # self._binding_engine.bind()

    def _post_attach(self, parent):
        self._add_name_to_parent(parent)
        self.binding_context = parent.binding_context

    def _add_name_to_parent(self, parent):
        if self.name:
            parent.__dict__[self.name.replace("-", "_")] = self
