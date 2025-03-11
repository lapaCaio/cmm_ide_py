import tkinter as tk
from tkinter import scrolledtext
import os
import io
import sys
import analisador
import re

# Cores do tema Dracula
BG_COLOR = "#282a36"
FG_COLOR = "#f8f8f2"
TEXT_BG = "#44475a"
TEXT_FG = "#f8f8f2"
BUTTON_BG = "#6272a4"
BUTTON_FG = "#f8f8f2"
RESERVED_COLOR = "#ff79c6"  # Rosa para palavras-chave
NUMBER_COLOR = "#bd93f9"    # Roxo para números
FUNCTION_COLOR = "#50fa7b"   # Verde para funções

# Expressões regulares para identificação
tokens_regex = {
    "RESERVED": re.compile(r"\b(int|return|void|main)\b"),
    "NUMBER": re.compile(r"\b\d+\b"),
    "FUNCTION": re.compile(r"\b[a-zA-Z_][a-zA-Z_0-9]*\s*(?=\()")
}

def highlight_syntax(event=None):
    editor_text.tag_remove("keyword", "1.0", tk.END)
    editor_text.tag_remove("number", "1.0", tk.END)
    editor_text.tag_remove("function", "1.0", tk.END)

    # Palavras reservadas em rosa
    keywords = r"\b(int|float|double|char|bool|short|long|return|void|main|struct|if|else|switch)\b"
    # Diretivas do pré-processador em laranja
    preprocessor = r"\#include"
    # Números em roxo
    numbers = r"\b\d+\b"
    # Funções (identificadores seguidos de '()') em verde
    functions = r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*(?=\()"

    apply_highlight(keywords, "keyword", "#ff79c6")  # Rosa
    apply_highlight(preprocessor, "preprocessor", "#ffb86c")  # Laranja
    apply_highlight(numbers, "number", "#bd93f9")    # Roxo
    apply_highlight(functions, "function", "#50fa7b")  # Verde


def apply_highlight(pattern, tag, color):
    editor_text.tag_configure(tag, foreground=color)
    text_content = editor_text.get("1.0", tk.END)
    for match in re.finditer(pattern, text_content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        editor_text.tag_add(tag, start, end)


def compilar():
    codigo = editor_text.get("1.0", tk.END)
    with open("main.c", "w", encoding="utf-8") as f:
        f.write(codigo)
    output_text.delete("1.0", tk.END)

    buffer = io.StringIO()
    stdout_old = sys.stdout
    sys.stdout = buffer
    try:
        analisador.sintatico()
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        sys.stdout = stdout_old

    resultado = buffer.getvalue()
    if os.path.exists("main.c"):
        with open("main.c", "r", encoding="utf-8") as f:
            resultado += "\n" + f.read()
    else:
        resultado += "\nArquivo 'main.c' não foi gerado."
    output_text.insert(tk.END, resultado)

# Configuração da interface
janela = tk.Tk()
janela.title("CMM IDE - Caio Lapa, Kaio Stefan, Gustavo Provete, Vinicin")
janela.configure(bg=BG_COLOR)

label_editor = tk.Label(janela, text="Text View", bg=BG_COLOR, fg=FG_COLOR)
label_editor.pack(padx=5, pady=5)

editor_text = scrolledtext.ScrolledText(janela, width=80, height=20, bg=TEXT_BG, fg=TEXT_FG, insertbackground=FG_COLOR, undo=True)
editor_text.pack(padx=5, pady=5)

# Configuração das cores das tags
define_tags = {
    "RESERVED": RESERVED_COLOR,
    "NUMBER": NUMBER_COLOR,
    "FUNCTION": FUNCTION_COLOR
}
for tag, color in define_tags.items():
    editor_text.tag_configure(tag, foreground=color)

editor_text.bind("<KeyRelease>", highlight_syntax)

botao_compilar = tk.Button(janela, text="Compilar", command=compilar, bg=BUTTON_BG, fg=BUTTON_FG)
botao_compilar.pack(padx=5, pady=10)

label_saida = tk.Label(janela, text="Console", bg=BG_COLOR, fg=FG_COLOR)
label_saida.pack(padx=5, pady=5)

output_text = scrolledtext.ScrolledText(janela, width=80, height=20, bg=TEXT_BG, fg=TEXT_FG, insertbackground=FG_COLOR)
output_text.pack(padx=5, pady=5)

janela.mainloop()
