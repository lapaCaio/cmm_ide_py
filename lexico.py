# lexico.py
import re

token_specification = [
    ('COMMENT',       r'//.*'),  # Comentários de linha
    ('DEFINE',        r'\#define'),
    ('CRLF',          r'\n'),
    ('AUTO',          r'\bauto\b'),
    ('STATIC',        r'\bstatic\b'),
    ('EXTERN',        r'\bextern\b'),
    ('CONST',         r'\bconst\b'),
    ('VOID',          r'\bvoid\b'),
    ('CHAR',          r'\bchar\b'),
    ('FLOAT',         r'\bfloat\b'),
    ('DOUBLE',        r'\bdouble\b'),
    ('SIGNED',        r'\bsigned\b'),
    ('UNSIGNED',      r'\bunsigned\b'),
    ('SHORT',         r'\bshort\b'),
    ('INT',           r'\bint\b'),
    ('LONG',          r'\blong\b'),
    ('RETURN',        r'\breturn\b'),
    ('MAIN',          r'\bmain\b'),
    ('STRUCT',        r'\bstruct\b'),
    ('IF',            r'\bif\b'),
    ('ELSE',          r'\belse\b'),
    ('SWITCH',        r'\bswitch\b'),
    ('PRINTF',        r'\bprintf\b'),
    ('SCANF',         r'\bscanf\b'),
    ('BREAK',         r'\bbreak\b'),
    ('OR',            r'\bor\b'),
    ('AND',           r'\band\b'),
    ('IDENT',         r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('NUM',           r'\b\d+(\.\d+)?\b'),
    ('LITERAL',       r'\'[A-Za-z0-9_]*\''),  # Literal de caractere (simplificado)
    ('OP',            r'[\+\-\*/]'),
    ('EQUALS',        r'='),
    ('MUL_EQ',        r'\*='),
    ('DIV_EQ',        r'/='),
    ('MOD_EQ',        r'%='),
    ('ADD_EQ',        r'\+='),
    ('SUB_EQ',        r'-='),
    ('LPAREN',        r'\('),
    ('RPAREN',        r'\)'),
    ('LBRACE',        r'\{'),
    ('RBRACE',        r'\}'),
    ('LBRACKET',      r'\['),
    ('RBRACKET',      r'\]'),
    ('SEMICOLON',     r';'),
    ('COMMA',         r','),
    ('LT',            r'<'),
    ('GT',            r'>'),
    ('SKIP',          r'[ \t]+'),
    ('MISMATCH',      r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos
    def __repr__(self):
        return f"Token({self.type}, {self.value}, pos={self.pos})"

def tokenize(code):
    pos = 0
    tokens = []
    while pos < len(code):
        # Pula comentários de linha
        if code[pos:pos+2] == "//":
            while pos < len(code) and code[pos] != "\n":
                pos += 1
        mo = get_token(code, pos)
        if not mo:
            break
        typ = mo.lastgroup
        value = mo.group(typ)
        if typ in ('SKIP', 'COMMENT'):
            pass
        elif typ == 'MISMATCH':
            print(f"Erro. Token Invalido: '{value}' na posição {pos}")
        else:
            tokens.append(Token(typ, value, pos))
        pos = mo.end()
    tokens.append(Token("EOF", "", pos))
    return tokens

if __name__ == '__main__':
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    tokens = tokenize(code)
    for token in tokens:
        print(token)
