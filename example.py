from sys import argv
from faerie.lexer import Lexer


def main(path: str):
    lex = Lexer(path, True)

    for tok in lex:
        print(tok)


if __name__ == '__main__':
    main(argv[1])
