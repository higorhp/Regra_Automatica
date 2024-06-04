import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import pyautogui
import time
import pyperclip
import sys

# Importe suas funções específicas para automação
from automacao_acesso import executar_automacao, salvar_no_final, clicar_pagina_x_usuarios

IMAGEM_PATH = "C:\\Users\\higor.pacheco\\Desktop\\estudo\\regradeacesso_2\\imagens"
primeira_vez = True
nome_entry_ref = None  # Referência para o Entry onde o usuário digita o nome

# Função auxiliar para redirecionar o print
class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()  # Atualiza a interface gráfica


    def flush(self):
        pass


def iniciar_automacao():
    nomes = nome_entry.get().split(",")
    sistemas = [sistemas_listbox.get(i) for i in sistemas_listbox.curselection()]
    total_usuarios = len(nomes)
    total_sistemas = len(sistemas)
    
    for i, nome in enumerate(nomes):
        nome = nome.strip()
        for j, sistema in enumerate(sistemas):
            sistema = sistema.strip()
            executar_automacao(nome, sistema, nome_campo_combobox.get(), parametro_entry.get())
            if sistema == "PONTO WEB":
                executar_automacao(nome, "OPERCIONAL", nome_campo_combobox.get(), parametro_entry.get())
            if sistema == "CONTRATOS":
                executar_automacao(nome, "ESTUDO DE CUSTO VERSÃO 2", nome_campo_combobox.get(), parametro_entry.get())
            if sistema == "REVISÃO":
                executar_automacao(nome, "ANUAL", nome_campo_combobox.get(), parametro_entry.get())
            
            if salvar_var.get() == 1 and i == total_usuarios - 1 and j == total_sistemas - 1:
                salvar_no_final(nome, sistemas)
    
    if pagina_var.get() == 1:
        ultimo_nome = nomes[-1].strip() if nomes else ""
        clicar_pagina_x_usuarios(ultimo_nome, sistemas)

def importar_usuarios():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if filepath:
        df = pd.read_excel(filepath)
        required_columns = {"Nome", "Nome do Campo", "Parâmetro"}
        systems_columns = set(df.columns) - required_columns
        
        if not required_columns.issubset(df.columns):
            messagebox.showerror("Erro", "A planilha deve conter os cabeçalhos: Nome, Nome do Campo, Parâmetro e os sistemas.")
            return

        total_usuarios = len(df)
        for index, row in df.iterrows():
            nome = row["Nome"]
            nome_campo = row["Nome do Campo"]
            parametro = row["Parâmetro"]
            sistemas = []

            for sistema in systems_columns:
                if pd.notna(row[sistema]) and row[sistema].strip().lower() == 'x':
                    sistemas.append(sistema)
                    executar_automacao(nome, sistema, nome_campo, parametro)
                    if sistema == "PONTO WEB":
                        executar_automacao(nome, "OPERCIONAL", nome_campo, parametro)
                    if sistema == "CONTRATOS":
                        executar_automacao(nome, "ESTUDO DE CUSTO VERSÃO 2", nome_campo, parametro)
                    if sistema == "REVISÃO":
                        executar_automacao(nome, "ANUAL", nome_campo, parametro)

            if salvar_var.get() == 1 and index == total_usuarios - 1:
                salvar_no_final(nome, sistemas)
                
        if pagina_var.get() == 1:
            ultimo_nome = df["Nome"].iloc[-1].strip() if not df.empty else ""
            clicar_pagina_x_usuarios(ultimo_nome, sistemas)

def mostrar_mensagem_formato():
    messagebox.showinfo("Formato da Planilha", "A planilha deve conter os seguintes cabeçalhos: Nome, Nome do Campo, Parâmetro e os sistemas como colunas.")

def iniciar_reset_senhas():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if filepath:
        df = pd.read_excel(filepath)
        if 'Login' not in df.columns or 'Status' not in df.columns:
            messagebox.showerror("Erro", "A planilha deve conter os cabeçalhos: Login e Status.")
            return

        # Sua lógica de reset de senhas vai aqui
        for index, row in df.iterrows():
            login = row["Login"]
            status = row["Status"]
            if status.lower() != 'ok':
                # Adicione aqui a lógica para reset de senhas
                # Exemplo: resetar_senha(login)
                print(f"Reseting password for {login}")
                # Marcar como 'ok' após o reset
                df.at[index, 'Status'] = 'ok'
        
        # Salvar o arquivo atualizado
        df.to_excel(filepath, index=False)
        messagebox.showinfo("Sucesso", "Reset de senhas concluído e status atualizado.")

def abrir_janela_log():
    janela_log = tk.Toplevel(root)
    janela_log.title("Log")
    janela_log.geometry("600x400")
    janela_log.configure(bg="#add8e6")

    log_text = tk.Text(janela_log, height=20, width=80)
    log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Redireciona a saída padrão (print) para o widget de texto na nova janela
    sys.stdout = PrintRedirector(log_text)

    # Adiciona um botão para fechar a janela de log
    tk.Button(janela_log, text="Fechar", command=janela_log.destroy, bg="#FF6347", fg="white", font=("Roboto", 10, "bold")).pack(pady=10)

root = tk.Tk()
root.title("Regra de acesso automática")
root.configure(bg="#add8e6")
root.geometry("420x460")
root.resizable(False, False)  # Isso impede que a janela seja redimensionada

entry_width = 32

# Estilo para o Notebook
style = ttk.Style()
style.configure('TNotebook.Tab', background="#6495ED", padding=[50, 1])
style.map('TNotebook.Tab', background=[('selected', '#add8e6')])
style.configure('TNotebook', tabposition='n') 

