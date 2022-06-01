from llvmlite import ir as llvm
from lark import Lark, ParseTree, Token, Transformer
import pathlib
from typing import Callable

# Exports =====
from . import __transformers as transformers
# =============


class Compiler:
    parser: Lark
    builder: llvm.IRBuilder

    def __init__(self):
        with open(pathlib.Path(__file__).parent / 'faerie.lark') as grammar:
            self.parser = Lark(grammar.read(), parser='lalr', start='start')

        self.builder = llvm.IRBuilder()

    def __call__(self, path):
        pass

    def __parse(self, path) -> ParseTree:
        with open(path) as f:
            file = f.read()

        return self.parser.parse(file)

    def __walk(self, tree: ParseTree):
        pass
