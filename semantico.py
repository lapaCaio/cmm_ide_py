output_file = None

def init_semantico():
    global output_file
    output_file = open("main.c", "w", encoding="utf-8")
    # Escreve o cabeçalho básico do programa C
    output_file.write("#include <stdio.h>\n\n")
    output_file.write("int main(void) {\n")

def declaration_action(typ, ident, expr):
    global output_file
    # Gera uma declaração de variável
    output_file.write(f"    {typ} {ident} = {expr};\n")

def expression_action(expr):
    global output_file
    # Gera uma expressão (por exemplo, pode ser uma atribuição ou cálculo)
    output_file.write(f"    {expr};\n")

def return_action(expr):
    global output_file
    output_file.write(f"    return {expr};\n")

def end_semantico():
    global output_file
    output_file.write("}\n")
    output_file.close()
