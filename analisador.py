# analisador.py
import lexico
import semantico

tokens = []  # Lista global de tokens
current = 0  # Ponteiro para o token atual

def sintatico():
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    global tokens, current
    tokens = lexico.tokenize(code)
    current = 0
    semantico.init_semantico()  # Abre e escreve o cabeçalho no arquivo de saída
    program()
    semantico.end_semantico()   # Finaliza o arquivo de saída
    print("Programa compilado com sucesso.")

def consume(expected_type):
    global current
    if current < len(tokens) and tokens[current].type == expected_type:
        current += 1
    else:
        error(f"Esperado {expected_type} mas encontrou {tokens[current].type} na posição {tokens[current].pos}")

def error(message):
    print("Erro sintático:", message)
    raise Exception(message)

def program():
    header()
    main_func()

def header():
    # header -> (KEY_INCLUDE LT HEADER GT)*
    while current < len(tokens) and tokens[current].type == "KEY_INCLUDE":
        consume("KEY_INCLUDE")
        consume("LT")
        consume("HEADER")
        consume("GT")

def main_func():
    # main -> INT MAIN LPAREN VOID RPAREN compound_stmt
    consume("INT")
    consume("MAIN")
    consume("LPAREN")
    consume("VOID")
    consume("RPAREN")
    compound_stmt()

def compound_stmt():
    # compound_stmt -> LBRACE stmt_list RBRACE
    consume("LBRACE")
    stmt_list()
    consume("RBRACE")

def stmt_list():
    # stmt_list -> stmt stmt_list | ε
    if current < len(tokens) and tokens[current].type in ("INT", "RETURN", "IDENT"):
        stmt()
        stmt_list()

def stmt():
    # stmt -> declaration | expression_stmt | return_stmt
    if tokens[current].type == "INT":
        declaration()
    elif tokens[current].type == "RETURN":
        return_stmt()
    else:
        expression_stmt()

def declaration():
    # declaration -> INT IDENT EQUALS expression SEMICOLON
    consume("INT")
    ident_token = tokens[current]
    consume("IDENT")
    consume("EQUALS")
    expr = expression()
    consume("SEMICOLON")
    semantico.declaration_action("int", ident_token.value, expr)

def expression_stmt():
    # expression_stmt -> expression SEMICOLON
    expr = expression()
    consume("SEMICOLON")
    semantico.expression_action(expr)

def expression():
    # expression -> term { OP term }*
    left = term()
    while current < len(tokens) and tokens[current].type == "OP":
        op = tokens[current].value
        consume("OP")
        right = term()
        left = f"({left} {op} {right})"
    return left

def term():
    # term -> IDENT | NUM
    if tokens[current].type == "IDENT":
        val = tokens[current].value
        consume("IDENT")
        return val
    elif tokens[current].type == "NUM":
        val = tokens[current].value
        consume("NUM")
        return val
    else:
        error("Esperado IDENT ou NUM em term")

def return_stmt():
    # return_stmt -> RETURN expression SEMICOLON
    consume("RETURN")
    expr = expression()
    consume("SEMICOLON")
    semantico.return_action(expr)

if __name__ == '__main__':
    sintatico()
