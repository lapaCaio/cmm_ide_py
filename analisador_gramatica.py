# analisador_gramatica.py
import lexico

# Lista global de tokens e ponteiro para o token atual
tokens = []
current = 0

def error(msg):
    print("Erro sintático:", msg)
    raise Exception(msg)

def consume(expected):
    global current
    if current < len(tokens) and tokens[current].type == expected:
        current += 1
    else:
        found = tokens[current].type if current < len(tokens) else "EOF"
        error(f"Esperado '{expected}', mas encontrou '{found}' na posição {tokens[current].pos if current < len(tokens) else 'EOF'}")

# <programa> → <especificador> <tipo> ID <programa2>
#           | #define ID NUM <CRLF> <programa>
#           | ε
def programa():
    global current
    if current >= len(tokens) or tokens[current].type == "EOF":
        return
    if tokens[current].type == "DEFINE":
        consume("DEFINE")
        consume("IDENT")
        consume("NUM")
        consume("CRLF")
        programa()
    elif tokens[current].type in {"AUTO", "STATIC", "EXTERN", "CONST", "VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG"}:
        especificador()
        tipo()
        consume("IDENT")
        programa2()
    else:
        return

# <especificador> → AUTO | STATIC | EXTERN | CONST | ε
def especificador():
    if current < len(tokens) and tokens[current].type in {"AUTO", "STATIC", "EXTERN", "CONST"}:
        consume(tokens[current].type)

# <tipo> → VOID | CHAR | FLOAT | DOUBLE | SIGNED <inteiro> | UNSIGNED <inteiro> | <inteiro>
def tipo():
    if current < len(tokens) and tokens[current].type in {"VOID", "CHAR", "FLOAT", "DOUBLE"}:
        consume(tokens[current].type)
    elif current < len(tokens) and tokens[current].type in {"SIGNED", "UNSIGNED"}:
        consume(tokens[current].type)
        inteiro()
    else:
        inteiro()

# <inteiro> → SHORT | INT | LONG
def inteiro():
    if current < len(tokens) and tokens[current].type in {"SHORT", "INT", "LONG"}:
        consume(tokens[current].type)
    else:
        error("Esperado um tipo inteiro (SHORT, INT ou LONG)")

# <programa2> → ; <programa>
#            | [ NUM ] ; <programa>
#            | ( <listaParametros> ) <bloco> <programa>
#            | , <listaID> <programa>
def programa2():
    if current < len(tokens):
        if tokens[current].type == "SEMICOLON":
            consume("SEMICOLON")
            programa()
        elif tokens[current].type == "LBRACKET":
            consume("LBRACKET")
            consume("NUM")
            consume("RBRACKET")
            consume("SEMICOLON")
            programa()
        elif tokens[current].type == "LPAREN":
            consume("LPAREN")
            listaParametros()
            consume("RPAREN")
            bloco()
            programa()
        elif tokens[current].type == "COMMA":
            consume("COMMA")
            listaID()
            programa()

# <listaID> → ID <declaracaoParam2> <listaIDTail>
def listaID():
    consume("IDENT")
    declaracaoParam2()
    listaIDTail()

# <listaIDTail> → ; | , <listaID>
def listaIDTail():
    if current < len(tokens):
        if tokens[current].type == "SEMICOLON":
            consume("SEMICOLON")
        elif tokens[current].type == "COMMA":
            consume("COMMA")
            listaID()
        else:
            error("Esperado ';' ou ',' em listaIDTail")

# <listaParametros> → <listaParamRestante> | ε
def listaParametros():
    if current < len(tokens) and tokens[current].type in {"VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG"}:
        listaParamRestante()

# <listaParamRestante> → <declaracaoParam> <declParamRestante>
def listaParamRestante():
    declaracaoParam()
    declParamRestante()

# <declaracaoParam> → <tipo> ID <declaracaoParam2>
def declaracaoParam():
    tipo()
    consume("IDENT")
    declaracaoParam2()

# <declaracaoParam2> → [ NUM ] | ε
def declaracaoParam2():
    if current < len(tokens) and tokens[current].type == "LBRACKET":
        consume("LBRACKET")
        consume("NUM")
        consume("RBRACKET")

