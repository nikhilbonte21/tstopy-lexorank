from lexoInteger import LexoInteger

class LexoDecimal:
    def __init__(self, mag, sig):
        self.mag = mag
        self.sig = sig

    @staticmethod
    def half(sys):
        mid = sys.get_base() // 2
        return LexoDecimal.make(LexoInteger.make(sys, 1, [mid]), 1)

    @staticmethod
    def parse(string, system):
        partial_index = string.find(system.get_radix_point_char())
        if string.rfind(system.get_radix_point_char()) != partial_index:
            raise ValueError(f"More than one {system.get_radix_point_char()}")

        if partial_index < 0:
            return LexoDecimal.make(LexoInteger.parse(string, system), 0)

        int_str = string[:partial_index] + string[partial_index + 1:]
        return LexoDecimal.make(LexoInteger.parse(int_str, system), len(string) - 1 - partial_index)

    @staticmethod
    def from_integer(integer):
        return LexoDecimal.make(integer, 0)

    @staticmethod
    def make(integer, sig):
        if integer.is_zero():
            return LexoDecimal(integer, 0)

        zero_count = 0
        for i in range(sig):
            if integer.get_mag(i) == 0:
                zero_count += 1
            else:
                break

        new_integer = integer.shift_right(zero_count)
        new_sig = sig - zero_count
        return LexoDecimal(new_integer, new_sig)

    def get_system(self):
        return self.mag.get_system()

    def add(self, other):
        tmag = self.mag
        tsig = self.sig
        omag = other.mag
        osig = other.sig

        while tsig < osig:
            tmag = tmag.shift_left()
            tsig += 1

        while tsig > osig:
            omag = omag.shift_left()
            osig += 1

        return LexoDecimal.make(tmag.add(omag), tsig)

    def subtract(self, other):
        this_mag = self.mag
        this_sig = self.sig
        other_mag = other.mag
        other_sig = other.sig

        while this_sig < other_sig:
            this_mag = this_mag.shift_left()
            this_sig += 1

        while this_sig > other_sig:
            other_mag = other_mag.shift_left()
            other_sig += 1

        return LexoDecimal.make(this_mag.subtract(other_mag), this_sig)

    def multiply(self, other):
        return LexoDecimal.make(self.mag.multiply(other.mag), self.sig + other.sig)

    def floor(self):
        return self.mag.shift_right(self.sig)

    def ceil(self):
        if self.is_exact():
            return self.mag

        floor = self.floor()
        return floor.add(LexoInteger.one(floor.get_system()))

    def is_exact(self):
        if self.sig == 0:
            return True

        for i in range(self.sig):
            if self.mag.get_mag(i) != 0:
                return False

        return True

    def get_scale(self):
        return self.sig

    def set_scale(self, nsig, ceiling=False):
        if nsig >= self.sig:
            return self

        if nsig < 0:
            nsig = 0

        diff = self.sig - nsig
        nmag = self.mag.shift_right(diff)
        if ceiling:
            nmag = nmag.add(LexoInteger.one(nmag.get_system()))

        return LexoDecimal.make(nmag, nsig)

    def compare_to(self, other):
        if self == other:
            return 0

        if not other:
            return 1

        t_mag = self.mag
        o_mag = other.mag
        if self.sig > other.sig:
            o_mag = o_mag.shift_left(self.sig - other.sig)
        elif self.sig < other.sig:
            t_mag = t_mag.shift_left(other.sig - self.sig)

        return t_mag.compare_to(o_mag)

    def format(self):
        int_str = self.mag.format()
        if self.sig == 0:
            return int_str

        sb = list(int_str)
        head = sb[0]
        special_head = head == self.mag.get_system().get_positive_char() or head == self.mag.get_system().get_negative_char()

        if special_head:
            sb.pop(0)

        while len(sb) < self.sig + 1:
            sb.insert(0, self.mag.get_system().to_char(0))

        sb.insert(len(sb) - self.sig, self.mag.get_system().get_radix_point_char())

        if len(sb) - self.sig == 0:
            sb.insert(0, self.mag.get_system().to_char(0))

        if special_head:
            sb.insert(0, head)

        return ''.join(sb)

    def equals(self, other):
        if self == other:
            return True

        if not other:
            return False

        return self.mag.equals(other.mag) and self.sig == other.sig

    def __str__(self):
        return self.format()


