from typing import Optional
from lexoInteger import LexoInteger
from lexoNumeralSystem36 import LexoNumeralSystem36

class LexoRankBucket:
    _NUMERAL_SYSTEM: LexoNumeralSystem36
    _BUCKET_0 = None
    _BUCKET_1 = None
    _BUCKET_2 = None
    _VALUES = None

    @classmethod
    def BUCKET_0(cls):
        if cls._BUCKET_0 is None:
            cls._BUCKET_0 = LexoRankBucket('0')
        return cls._BUCKET_0

    @classmethod
    def BUCKET_1(cls):
        if cls._BUCKET_1 is None:
            cls._BUCKET_1 = LexoRankBucket('1')
        return cls._BUCKET_1

    @classmethod
    def BUCKET_2(cls):
        if cls._BUCKET_2 is None:
            cls._BUCKET_2 = LexoRankBucket('2')
        return cls._BUCKET_2

    @classmethod
    def VALUES(cls):
        if cls._VALUES is None:
            cls._VALUES = [cls.BUCKET_0(), cls.BUCKET_1(), cls.BUCKET_2()]
        return cls._VALUES

    @classmethod
    def max(cls):
        return cls.VALUES()[-1]

    @classmethod
    def from_str(cls, str_val):
        val = LexoInteger.parse(str_val, LexoNumeralSystem36())
        for bucket in cls.VALUES():
            if bucket.value.equals(val):
                return bucket
        raise ValueError(f'Unknown bucket: {str_val}')

    @classmethod
    def resolve(cls, bucket_id):
        for bucket in cls.VALUES():
            if bucket.equals(cls.from_str(str(bucket_id))):
                return bucket
        raise ValueError(f'No bucket found with id {bucket_id}')

    def __init__(self, val):
        self.value = LexoInteger.parse(val, LexoNumeralSystem36())

    def format(self):
        return self.value.format()

    def next(self):
        if self.equals(LexoRankBucket.BUCKET_0()):
            return LexoRankBucket.BUCKET_1()
        if self.equals(LexoRankBucket.BUCKET_1()):
            return LexoRankBucket.BUCKET_2()
        return LexoRankBucket.BUCKET_0() if self.equals(LexoRankBucket.BUCKET_2()) else LexoRankBucket.BUCKET_2()

    def prev(self):
        if self.equals(LexoRankBucket.BUCKET_0()):
            return LexoRankBucket.BUCKET_2()
        if self.equals(LexoRankBucket.BUCKET_1()):
            return LexoRankBucket.BUCKET_0()
        return LexoRankBucket.BUCKET_1() if self.equals(LexoRankBucket.BUCKET_2()) else LexoRankBucket.BUCKET_0()

    def equals(self, other):
        if self is other:
            return True
        if other is None:
            return False
        return self.value.equals(other.value)


