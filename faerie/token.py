from enum import Enum
import re


class TokenType(Enum):
    """
    Faerie Token Definitions

    Ranges
    -------------------------------------
    [-1, 10]   -> Meta      [No Prefix]
    [11, 100]  -> Literals  [Prefix: LIT]
    [101, 200] -> Keywords  [Prefix: KEY]
    [201, 300] -> Operators [Prefix: OP]
    [301, 400] -> Separator [Prefix: SEP]
    """
    EOF = -1
    INVALID = 0
    IDENTIFER = 1
    COLON = 2
    COMMA = 3

    # Literals
    LIT_NUM = 11
    LIT_BOOL = 12
    LIT_STR = 13
    LIT_BYTE = 14

    # Keywords
    KEY_IF = 101
    KEY_ELSE = 102
    KEY_FOR = 103
    KEY_WHILE = 104
    KEY_INT = 105
    KEY_DEC = 106
    KEY_BOOL = 107
    KEY_STR = 108
    KEY_BYTE = 109
    KEY_VEC = 110
    KEY_RET = 111
    KEY_IN = 112

    # Operators
    OP_ASSIGN = 201
    OP_FUNCTIONAL = 202
    OP_PLUS = 203
    OP_MINUS = 204
    OP_MULT = 205
    OP_DIV = 206
    OP_MOD = 207
    OP_EXP = 208
    OP_AND = 209
    OP_OR = 210
    OP_NOT = 211
    OP_EQ = 212
    OP_NEQ = 213
    OP_LE = 214
    OP_LEQ = 215
    OP_GE = 216
    OP_GEQ = 217
    OP_BITAND = 218
    OP_BITOR = 219
    OP_BITLSHIFT = 220
    OP_BITRSHIFT = 221
    OP_BITNOT = 222
    OP_BITXOR = 223
    OP_PERIOD = 224

    # Separators
    SEP_LCURL = 301
    SEP_RCURL = 302
    SEP_LPARENTH = 303
    SEP_RPARENTH = 304
    SEP_LBRACKET = 305
    SEP_RBRACKET = 306


class Token:
    text: str
    kind: TokenType

    def __init__(self, text: str, kind: TokenType = None):
        self.text = text

        if kind is None:
            self.parse()
        else:
            self.kind = kind

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.text == other.text and self.kind == other.kind
        else:
            return False

    def __repr__(self):
        return f'({self.text}, {self.kind})'

    def parse(self):
        # Is a literal?
        is_num = re.compile("([+-]?(\d*\.)?\d+)([eE][+-]?\d+)?")
        is_str = re.compile("(\".*\")|(\'.*\')")
        is_byte = re.compile(r"0x[0-9a-fA-F]+")
        matched = [False, False, False]
        if is_num.match(self.text) is not None:
            matched[0] = True
        if is_str.match(self.text) is not None:
            matched[1] = True
        if is_byte.match(self.text) is not None:
            matched[2] = True

        if sum(matched) > 1:
            self.kind = TokenType.INVALID
        elif matched[0]:
            if not self.text.isdigit():
                self.kind = TokenType.INVALID
            else:
                self.kind = TokenType.LIT_NUM
        elif matched[1]:
            self.kind = TokenType.LIT_STR
        elif matched[2]:
            self.kind = TokenType.LIT_BYTE
        else:
            # Is not a literal
            match self.text:
                case '\0':
                    self.kind = TokenType.EOF
                case '{':
                    self.kind = TokenType.SEP_LCURL
                case '}':
                    self.kind = TokenType.SEP_RCURL
                case '(':
                    self.kind = TokenType.SEP_LPARENTH
                case ')':
                    self.kind = TokenType.SEP_RPARENTH
                case '[':
                    self.kind = TokenType.SEP_LBRACKET
                case ']':
                    self.kind = TokenType.SEP_RBRACKET
                case ':':
                    self.kind = TokenType.COLON
                case ',':
                    self.kind = TokenType.COMMA
                case 'true':
                    self.kind = TokenType.KEY_BOOL
                case 'false':
                    self.kind = TokenType.KEY_BOOL
                case 'return':
                    self.kind = TokenType.KEY_RET
                case 'int':
                    self.kind = TokenType.KEY_INT
                case 'dec':
                    self.kind = TokenType.KEY_DEC
                case 'bool':
                    self.kind = TokenType.KEY_BOOL
                case 'str':
                    self.kind = TokenType.KEY_STR
                case 'byte':
                    self.kind = TokenType.KEY_BYTE
                case 'if':
                    self.kind = TokenType.KEY_IF
                case 'else':
                    self.kind = TokenType.KEY_ELSE
                case 'for':
                    self.kind = TokenType.KEY_FOR
                case 'while':
                    self.kind = TokenType.KEY_WHILE
                case 'in':
                    self.kind = TokenType.KEY_IN
                case 'vec':
                    self.kind = TokenType.KEY_VEC
                case ':=':
                    self.kind = TokenType.OP_ASSIGN
                case '=>':
                    self.kind = TokenType.OP_FUNCTIONAL
                case '+':
                    self.kind = TokenType.OP_PLUS
                case '-':
                    self.kind = TokenType.OP_MINUS
                case '*':
                    self.kind = TokenType.OP_MULT
                case '/':
                    self.kind = TokenType.OP_DIV
                case '%':
                    self.kind = TokenType.OP_MOD
                case '^':
                    self.kind = TokenType.OP_EXP
                case 'and':
                    self.kind = TokenType.OP_AND
                case 'or':
                    self.kind = TokenType.OP_OR
                case '!':
                    self.kind = TokenType.OP_NOT
                case '==':
                    self.kind = TokenType.OP_EQ
                case '!=':
                    self.kind = TokenType.OP_NEQ
                case '<':
                    self.kind = TokenType.OP_LE
                case '<=':
                    self.kind = TokenType.OP_LEQ
                case '>':
                    self.kind = TokenType.OP_GE
                case '>=':
                    self.kind = TokenType.OP_GEQ
                case '&':
                    self.kind = TokenType.OP_BITAND
                case '|':
                    self.kind = TokenType.OP_BITOR
                case '<<':
                    self.kind = TokenType.OP_BITLSHIFT
                case '>>':
                    self.kind = TokenType.OP_BITRSHIFT
                case '~':
                    self.kind = TokenType.OP_BITNOT
                case 'xor':
                    self.kind = TokenType.OP_BITXOR
                case '.':
                    self.kind = TokenType.OP_PERIOD
                case _:
                    self.kind = TokenType.IDENTIFER