# <declParamRestante> → , <listaParamRestante> | ε
def declParamRestante():
    if current < len(tokens) and tokens[current].type == "COMMA":
        consume("COMMA")
        listaParamRestante()

# <bloco> → { <conjuntoInst> } | ; <conjuntoInst>
def bloco():
    if current < len(tokens) and tokens[current].type == "LBRACE":
        consume("LBRACE")
        conjuntoInst()
        consume("RBRACE")
    elif current < len(tokens) and tokens[current].type == "SEMICOLON":
        consume("SEMICOLON")
        conjuntoInst()
    else:
        error("Esperado '{' ou ';' para iniciar um bloco")

# <conjuntoInst> → <programa> <conjuntoInst> | <instrucoes> <conjuntoInst> | ε
def conjuntoInst():
    while current < len(tokens) and tokens[current].type not in {"RBRACE"}:
        if tokens[current].type in {"IDENT", "RETURN", "PRINTF", "SCANF", "BREAK", "IF"}:
            instrucoes()
        else:
            programa()

# <instrucoes> → ID <expressao> ;
#              | RETURN <expr> ;
#              | PRINTF ( <expr> ) ;
#              | SCANF ( ID ) ;
#              | BREAK ;
#              | IF ( <expr> ) <instrucoes> <instrucoesIf>
def instrucoes():
    if current < len(tokens):
        if tokens[current].type == "IDENT":
            consume("IDENT")
            expressao()
            consume("SEMICOLON")
        elif tokens[current].type == "RETURN":
            consume("RETURN")
            expr()
            consume("SEMICOLON")
        elif tokens[current].type == "PRINTF":
            consume("PRINTF")
            consume("LPAREN")
            expr()
            consume("RPAREN")
            consume("SEMICOLON")
        elif tokens[current].type == "SCANF":
            consume("SCANF")
            consume("LPAREN")
            consume("IDENT")
            consume("RPAREN")
            consume("SEMICOLON")
        elif tokens[current].type == "BREAK":
            consume("BREAK")
            consume("SEMICOLON")
        elif tokens[current].type == "IF":
            consume("IF")
            consume("LPAREN")
            expr()
            consume("RPAREN")
            instrucoes()
            instrucoesIf()
        else:
            error("Token inesperado em instrucoes")

# <instrucoesIf> → ELSE <instrucoes> | ε
def instrucoesIf():
    if current < len(tokens) and tokens[current].type == "ELSE":
        consume("ELSE")
        instrucoes()

# <expressao> → <atribuicao>
#              | [ <expr> ] <atribuicao>
#              | ( exprList )
#              | ε
def expressao():
    if current < len(tokens) and tokens[current].type == "LBRACKET":
        consume("LBRACKET")
        expr()
        consume("RBRACKET")
        atribuicao()
    elif current < len(tokens) and tokens[current].type == "LPAREN":
        consume("LPAREN")
        exprList()
        consume("RPAREN")
    else:
        atribuicao()

# <atribuicao> → <operadorAtrib> <expr>
def atribuicao():
    if current < len(tokens) and tokens[current].type in {"EQUALS", "MUL_EQ", "DIV_EQ", "MOD_EQ", "ADD_EQ", "SUB_EQ"}:
        operadorAtrib()
        expr()

# <operadorAtrib> → = | *= | /= | %= | += | -=
def operadorAtrib():
    if current < len(tokens) and tokens[current].value in {"=", "*=", "/=", "%=", "+=", "-="}:
        consume(tokens[current].type)
    else:
        error("Operador de atribuição esperado")

# <expr> → <exprAnd> <exprOr>
def expr():
    exprAnd()
    exprOr()

# <exprList> → <expr> <exprListTail> | ε
def exprList():
    if current < len(tokens) and tokens[current].type != "RPAREN":
        expr()
        exprListTail()

# <exprListTail> → , <exprList> | ε
def exprListTail():
    if current < len(tokens) and tokens[current].type == "COMMA":
        consume("COMMA")
        exprList()

