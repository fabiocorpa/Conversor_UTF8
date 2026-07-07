import unicodedata
import tkinter as tk
from tkinter import ttk
from ftfy import fix_text


def remover_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def processar(event=None):
    texto = entrada.get("1.0", tk.END).strip()

    texto = fix_text(texto)

    if remover_var.get():
        texto = remover_acentos(texto)

    saida.delete("1.0", tk.END)
    saida.insert("1.0", texto)
    status_var.set("Texto processado.")


def copiar():
    texto = saida.get("1.0", tk.END).strip()
    janela.clipboard_clear()
    janela.clipboard_append(texto)
    status_var.set("Texto copiado.")


def colar():
    try:
        texto = janela.clipboard_get()
        entrada.delete("1.0", tk.END)
        entrada.insert("1.0", texto)
        status_var.set("Texto colado.")
    except tk.TclError:
        status_var.set("Área de transferência vazia.")


def limpar(event=None):
    entrada.delete("1.0", tk.END)
    saida.delete("1.0", tk.END)
    status_var.set("Campos limpos.")


def selecionar_saida(event=None):
    saida.tag_add("sel", "1.0", tk.END)
    return "break"


janela = tk.Tk()
janela.title("Conversor UTF-8")
janela.geometry("850x650")
janela.minsize(650, 500)

style = ttk.Style()
style.theme_use("clam")

main = ttk.Frame(janela, padding=12)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Texto original").pack(anchor="w")

entrada = tk.Text(main, height=10, wrap="word", undo=True)
entrada.pack(fill="both", expand=True, pady=(4, 10))

remover_var = tk.BooleanVar(value=True)

opcoes = ttk.Frame(main)
opcoes.pack(fill="x", pady=(0, 10))

ttk.Checkbutton(
    opcoes,
    text="Remover acentos e ç",
    variable=remover_var
).pack(side="left")

botoes = ttk.Frame(main)
botoes.pack(pady=6)

ttk.Button(botoes, text="Colar", command=colar).pack(side="left", padx=5)
ttk.Button(botoes, text="Processar", command=processar).pack(side="left", padx=5)
ttk.Button(botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

ttk.Label(main, text="Texto convertido").pack(anchor="w", pady=(10, 0))

saida = tk.Text(main, height=10, wrap="word", undo=True)
saida.pack(fill="both", expand=True, pady=(4, 10))

ttk.Button(main, text="Copiar texto convertido", command=copiar).pack(pady=5)

status_var = tk.StringVar(value="Pronto.")
ttk.Label(main, textvariable=status_var).pack(anchor="w", pady=(8, 0))

janela.bind("<Control-Return>", processar)
janela.bind("<Control-l>", limpar)
saida.bind("<Double-Button-1>", selecionar_saida)

janela.mainloop()
