from faerie.lexer import Lexer
from faerie.token import Token, TokenType
import unittest


class TestLexer(unittest.TestCase):
    def test_iter(self):
        lexer = Lexer('int some_int := 1\nstr some_str := "example"\n')
        control = [
            Token('int', TokenType.KEY_INT),
            Token('some_int', TokenType.IDENTIFER),
            Token(':=', TokenType.OP_ASSIGN),
            Token('1', TokenType.LIT_NUM),
            Token('str', TokenType.KEY_STR),
            Token('some_str', TokenType.IDENTIFER),
            Token(":=", TokenType.OP_ASSIGN),
            Token('"example"', TokenType.LIT_STR)
        ]
        for idx, tok in enumerate(lexer):
            try:
                self.assertEqual(tok, control[idx])
            except AssertionError:
                print(f'Index  : {idx}')
                print(f'Actual : {control[idx]}')
                print(f'Given  : {tok}')
                self.fail()


if __name__ == 'main':
    unittest.main()
