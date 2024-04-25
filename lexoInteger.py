
from typing import List
from lexoNumeralSystem import ILexoNumeralSystem

class LexoInteger:
    def __init__(self, system: 'ILexoNumeralSystem', sign: int, mag: List[int]):
        self.sys = system
        self.sign = sign
        self.mag = mag

    @staticmethod
    def parse(str_full: str, system: 'ILexoNumeralSystem') -> 'LexoInteger':
        str_ = str_full
        sign = 1
        if str_full.startswith(system.get_positive_char()):
            str_ = str_full[1:]
        elif str_full.startswith(system.get_negative_char()):
            str_ = str_full[1:]
            sign = -1

        mag = [0] * len(str_)
        str_index = len(mag) - 1

        for mag_index in range(len(mag)):
            mag[mag_index] = system.to_digit(str_[str_index])
            str_index -= 1

        return LexoInteger.make(system, sign, mag)

    @staticmethod
    def zero(sys: 'ILexoNumeralSystem') -> 'LexoInteger':
        return LexoInteger(sys, 0, [0])

    @staticmethod
    def one(sys: 'ILexoNumeralSystem') -> 'LexoInteger':
        return LexoInteger.make(sys, 1, [1])

    @staticmethod
    def make(sys: 'ILexoNumeralSystem', sign: int, mag: List[int]) -> 'LexoInteger':
        actual_length = len(mag)
        while actual_length > 0 and mag[actual_length - 1] == 0:
            actual_length -= 1

        if actual_length == 0:
            return LexoInteger.zero(sys)

        if actual_length == len(mag):
            return LexoInteger(sys, sign, mag)

        nmag = [0] * actual_length
        for i in range(actual_length):
            nmag[i] = mag[i]
        return LexoInteger(sys, sign, nmag)

    @staticmethod
    def add_3(sys: 'ILexoNumeralSystem', l: List[int], r: List[int]) -> List[int]:
        estimated_size = max(len(l), len(r))
        result = [0] * estimated_size
        carry = 0
        for i in range(estimated_size):
            lnum = l[i] if i < len(l) else 0
            rnum = r[i] if i < len(r) else 0
            sum_ = lnum + rnum + carry
            carry = 0
            while sum_ >= sys.get_base():
                sum_ -= sys.get_base()
                carry += 1

            result[i] = sum_

        if carry > 0:
            result.append(carry)

        return result

    @staticmethod
    def subtract_3(sys: 'ILexoNumeralSystem', l: List[int], r: List[int]) -> List[int]:
        r_complement = LexoInteger.complement_3(sys, r, len(l))
        r_sum = LexoInteger.add_3(sys, l, r_complement)
        r_sum[-1] = 0
        return LexoInteger.add_3(sys, r_sum, [1])

    @staticmethod
    def multiply(sys: 'ILexoNumeralSystem', l: List[int], r: List[int]) -> List[int]:
        result = [0] * (len(l) + len(r))
        for li in range(len(l)):
            for ri in range(len(r)):
                result_index = li + ri
                result[result_index] += l[li] * r[ri]
                while result[result_index] >= sys.get_base():
                    result[result_index + 1] += 1
                    result[result_index] -= sys.get_base()

        return result

    @staticmethod
    def complement_3(sys: 'ILexoNumeralSystem', mag: List[int], digits: int) -> List[int]:
        if digits <= 0:
            raise ValueError('Expected at least 1 digit')

        nmag = [sys.get_base() - 1] * digits
        for i in range(len(mag)):
            nmag[i] = sys.get_base() - 1 - mag[i]

        return nmag

    @staticmethod
    def compare(l: List[int], r: List[int]) -> int:
        if len(l) < len(r):
            return -1
        if len(l) > len(r):
            return 1

        for i in range(len(l) - 1, -1, -1):
            if l[i] < r[i]:
                return -1
            if l[i] > r[i]:
                return 1

        return 0

    def add(self, other: 'LexoInteger') -> 'LexoInteger':
        self.check_system(other)
        if self.is_zero():
            return other
        if other.is_zero():
            return self

        if self.sign != other.sign:
            pos = self.negate() if self.sign == -1 else other.negate()
            val = pos.subtract(other if self.sign == -1 else self)
            return val.negate()

        result = LexoInteger.add_3(self.sys, self.mag, other.mag)
        return LexoInteger.make(self.sys, self.sign, result)

    def subtract(self, other: 'LexoInteger') -> 'LexoInteger':
        self.check_system(other)
        if self.is_zero():
            return other.negate()
        if other.is_zero():
            return self

        if self.sign != other.sign:
            negate = self.negate() if self.sign == -1 else other.negate()
            return self.add(negate)

        cmp = LexoInteger.compare(self.mag, other.mag)
        if cmp == 0:
            return LexoInteger.zero(self.sys)

        sign = -1 if cmp < 0 else 1
        mag = LexoInteger.subtract_3(self.sys, other.mag, self.mag) if cmp < 0 else LexoInteger.subtract_3(self.sys, self.mag, other.mag)
        return LexoInteger.make(self.sys, sign, mag)

    def multiply(self, other: 'LexoInteger') -> 'LexoInteger':
        self.check_system(other)
        if self.is_zero() or other.is_zero():
            return LexoInteger.zero(self.sys)

        if self.is_oneish():
            return LexoInteger.make(self.sys, self.sign * other.sign, other.mag)
        if other.is_oneish():
            return LexoInteger.make(self.sys, self.sign * other.sign, self.mag)

        new_mag = LexoInteger.multiply(self.sys, self.mag, other.mag)
        return LexoInteger.make(self.sys, self.sign * other.sign, new_mag)

    def negate(self) -> 'LexoInteger':
        return self if self.is_zero() else LexoInteger.make(self.sys, -self.sign, self.mag)

    def shift_left(self, times: int = 1) -> 'LexoInteger':
        if times == 0:
            return self
        if times < 0:
            return self.shift_right(-times)

        nmag = [0] * (len(self.mag) + times)
        for i in range(len(self.mag)):
            nmag[i + times] = self.mag[i]
        return LexoInteger.make(self.sys, self.sign, nmag)

    def shift_right(self, times: int = 1) -> 'LexoInteger':
        if len(self.mag) - times <= 0:
            return LexoInteger.zero(self.sys)

        nmag = self.mag[times:]
        return LexoInteger.make(self.sys, self.sign, nmag)

    def complement(self) -> 'LexoInteger':
        return self.complement_digits(len(self.mag))

    def complement_digits(self, digits: int) -> 'LexoInteger':
        return LexoInteger.make(self.sys, self.sign, LexoInteger.complement(self.sys, self.mag, digits))

    def is_zero(self) -> bool:
        return self.sign == 0 and len(self.mag) == 1 and self.mag[0] == 0

    def is_one(self) -> bool:
        return self.sign == 1 and len(self.mag) == 1 and self.mag[0] == 1

    def get_mag(self, index: int) -> int:
        return self.mag[index]

    def compare_to(self, other: 'LexoInteger') -> int:
        if self is other:
            return 0
        if other is None:
            return 1

        if self.sign == -1:
            if other.sign == -1:
                cmp = LexoInteger.compare(self.mag, other.mag)
                return 1 if cmp == -1 else -1 if cmp == 1 else 0
            return -1

        if self.sign == 1:
            return LexoInteger.compare(self.mag, other.mag) if other.sign == 1 else 1

        if other.sign == -1:
            return 1
        return -1 if other.sign == 1 else 0

    def get_system(self) -> 'ILexoNumeralSystem':
        return self.sys

    def format(self) -> str:
        if self.is_zero():
            return str(self.sys.to_char(0))

        sb = []
        for digit in self.mag:
            sb.insert(0, self.sys.to_char(digit))

        if self.sign == -1:
            sb.insert(0, self.sys.get_negative_char())

        return ''.join(sb)

    def equals(self, other: 'LexoInteger') -> bool:
        if self is other:
            return True
        if other is None:
            return False

        return self.sys.get_base() == other.sys.get_base() and self.compare_to(other) == 0

    def __str__(self) -> str:
        return self.format()

    def is_oneish(self) -> bool:
        return len(self.mag) == 1 and self.mag[0] == 1

    def check_system(self, other: 'LexoInteger'):
        if self.sys.get_base() != other.sys.get_base():
            raise ValueError('Expected numbers of same numeral sys')

#This Python code translates the provided TypeScript code for the `LexoInteger` class. It uses native Python data structures and functions for similar data structures in the input code. The class provides methods for parsing, creating, adding, subtracting, multiplying, negating, shifting, complementing, and comparing `LexoInteger` objects. It also includes helper methods for performing arithmetic operations on the underlying magnitude arrays.

#Note that the `ILexoNumeralSystem` interface and the `lexoHelper` module are not provided in the input code, so they are represented as string types in the Python code. You may need to replace them with appropriate implementations or import statements.

