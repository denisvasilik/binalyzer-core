# -*- coding: utf-8 -*-
"""
    binalyzer_core
    ~~~~~~~~~~~~~~

    The core package of the Binalyzer library.

    :copyright: 2020 Denis Vasilík
    :license: MIT, see LICENSE for details.
"""

name = "binalyzer_core"

__tag__ = ""
__build__ = 0
__version__ = "{}".format(__tag__)
__commit__ = "0000000"

from .binalyzer import (
    Binalyzer,
)
from .extension import (
    BinalyzerExtension,
)
from .template import (
    Template,
)
from .properties import (
    PropertyBase,
    ValueProperty,
    FunctionProperty,
    ReferenceProperty,
    AutoSizeValueProperty,
    AutoSizeReferenceProperty,
    StretchSizeProperty,
    RelativeOffsetValueProperty,
    RelativeOffsetReferenceProperty,
    LEB128UnsignedBindingProperty,
)
from .context import (
    BindingContext,
    BackedBindingContext,
)
from .template_provider import (
    TemplateProviderBase,
    TemplateProvider,
    PlainTemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    DataProvider,
    BufferedIODataProvider,
    ZeroedDataProvider,
)
from .utils import (
    siblings,
    rightsiblings,
    leftsiblings,
)
from .value_provider import (
    ValueProviderBase,
    ValueProvider,
    FunctionValueProvider,
    ReferenceValueProvider,
    LEB128UnsignedBindingValueProvider,
    LEB128SizeBindingValueProvider,
    RelativeOffsetValueProvider,
    RelativeOffsetReferenceValueProvider,
    AutoSizeValueProvider,
    StretchSizeValueProvider,
)
from .converter import (
    IdentityValueConverter,
    IntegerValueConverter,
    LEB128UnsignedValueConverter,
)
from .factory import (
    TemplateFactory,
)