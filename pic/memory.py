
DEFAULT_REGISTER_BANK_SIZE = 0x7F

class RegisterBank(object):
    def __init__(self,
                 registers: list,
                 size: int=DEFAULT_REGISTER_BANK_SIZE):

        self._registers = [None]*size
        self._size = size
        self._nameMap = {} # str -> index

        for i in range(min(len(registers), size)):
            self.registers[i] = registers[i]
            if registers[i].name is not None:
                self._nameMap[registers[i].name] = registers[i]

        for i in range(min(len(registers), size), size):
            self.registers[i] = Register(name=None)

    @property
    def size(self) -> int:
        return self._size

    @property
    def registers(self) -> list:
        return self._registers

    def checkBounds(self, addr: int, exceptoob: bool=False):
        if add < 0 or add >= self.size:
            if not exceptoob:
                return False
            raise ValueError("Register address of 0x{addr:08X} is out of "
                             "bounds! - max address 0x{max:08X}"
                             .format(addr=addr, max=self.size))
        return True

    def getNamedRegister(self, name: str):
        return self._nameMap.get(name, None)

class RunningMemory(object):

    def __init__(self):
        pass
