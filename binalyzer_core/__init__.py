# -*- coding: utf-8 -*-
"""
    binalyzer_core
    ~~~~~~~~~~~~~~

    A library supporting the analysis of binary data.

    :copyright: 2020 Denis Vasilík
    :license: MIT, see LICENSE for details.
"""

name = "binalyzer_core"

__tag__ = ""
__build__ = 0
__version__ = "{}".format(__tag__)
__commit__ = "00000000"

from .binalyzer import (
    Binalyzer
)
from .template import (
    Offset,
    Size,
    Boundary,
    ByteOrder,
    AddressingMode,
    ResolvableValue,
    Template,
    Sizing,
    PaddingAfter,
    PaddingBefore,
)
from .context import (
    BindingContext,
)
from .template_provider import (
    TemplateProviderBase,
    SimpleTemplateProvider,
    EmptyTemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    SimpleDataProvider,
    ZeroDataProvider,
)