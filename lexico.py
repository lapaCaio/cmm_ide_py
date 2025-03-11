import re

# Especificação dos tokens para um subconjunto de C
token_specification = [
    ('COMMENT',       r'//.*'),  # Captura comentários de linha
    ('KEY_INCLUDE',   r'\#include'),
    ('LT',            r'<'),
    ('GT',            r'>'),
    ('INT',           r'\bint\b'),
    ('FLOAT',         r'\bfloat\b'),
    ('DOUBLE',        r'\bdouble\b'),
    ('CHAR',          r'\bchar\b'),
    ('BOOL',          r'\bbool\b'),
    ('SHORT',         r'\bshort\b'),
    ('LONG',          r'\blong\b'),
    ('RETURN',        r'\breturn\b'),
    ('VOID',          r'\bvoid\b'),
    ('MAIN',          r'\bmain\b'),
    ('STRUCT',        r'\bstruct\b'),
    ('IF',            r'\bif\b'),
    ('ELSE',          r'\belse\b'),
    ('SWITCH',        r'\bswitch\b'),
    ('ELSE_IF',       r'\belse\s+if\b'),  # else if
    ('HEADER',        r'[a-zA-Z0-9_]+\.[a-zA-Z0-9_.]*'),
    ('TEXT',         r'"[^"]*"|\'[^\']*\''),  # Texto entre aspas duplas ou simples
    ('IDENT',         r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NUM',           r'\b\d+\b'),
    ('OP',            r'[\+\-\*/]'),
    ('EQUALS',        r'='),
    ('LPAREN',        r'\('),
    ('RPAREN',        r'\)'),
    ('LBRACE',        r'\{'),
    ('RBRACE',        r'\}'),
    ('LBRACKET',      r'\['),  # [
    ('RBRACKET',      r'\]'),  # ]
    ('SEMICOLON',     r';'),
    ('COMMA',         r','),
    ('COLON',         r':'),   # :
    ('AMPERSAND',     r'&'),   # &
    ('NEWLINE',       r'\n'),
    ('SKIP',          r'[ \t]+'),
    ('MISMATCH',      r'.')
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
        if code[pos:pos+2] == "//":  # Ignorar comentários de linha
            while pos < len(code) and code[pos] != "\n":
                pos += 1
        mo = get_token(code, pos)
        if not mo:
            break
        typ = mo.lastgroup
        value = mo.group(typ)
        if typ in ('NEWLINE', 'SKIP', 'COMMENT'):
            pass
        elif typ == 'MISMATCH':
            print(f"Erro. Token Invalido: '{value}' na posição {pos}")
        else:
            tokens.append(Token(typ, value, pos))
        pos = mo.end()
    tokens.append(Token("EOF", "", pos))
    return tokens

if __name__ == '__main__':
    # Para testes: leia o código do arquivo de entrada e mostre os tokens
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    tokens = tokenize(code)
    for token in tokens:
        if token.type == "TEXT":
            print(f"\033[33m{token}\033[0m")  # Exibir TEXT em amarelo
        else:
            print(token)
