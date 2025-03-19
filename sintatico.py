import cmm_ide


class Sintatico:
    def __init__(self, tokens, log_callback):
        self.tokens = tokens
        self.log_callback = log_callback
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao] if self.tokens else None

    def avancar(self):
        """Avança para o próximo token na lista."""
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]
        else:
            self.token_atual = None

    def erro(self, mensagem):
        """Lança um erro de sintaxe."""
        #  print(f"Tokens restantes: {self.tokens}")
        raise SyntaxError(f"Erro sintático: {mensagem} no token {self.token_atual}")


    def consumir(self, tipo):
        """Verifica se o token atual é do tipo esperado e avança.
        Retorna True se consumiu o token, False se não consumiu."""
        if self.token_atual and self.token_atual.type == tipo:
            self.avancar()
            return True  # Token foi consumido
        return False  # Não consumiu

    def analisar(self):
        """Inicia a análise sintática a partir da regra principal."""
        try:
            self.programa()
            return "Análise concluída com sucesso!"
        except Exception as e:
            self.log_callback(f"Erro na Análise Sintática: {e}")
            return "\n"

    def diretiva(self):
        if self.consumir("INCLUDE"):
            return True
        return False

    # <programa> → <especificador> <tipo> ID <programa2> | #define ID NUM <CRLF> <programa> | ε
    def programa(self):
        # Produção ε: fim da entrada ou fechamento de bloco
        if self.token_atual is None or self.token_atual.type == "RBRACE":
            return

        # Processa diretivas (por exemplo, #include)
        while self.diretiva():
            pass

        if self.token_atual is None or self.token_atual.type == "RBRACE":
            return

        # Produção para #define: #define ID NUM <CRLF> <programa>
        if self.token_atual.type == "DEFINE":
            self.consumir("DEFINE")
            if not self.consumir("ID"):
                self.erro("Esperado ID após #define")
            if not self.consumir("NUM"):
                self.erro("Esperado NUM após ID no #define")
            if not self.consumir("CRLF"):
                self.erro("Esperado CRLF após NUM no #define")
            self.programa()  # Continua o processamento
            return

        # Se o token iniciar com um especificador ou com um tipo, trata como declaração
        if self.token_atual.type in (
                "AUTO", "STATIC", "EXTERN", "CONST",
                "VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG"
        ):
            # Produção: <especificador> <tipo> ID <programa2>
            self.especificador()  # Opcional
            if not (self.token_atual and self.token_atual.type in (
                    "VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG"
            )):
                self.erro("Esperado um tipo (como 'int') antes do identificador")
            self.tipo()  # Consome o token de tipo
            if not self.consumir("ID"):
                self.erro("Esperado ID após o tipo")
            # Regra nova: inicialização opcional
            if self.token_atual and self.token_atual.type == "ASSIGN":
                self.consumir("ASSIGN")
                self.expr()
            self.programa2()  # Processa o que vier depois (por exemplo, ';', '[', '(', ou ',')
        # Caso contrário, se o token iniciar uma instrução (ex.: RETURN, ID, PRINTF, etc.)
        elif self.token_atual.type in ("ID", "RETURN", "PRINTF", "SCANF", "BREAK", "IF"):
            self.instrucoes()
        else:
            self.erro("Instrução inválida ou ausente")

    # <especificador> → AUTO | STATIC | EXTERN | CONST | ε
    def especificador(self):
        self.consumir("AUTO") or self.consumir("STATIC") or self.consumir("EXTERN") or self.consumir("CONST")
        # ε permitido

    # <tipo> → VOID | CHAR | FLOAT | DOUBLE | SIGNED <inteiro> | UNSIGNED <inteiro> | <inteiro>
    def tipo(self):
        if self.consumir("VOID") or self.consumir("CHAR") or self.consumir("FLOAT") or self.consumir("DOUBLE"):
            return  # Consomeu um tipo básico
        if self.consumir("SIGNED") or self.consumir("UNSIGNED"):
            self.inteiro()  # Após SIGNED/UNSIGNED, <inteiro> é obrigatório
            return
        # Se não for nenhum dos casos acima, deve ser um inteiro
        self.inteiro()

    # <inteiro> → SHORT | INT | LONG (não pode ser vazio)
    def inteiro(self):
        if not (self.consumir("SHORT") or self.consumir("INT") or self.consumir("LONG")):
            tipo_atual = self.token_atual.type if self.token_atual else "FIM DA ENTRADA"
            self.erro(f"Esperado um tipo inteiro (SHORT, INT ou LONG), encontrado {tipo_atual}")

    # <programa2> → ; <programa> | [ NUM ] ; <programa> | (<listaParametros>) <bloco> <programa> | , <listaID> <programa>
    def programa2(self):
        if self.consumir("SEMICOLON"):
            self.programa()
            return
        if self.consumir("LBRACKET"):
            if not self.consumir("NUM"):
                self.erro("Esperado NUM após '[' em programa2")
            if not self.consumir("RBRACKET"):
                self.erro("Esperado ']' após NUM em programa2")
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após ']' em programa2")
            self.programa()
            return
        if self.consumir("LPAREN"):
            self.lista_parametros()  # Pode ser vazio
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após lista de parâmetros em programa2")
            self.bloco()
            self.programa()
            return
        if self.consumir("COMMA"):
            self.lista_id()
            self.programa()
            return
        self.erro("Esperado ';', '[', '(', ou ',' em programa2")

    # <listaID> → ID <declaracaoParam2> <listaIDTail>
    def lista_id(self):
        if not self.consumir("ID"):
            self.erro("Esperado ID no início da lista de IDs")
        # Nova regra: Inicialização opcional para declarações em lista
        if self.token_atual and self.token_atual.type == "ASSIGN":
            self.consumir("ASSIGN")
            self.expr()  # Processa a expressão de inicialização
        else:
            self.declaracao_param2()
        self.lista_id_tail()

    # <listaIDTail> → ; | , <listaID>
    def lista_id_tail(self):
        if self.consumir("SEMICOLON"):
            return
        elif self.consumir("COMMA"):
            self.lista_id()
            return
        else:
            self.erro("Esperado ';' ou ',' ao final da lista de IDs")

    # <listaParametros> → <listaParamRestante> | ε
    def lista_parametros(self):
        # Se o token atual pode iniciar uma declaração de parâmetro, processa; caso contrário, ε é permitido.
        # (Assume-se que tipos válidos iniciam a declaração)
        if self.token_atual and self.token_atual.type in ("VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG"):
            self.lista_param_restante()
        # Senão, ε

    # <listaParamRestante> → <declaracaoParam> <declParamRestante>
    def lista_param_restante(self):
        self.declaracao_param()
        self.declaracao_param_restante()

    # <declaracaoParam> → <tipo> ID <declaracaoParam2>
    def declaracao_param(self):
        self.tipo()
        if not self.consumir("ID"):
            self.erro("Esperado ID na declaração de parâmetro")
        self.declaracao_param2()

    # <declaracaoParam2> → [ NUM ] | ε
    def declaracao_param2(self):
        if self.consumir("LBRACKET"):
            if not self.consumir("NUM"):
                self.erro("Esperado NUM após '[' em declaração de parâmetro")
            if not self.consumir("RBRACKET"):
                self.erro("Esperado ']' após NUM em declaração de parâmetro")
            return
        # ε permitido

    # <declParamRestante> → , <listaParamRestante> | ε
    def declaracao_param_restante(self):
        if self.consumir("COMMA"):
            self.lista_param_restante()
        # ε permitido

    # <bloco> → { <conjuntoInst> } | ; <conjuntoInst>
    def bloco(self):
        if self.consumir("LBRACE"):
            # Processa o conjunto de instruções dentro do bloco
            self.conjunto_inst()
            # Caso sobre tokens dentro do bloco, tenta consumi-los com instrucoes()
            while self.token_atual is not None and self.token_atual.type != "RBRACE":
                self.instrucoes()
            if not self.consumir("RBRACE"):
                self.erro("Esperado '}' para fechar o bloco")
        elif self.consumir("SEMICOLON"):
            self.conjunto_inst()
        else:
            self.erro("Esperado '{' ou ';' para iniciar o bloco")

    # <conjuntoInst> → <programa> <conjuntoInst> | <instrucoes> <conjuntoInst> | ε
    def conjunto_inst(self):
        while self.token_atual is not None and self.token_atual.type != "RBRACE":
            # Se o token iniciar com um especificador, tipo ou diretiva, chama programa() para processar uma declaração
            if self.token_atual.type in (
                    "AUTO", "STATIC", "EXTERN", "CONST",
                    "VOID", "CHAR", "FLOAT", "DOUBLE", "SIGNED", "UNSIGNED", "SHORT", "INT", "LONG",
                    "DEFINE", "INCLUDE"
            ):
                self.programa()
            # Se o token indicar uma instrução, chama instrucoes()
            elif self.token_atual.type in ("ID", "RETURN", "PRINTF", "SCANF", "BREAK", "IF"):
                self.instrucoes()
            else:
                self.erro("Instrução inválida ou ausente (não permite vazio)")

    # <instrucoes> → ID <expressao> ; | RETURN <expr> ; | PRINTF ( <expr> ) ; | SCANF ( ID ) ; | BREAK ; | IF ( <expr> ) <instrucoes> <instrucoesIf>
    def instrucoes(self):
        if self.consumir("ID"):
            self.expressao()
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após expressão na instrução")
            return
        if self.consumir("RETURN"):
            self.expr()
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após RETURN")
            return
        if self.consumir("PRINTF"):
            if not self.consumir("LPAREN"):
                self.erro("Esperado '(' após PRINTF")
            self.expr()
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após expressão no PRINTF")
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após PRINTF")
            return
        if self.consumir("SCANF"):
            if not self.consumir("LPAREN"):
                self.erro("Esperado '(' após SCANF")
            if not self.consumir("ID"):
                self.erro("Esperado ID em SCANF")
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após ID em SCANF")
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após SCANF")
            return
        if self.consumir("BREAK"):
            if not self.consumir("SEMICOLON"):
                self.erro("Esperado ';' após BREAK")
            return
        if self.consumir("IF"):
            if not self.consumir("LPAREN"):
                self.erro("Esperado '(' após IF")
            self.expr()
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após condição do IF")
            self.instrucoes()
            self.instrucoes_if()
            return
        self.erro("Instrução inválida ou ausente (não permite vazio)")

    # <instrucoesIf> → ELSE <instrucoes> | ε
    def instrucoes_if(self):
        if self.consumir("ELSE"):
            self.instrucoes()
        # ε permitido

    # <expressao> → <atribuicao> | [ <expr> ] <atribuicao> | ( exprList ) | ε
    def expressao(self):
        # Se o token atual indicar início de uma atribuição ou expressão, processa; caso contrário, ε é permitido.
        # Aqui, como há ambiguidade, tenta a alternativa com [ ou (
        if self.atribuicao_possivel():
            self.atribuicao()
            return
        if self.consumir("LBRACKET"):
            self.expr()
            if not self.consumir("RBRACKET"):
                self.erro("Esperado ']' após expressão em expressao")
            self.atribuicao()
            return
        if self.consumir("LPAREN"):
            self.expr_list()
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após exprList em expressao")
            return
        # ε permitido

    def atribuicao_possivel(self):
        # Verifica se o token atual pode iniciar um operador de atribuição
        return self.token_atual and self.token_atual.type in (
            "ASSIGN", "MULT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN"
        )

    # <atribuicao> → <operadorAtrib> <expr>
    def atribuicao(self):
        self.operador_atrib()
        self.expr()

    # <operadorAtrib> → = | *= | /= | %= | += | -=
    def operador_atrib(self):
        if self.consumir("ASSIGN") or self.consumir("MULT_ASSIGN") or self.consumir("DIV_ASSIGN") or \
           self.consumir("MOD_ASSIGN") or self.consumir("ADD_ASSIGN") or self.consumir("SUB_ASSIGN"):
            return
        self.erro("Esperado operador de atribuição (=, *=, /=, %=, += ou -=)")

    # <expr> → <exprAnd> <exprOr>
    def expr(self):
        self.expr_and()
        self.expr_or()

    # <exprList> → <expr> <exprListTail> | ε
    def expr_list(self):
        # Se o token atual pode iniciar uma expressão, processa; senão, ε é permitido.
        if self.token_atual and self.token_atual.type in ("ID", "NUM", "LITERAL", "LPAREN", "PLUS", "MINUS"):
            self.expr()
            self.expr_list_tail()
        # ε permitido

    # <exprListTail> → , <exprList> | ε
    def expr_list_tail(self):
        if self.consumir("COMMA"):
            self.expr_list()
        # ε permitido

    # <exprOr> → OR <exprAnd> <exprOr> | ε
    def expr_or(self):
        if self.consumir("OR_OP"):
            self.expr_and()
            self.expr_or()
        # ε permitido

    # <exprAnd> → <exprEqual> <exprAnd2>
    def expr_and(self):
        self.expr_equal()
        self.expr_and2()

    # <exprAnd2> → AND <exprEqual> <exprAnd2> | ε
    def expr_and2(self):
        if self.consumir("AND_OP"):
            self.expr_equal()
            self.expr_and2()
        # ε permitido

    # <exprEqual> → <exprRelational> <exprEqual2>
    def expr_equal(self):
        self.expr_relational()
        self.expr_equal2()

    # <exprEqual2> → == <exprRelational> <exprEqual2> | != <exprRelational> <exprEqual2> | ε
    def expr_equal2(self):
        if self.consumir("EQUAL"):
            self.expr_relational()
            self.expr_equal2()
            return
        if self.consumir("NOT_EQUAL"):
            self.expr_relational()
            self.expr_equal2()
            return
        # ε permitido

    # <exprRelational> → <exprPlus> <exprRelational2>
    def expr_relational(self):
        self.expr_plus()
        self.expr_relational2()

    # <exprRelational2> → < <exprPlus> <exprRelational2> | <= <exprPlus> <exprRelational2> | > <exprPlus> <exprRelational2> | >= <exprPlus> <exprRelational2> | ε
    def expr_relational2(self):
        if self.consumir("LESS_THEN"):
            self.expr_plus()
            self.expr_relational2()
            return
        if self.consumir("LESS_EQUAL"):
            self.expr_plus()
            self.expr_relational2()
            return
        if self.consumir("GREATER_THEN"):
            self.expr_plus()
            self.expr_relational2()
            return
        if self.consumir("GRATER_EQUAL"):
            self.expr_plus()
            self.expr_relational2()
            return
        # ε permitido

    # <exprPlus> → <exprMult> <exprPlus2>
    def expr_plus(self):
        self.expr_mult()
        self.expr_plus2()

    # <exprPlus2> → + <exprMult> <exprPlus2> | - <exprMult> <exprPlus2> | ε
    def expr_plus2(self):
        if self.consumir("PLUS"):
            self.expr_mult()
            self.expr_plus2()
            return
        if self.consumir("MINUS"):
            self.expr_mult()
            self.expr_plus2()
            return
        # ε permitido

    # <exprMult> → <exprUnary> <exprMult2>
    def expr_mult(self):
        self.expr_unary()
        self.expr_mult2()

    # <exprMult2> → * <exprUnary> <exprMult2> | / <exprUnary> <exprMult2> | ε
    def expr_mult2(self):
        if self.consumir("MULT"):
            self.expr_unary()
            self.expr_mult2()
            return
        if self.consumir("DIV"):
            self.expr_unary()
            self.expr_mult2()
            return
        # ε permitido

    # <exprUnary> → + <exprParenthesis> | - <exprParenthesis> | <exprParenthesis>
    def expr_unary(self):
        if self.consumir("PLUS"):
            self.expr_parenthesis()
            return
        if self.consumir("MINUS"):
            self.expr_parenthesis()
            return
        # Como não permite vazio, <exprParenthesis> deve ocorrer
        self.expr_parenthesis()

    # <exprParenthesis> → ( <expr> ) | <primary>
    def expr_parenthesis(self):
        if self.consumir("LPAREN"):
            self.expr()
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após expressão entre parênteses")
            return
        self.primary()

    # <primary> → ID <primaryID> | NUM | LITERAL
    def primary(self):
        if self.consumir("ID"):
            self.primary_id()
            return
        if self.consumir("NUM"):
            return
        if self.consumir("LITERAL"):
            return
        self.erro("Esperado uma expressão primária (ID, NUM ou LITERAL)")

    # <primaryID> → [ <primary> ] | ( <exprList> ) | ε
    def primary_id(self):
        if self.consumir("LBRACKET"):
            self.primary()
            if not self.consumir("RBRACKET"):
                self.erro("Esperado ']' após primary em primary_id")
            return
        if self.consumir("LPAREN"):
            self.expr_list()
            if not self.consumir("RPAREN"):
                self.erro("Esperado ')' após exprList em primary_id")
            return
        # ε permitido
