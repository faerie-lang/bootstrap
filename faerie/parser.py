from sys import argv
from lark import Lark, tree
from pathlib import Path
from compiler import transformers


def grammar(path: str):
    with open(path, 'r') as f:
        grammar_def = f.read()

    return Lark(grammar_def, parser='lalr', start="start")


if __name__ == "__main__":
    l = grammar(Path(__file__).parent / 'faerie.lark')
    with open(argv[1]) as f:
        string = f.read()

    # Print pretty parse tree
    parsed = l.parse(string)
    # print(parsed.pretty())
    x = transformers.StepOneTransformer().transform(parsed)
    x = transformers.StepTwoTransformer().transform(x)
    print(x.pretty())
