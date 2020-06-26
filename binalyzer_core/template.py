# -*- coding: utf-8 -*-
"""
    binalyzer.template
    ~~~~~~~~~~~~~~~~~~

    This module implements the concepts of the template mechanism.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
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


class Template(object):
    """This class implements the concept described in :ref:`template`. It is
    used to establish the template object model that makes binary data
    accessible.
    """

    def __init__(self, id=None, parent=None):
        #: The unique identifier of the template
        self.id = id

        #: Parent of the template (optional)
        self.parent = parent

        #: Children of the template
        self.children = []

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

        #: :class:`~binalyzer.binalyzer.BindingContext` of the template
        self.binding_context = None

        if self.parent:
            self.binding_context = self.parent.binding_context
            self.parent.add_child(self)
        self._value = bytes([0])

    @property
    def root(self):
        if self.parent is None:
            return self
        return self.parent.root

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

    def add_child(self, value):
        """Add a template as children to this template.
        """
        self.children.append(value)
        if value.id:
            self.__dict__[value.id.replace("-", "_")] = value
        if self.binding_context:
            self.propagate()

    def find(self, ref_id):
        """Find an element using the given ``ref_id``. Returns the element if
        found; otherwise ``None``.

        .. note:: The :py:attr:`~binalyzer.template.Template.find` method just searches
                  for the first occurrence of an ``ref_id``. If an identical
                  ``ref_id`` exists multiple times, the first found will be returned.
        """
        return_value = None
        for child in self.children:
            if child.id == ref_id:
                return child
            return_value = child.find(ref_id)
            if return_value:
                return return_value
        return return_value

    def propagate(self):
        """Propagates the binding context top-down from this element to its
        children.
        """
        for child in self.children:
            child.binding_context = self.binding_context
            child.propagate()

    def get_siblings(self):
        return [sibling for sibling in self.parent.children if sibling != self]

    def get_previous_sibling(self):
        previous_siblings = self.get_previous_siblings()
        if previous_siblings:
            return previous_siblings[-1]
        else:
            return None

    def get_previous_siblings(self):
        if not self.parent:
            return []
        return [
            sibling
            for sibling in self.parent.children
            if sibling != self and sibling.offset.value < self.offset.value
        ]

    def get_next_sibling(self):
        next_siblings = self.get_next_siblings()
        if next_siblings:
            return next_siblings[0]
        else:
            return None

    def get_next_siblings(self):
        if not self.parent:
            return []
        return [
            sibling
            for sibling in self.parent.children
            if sibling != self and sibling.offset.value > self.offset.value
        ]

def get_root_template(template: Template):
    if template.parent is None:
        return template
    return template.parent.root