# <exprOr> → OR <exprAnd> <exprOr> | ε
def exprOr():
    if current < len(tokens) and tokens[current].type == "OR":
        consume("OR")
        exprAnd()
        exprOr()

# <exprAnd> → <exprEqual> <exprAnd2>
def exprAnd():
    exprEqual()
    exprAnd2()

# <exprAnd2> → AND <exprEqual> <exprAnd2> | ε
def exprAnd2():
    if current < len(tokens) and tokens[current].type == "AND":
        consume("AND")
        exprEqual()
        exprAnd2()

# <exprEqual> → <exprRelational> <exprEqual2>
def exprEqual():
    exprRelational()
    exprEqual2()

# <exprEqual2> → == <exprRelational> <exprEqual2>
#               | != <exprRelational> <exprEqual2>
#               | ε
def exprEqual2():
    if current < len(tokens) and tokens[current].value in {"==", "!="}:
        consume(tokens[current].type)
        exprRelational()
        exprEqual2()

# <exprRelational> → <exprPlus> <exprRelational2>
def exprRelational():
    exprPlus()
    exprRelational2()

# <exprRelational2> → < <exprPlus> <exprRelational2>
#                    | <= <exprPlus> <exprRelational2>
#                    | > <exprPlus> <exprRelational2>
#                    | >= <exprPlus> <exprRelational2>
#                    | ε
def exprRelational2():
    if current < len(tokens) and tokens[current].value in {"<", "<=", ">", ">="}:
        consume(tokens[current].type)
        exprPlus()
        exprRelational2()

# <exprPlus> → <exprMult> <exprPlus2>
def exprPlus():
    exprMult()
    exprPlus2()

# <exprPlus2> → + <exprMult> <exprPlus2>
#              | - <exprMult> <exprPlus2>
#              | ε
def exprPlus2():
    if current < len(tokens) and tokens[current].value in {"+", "-"}:
        consume(tokens[current].type)
        exprMult()
        exprPlus2()

# <exprMult> → <exprUnary> <exprMult2>
def exprMult():
    exprUnary()
    exprMult2()

# <exprMult2> → * <exprUnary> <exprMult2>
#              | / <exprUnary> <exprMult2>
#              | ε
def exprMult2():
    if current < len(tokens) and tokens[current].value in {"*", "/"}:
        consume(tokens[current].type)
        exprUnary()
        exprMult2()

# <exprUnary> → + <exprParenthesis>
#             | - <exprParenthesis>
#             | <exprParenthesis>
def exprUnary():
    if current < len(tokens) and tokens[current].value in {"+", "-"}:
        consume(tokens[current].type)
        exprParenthesis()
    else:
        exprParenthesis()

# <exprParenthesis> → ( <expr> ) | <primary>
def exprParenthesis():
    if current < len(tokens) and tokens[current].type == "LPAREN":
        consume("LPAREN")
        expr()
        consume("RPAREN")
    else:
        primary()

# <primary> → ID <primaryID> | NUM | LITERAL
def primary():
    if current < len(tokens):
        if tokens[current].type == "IDENT":
            consume("IDENT")
            primaryID()
        elif tokens[current].type == "NUM":
            consume("NUM")
        elif tokens[current].type == "LITERAL":
            consume("LITERAL")
        else:
            error("Esperado ID, NUM ou LITERAL em primary")
    else:
        error("Fim inesperado de input em primary")

# <primaryID> → [ <primary> ] | ( <exprList> ) | ε
def primaryID():
    if current < len(tokens):
        if tokens[current].type == "LBRACKET":
            consume("LBRACKET")
            primary()
            consume("RBRACKET")
        elif tokens[current].type == "LPAREN":
            consume("LPAREN")
            exprList()
            consume("RPAREN")

def parse():
    global tokens, current
    with open("main.c", "r", encoding="utf-8") as f:
        code = f.read()
    tokens = lexico.tokenize(code)
    current = 0
    programa()
    if tokens[current].type != "EOF":
        error("Conteúdo não processado após a análise")
    print("Programa compilado com sucesso.")

if __name__ == '__main__':
    parse()
