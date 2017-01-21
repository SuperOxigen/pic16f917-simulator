

class ProgramCounter(object):
    def __init__(self, width: int, pclath, pclathBits: [int]):
        self._size = 2**width
        self._pclath = pclath
        self._pclathBits = pclathBits

        if len(pclathBits) > 0:
            self._internalMax = 2**min(pclathBits)
        else:
            self._internalMax = self.size
        self._internal = 0

    @property
    def size(self) -> int:
        return self._size

    @property
    def pclath(self):
        return self._pclath

    @property
    def pclathBits(self) -> [int]:
        return self._pclathBits

    @property
    def internal(self) -> int:
        return self._internal

    @property
    def internalMax(self) -> int:
        return self._internalMax

    @property
    def external(self) -> int:
        return self.pclath.getBits(self.pclathBits) * self.internalMax

    @property
    def current(self):
        return (self.internal + self.external) % self.size

    @current.setter
    def current(self, value: int):
        self._internal = value % self.internalMax

    def inc(self):
        self._internal = (self.internal + 1) % self.internalMax

    def dec(self):
        if self.internal == 0:
            self._internal = self.internalMax - 1
        else:
            self._internal = self.internal - 1
