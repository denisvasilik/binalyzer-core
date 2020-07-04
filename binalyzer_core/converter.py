
class IdentityValueConverter(object):

    def convert(self, value, template):
        return value

    def convert_back(self, value, template):
        return value


class IntegerValueConverter(object):

    def convert(self, value, template):
        return int.from_bytes(value, template.byte_order)

    def convert_back(self, value, template):
        return value.to_bytes(template.size, template.byte_order)
