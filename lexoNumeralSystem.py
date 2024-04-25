from abc import ABC, abstractmethod

class ILexoNumeralSystem(ABC):

    @abstractmethod
    def get_base(self) -> int:
        pass

    @abstractmethod
    def get_positive_char(self) -> str:
        pass

    @abstractmethod
    def get_negative_char(self) -> str:
        pass

    @abstractmethod
    def get_radix_point_char(self) -> str:
        pass

    @abstractmethod
    def to_digit(self, var1: str) -> int:
        pass

    @abstractmethod
    def to_char(self, var1: int) -> str:
        pass
