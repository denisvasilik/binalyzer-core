from .template_provider import (
    TemplateProviderBase,
    EmptyTemplateProvider,
)
from .data_provider import (
    DataProviderBase,
    ZeroDataProvider,
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

        #: The data provider to use.
        #: Defaults to :class:`~binalyzer.provider.BufferedIODataProvider`.
        self.data_provider = data_provider

        if self.template_provider is None:
            self.template_provider = EmptyTemplateProvider()

        if self.data_provider is None:
            self.data_provider = ZeroDataProvider(
                self.template_provider.template.size.value
            )

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
        # FIXME: Move propagate to template, it should be called if binding
        #        context changes.
        self.template_provider.template.propagate()

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


class EmptyBindingContext(BindingContext):

    def __init__(self):
        super(EmptyBindingContext, self).__init__(
            EmptyTemplateProvider(), ZeroDataProvider())
