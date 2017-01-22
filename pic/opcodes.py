
class Literal(object):
    def __init__(self, value: int):
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = int(value)

class OpCode(object):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def execute(self) -> int:
        raise NotImplementedError("Opcode {name} has not been implemented"
                                  .format(name=self.name))

class AddLW(OpCode):
    def __init__(self, literal, workingReg, statusReg):
        super().__init__(name="ADDLW")
        self._literal = literal
        self._statusRegister = statusReg
        self._workingRegister = workingReg

    @property
    def literal(self):
        return self._literal

    @property
    def statusRegister(self):
        return self._statusRegister

    @property
    def workingRegister(self):
        return self._workingRegister

    def __str__(self) -> str:
        return "{name} {value}".format(name=self.name,
                                       value=self.literal.value)

    def execute(self) -> int:
        oldValue = self.workingRegister.value
        newValue = self.literal.value + oldValue

        self.workingRegister.value = newValue

        if (newValue & self.workingRegister.maxValue) == newValue:
            self.statusRegister.clearNamedBit("C")
        else:
            self.statusRegister.setNamedBit("C")

        if newValue == 0:
            self.statusRegister.setNamedBit("Z")
        else:
            self.statusRegister.clearNamedBit("Z")

        if (oldValue & 0xF) + (self.literal.value & 0xF) > 0xF:
            self.statusRegister.setNamedBit("DC")
        else:
            self.statusRegister.clearNamedBit("DC")

        return 1

class AddWF(OpCode):
    def __init__(self, register, storeToFile: bool, workingReg, statusReg):
        super().__init__(name="ADDWF")
        self._register = register
        self._storeToFile = storeToFile
        self._workingRegister = workingReg
        self._statusRegister = statusReg

    @property
    def register(self):
        return self._register

    @property
    def storeToFile(self) -> bool:
        return self._storeToFile

    @property
    def destinationRegister(self):
        return self.register if self.storeToFile else self.workingRegister

    @property
    def statusRegister(self):
        return self._statusRegister

    @property
    def workingRegister(self):
        return self._workingRegister

    def __str__(self) -> str:
        return ("{name} {file},"
                "{dest}".format(name=self.name,
                                file=self.register.name,
                                dest="F" if self.storeToFile else "W"))

    def execute(self) -> int:
        oldValue = self.destinationRegister.value
        newValue = self.register.value + self.workingRegister.value

        self.destinationRegister.value = newValue

        if (newValue & self.destinationRegister.maxValue) == newValue:
            self.statusRegister.clearNamedBit("C")
        else:
            self.statusRegister.setNamedBit("C")

        if newValue == 0:
            self.statusRegister.setNamedBit("Z")
        else:
            self.statusRegister.clearNamedBit("Z")

        smallValue = (self.register.value & 0xF)
        smallValue += (self.workingRegister.value & 0xF)

        if smallValue > 0xF:
            self.statusRegister.setNamedBit("DC")
        else:
            self.statusRegister.clearNamedBit("DC")

        return 1

class AndLW(OpCode):
    def __init__(self, literal, workingReg, statusReg):
        super().__init__(name="ANDLW")
        self._literal = literal
        self._statusRegister = statusReg
        self._workingRegister = workingReg

    @property
    def literal(self):
        return self._literal

    @property
    def statusRegister(self):
        return self._statusRegister

    @property
    def workingRegister(self):
        return self._workingRegister

    def __str__(self) -> str:
        return "{name} {value}".format(name=self.name,
                                       value=self.literal.value)

    def execute(self) -> int:
        oldValue = self.workingRegister.value
        newValue = self.literal.value & oldValue

        self.workingRegister.value = newValue

        if newValue == 0:
            self.statusRegister.setNamedBit("Z")
        else:
            self.statusRegister.clearNamedBit("Z")

        return 1

class AndWF(OpCode):
    def __init__(self, register, storeToFile: bool, workingReg, statusReg):
        super().__init__(name="ANDWF")
        self._register = register
        self._storeToFile = storeToFile
        self._workingRegister = workingReg
        self._statusRegister = statusReg

    @property
    def register(self):
        return self._register

    @property
    def storeToFile(self) -> bool:
        return self._storeToFile

    @property
    def destinationRegister(self):
        return self.register if self.storeToFile else self.workingRegister

    @property
    def statusRegister(self):
        return self._statusRegister

    @property
    def workingRegister(self):
        return self._workingRegister

    def __str__(self) -> str:
        return ("{name} {file},"
                "{dest}".format(name=self.name,
                                file=self.register.name,
                                dest="F" if self.storeToFile else "W"))

    def execute(self) -> int:
        newValue = self.register.value & self.workingRegister.value

        self.destinationRegister.value = newValue

        if newValue == 0:
            self.statusRegister.setNamedBit("Z")
        else:
            self.statusRegister.clearNamedBit("Z")

        return 1

class Bcf(OpCode):
    def __init__(self, register, position):
        super().__init__(name="BCF")
        self._register = register
        self._position = position

    @property
    def register(self):
        return self._register

    @property
    def position(self):
        return self._position

    def isNamedBit(self) -> bool:
        return isinstance(self.position, str)

    def __str__(self) -> str:
        return "{name} {file},{pos}".format(name=self.name,
                                            file=self.register.name,
                                            pos=self.position)

    def execute(self) -> int:
        if self.isNamedBit():
            self.register.clearNamedBit(self.position)
        else:
            self.register.clearBit(self.position)

        return 1

class Bsf(OpCode):
    def __init__(self, register, position):
        super().__init__(name="BSF")
        self._register = register
        self._position = position

    @property
    def register(self):
        return self._register

    @property
    def position(self):
        return self._position

    def isNamedBit(self) -> bool:
        return isinstance(self.position, str)

    def __str__(self) -> str:
        return "{name} {file},{pos}".format(name=self.name,
                                            file=self.register.name,
                                            pos=self.position)

    def execute(self) -> int:
        if self.isNamedBit():
            self.register.setNamedBit(self.position)
        else:
            self.register.setBit(self.position)

        return 1

#
