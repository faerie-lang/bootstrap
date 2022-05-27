/*
Faerie Initial Grammar
*/

%define lr.type ielr

%token
    IDENTIFIER
    COLON ":"
    COMMA ","
    KEY_IF "if"
    KEY_ELSE "else"
    KEY_FOR "for"
    KEY_WHILE "while"
    KEY_RET "return"
    KEY_IN "in"
    KEY_INT "int"
    KEY_DEC "dec"
    KEY_BOOL "bool"
    KEY_STR "str"
    KEY_BYTE "byte"
    KEY_VEC "vec"
    LIT_NUM
    LIT_BOOL
    LIT_STR
    LIT_BYTE
    OP_ASSIGN ":="
    OP_FUNCTIONAL "=>"
    OP_PLUS "+"
    OP_MINUS "-"
    OP_MULT "*"
    OP_DIV "/"
    OP_MOD "%"
    OP_EXP "^"
    OP_AND "and"
    OP_OR "or"
    OP_NOT "!"
    OP_EQ "=="
    OP_NEQ "!="
    OP_LE "<"
    OP_LEQ "<="
    OP_GE ">"
    OP_GEQ ">="
    OP_BITAND "&"
    OP_BITOR "|"
    OP_BITLSHIFT "<<"
    OP_BITRSHIFT ">>"
    OP_BITNOT "~"
    OP_BITXOR "xor"
    OP_PERIOD "."
    SEP_LCURL "{"
    SEP_RCURL "}"
    SEP_LPARENTH "("
    SEP_RPARENTH ")"
    SEP_LBRACKET "["
    SEP_RBRACKET "]"

%%
expr: var
    | declaration
    | group
    | statement

// literals
literal: LIT_NUM | LIT_BOOL | LIT_STR | LIT_BYTE;

// types
type: "int" | "dec" | "bool" | "str" | "byte" | "vec"

// general
var: literal | IDENTIFIER
declaration: "{" expr "}"
group: "(" expr ")"
range: expr ":" expr

typedarg: type IDENTIFIER
   | type IDENTIFIER ":" expr
typedargs: typedarg
    | typedargs "," arg
typedarglist: "(" typedargs ")"
function: IDENTIFIER "=>" typedarglist ":" type declaration
procedure: IDENTIFIER "=>" typedarglist declaration

arg: var | IDENTIFIER ":" var
args: arg | args "," arg
arglist: "(" args ")"
call: IDENTIFIER arglist

statement: operation | arithmetic | logical | bitwise | call | procedure | function

/* operations */
assignment: type IDENTIFIER ":=" expr
if: "if" expr declaration
ife: if | if "else" declaration
ifelse: ife | ife "else" ife
while: "while" expr declaration
for: "for" IDENTIFIER "in" expr declaration
operation: assignment
         | ifelse
         | while
         | for

/** arithmetic **/
add: expr "+" expr
subtract: expr "-" expr
multiply: expr "*" expr
divide: expr "/" expr
modulo: expr "%" expr
exp: expr "^" expr
arithmetic: add
          | subtract
          | multiply
          | divide
          | modulo
          | exp

/** logical **/
logical_and: expr "and" expr
logical_or: expr "or" expr
logical_not: "!" expr
equality: expr "==" expr
no_equality: expr "!=" expr
less_than: expr "<" expr
less_than_eq: expr "<=" expr
greater_than: expr ">" expr
greater_than_eq: expr ">=" expr
logical: logical_and
       | logical_or
       | logical_not
       | equality
       | no_equality
       | less_than
       | less_than_eq
       | greater_than
       | greater_than_eq

/** bitwise **/
bitwise_and: expr "&" expr
bitwise_or: expr "|" expr
bitwise_left_shift: expr "<<" expr
bitwise_right_shift: expr ">>" expr
bitwise_not: "~" expr
bitwise_xor: expr "xor" expr
bitwise: bitwise_and
       | bitwise_or
       | bitwise_left_shift
       | bitwise_right_shift
       | bitwise_not
       | bitwise_xor
%%