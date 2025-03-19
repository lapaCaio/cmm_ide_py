import re

# Especificação dos tokens para um subconjunto de C
token_specification = [
    # Tokens mais específicos primeiro: palavras reservadas
    ('AUTO', r'\bauto\b'),
    ('STATIC', r'\bstatic\b'),
    ('EXTERN', r'\bextern\b'),
    ('CONST', r'\bconst\b'),
    ('VOID', r'\bvoid\b'),
    ('CHAR', r'\bchar\b'),
    ('FLOAT', r'\bfloat\b'),
    ('DOUBLE', r'\bdouble\b'),
    ('SIGNED', r'\bsigned\b'),
    ('UNSIGNED', r'\bunsigned\b'),
    ('SHORT', r'\bshort\b'),
    ('INT', r'\bint\b'),
    ('LONG', r'\blong\b'),
    ('RETURN', r'\breturn\b'),
    ('PRINTF', r'\bprintf\b'),
    ('SCANF', r'\bscanf\b'),
    ('BREAK', r'\bbreak\b'),
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),

    # Outros tokens que não são palavras reservadas
    ('VAR_ACCESS', r'[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*'),
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('NUM', r'\d+(\.\d+)?'),
    ('LITERAL', r'"([^"\\]*(\\.[^"\\]*)*)"|\'([^\'\\]*(\\.[^\'\\]*)*)\''),
    ('INCLUDE', r'#include\s*(<[^>]+>|"[^"]+")'),

    # Operadores, pontuação e outros tokens
    ('OR_OP', r'\|\|'),
    ('AND_OP', r'&&'),
    ('AMPERSAND', r'&'),
    ('EQUAL', r'=='),
    ('NOT_EQUAL', r'!='),
    ('LESS_EQUAL', r'<='),
    ('GREATER_EQUAL', r'>='),
    ('LESS_THEN', r'<'),
    ('GREATER_THEN', r'>'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULT', r'\*'),
    ('DIV', r'/'),
    ('ASSIGN', r'='),
    ('MULT_ASSIGN', r'\*='),
    ('DIV_ASSIGN', r'/='),
    ('MOD_ASSIGN', r'%='),
    ('ADD_ASSIGN', r'\+='),
    ('SUB_ASSIGN', r'-='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('CRLF', r'\r\n'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]

# CMM_IDE (MAIN)
    # ANALISADOR
        # LEXICO -> APENAS CLASSIFICAÇÃO E VALIDAÇÃO DOS TOKENS -> CATEGORIZA OS TOKENS E OS COLOCA EM UMA LISTA
        # SINTATICO -> VERIFICAÇÃO DE AUSÊNCIA DE TERMOS, PARENTESES, CHAVES, PONTO E VIRGULA... ->
        # SEMANTICO -> VERIFICAÇÃO COM BASE NO ESCOPO -> ANALISA A PILHA E LISTA
    # VIEW -> O FRONT PROPRIAMENTE DITO

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
compiled_regex = re.compile(tok_regex)

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line  # Número da linha no código
        self.column = column  # Posição do token na linha

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"


def tokenize(code):
    tokens = []
    lines = code.splitlines()

    for line_num, line in enumerate(lines, start=1):

        if line.lstrip().startswith('//'):
            continue

        column = 1
        for match in compiled_regex.finditer(line):
            kind = match.lastgroup
            value = match.group(kind)

            if kind == "NEWLINE":  # Ignora quebras de linha explícitas
                continue
            elif kind == "SKIP":  # Ignora espaços e tabs
                column += len(value)
                continue
            elif kind == "MISMATCH":  # Caractere inesperado
                raise SyntaxError(f"Caractere inesperado {value!r} na linha {line_num}, coluna {column}")

            tokens.append(Token(kind, value, line_num, column))
            column += len(value)

    return tokens

# É possível verificar a tokenização manualmente a partir de um código adicionádo à uma classe "main.c" na pasta do projeto
if __name__ == '__main__':
    # Para testes: leia o código do arquivo de entrada e mostre os tokens
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    tokens = tokenize(code)