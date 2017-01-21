
class Register(object):
    def __init__(self, name: str, size: int=1, special: bool=False):
        self._value = 0
        self._name = name
        self._size = size
        self._special = special

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def value(self) -> int:
        return self._value

    @property
    def special(self) -> bool:
        return self._special

    @value.setter
    def value(self, value: int):
        if value >= self.minValue and value <= self.maxValue:
            self._value = value
        else:
            raise ValueError("Register {name} cannot have a value of "
                             "0x{value:08X} - largest value is {max:08X}"
                             .format(name=self.name,
                                     value=value,
                                     max=self.maxValue))

    @property
    def maxValue(self) -> int:
        return 2**(self.size*8) - 1

    @property
    def minValue(self) -> int:
        return 0

    def clear(self):
        self._value = 0

    def setBit(self, pos: int):
        if pos >= 0 and pos < self.size * 8:
            self.value = (self.value | 2**pos)
        else:
            raise ValueError("Register {name} does not have a bit index of "
                             "{value} - largest bit index is {max}"
                             .format(name=self.name,
                                     value=pos,
                                     max=self.size * 8 - 1))

    def clearBit(self, pos: int):
        if pos >= 0 and pos < self.size * 8:
            self.value = (self.value & (self.maxValue - 2**pos))
        else:
            raise ValueError("Register {name} does not have a bit index of "
                             "{value} - largest bit index is {max}"
                             .format(name=self.name,
                                     value=pos,
                                     max=self.size * 8 - 1))

    def getBit(self, pos: int) -> int:
        if pos >= pos and pos < self.size * 8:
            self.value = 0 if (self.value & (self.maxValue - 2**)) == 0 else 1

    def setBits(self, poses: [int]) -> int:
        for pos in poses:
            self.setBit(pos)

    def clearBits(self, poses: [int]):
        for pos in poses:
            self.clearBit(pos)

    def getBits(self, poses: [int]) -> int:
        minPos = min(poses)

        for pos in poses:
            if pos < 0 or pos >= self.size * 8:
                raise ValueError("Register {name} does not have a bit index of "
                                 "{value} - largest bit index is {max}"
                                 .format(name=self.name,
                                         value=pos,
                                         max=self.size * 8 - 1))

        return sum([(2**pos | self.value) for pos in (set(poses))]) >> minPOs

class UnimplementedRegister(Register):
    def __init__(self, size: int=1):
        super().__init__("unimplemented", size=size, special=True)
        zero = lambda _, *args: 0
        none = lambda _, *args: None
        self.clear = none
        self.setBit = none
        self.clearBits = none
        self.getBit = zero
        self.setBits = none
        self.clearBits = none
        self.getBits = zero

    @property
    def value(self) -> int:
        return 0

    # The following functions are intensionally set as pass.

    @value.setter
    def value(self, _):
        pass
