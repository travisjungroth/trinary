from __future__ import annotations

import threading
from functools import wraps
from typing import Callable, Final, Optional, Union, final


@final
class UnknownClass:
    """
    Trinary logic. Unknown represents both True and False and is a singleton.
    https://en.wikipedia.org/wiki/Three-valued_logic

    >>> Unknown & True
    Unknown
    >>> Unknown | True
    True
    >>> Unknown == False
    Unknown
    >>> Unknown == Unknown
    Unknown
    >>> Unknown is False
    False
    >>> Unknown is Unknown
    True
    >>> Unknown <= False
    Unknown
    >>> ~Unknown
    Unknown
    >>> isinstance(True, Trinary)
    True

    Unknown can't be cast with bool since it could be either.
    Choose with strictly or weakly.
    >>> correct = Unknown
    >>> strictly(correct)
    False
    >>> weakly(correct)
    True
    >>> weakly(False)
    False
    """

    __slots__ = ()
    _instance: Optional[UnknownClass] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> UnknownClass:
        if cls._instance is None:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "Unknown"

    @staticmethod
    def _only_bool(
        method: Callable[[UnknownClass, bool], Trinary]
    ) -> Callable[[UnknownClass, Trinary], Trinary]:
        """
        Handle non-bools before passing to the decorated method, a binary operator.
        """

        @wraps(method)
        def inner(self: UnknownClass, other: Trinary) -> Trinary:
            if isinstance(other, bool):
                return method(self, other)
            # Any binary operator with Unknown as both inputs
            # except T or F returns Unknown
            if other is self:
                return self
            return NotImplemented

        return inner

    @_only_bool
    def __and__(self, other: Trinary) -> Trinary:
        return other and self

    __rand__ = __and__

    @_only_bool
    def __or__(self, other: Trinary) -> Trinary:
        return other or self

    __ror__ = __or__

    @_only_bool
    def __eq__(self, other: Trinary) -> Trinary:
        return self

    __xor__ = __rxor__ = __ne__ = __eq__

    def __invert__(self) -> Trinary:
        return self

    @_only_bool
    def __gt__(self, other: Trinary) -> Trinary:
        return False if other is True else self

    @_only_bool
    def __ge__(self, other: Trinary) -> Trinary:
        return True if other is False else self

    __lt__ = __and__
    __le__ = __or__

    def __hash__(self) -> int:
        return hash(UnknownClass)

    def __bool__(self):
        raise TypeError("Unknown can't cast to a bool. Use strongly() or weakly().")


Trinary = Union[bool, UnknownClass]
Unknown: Final[UnknownClass] = UnknownClass()


def strictly(val) -> bool:
    """
    Unknown -> False
    """
    return val is not Unknown and bool(val)


def weakly(val) -> bool:
    """
    Unknown -> True
    """
    return val is Unknown or bool(val)
