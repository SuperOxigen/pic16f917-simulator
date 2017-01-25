
class Bit(object):

    def __init__(self,
                 defaultValue: int=0,
                 writable: bool=True,
                 onSet=None, onClear=None, onReset=None, onChange=None):
        self.default = defaultValue
        self.value = self.default
        self._writable = writable

        # Event callbacks
        self._onSet = onSet
        self._onClear = onClear
        self._onReset = onReset
        self._onChange = onChange

    @property
    def value(self) -> int:
        return 0 if self._value == 0 else 1

    @value.setter
    def value(self, value: int):
        self._value = 0 if value == 0 else 1

    @property
    def default(self) -> int:
        return 0 if self._default == 0 else 1

    def isWritable(self) -> bool:
        return self._writable

    def triggerSet(self):
        if self._onSet is not None:
            self._onSet(self)

    def triggerClear(self):
        if self._clear is not None:
            self._onClear(self)

    def triggerReset(self):
        if self._onReset is not None:
            self._onReset(self)

    def triggerChange(self):
        if self._onChange is not None:
            self._onChange(self)

    def setCallbackOnSet(self, onSet):
        self._onSet = onSet

    def setCallbackOnClear(self, onClear):
        self._onClear = onClear

    def setCallbackOnReset(self, onReset):
        self._onReset = onReset

    def setCallbackOnChange(self, onChange):
        self._onChange = onChange

    def set(self):
        """Set Bit

        If writable, then the bit value will be set to 1, otherwise
        the bit will remain unchanged.

        If an on-set callback is assigned, then the callback will be
        called.  Regardless of whether the value was changed or not.

        If an on-change callback is assigned and the new value is
        different from the previous value, then the callback will be
        called.
        """

        oldValue = self.value
        if self.isWritable():
            self.value = 1

        self.triggerSet()

        if oldValue == 0:
            self.triggerChange()

    def clear(self):
        """Clear Bit

        If writable, then the bit value will be set to 0, otherwise
        the bit will remain unchanged.

        If an on-clear callback is assigned, then the callback will be
        called.  Regardless of whether the value was changed or not.

        If an on-change callback is assigned and the new value is
        different from the previous value, then the callback will be
        called.
        """

        oldValue = self.value
        if self.isWritable():
            self.value = 0

        self.triggerClear()
        if oldValue == 1:
            self.triggerChange()

    def reset(self):
        """Reset Bit

        The value stored in this bit will be set to the default value
        given on instantiation.

        If an on-reset callback is assigned, then the callback will be
        called.
        """

        self.value = self.default
        self.triggerReset()

    def byteValue(self, pos: int) -> int:
        """Byte Value of Bit

        If the bit is set to 1, then the numerical value of a bit at
        position 'pos' in a byte will be returned.  If the bit is set
        to 0, then the value 0 will be returned.

        Bit positions are assumed index from zero.

        Example:
        >>> myBit = Bit(0)
        >>> myBit.value
        0
        >>> myBit.byteValue(7)
        0
        >>> myBit.byteValue(0)
        0
        >>> myBit.value = 1
        >>> myBit.byteValue(7)
        128
        >>> myBit.byteValue(0)
        1
        >>> myBit.byteValue(4)
        16

        Parameters:
            pos: int
                A non-negative position of the bit value in a byte,
                starting at index 0.
        Returns:
            int
                A power of 2 integer which represents the bits value
                in a byte if the bit value is 1.  Else it will return
                0.
        """

        if pos < 0:
            raise ValueError("bit position must be non-negative")

        if self.value == 0:
            return 0
        return 2**pos
