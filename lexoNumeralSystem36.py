class LexoNumeralSystem36:
    def __init__(self):
        self.DIGITS = list('0123456789abcdefghijklmnopqrstuvwxyz')

    def get_base(self):
        return 36

    def get_positive_char(self):
        return '+'

    def get_negative_char(self):
        return '-'

    def get_radix_point_char(self):
        return ':'

    def to_digit(self, ch):
        if '0' <= ch <= '9':
            return ord(ch) - 48

        if 'a' <= ch <= 'z':
            return ord(ch) - 97 + 10

        raise ValueError(f'Not valid digit: {ch}')

    def to_char(self, digit):
        return self.DIGITS[digit]


