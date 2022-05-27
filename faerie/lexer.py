import enum
from faerie.token import Token
import re


class Lexer:
    text: list[str]
    idx: int
    tok: str

    def __init__(self, input: str, is_file: bool = False):
        if is_file:
            with open(input, 'r') as f:
                self.text = f.read()
        else:
            self.text = input

        # Remove multiline comments
        self.text = re.sub(r"(?s)(#>>).*?(<<#(\n|\Z))",
                           '', self.text, flags=re.DOTALL)

        # Remove single line comments
        self.text = re.sub(r'#.*?\n', '', self.text, flags=re.DOTALL)

        # Split text by whitespace
        self.text = self.text.split()

        regsep = r'([\(\)\[\]\{\}\.\,])'
        self.text = [re.split(regsep, x) if re.search(
            regsep, x) is not None else x for x in self.text]
        self.text = self.__flatten(self.text)
        self.text = [x for x in self.text if x != '']

        self.idx = -1
        self.tok = ''

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.idx < 0:
            self.idx = 0
        try:
            self.tok = self.text[self.idx]
        except IndexError:
            raise StopIteration()
        self.idx += 1

        return Token(self.tok)

    def __flatten(self, items):
        from typing import Iterable
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                for sub_x in self.__flatten(x):
                    yield sub_x
            else:
                yield x
