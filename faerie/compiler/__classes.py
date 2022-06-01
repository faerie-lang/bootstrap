from typing import Any
from llvmlite import ir
from lark import Token
from abc import ABC, abstractmethod


def string_type(chars: int): return ir.VectorType(ir.IntType(8), chars)
def integer_type(bits: int): return ir.IntType(bits)
def decimal_type(_): return ir.DoubleType()
def raw_type(_): return integer_type(4)
def boolean_type(_): return integer_type(1)


class FaerieStructure(ABC):
    @abstractmethod
    def llvm(self) -> ir.Value:
        pass


class Literal(FaerieStructure):
    __type: ir.Type
    __value: Any

    def __init__(self, type: ir.Type, value: Any):
        self.__type = type,
        self.__value = value

    def __repr__(self):
        return f'Literal({self.__value})'

    def llvm(self) -> ir.Value:
        return ir.Constant(self.__type, self.__value)


class Identifier(FaerieStructure):
    __name: Token
    __type: ir.Type | None
    __value: Any

    def __init__(self, name: Token, type: ir.Type | None = None, value: Any = None):
        self.__name = name
        self.__type = type
        self.__value = value

    @property
    def name(self):
        return self.__name.value

    def __repr__(self):
        return f'Identifier({self.__name.value})'


class Operation(FaerieStructure):
    __lhs: Any
    __rhs: Any
    __op: str

    def __init__(self, operator: str, lhs: Any = None, rhs: Any = None):
        self.__op = operator
        self.__lhs = lhs
        self.__rhs = rhs

    def is_unary(self):
        return self.__lhs is None and self.__rhs is not None and self.__op in ['~', '!', 'not']

    def __repr__(self):
        return f'Operation({self.__op}, {self.__lhs}, {self.__rhs})'


class Assignment(FaerieStructure):
    __kind: ir.Type
    __lhs: Identifier
    __rhs: Any

    def __init__(self, kind: ir.Type, lhs: Identifier, rhs: Any):
        self.__kind = kind
        self.__lhs = lhs
        self.__rhs = rhs

    def __repr__(self):
        return f'Assignment<{self.__kind}>({self.__lhs}, {self.__rhs})'


class FunctionCallArguments(FaerieStructure):
    __args: dict[str, Any]

    def __init__(self, **kwargs):
        self.__args = kwargs

    def __repr__(self):
        return f'({", ".join([f"{key}: {value}" for key, value in self.__args.items()])})'


class FunctionCall(FaerieStructure):
    __identifier: Identifier
    __args: FunctionCallArguments

    def __init__(self, identifier: Identifier, args: FunctionCallArguments):
        self.__identifier = identifier
        self.__args = args

    def __repr__(self):
        return f'FunctionCall({self.__identifier.name}, {self.__args})'


class FunctionDefinitionArgument(FaerieStructure):
    __type: ir.Type
    __identifier: Identifier
    __default: Any

    def __init__(self, type: ir.Type, identifier: Identifier, default: Any = None):
        self.__type = type
        self.__identifier = identifier
        self.__default = default

    def __repr__(self):
        return f'{self.__type} {self.__identifier.name}{"".join([" = ", repr(self.__default)]) if self.__default is not None else ""}'


class FunctionDefinition(FaerieStructure):
    __args: list[FunctionDefinitionArgument]
    __return: ir.Type
    __body: Any

    def __init__(self, _args: list[FunctionDefinitionArgument], _return: ir.Type, _body: Any):
        self.__args = _args
        self.__return = _return
        self.__body = _body

    def __repr__(self):
        return f'Function({self.__args}) -> {self.__return} {self.__body}'


class IfThenStatement(FaerieStructure):
    __pred: Any
    __then: Any
    __else: Any | None

    def __init__(self, pred, _then: Any, _else: Any = None):
        self.__pred = pred
        self.__then = _then
        self.__else = _else

    def __repr__(self):
        return f'{{IF({self.__pred}) ==> THEN({self.__then}) ==> ELSE({self.__else})}}'