# Cria o Notebook (abas)
notebook = ttk.Notebook(root, style='TNotebook')
notebook.pack(padx=0, pady=0, fill='both', expand=True)

# Cria o frame para a aba de Regra de Acesso
frame_regra_acesso = tk.Frame(notebook, bg="#add8e6")
notebook.add(frame_regra_acesso, text="Regra de Acesso")

# Cria o frame para a aba de Reset de Senhas
frame_reset_senhas = tk.Frame(notebook, bg="#add8e6")
notebook.add(frame_reset_senhas, text="Reset de Senhas")

# Centraliza os widgets da aba de Regra de Acesso
titulo_janela = tk.Label(frame_regra_acesso, text="Regra de Acesso Automática", bg="#add8e6", fg="black", font=("Roboto", 16, "bold"))
titulo_janela.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

tk.Label(frame_regra_acesso, text="Nome do Colaborador:", bg="#add8e6", fg="black", font=("Roboto", 10, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="e")
nome_entry = tk.Entry(frame_regra_acesso, font=("Roboto", 10, "bold"), fg="black", width=entry_width)
nome_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame_regra_acesso, text="Nome do Campo:", bg="#add8e6", fg="black", font=("Roboto", 10, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
nome_campo_combobox = ttk.Combobox(frame_regra_acesso, values=["SUPERVISOR", "GERENTE", "GERENTE REGIONAL", "DIRETOR", "DIRETOR EXECUTIVO", "EMPRESA M&A"], width=34)
nome_campo_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
nome_campo_combobox.current(0)

tk.Label(frame_regra_acesso, text="Parâmetro:", bg="#add8e6", fg="black", font=("Roboto", 10, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="e")
parametro_entry = tk.Entry(frame_regra_acesso, font=("Roboto", 10, "bold"), fg="black", width=entry_width)
parametro_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(frame_regra_acesso, text="Sistema(s):", bg="#add8e6", fg="black", font=("Roboto", 10, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="e")
sistemas_listbox = tk.Listbox(frame_regra_acesso, selectmode=tk.MULTIPLE, width=entry_width + 5, height=4)
sistemas_listbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Adicionar sistemas à listbox
sistemas = ["MOVIMENTAÇÃO RECURSOS HUMANOS", "CONTROLE POLICIA FEDERAL", "TELEFONIA", "OCORRENCIA","PONTO WEB","REVISÃO", "CONTRATOS", "SISTEMA DE DOCUMENTOS", "SISTEMA DE BENEFÍCIOS", "EXPORTACAO", "GPS 360"]
for sistema in sistemas:
    sistemas_listbox.insert(tk.END, sistema)

# Botão para iniciar a automação
iniciar_button = tk.Button(frame_regra_acesso, text="Iniciar Automação", command=iniciar_automacao, bg="#008000", fg="white", font=("Roboto", 10, "bold"))
iniciar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Botão para importar usuários do Excel
importar_button = tk.Button(frame_regra_acesso, text="Importar Usuários", command=importar_usuarios, bg="#000080", fg="white", font=("Roboto", 10, "bold"))
importar_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Checkbutton para salvar no final
salvar_var = tk.IntVar()
salvar_checkbutton = tk.Checkbutton(frame_regra_acesso, text="Salvar Regras", variable=salvar_var, bg="#add8e6", fg="black", font=("Roboto", 10, "bold"))
salvar_checkbutton.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Checkbutton para executar clicar_pagina_x_usuarios
pagina_var = tk.IntVar()
pagina_checkbutton = tk.Checkbutton(frame_regra_acesso, text="Pagina x Usuários", variable=pagina_var, bg="#add8e6", fg="black", font=("Roboto", 10, "bold"))
pagina_checkbutton.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Botão para mostrar o formato da planilha
formato_button = tk.Button(frame_regra_acesso, text="Formato da Planilha", command=mostrar_mensagem_formato, bg="#FFD700", fg="black", font=("Roboto", 10, "bold"))
formato_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Adicionando botão de Log
tk.Button(frame_regra_acesso, text="Log", command=abrir_janela_log, bg="#FF6347", fg="white", font=("Roboto", 10, "bold")).grid(row=8, column=1, padx=10, pady=5, sticky="e")

# Adiciona o texto centralizado na aba de Reset de Senhas
label_texto_reset = tk.Label(frame_reset_senhas, text="Reset de Senhas", bg="#add8e6", fg="black", font=("Roboto", 16, "bold"))
label_texto_reset.grid(row=0, column=0, columnspan=2, padx=(130, 100), pady=5, sticky="n")

iniciar_reset_button = tk.Button(frame_reset_senhas, text="Iniciar Reset de Senhas", command=iniciar_reset_senhas, bg="#008000", fg="white", font=("Roboto", 10, "bold"))
iniciar_reset_button.grid(row=1, column=0, columnspan=2, padx=(130, 100), pady=5, sticky="ew")

# Adiciona o texto informando sobre as colunas necessárias na aba de Reset de Senhas
mensagem_reset = """
Certifique-se de que a planilha contenha as seguintes colunas:
- Uma coluna para o Login
- Uma coluna para o Status

Exemplo:
Login | Status
"""
label_mensagem_reset = tk.Label(frame_reset_senhas, text=mensagem_reset, bg="#add8e6", fg="black", font=("Roboto", 10))
label_mensagem_reset.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=5, sticky="n")

root.mainloop()
