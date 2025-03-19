class Semantico:
    def __init__(self, tokens, log_callback):
        self.tokens = tokens
        self.log_callback = log_callback
        self.tabela_simbolos = {}  # Armazena as variáveis e seus tipos

    def log_erro(self, mensagem):
        self.log_callback(mensagem)

    def analisar(self):
        variaveis_inicializadas = set()

        for i, token in enumerate(self.tokens):
            if token.type in ("INT", "CHAR", "FLOAT"):  # Declaração de variável
                identificador = self.tokens[i + 1] if i + 1 < len(self.tokens) else None
                if identificador and identificador.type == "ID":
                    self.tabela_simbolos[identificador.value] = token.type
                else:
                    self.log_erro(f"Erro: Nome de variável ausente após {token.type}.")

            elif token.type == "ID":  # Verificação de uso da variável
                if token.value not in self.tabela_simbolos:
                    self.log_erro(f"Erro: Variável '{token.value}' usada sem declaração.")
                elif token.value not in variaveis_inicializadas:
                    self.log_erro(f"Aviso: Variável '{token.value}' pode não estar inicializada.")

            elif token.type == "ATRIBUICAO":  # Verificação de tipo em atribuições
                identificador = self.tokens[i - 1] if i > 0 else None
                valor = self.tokens[i + 1] if i + 1 < len(self.tokens) else None

                if identificador and identificador.type == "IDENTIFICADOR":
                    if identificador.value in self.tabela_simbolos:
                        tipo_var = self.tabela_simbolos[identificador.value]
                        tipo_valor = valor.type if valor else None

                        if tipo_valor and tipo_var != tipo_valor:
                            self.log_erro(
                                f"Erro: Incompatibilidade de tipos na atribuição de '{identificador.value}'. Esperado {tipo_var}, encontrado {tipo_valor}.")
                        else:
                            variaveis_inicializadas.add(identificador.value)
                    else:
                        self.log_erro(f"Erro: Variável '{identificador.value}' não declarada antes da atribuição.")

            elif token.type == "OP":  # Operações entre tipos incompatíveis
                op1 = self.tokens[i - 1] if i > 0 else None
                op2 = self.tokens[i + 1] if i + 1 < len(self.tokens) else None

                if op1 and op2 and op1.type in self.tabela_simbolos and op2.type in self.tabela_simbolos:
                    tipo1 = self.tabela_simbolos[op1.value]
                    tipo2 = self.tabela_simbolos[op2.value]
                    if tipo1 != tipo2:
                        self.log_erro(f"Erro: Operação entre tipos incompatíveis: {tipo1} e {tipo2}.")

        return "Análise semântica concluída com sucesso!"
