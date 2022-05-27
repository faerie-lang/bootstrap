from sys import argv
from lark import Lark
from pathlib import Path


def grammar(path: str):
    with open(path, 'r') as f:
        grammar_def = f.read()

    return Lark(grammar_def, parser='lalr', start="start")


if __name__ == "__main__":
    l = grammar(Path(__file__).parent / 'faerie.lark')
    with open(argv[1]) as f:
        string = f.read()

    # Print pretty parse tree
    print(l.parse(string).pretty())
