from .template import Template


class TemplateProviderBase(object):
    @property
    def template(self) -> Template:
        pass

    @template.setter
    def template(self, value: Template):
        pass


class SimpleTemplateProvider(TemplateProviderBase):
    def __init__(self, template):
        self._template = template

    @property
    def template(self) -> Template:
        return self._template

    @template.setter
    def template(self, value: Template):
        self._template = value


class EmptyTemplateProvider(SimpleTemplateProvider):
    def __init__(self, template=None):
        if template is None:
            template = Template()
        super(EmptyTemplateProvider, self).__init__(template)
