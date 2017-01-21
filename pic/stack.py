
DEFAULT_STACK_SIZE = 8

class PcStack(object):

    def __init__(self, programCounter, size: int=DEFAULT_STACK_SIZE):
        self._programCounter = programCounter
        self._size = size
        self._stack = [0]*size
        self._stackPointer = 0

    @property
    def programCounter(self):
        return self._programCounter

    @property
    def size(self) -> int:
        return self._size

    @property
    def stack(self):
        return self._stack

    @property
    def stackPointer(self) -> int:
        return self._stackPointer

    @stackPointer.setter
    def stackPointer(self, value: int):
        self._stackPointer = value

    @property
    def current(self):
        return self.stack[self.stackPointer]

    @current.setter
    def current(self, value: int):
        self.stack[self.stackPointer] = value

    def incStackPointer(self):
        self._stackPointer = (self.stackPointer + 1) % self.size

    def decStackPointer(self):
        if self.stackPointer == 0:
            self.stackPointer = self.size - 1
        else:
            self.stackPointer = self.stackPointer - 1

    def push(self, address):
        self.current = self.programCounter.address + 1
        self.incStackPointer()
        self.programCounter.address = address

    def pop(self):
        self.decStackPointer()
        self.programCounter.address = self.current
