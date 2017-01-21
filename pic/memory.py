
class RegisterBank(object):
    def __init__(self,
                 registers: list,
                 size: int):

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

class FileMemory(object):

    def __init__(self, banks: list, fsrReg):
        self._fsrRegister = fsr
        self._banks = banks

    @property
    def fsrRegister(self):
        return self._fsrRegister

    @property
    def banks(self) -> list:
        return self._banks

    def getRegister(self, bankIdx: int, addr: int):
        bank = self.banks[bankIdx]
        return bank.registers[addr % bank.size]
