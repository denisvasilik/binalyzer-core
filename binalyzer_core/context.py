from .template_provider import (
    TemplateProviderBase,
    TemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    ZeroedDataProvider,
)


class BindingContext(object):
    """The :class:`BindingContext` is a data container that holds contextual
    information about the binding between a template and binary data. It is
    mainly an interface that is used to decouple the :class:`~binalyzer.template.Template`
    from the :class:`Binalyzer` and :class:`~binalyzer.provider.DataProvider`.

    :param template: the template to provide by the context
    :param stream: the stream to provide by the context
    """

    def __init__(
        self, template_provider: TemplateProviderBase, data_provider: DataProviderBase
    ):
        #: The template to provide by the context. It usually is the *top-most*
        #: or *root* template.
        self.template_provider = template_provider
        self.template_provider.template.binding_context = self

        #: The data provider to use.
        #: Defaults to :class:`~binalyzer.provider.BufferedIODataProvider`.
        self.data_provider = data_provider

    @property
    def template(self):
        """A :class:`~binalyzer.template.Template` that is bound to the
        corresponding :attr:`~binalyzer.binalyzer.Binalyzer.stream`. In
        case a new template is assigned it gets rebound to the buffered IO
        stream.
        """
        return self.template_provider.template

    @template.setter
    def template(self, value):
        self.template_provider.template = value
        self.template_provider.template.binding_context = self

    @property
    def data(self):
        """A buffered IO stream that is bound to the corresponding
        :attr:`~binalyzer.binalyzer.Binalyzer.template`.
        In case a new stream is assigned it gets rebound to the template.
        """
        return self.data_provider.data

    @data.setter
    def data(self, value):
        self.data_provider.data = value


class BackedBindingContext(BindingContext):

    def __init__(self, template):
        super(BackedBindingContext, self).__init__(
            TemplateProvider(template), ZeroedDataProvider())
