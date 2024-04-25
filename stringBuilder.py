class StringBuilder:
    def __init__(self, str=''):
        self._str = str

    @property
    def length(self):
        return len(self._str)

    @length.setter
    def length(self, value):
        self._str = self._str[:value]

    def append(self, str):
        self._str += str
        return self

    def remove(self, start_index, length):
        self._str = self._str[:start_index] + self._str[start_index + length:]
        return self

    def insert(self, index, value):
        self._str = self._str[:index] + value + self._str[index:]
        return self

    def toString(self):
        return self._str


