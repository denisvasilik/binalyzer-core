import io


class DataProviderBase(object):
    @property
    def data(self):
        pass

    @data.setter
    def data(self, value):
        pass

    def read(self, template):
        pass

    def write(self, template, value):
        pass


class DataProvider(DataProviderBase):
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def read(self, template):
        absolute_address = template.absolute_address.value
        size = template.size.value
        self.data.seek(absolute_address)
        return self.data.read(size)

    def write(self, template, value):
        self.data.seek(template.absolute_address.value)
        self.data.write(value)


class BufferedIODataProvider(DataProvider):

    def __init__(self, size=0, value=0):
        super(BufferedIODataProvider, self).__init__(
            io.BytesIO(bytes([value] * size)))


class ZeroedDataProvider(BufferedIODataProvider):
    def __init__(self, size=0):
        super(ZeroedDataProvider, self).__init__(size, 0)
