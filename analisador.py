import lexico
import semantico

tokens = []  # lista global de tokens
current = 0  # ponteiro para o token atual


def sintatico():
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    global tokens, current
    tokens = lexico.tokenize(code)
    current = 0
    semantico.init_semantico()  # abre e escreve o cabeçalho no arquivo de saída
    program()
    semantico.end_semantico()  # finaliza o arquivo de saída
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
    declarations()
    main_func()


def header():
    while current < len(tokens) and tokens[current].type == "KEY_INCLUDE":
        consume("KEY_INCLUDE")
        consume("LT")
        consume("HEADER")
        consume("GT")


def declarations():
    while current < len(tokens) and tokens[current].type in ("STRUCT", "INT", "FLOAT", "CHAR"):
        if tokens[current].type == "STRUCT":
            struct_declaration()
        elif tokens[current].type in ("INT", "FLOAT", "CHAR"):
            declaration()


def function():
    # function -> type IDENT LPAREN param_list RPAREN compound_stmt
    return_type = tokens[current].value
    consume("TYPE")  # Tipo de retorno (int, float, etc.)

    func_name = tokens[current].value
    consume("IDENT")  # Nome da função

    consume("LPAREN")  # (
    params = param_list()  # Lista de parâmetros
    consume("RPAREN")  # )

    semantico.function_action(return_type, func_name, params)  # Ação semântica

    compound_stmt()  # Corpo da função


def param_list():
    # param_list -> type IDENT { COMMA type IDENT }* | ε
    params = []
    if tokens[current].type == "TYPE":
        while current < len(tokens) and tokens[current].type == "TYPE":
            param_type = tokens[current].value
            consume("TYPE")  # Tipo do parâmetro

            param_name = tokens[current].value
            consume("IDENT")  # Nome do parâmetro

            params.append((param_type, param_name))

            if current < len(tokens) and tokens[current].type == "COMMA":
                consume("COMMA")  # ,
            else:
                break
    return params


def struct_declaration():
    consume("STRUCT")
    struct_name = tokens[current].value
    consume("IDENT")
    consume("LBRACE")
    members = struct_members()
    consume("RBRACE")
    consume("SEMICOLON")
    semantico.struct_action(struct_name, members)


def struct_members():
    members = []
    while current < len(tokens) and tokens[current].type in ("INT", "FLOAT", "CHAR"):
        type_token = tokens[current].value
        consume(tokens[current].type)
        member_name = tokens[current].value
        consume("IDENT")

        # Verifica se é um vetor
        if current < len(tokens) and tokens[current].type == "LBRACKET":
            consume("LBRACKET")
            size = tokens[current].value
            consume("NUM")
            consume("RBRACKET")
            consume("SEMICOLON")
            members.append((type_token, member_name, size))  # Adiciona vetor com tamanho
        else:
            consume("SEMICOLON")
            members.append((type_token, member_name))  # Adiciona variável normal

    return members


def main_func():
    consume("INT")
    consume("MAIN")
    consume("LPAREN")
    consume("VOID")
    consume("RPAREN")
    compound_stmt()


def compound_stmt():
    consume("LBRACE")
    stmt_list()
    consume("RBRACE")


def stmt_list():
    if current < len(tokens) and tokens[current].type in ("INT", "FLOAT", "CHAR", "RETURN", "IDENT"):
        stmt()
        stmt_list()


def stmt():
    # stmt -> declaration | function | expression_stmt | return_stmt
    if tokens[current].type == "TYPE":
        if current + 1 < len(tokens) and tokens[current + 1].type == "IDENT":
            if current + 2 < len(tokens) and tokens[current + 2].type == "LPAREN":
                function()  # Identifica uma função
            else:
                declaration()  # Identifica uma variável
    elif tokens[current].type == "RETURN":
        return_stmt()
    else:
        expression_stmt()



def declaration():
    type_token = tokens[current].value
    consume(tokens[current].type)
    ident_token = tokens[current]

    consume("IDENT")

    # Se for um vetor, processa como vetor
    if current < len(tokens) and tokens[current].type == "LBRACKET":
        vector_declaration(type_token, ident_token)
    else:
        consume("EQUALS")
        expr = expression()
        consume("SEMICOLON")
        semantico.declaration_action(type_token, ident_token.value, expr)


def vector_declaration(type_token, ident_token):
    consume("LBRACKET")
    size = tokens[current].value
    consume("NUM")
    consume("RBRACKET")
    consume("SEMICOLON")
    semantico.vector_action(type_token, ident_token.value, size)


def expression_stmt():
    expr = expression()
    consume("SEMICOLON")
    semantico.expression_action(expr)


def expression():
    left = term()
    while current < len(tokens) and tokens[current].type == "OP":
        op = tokens[current].value
        consume("OP")
        right = term()
        left = f"({left} {op} {right})"
    return left


def term():
    if tokens[current].type == "IDENT":
        val = tokens[current].value
        consume("IDENT")

        # Verifica se é acesso a um vetor: IDENT[LBRACKET NUM RBRACKET]
        if current < len(tokens) and tokens[current].type == "LBRACKET":
            consume("LBRACKET")
            index = tokens[current].value
            consume("NUM")
            consume("RBRACKET")
            return f"{val}[{index}]"

        return val
    elif tokens[current].type == "NUM":
        val = tokens[current].value
        consume("NUM")
        return val
    elif tokens[current].type == "CHAR_LITERAL":
        val = tokens[current].value
        consume("CHAR_LITERAL")
        return val
    elif tokens[current].type == "FLOAT_LITERAL":
        val = tokens[current].value
        consume("FLOAT_LITERAL")
        return val
    else:
        error("Esperado IDENT, NUM, CHAR_LITERAL ou FLOAT_LITERAL em term")


def return_stmt():
    consume("RETURN")
    expr = expression()
    consume("SEMICOLON")
    semantico.return_action(expr)
