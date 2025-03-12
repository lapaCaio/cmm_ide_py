import re

# Especificação dos tokens para um subconjunto de C
token_specification = [
    ('ML_COMMENT',    r'/\*[\s\S]*?\*/'),  # Comentário de várias linhas
    ('COMMENT',       r'//.*'),            # Comentário de linha
    ('KEY_INCLUDE',   r'\#include'),
    ('AUTO',          r'\bauto\b'),        # Palavra reservada auto
    ('CONST',         r'\bconst\b'),       # Palavra reservada const
    ('SIGNED',        r'\bsigned\b'),      # Palavra reservada signed
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
    ('ELSE_IF',       r'\belse\s+if\b'),
    ('HEADER',        r'[a-zA-Z0-9_]+\.[a-zA-Z0-9_.]*'),
    ('TEXT',          r'"[^"]*"|\'[^\']*\''),
    ('IDENT',         r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('NUM',           r'\b\d+\b'),
    ('LOGICAL_OR',    r'\|\|'),             # Operador lógico OU
    ('NOT_EQUALS',    r'!='),               # Operador de desigualdade
    ('OP',            r'[\+\-\*/]'),
    ('EQUALS',        r'='),                # Atribuição
    ('LPAREN',        r'\('),
    ('RPAREN',        r'\)'),
    ('LBRACE',        r'\{'),
    ('RBRACE',        r'\}'),
    ('LBRACKET',      r'\['),
    ('RBRACKET',      r'\]'),
    ('SEMICOLON',     r';'),
    ('COMMA',         r','),
    ('COLON',         r':'),
    ('AMPERSAND',     r'&'),
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
        mo = get_token(code, pos)
        if not mo:
            break
        typ = mo.lastgroup
        value = mo.group(typ)
        # Ignora espaços, quebras de linha e comentários
        if typ in ('NEWLINE', 'SKIP', 'COMMENT', 'ML_COMMENT'):
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
