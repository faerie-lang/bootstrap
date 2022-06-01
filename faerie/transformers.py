from typing import Any
from lark import Transformer
from enum import Enum


class Operator(Enum):
    pass


class Operation:
    _lhs: Any
    _rhs: Any
    _op: Operator


class Identifier:
    __name: str
    __value: Any | None

    def __init__(self, name, value=None):
        self.__name = name
        self.__value = value

    def __repr__(self):
        return f'{self.__name} -> {"Undefined" if self.__value is None else self.__value}'
