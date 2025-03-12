import tkinter as tk
from tkinter import scrolledtext
import os
import io
import sys
import analisador
import re

# Definição das cores do tema Dracula
BG_COLOR = "#282a36"  # Cor de fundo
FG_COLOR = "#f8f8f2"  # Cor do texto
TEXT_BG = "#44475a"  # Fundo do editor
TEXT_FG = "#f8f8f2"  # Texto do editor
BUTTON_BG = "#6272a4"  # Fundo do botão
BUTTON_FG = "#f8f8f2"  # Texto do botão

# Cores para realce de sintaxe
RESERVED_COLOR = "#ff79c6"  # Rosa para palavras-chave
NUMBER_COLOR = "#bd93f9"  # Roxo para números
FUNCTION_COLOR = "#50fa7b"  # Verde para funções

# Expressões regulares para identificação de tokens
highlight_patterns = {
    "keyword": (r"\b(int|float|double|char|bool|short|long|return|void|main|struct|if|else|switch)\b", "#ff79c6"),
    # Rosa
    "preprocessor": (r"\#include", "#ffb86c"),  # Laranja
    "number": (r"\b\d+\b", "#bd93f9"),  # Roxo
    "function": (r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*(?=\()", "#50fa7b")  # Verde
}


def highlight_syntax(event=None):
    """Aplica realce de sintaxe ao código fonte."""
    for tag in highlight_patterns:
        editor_text.tag_remove(tag, "1.0", tk.END)

    for tag, (pattern, color) in highlight_patterns.items():
        apply_highlight(pattern, tag, color)


def apply_highlight(pattern, tag, color):
    """Aplica um padrão de realce ao texto no editor."""
    editor_text.tag_configure(tag, foreground=color)
    text_content = editor_text.get("1.0", tk.END)
    for match in re.finditer(pattern, text_content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        editor_text.tag_add(tag, start, end)


def compilar():
    """Compila o código e exibe o resultado no console."""
    codigo = editor_text.get("1.0", tk.END)

    # Salva o código em um arquivo
    with open("main.c", "w", encoding="utf-8") as f:
        f.write(codigo)

    # Limpa o console
    output_text.delete("1.0", tk.END)

    # Redireciona a saída para capturar a execução do analisador
    buffer = io.StringIO()
    stdout_old = sys.stdout
    sys.stdout = buffer
    try:
        analisador.sintatico()
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        sys.stdout = stdout_old

    # Exibe o resultado da compilação
    resultado = buffer.getvalue()
    if os.path.exists("main.c"):
        with open("main.c", "r", encoding="utf-8") as f:
            resultado += "\n" + f.read()
    else:
        resultado += "\nArquivo 'main.c' não foi gerado."
    output_text.insert(tk.END, resultado)


# Configuração da interface gráfica
janela = tk.Tk()
janela.title("CMM IDE - Caio Lapa, Kaio Stefan, Gustavo Provete, Vinicin")
janela.configure(bg=BG_COLOR)

# Editor de código
label_editor = tk.Label(janela, text="Text View", bg=BG_COLOR, fg=FG_COLOR)
label_editor.pack(padx=5, pady=5)

editor_text = scrolledtext.ScrolledText(janela, width=80, height=20, bg=TEXT_BG, fg=TEXT_FG, insertbackground=FG_COLOR,
                                        undo=True)
editor_text.pack(padx=5, pady=5)

# Configuração das cores das tags para realce de sintaxe
for tag, (_, color) in highlight_patterns.items():
    editor_text.tag_configure(tag, foreground=color)

# Adiciona o evento de realce ao digitar
editor_text.bind("<KeyRelease>", highlight_syntax)

# Botão de compilação
botao_compilar = tk.Button(janela, text="Compilar", command=compilar, bg=BUTTON_BG, fg=BUTTON_FG)
botao_compilar.pack(padx=5, pady=10)

# Área de saída do console
label_saida = tk.Label(janela, text="Console", bg=BG_COLOR, fg=FG_COLOR)
label_saida.pack(padx=5, pady=5)

output_text = scrolledtext.ScrolledText(janela, width=80, height=20, bg=TEXT_BG, fg=TEXT_FG, insertbackground=FG_COLOR)
output_text.pack(padx=5, pady=5)

# Inicia a aplicação
janela.mainloop()