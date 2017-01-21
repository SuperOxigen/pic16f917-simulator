
class ProgramMemory(object):

    def __init__(self, size: int, programCounter):
        self._operations = [None] * size
        self._programCounter = programCounter

    @property
    def operations(self) -> list:
        return self._operations

    @property
    def programCounter(self):
        return self._programCounter

    def nextOp(self):
        return self.operations[self.programCounter.value]
