# -*- coding: utf-8 -*-
"""
    binalyzer.template
    ~~~~~~~~~~~~~~~~~~

    This module implements the concepts of the template mechanism.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
from .utils import classproperty_support, classproperty
from .binalyzer import BindingContext


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


@classproperty_support
class ByteOrder(object):
    """Determines how to interprete the data the :class:`Template` is bound to.
    """

    LITTLE_ENDIAN_VALUE = "LittleEndian"
    BIG_ENDIAN_VALUE = "BigEndian"
    DEFAULT_VALUE = LITTLE_ENDIAN_VALUE
    BYTE_ORDERS = [LITTLE_ENDIAN_VALUE, BIG_ENDIAN_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'LittleEndian' or 'BigEndian'.")

    def _is_valid(self, value):
        return value in self.BYTE_ORDERS

    @classproperty
    def LittleEndian(cls):
        return cls(cls.LITTLE_ENDIAN_VALUE)

    @classproperty
    def BigEndian(cls):
        return cls(cls.BIG_ENDIAN_VALUE)

    def __eq__(self, other):
        return self.value == other.value


@classproperty_support
class Sizing(object):
    """Determines whether the sizing of a :class:`Template` should be ``fix`` or
    dynamically calculated using ``auto`` or ``stretch``.
    """

    AUTO_VALUE = "auto"
    FIX_VALUE = "fix"
    STRETCH_VALUE = "stretch"
    DEFAULT_VALUE = AUTO_VALUE
    SIZING = [AUTO_VALUE, FIX_VALUE, STRETCH_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'auto', 'fix' or 'stretch'.")

    def _is_valid(self, value):
        return value in self.SIZING

    @classproperty
    def Auto(cls):
        return cls(cls.AUTO_VALUE)

    @classproperty
    def Fix(cls):
        return cls(cls.FIX_VALUE)

    @classproperty
    def Stretch(cls):
        return cls(cls.STRETCH_VALUE)

    def __eq__(self, other):
        return self.value == other.value


@classproperty_support
class AddressingMode(object):
    """Determines whether the addressing of the :class:`Template` is ``absolute``
    or ``relative``.
    """

    ABSOLUTE_VALUE = "absolute"
    RELATIVE_VALUE = "relative"
    DEFAULT_VALUE = ABSOLUTE_VALUE
    ADDRESSING_MODES = [ABSOLUTE_VALUE, RELATIVE_VALUE]

    def __init__(self, value=None):
        self._value = self.DEFAULT_VALUE
        if value is None:
            self.value = self.DEFAULT_VALUE
        else:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise RuntimeError("Expected 'relative' or 'absolute'.")

    def _is_valid(self, value):
        return value in self.ADDRESSING_MODES

    @classproperty
    def Absolute(cls):
        return cls(cls.ABSOLUTE_VALUE)

    @classproperty
    def Relative(cls):
        return cls(cls.RELATIVE_VALUE)

    def __eq__(self, other):
        return self.value == other.value


class ResolvableValue(object):
    """The :class:`ResolvableValue` implements the ability to resolve the value
    of a template attribute value from another template's data.
    See :ref:`revolvable_value`.

    .. note:: The size of the template attribute must match the size of the data
              to resolve.
    """

    def __init__(
        self,
        value=None,
        ref_id=None,
        addressing_mode=None,
        byte_order=None,
        template=None,
    ):
        self.template = template
        self._value = value
        self._ref_id = ref_id
        self.addressing_mode = addressing_mode
        if self.addressing_mode is None:
            self.addressing_mode = AddressingMode.Relative
        self.byte_order = byte_order
        if self.byte_order is None:
            self.byte_order = ByteOrder.LittleEndian

    @property
    def ref_id(self):
        return self._ref_id

    @property
    def is_reference(self):
        return self._ref_id is not None

    @property
    def value(self):
        if self._value is not None:
            return self._value
        elif self.is_reference:
            return self._get_reference_value()
        else:
            return 0

    def _get_reference_value(self):
        return self._interprete(self._get_reference_raw())

    def _get_reference_raw(self):
        return self.template.root.find(self.ref_id).value

    def _interprete(self, bytes):
        if self.byte_order == ByteOrder.LittleEndian:
            return int.from_bytes(bytes, byteorder="little")
        else:
            return int.from_bytes(bytes, byteorder="big")


class Offset(ResolvableValue):
    """The :class:`Offset` represents the offset attribute. See :ref:`offset`.
    """

    @property
    def value(self):
        if self._value:
            return self._value
        elif self.is_reference:
            return self._get_reference_value()
        elif self.addressing_mode == AddressingMode.Absolute:
            return 0
        else:
            return self._get_relative_offset()

    @value.setter
    def value(self, value):
        self._value = value

    def _get_relative_offset(self):
        boundary_offset_relative_to_parent = 0
        boundary_offset_relative_to_sibling = 0

        if self.template.boundary and self.template.boundary.value > 0:
            boundary_offset_relative_to_parent = (
                self.template.parent.offset.value % self.template.boundary.value
            )

        sibling_relative_offset = self._get_relative_offset_end_of_previous_sibling()

        if (
            self.template.boundary
            and self.template.boundary.value > 0
            and sibling_relative_offset > 0
            and sibling_relative_offset % self.template.boundary.value
        ):
            boundary_offset_relative_to_sibling = self.template.boundary.value - (
                sibling_relative_offset % self.template.boundary.value
            )

        return (
            self.template.padding_before.value
            + boundary_offset_relative_to_parent
            + sibling_relative_offset
            + boundary_offset_relative_to_sibling
        )

    def _get_relative_offset_end_of_previous_sibling(self):
        # Need at least two children to grab previous sibling
        if self.template.parent and len(self.template.parent.children) >= 2:
            index = 0
            for (count, value) in enumerate(self.template.parent.children):
                if value == self.template:
                    index = count
                    break
            if index == 0:
                return 0
            else:
                previous_sibling = self.template.parent.children[index - 1]
                return (
                    previous_sibling.offset.value
                    + previous_sibling.size.value
                    + previous_sibling.padding_after.value
                )
        else:
            return 0


class Size(ResolvableValue):
    """The :class:`Size` represents the size attribute. See :ref:`size`.
    """

    @property
    def value(self):
        if self._value is not None:
            return self._value
        elif self.is_reference:
            return self._get_reference_value()
        elif self.template.sizing == Sizing.Stretch:
            return self._calculate_stretched_size()
        elif self.template.sizing == Sizing.Auto and self.template.children:
            return self._get_total_size_of_children()
        elif self.template.boundary:
            return self.template.boundary.value
        else:
            return 0

    @value.setter
    def value(self, value):
        self._value = value

    def _calculate_stretched_size(self):
        next_sibling = self.template.get_next_sibling()
        if next_sibling:
            return next_sibling.offset.value - self.template.offset.value
        elif self.template.parent:
            return self.template.parent.size.value - self.template.offset.value
        elif self.template.binding_context.stream:
            stream = self.template.binding_context.stream
            stream.seek(0, 2)
            return stream.tell()
        else:
            return 0

    def _get_total_size_of_children(self):
        return max(
            self._get_total_size_of_child(child) for child in self.template.children
        )

    def _get_total_size_of_child(self, child):
        # NOTE: child.offset already contains the value of padding-before!!!
        value = child.offset.value + child.size.value + child.padding_after.value

        return self.multiple_of_boundary(value, child.parent.boundary)

    def multiple_of_boundary(self, value, boundary_attribute):
        if boundary_attribute.value == 0:
            return value
        boundary_multiplier = int(value / boundary_attribute.value)
        if value % boundary_attribute.value:
            boundary_multiplier += 1
        return boundary_multiplier * boundary_attribute.value


class Boundary(ResolvableValue):
    """The :class:`Boundary` represents the boundary attribute.
    See :ref:`boundary`.
    """

    pass


class PaddingBefore(ResolvableValue):
    """The :class:`PaddingBefore` describes the padding before the template
    element. See :ref:`padding`.
    """

    pass


class PaddingAfter(ResolvableValue):
    """The :class:`PaddingAfter` describes the padding after the template
    element. See :ref:`padding`.
    """

    pass
