class TemplateProviderBase(object):
    @property
    def template(self):
        pass

    @template.setter
    def template(self, value):
        pass


class TemplateProvider(TemplateProviderBase):
    def __init__(self, template):
        self._template = template

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value


class EmptyTemplateProvider(TemplateProvider):
    def __init__(self, template=None):
        from .template import Template

        if template is None:
            template = Template()
        super(EmptyTemplateProvider, self).__init__(template)
