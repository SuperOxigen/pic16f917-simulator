
class Register(object):
    def __init__(self,
                 bits: list,
                 bitNames: list=None,
                 defaultValue: int=0,
                 writable: bool=True,
                 name: str=None):

        self._bits = bits[:]

        self._bitNameMap = {}

        if bitNames is not None:
            for index, name in enumerate(bitNames):
                if name is not None:
                    self.bitNameMap[name] = self.bits[index]

        self._writable = writable
        self._name = name
        self._default = defaultValue & self.maxValue
        self.value = self.default

    @property
    def name(self) -> str:
        return self._name

    @property
    def bits(self) -> list:
        return self._bits

    @property
    def width(self) -> list:
        return len(self.bits)

    @property
    def bitNameMap(self) -> dict:
        return self._bitNameMap

    @property
    def default(self) -> int:
        return self._default

    @property
    def value(self) -> int:
        value = 0

        for i in range(len(self.bits)):
            value += self.bits[i].byteValue(i)

        return value

    @value.setter
    def value(self, value: int):
        if value < self.minValue:
            raise ValueError("Register {name} cannot have a value of "
                             "0x{value:08X} - largest value is {max:08X}"
                             .format(name=self.name,
                                     value=value,
                                     max=self.maxValue))
        if value > self.maxValue:
            value = value & self.maxValue

        for i in range(len(self.bits)):
            self.bits[i].value = 0 if (value & 2**i) == 0 else 1

    @property
    def maxValue(self) -> int:
        return 2**self.width - 1

    @property
    def minValue(self) -> int:
        return 0

    def isWritable(self) -> bool:
        return self._writable

    def set(self, value: int):
        if self.isWritable():
            self.value = value

    def clear(self):
        if self.isWritable():
            self._value = 0

    def reset(self):
        self.value = self.default

    def getBitByPos(self, pos: int) -> int:
        if pos < 0 or pos >= self.width:
            raise ValueError("Register {name} does not have a bit index of "
                             "{value} - largest bit index is {max}"
                             .format(name=self.name,
                                     value=pos,
                                     max=self.width - 1))
        return self.bits[pos].value

    def setBitByPos(self, pos: int):
        if pos < 0 or pos >= self.width:
            raise ValueError("Register {name} does not have a bit index of "
                             "{value} - largest bit index is {max}"
                             .format(name=self.name,
                                     value=pos,
                                     max=self.width - 1))
        if self.isWritable():
            self.bits[pos].set()

    def clearBitByPos(self, pos: int):
        if pos < 0 or pos >= self.width:
            raise ValueError("Register {name} does not have a bit index of "
                             "{value} - largest bit index is {max}"
                             .format(name=self.name,
                                     value=pos,
                                     max=self.size * 8 - 1))
        if self.isWritable():
            self.bits[pos].clear()

    def getBitByName(self, name: str) -> int:
        if name not in self.bitNameMap:
            raise ValueError("Register does not have a bit named {name}"
                             .format(name=name))
        return self.bitNameMap[name].value

    def setBitByName(self, name: str):
        if name not in self.bitNameMap:
            raise ValueError("Register does not have a bit named {name}"
                             .format(name=name))
        if self.isWritable():
            self.bitNameMap[name].set()

    def clearBitByName(self, name: str):
        if name not in self.bitNameMap:
            raise ValueError("Register does not have a bit named {name}"
                             .format(name=name))
        if self.isWritable():
            self.bitNameMap[name].clear()
