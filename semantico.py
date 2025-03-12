

# Variável global para armazenar o arquivo de saídA
output_file = None


def init_semantico():
    """
    Inicializa o gerador de código semântico, criando o arquivo `main.c`
    e escrevendo a estrutura básica de um programa em C.
    """
    global output_file
    output_file = open("main.c", "w", encoding="utf-8")

    # Escreve a inclusão da biblioteca padrão de entrada e saída
    output_file.write("#include <stdio.h>\n\n")

    # Inicia a função principal do programa
    output_file.write("int main(void) {\n")


def declaration_action(typ, ident, expr):
    """
    Gera uma linha de código para a declaração de uma variável em C.

    Parâmetros:
    - typ: Tipo da variável (ex: int, float, char).
    - ident: Nome do identificador da variável.
    - expr: Valor inicial da variável.
    """
    global output_file
    output_file.write(f"    {typ} {ident} = {expr};\n")

def struct_action(struct_name, members):
    """
    Registra a definição de uma struct e seus membros.
    """
    print(f"Definição de struct: {struct_name}")
    for member in members:
        if len(member) == 2:
            print(f"  - {member[0]} {member[1]};")  # Tipo e nome do membro
        elif len(member) == 3:
            print(f"  - {member[0]} {member[1]}[{member[2]}];")  # Vetor na struct

def function_action(return_type, func_name, params):
    """
    Registra a definição de uma função.
    """
    print(f"Definição da função: {return_type} {func_name}({', '.join(f'{t} {n}' for t, n in params)})")


def expression_action(expr):
    """
    Gera uma linha de código para uma expressão genérica em C.

    Parâmetros:
    - expr: Expressão a ser escrita (ex: "x = x + 1").
    """
    global output_file
    output_file.write(f"    {expr};\n")


def return_action(expr):
    """
    Gera uma instrução de retorno para a função main.

    Parâmetros:
    - expr: Expressão de retorno (ex: "0" para indicar sucesso).
    """
    global output_file
    output_file.write(f"    return {expr};\n")


def end_semantico():
    """
    Finaliza a escrita do programa em C, fechando as chaves e o arquivo.
    """
    global output_file
    output_file.write("}\n")  # Fecha a função main
    output_file.close()