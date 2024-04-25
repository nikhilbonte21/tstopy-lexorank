
from typing import Optional
from lexoDecimal import LexoDecimal
from lexoRankBucket import LexoRankBucket
from stringBuilder import StringBuilder
from lexoNumeralSystem36 import LexoNumeralSystem36

class LexoRank:
    _NUMERAL_SYSTEM: Optional[LexoNumeralSystem36] = None
    _ZERO_DECIMAL: Optional[LexoDecimal] = None
    _ONE_DECIMAL: Optional[LexoDecimal] = None
    _EIGHT_DECIMAL: Optional[LexoDecimal] = None
    _MIN_DECIMAL: Optional[LexoDecimal] = None
    _MAX_DECIMAL: Optional[LexoDecimal] = None
    _MID_DECIMAL: Optional[LexoDecimal] = None
    _INITIAL_MIN_DECIMAL: Optional[LexoDecimal] = None
    _INITIAL_MAX_DECIMAL: Optional[LexoDecimal] = None

    @staticmethod
    def NUMERAL_SYSTEM() -> LexoNumeralSystem36:
        if LexoRank._NUMERAL_SYSTEM is None:
            LexoRank._NUMERAL_SYSTEM = LexoNumeralSystem36()
        return LexoRank._NUMERAL_SYSTEM

    @staticmethod
    def ZERO_DECIMAL() -> LexoDecimal:
        if LexoRank._ZERO_DECIMAL is None:
            LexoRank._ZERO_DECIMAL = LexoDecimal.parse('0', LexoRank.NUMERAL_SYSTEM())
        return LexoRank._ZERO_DECIMAL

    @staticmethod
    def ONE_DECIMAL() -> LexoDecimal:
        if LexoRank._ONE_DECIMAL is None:
            LexoRank._ONE_DECIMAL = LexoDecimal.parse('1', LexoRank.NUMERAL_SYSTEM())
        return LexoRank._ONE_DECIMAL

    @staticmethod
    def EIGHT_DECIMAL() -> LexoDecimal:
        if LexoRank._EIGHT_DECIMAL is None:
            LexoRank._EIGHT_DECIMAL = LexoDecimal.parse('8', LexoRank.NUMERAL_SYSTEM())
        return LexoRank._EIGHT_DECIMAL

    @staticmethod
    def MIN_DECIMAL() -> LexoDecimal:
        if LexoRank._MIN_DECIMAL is None:
            LexoRank._MIN_DECIMAL = LexoRank.ZERO_DECIMAL()
        return LexoRank._MIN_DECIMAL

    @staticmethod
    def MAX_DECIMAL() -> LexoDecimal:
        if LexoRank._MAX_DECIMAL is None:
            LexoRank._MAX_DECIMAL = LexoDecimal.parse('1000000', LexoRank.NUMERAL_SYSTEM()).subtract(LexoRank.ONE_DECIMAL())
        return LexoRank._MAX_DECIMAL

    @staticmethod
    def MID_DECIMAL() -> LexoDecimal:
        if LexoRank._MID_DECIMAL is None:
            LexoRank._MID_DECIMAL = LexoRank.between(LexoRank.MIN_DECIMAL(), LexoRank.MAX_DECIMAL())
        return LexoRank._MID_DECIMAL

    @staticmethod
    def INITIAL_MIN_DECIMAL() -> LexoDecimal:
        if LexoRank._INITIAL_MIN_DECIMAL is None:
            LexoRank._INITIAL_MIN_DECIMAL = LexoDecimal.parse('100000', LexoRank.NUMERAL_SYSTEM())
        return LexoRank._INITIAL_MIN_DECIMAL

    @staticmethod
    def INITIAL_MAX_DECIMAL() -> LexoDecimal:
        if LexoRank._INITIAL_MAX_DECIMAL is None:
            base = LexoRank.NUMERAL_SYSTEM().getBase()
            char = LexoRank.NUMERAL_SYSTEM().toChar(base - 2)
            value = f"{char}00000"
            LexoRank._INITIAL_MAX_DECIMAL = LexoDecimal.parse(value, LexoRank.NUMERAL_SYSTEM())
        return LexoRank._INITIAL_MAX_DECIMAL

    @staticmethod
    def min() -> 'LexoRank':
        return LexoRank.from_values(LexoRankBucket.BUCKET_0(), LexoRank.MIN_DECIMAL())

    @staticmethod
    def middle() -> 'LexoRank':
        min_lexo_rank = LexoRank.min()
        return min_lexo_rank.between(LexoRank.max(min_lexo_rank.bucket))

    @staticmethod
    def max(bucket: LexoRankBucket = LexoRankBucket.BUCKET_0) -> 'LexoRank':
        return LexoRank.from_values(bucket, LexoRank.MAX_DECIMAL())

    @staticmethod
    def initial(bucket: LexoRankBucket) -> 'LexoRank':
        if bucket == LexoRankBucket.BUCKET_0:
            return LexoRank.from_values(bucket, LexoRank.INITIAL_MIN_DECIMAL())
        else:
            return LexoRank.from_values(bucket, LexoRank.INITIAL_MAX_DECIMAL())

    @staticmethod
    def between(left: LexoDecimal, right: LexoDecimal) -> LexoDecimal:
        if left.get_system().getBase() != right.get_system().getBase():
            raise ValueError('Expected same system')

        left_val = left
        right_val = right
        new_left: Optional[LexoDecimal] = None
        if left.getScale() < right.getScale():
            new_left = right.setScale(left.getScale(), False)
            if left.compareTo(new_left) >= 0:
                return LexoRank.mid(left, right)
            right_val = new_left

        if left.getScale() > right_val.getScale():
            new_left = left.setScale(right_val.getScale(), True)
            if new_left.compareTo(right_val) >= 0:
                return LexoRank.mid(left, right)
            left_val = new_left

        new_right: Optional[LexoDecimal] = None
        for scale in range(left_val.getScale(), 0, -1):
            scale_1 = scale - 1
            left_1 = left_val.setScale(scale_1, True)
            new_right = right_val.setScale(scale_1, False)
            cmp = left_1.compareTo(new_right)
            if cmp == 0:
                return LexoRank.checkMid(left, right, left_1)
            if left_1.compareTo(new_right) > 0:
                break
            left_val = left_1
            right_val = new_right

        mid = LexoRank.middleInternal(left, right, left_val, right_val)

        new_scale: Optional[int] = None
        for m_scale in range(mid.getScale(), 0, -1):
            new_scale = m_scale - 1
            new_mid = mid.setScale(new_scale)
            if left.compareTo(new_mid) >= 0 or new_mid.compareTo(right) >= 0:
                break
            mid = new_mid

        return mid

    @staticmethod
    def parse(string: str) -> 'LexoRank':
        parts = string.split('|')
        bucket = LexoRankBucket.from_str(parts[0])
        decimal = LexoDecimal.parse(parts[1], LexoRank.NUMERAL_SYSTEM())
        return LexoRank(bucket, decimal)

    @staticmethod
    def from_values(bucket: LexoRankBucket, decimal: LexoDecimal) -> 'LexoRank':
        if decimal.get_system().get_base() != LexoRank.NUMERAL_SYSTEM().get_base():
            raise ValueError('Expected different system')
        return LexoRank(bucket, decimal)

    @staticmethod
    def middleInternal(lbound: LexoDecimal, rbound: LexoDecimal, left: LexoDecimal, right: LexoDecimal) -> LexoDecimal:
        mid = LexoRank.mid(left, right)
        return LexoRank.checkMid(lbound, rbound, mid)

    @staticmethod
    def checkMid(lbound: LexoDecimal, rbound: LexoDecimal, mid: LexoDecimal) -> LexoDecimal:
        if lbound.compareTo(mid) >= 0:
            return LexoRank.mid(lbound, rbound)
        return mid if mid.compareTo(rbound) < 0 else LexoRank.mid(lbound, rbound)

    @staticmethod
    def mid(left: LexoDecimal, right: LexoDecimal) -> LexoDecimal:
        sum_val = left.add(right)
        mid = sum_val.multiply(LexoDecimal.half(left.get_system()))
        scale = max(left.getScale(), right.getScale())
        if mid.getScale() > scale:
            round_down = mid.setScale(scale, False)
            if round_down.compareTo(left) > 0:
                return round_down
            round_up = mid.setScale(scale, True)
            if round_up.compareTo(right) < 0:
                return round_up
        return mid

    @staticmethod
    def formatDecimal(decimal: LexoDecimal) -> str:
        format_val = decimal.format()
        val = StringBuilder(format_val)
        partial_index = format_val.find(LexoRank.NUMERAL_SYSTEM().get_radix_point_char())
        zero = LexoRank.NUMERAL_SYSTEM().to_char(0)
        if partial_index < 0:
            partial_index = len(format_val)
            val.append(LexoRank.NUMERAL_SYSTEM().get_radix_point_char())

        while partial_index < 6:
            val.insert(0, zero)
            partial_index += 1


        #print(list(val.toString())[val.length - 1])

        #while val[val.length() - 1] == zero:
        while list(val.toString())[val.length - 1] == zero:
            val.length = val.length() - 1

        return val.toString()

    def __init__(self, bucket: LexoRankBucket, decimal: LexoDecimal):
        #print(type(LexoRankBucket._BUCKET_0))
        #print(bucket)
        self.value = f"{bucket.format()}|{LexoRank.formatDecimal(decimal)}"
        self.bucket = bucket
        self.decimal = decimal

    def genPrev(self) -> 'LexoRank':
        if self.isMax():
            return LexoRank(self.bucket, LexoRank.INITIAL_MAX_DECIMAL())

        floor_integer = self.decimal.floor()
        floor_decimal = LexoDecimal.from_integer(floor_integer)
        next_decimal = floor_decimal.subtract(LexoRank.EIGHT_DECIMAL())
        if next_decimal.compare_to(LexoRank.MIN_DECIMAL()) <= 0:
            next_decimal = LexoRank.between(LexoRank.MIN_DECIMAL(), self.decimal)

        return LexoRank(self.bucket, next_decimal)

    def genNext(self) -> 'LexoRank':
        if self.isMin():
            return LexoRank(self.bucket, LexoRank.INITIAL_MIN_DECIMAL())

        ceil_integer = self.decimal.ceil()
        ceil_decimal = LexoDecimal.from_integer(ceil_integer)
        next_decimal = ceil_decimal.add(LexoRank.EIGHT_DECIMAL())
        if next_decimal.compare_to(LexoRank.MAX_DECIMAL()) >= 0:
            next_decimal = LexoRank.between(self.decimal, LexoRank.MAX_DECIMAL())

        return LexoRank(self.bucket, next_decimal)

    def between(self, other: 'LexoRank') -> 'LexoRank':
        if not self.bucket.equals(other.bucket):
            raise ValueError('Between works only within the same bucket')

        cmp = self.decimal.compare_to(other.decimal)
        if cmp > 0:
            return LexoRank(self.bucket, LexoRank.between(other.decimal, self.decimal))
        if cmp == 0:
            raise ValueError(
                f"Try to rank between issues with same rank this={self} other={other} this.decimal={self.decimal} other.decimal={other.decimal}"
            )

        return LexoRank(self.bucket, LexoRank.between(self.decimal, other.decimal))

    def getBucket(self) -> LexoRankBucket:
        return self.bucket

    def getDecimal(self) -> LexoDecimal:
        return self.decimal

    def inNextBucket(self) -> 'LexoRank':
        return LexoRank.from_values(self.bucket.next(), self.decimal)

    def inPrevBucket(self) -> 'LexoRank':
        return LexoRank.from_values(self.bucket.prev(), self.decimal)

    def isMin(self) -> bool:
        return self.decimal.equals(LexoRank.MIN_DECIMAL())

    def isMax(self) -> bool:
        return self.decimal.equals(LexoRank.MAX_DECIMAL())

    def format(self) -> str:
        return self.value

    def __eq__(self, other: 'LexoRank') -> bool:
        if self is other:
            return True
        if other is None:
            return False
        return self.value == other.value

    def __str__(self) -> str:
        return self.value

    def compareTo(self, other: 'LexoRank') -> int:
        if self is other:
            return 0
        if other is None:
            return 1
        return self.value.__cmp__(other.value)



def main(): 
    print("hey there") 

    cache = []
    seed = LexoRank.min()
    print(seed)

    for i in range(1, 6):
        seed = seed.genNext()
        print(seed)

    print(LexoRank.parse("0|100008:").between(LexoRank.parse("0|10000g:")))
    
  
  
if __name__=="__main__": 
    main() 