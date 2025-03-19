import os.path

from customtkinter import *
from PIL import Image
import lexico
from sintatico import Sintatico

# Definição do esquema de cores do tema Drácula
DARK_BG = "#282a36"
LIGHT_BG = "#44475a"
TEXT_COLOR = "#f8f8f2"
ACCENT_COLOR = "#bd93f9"

# Configuração da janela principal
app = CTk()
app.geometry("1200x700")
app.resizable(False, False)  # 🔒 Impede o redimensionamento
app.title("CMM IDE - Caio, Kaio, Gustavo, Vinicius")
app.iconbitmap("assets\cmm_logo.ico")  # Substitua pelo caminho do seu arquivo .ico

set_appearance_mode("dark")  # Mantemos no modo escuro base

# Função para imprimir mensagens na telinha de log
def log_message(texto):
    log_textbox.configure(state="normal")  # Desbloqueia edição temporariamente
    log_textbox.insert("end", texto + "\n")  # Adiciona a nova linha ao log
    log_textbox.see("end")  # Rola automaticamente para a última linha
    log_textbox.configure(state="disabled")  # Bloqueia novamente

# Função para capturar saída do terminal e exibir no log
def click_handler():
    # Limpa o log antes de processar o novo código
    log_textbox.configure(state="normal")
    log_textbox.delete("1.0", "end")
    log_textbox.configure(state="disabled")

    code = textbox.get("0.0", "end").strip()
    if not code:
        log_message("Nenhum código para compilar.")
        return

    try:
        tokens = lexico.tokenize(code)
    except SyntaxError as e:
        log_message(f"SyntaxError: {str(e)}")
        return  # Certifique-se de retornar aqui, caso ocorra um erro

    parser = Sintatico(tokens, log_message)
    try:
        resultado = parser.analisar()
        log_message(resultado)
    except SyntaxError as e:
        log_message(f"SyntaxError: {str(e)}")


# Frame do código ocupa 60% da altura
frame_code = CTkFrame(master=app, fg_color=DARK_BG, border_width=2)
frame_code.pack(side="top", fill="both", expand=True)

# Frame inferior que contém log e botões (40% da altura)
frame_bottom = CTkFrame(master=app, fg_color=LIGHT_BG)
frame_bottom.pack(side="bottom", fill="both", expand=True)
frame_bottom.pack_propagate(False)

# Frame do log ocupa 70% da largura inferior
frame_log = CTkFrame(master=frame_bottom, fg_color=DARK_BG, border_width=1)
frame_log.pack(side="left", fill="both", expand=True)
frame_log.pack_propagate(False)

# Adicionando a caixa de texto do log (não editável) com fonte Fira Code
log_textbox = CTkTextbox(master=frame_log, state="disabled", fg_color=LIGHT_BG,
                         text_color=TEXT_COLOR, font=("Fira Code", 12))
log_textbox.pack(fill="both", expand=True, padx=10, pady=10)

# Frame do botão ocupa 30% da largura inferior
frame_btn = CTkFrame(master=frame_bottom, fg_color=DARK_BG, border_width=1)
frame_btn.pack(side="right", fill="both")
frame_btn.pack_propagate(False)

# Criando dois subframes dentro de frame_btn
frame_btn_top = CTkFrame(master=frame_btn, fg_color=DARK_BG)
frame_btn_top.pack(side="top", fill="both", expand=True)

frame_btn_bottom = CTkFrame(master=frame_btn, fg_color=DARK_BG)
frame_btn_bottom.pack(side="bottom", fill="both", expand=True)

# Aumentando o tamanho do ícone
img = CTkImage(dark_image=Image.open("assets/run_code_icon.png"), size=(32, 32))  # Ícone maior

# Adicionando o botão de compilar (centralizado verticalmente) com fonte Fira Code
btn = CTkButton(master=frame_btn_top, text="Compilar", corner_radius=6, height=50,
                fg_color=ACCENT_COLOR, text_color=TEXT_COLOR,
                font=("Fira Code", 14, "bold"),
                image=img, command=click_handler)
btn.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado verticalmente

# Adicionando uma imagem no frame inferior
img_display = CTkImage(dark_image=Image.open("assets/cmm_logo.png"), size=(64, 64))
img_label = CTkLabel(master=frame_btn_bottom, image=img_display, text="")
img_label.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado

# Campo de texto com fonte Fira Code
textbox = CTkTextbox(master=frame_code, fg_color=LIGHT_BG, text_color=TEXT_COLOR,
                     font=("Fira Code", 14))
textbox.pack(fill="both", expand=True, pady=10, padx=10)

# app.mainloop()
