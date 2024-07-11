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
from reset_senhas import selecionar_arquivo, processar_logins
from matricula_senha import selecionar_arquivo_matri, processar_logins_matri
from clicar_recursos import clicar_vr,clicar_vt,clicar_ao, clicar_admissa,clicar_fer,clicar_resci,clicar_CRM,clicar_va,clicar_SRA



diretorio_atual = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
IMAGEM_PATH = os.path.join(diretorio_atual, "imagens")
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

    if va_var.get() == 1:
        clicar_va()

    if vr_var.get() == 1:
        clicar_vr()
    
    if vt_var.get() == 1:
        clicar_vt()

    if ao_var.get() == 1:
        clicar_ao()

    if  admissao_var.get() == 1:
        clicar_admissa()
    
    if rescisao_var.get() == 1:
        clicar_resci()

    if ferias_var.get() == 1:
        clicar_fer()
    
    if crm_var.get() == 1:
        clicar_CRM()

    if sra_var.get() ==1:
        clicar_SRA()
    

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
    processar_logins()
    selecionar_arquivo()

def iniciar_matricula_senhas():
    processar_logins_matri()
    selecionar_arquivo_matri()

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
root.geometry("590x500")
root.resizable(False, False)  # Isso impede que a janela seja redimensionada

entry_width = 32

# Frame para organizar os dois Notebooks
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Notebook à esquerda para "Página x Usuário"
style_left = ttk.Style()
style_left.configure('Left.TNotebook.Tab', background="#6495ED", padding=[5, 1])
style_left.map('Left.TNotebook.Tab', background=[('selected', '#add8e6')])

notebook_left = ttk.Notebook(main_frame, style='Left.TNotebook')
notebook_left.pack(side='left', fill='both', expand=True)

# Notebook para as outras abas
style_right = ttk.Style()
style_right.configure('Right.TNotebook.Tab', background="#6495ED", padding=[50, 1])
style_right.map('Right.TNotebook.Tab', background=[('selected', '#add8e6')])

notebook_right = ttk.Notebook(main_frame, style='Right.TNotebook')
notebook_right.pack(side='left', fill='both', expand=True)

# Cria o frame para a aba de Página x Usuário
frame_pagina_usuario = tk.Frame(notebook_left, bg="#add8e6")
notebook_left.add(frame_pagina_usuario, text="Página x Usuário")

# Cria os frames para as outras abas
frame_regra_acesso = tk.Frame(notebook_right, bg="#add8e6")
notebook_right.add(frame_regra_acesso, text="Regra de Acesso")

frame_reset_senhas = tk.Frame(notebook_right, bg="#add8e6")
notebook_right.add(frame_reset_senhas, text="Controle de Acesso")

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
sistemas = ["MOVIMENTAÇÃO RECURSOS HUMANOS", "CONTROLE POLICIA FEDERAL", "TELEFONIA", "OCORRENCIA","PONTO WEB","REVISÃO", "CONTRATOS", "SISTEMA DE DOCUMENTOS", "SISTEMA DE BENEFÍCIOS", "EXPORTACAO","ALTERAÇÃO CR", "GPS 360"]
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

# Checkbutton para executar clicar_pagina_x_usuario
pagina_var = tk.IntVar()
pagina_checkbutton = tk.Checkbutton(frame_regra_acesso, text="Pagina x Usuários", variable=pagina_var, bg="#add8e6", fg="black", font=("Roboto", 10, "bold"))
pagina_checkbutton.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Botão para mostrar o formato da planilha
formato_button = tk.Button(frame_regra_acesso, text="Formato da Planilha", command=mostrar_mensagem_formato, bg="#FFD700", fg="black", font=("Roboto", 10, "bold"))
formato_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Adicionando botão de Log
tk.Button(frame_regra_acesso, text="Log", command=abrir_janela_log, bg="#FF6347", fg="white", font=("Roboto", 10, "bold")).grid(row=8, column=1, padx=10, pady=5, sticky="e")

##################### Página x Usuário opções ##############################
va_var = tk.IntVar()
vr_var = tk.IntVar()
vt_var = tk.IntVar()
ao_var = tk.IntVar()
ferias_var = tk.IntVar()
rescisao_var = tk.IntVar()
admissao_var = tk.IntVar()
crm_var = tk.IntVar()
sra_var = tk.IntVar()

label_pergunta = tk.Label(frame_pagina_usuario, text="Pastas:", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
label_pergunta.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

#Benefícios

label_beneficios = tk.Label(frame_pagina_usuario, text="Benefícios:", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
label_beneficios.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="n")

checkbox_va = tk.Checkbutton(frame_pagina_usuario, text="VA", variable=va_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_va.grid(row=2, column=1, padx=10, pady=5, sticky="w")

checkbox_vr = tk.Checkbutton(frame_pagina_usuario, text="VR", variable=vr_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_vr.grid(row=2, column=0, padx=10, pady=5, sticky="w")

checkbox_vt = tk.Checkbutton(frame_pagina_usuario, text="VT", variable=vt_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_vt.grid(row=3, column=0, padx=10, pady=5, sticky="w")

checkbox_ao = tk.Checkbutton(frame_pagina_usuario, text="AO", variable=ao_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_ao.grid(row=3, column=1, padx=10, pady=5, sticky="w")

#MRH

label_mrh = tk.Label(frame_pagina_usuario, text="MRH:", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
label_mrh.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="n")

checkbox_admissa = tk.Checkbutton(frame_pagina_usuario, text="Admissão", variable=admissao_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_admissa.grid(row=6, column=0, padx=10, pady=5, sticky="w")

checkbox_res = tk.Checkbutton(frame_pagina_usuario, text="Rescisão", variable=rescisao_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_res.grid(row=7, column=0, padx=10, pady=5, sticky="w")

checkbox_fer = tk.Checkbutton(frame_pagina_usuario, text="Férias", variable=ferias_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_fer.grid(row=8, column=0, padx=10, pady=5, sticky="w")

#CRM
label_crm = tk.Label(frame_pagina_usuario, text="Ocorrência:", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
label_crm.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="n")

checkbox_crm = tk.Checkbutton(frame_pagina_usuario, text="CRM", variable=crm_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_crm.grid(row=10, column=0, padx=10, pady=5, sticky="w")


#SRA
label_sra = tk.Label(frame_pagina_usuario, text="Exportação:", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
label_sra.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="n")

checkbox_sra = tk.Checkbutton(frame_pagina_usuario, text="SRA", variable=sra_var, bg="#add8e6", fg="black", font=("Roboto", 9, "bold"))
checkbox_sra.grid(row=12, column=0, padx=10, pady=5, sticky="w")


######################################################################################################

# Variável para armazenar a escolha do usuário
escolha_var = tk.StringVar(value="")

# Adiciona o texto centralizado na aba de Reset de Senhas
label_pergunta = tk.Label(frame_reset_senhas, text="O que você deseja fazer?", bg="#add8e6", fg="black", font=("Roboto", 14, "bold"))
label_pergunta.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

radio_reset_senhas = tk.Radiobutton(frame_reset_senhas, text="Reset de senhas", variable=escolha_var, value="reset_senhas", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
radio_reset_senhas.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

radio_matricula_senhas = tk.Radiobutton(frame_reset_senhas, text="Reset e Matrículas", variable=escolha_var, value="matricula_senhas", bg="#add8e6", fg="black", font=("Roboto", 12, "bold"))
radio_matricula_senhas.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Função para executar a ação baseada na escolha do usuário
def executar_acao():
    escolha = escolha_var.get()
    if escolha == "reset_senhas":
        iniciar_reset_senhas()
    elif escolha == "matricula_senhas":
        iniciar_matricula_senhas()
    else:
        messagebox.showwarning("Aviso", "Por favor, selecione uma opção antes de executar.")

botao_executar = tk.Button(frame_reset_senhas, text="Selecionar arquivo e executar", command=executar_acao, bg="#008000", fg="white", font=("Roboto", 12, "bold"))
botao_executar.grid(row=3, column=0, columnspan=2, padx=10, pady=20, sticky="n")

# Adiciona o texto informando sobre as colunas necessárias na aba de Reset de Senhas
mensagem_reset = """
Certifique-se de que a planilha contenha as seguintes colunas:
- Uma coluna para o Login
- Uma coluna para o Status

Exemplo:
Login | Status
"""

mensagem_reset2 = """
Antes de executar o programa, 
certifique-se de arrastar os ícones de senha e 
disquete para a esquerda, dentro do portal.
"""

label_mensagem_reset = tk.Label(frame_reset_senhas, text=mensagem_reset, bg="#add8e6", fg="purple", font=("Roboto", 10, "bold"))
label_mensagem_reset.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=5, sticky="n")

label_mensagem_reset = tk.Label(frame_reset_senhas, text=mensagem_reset2, bg="#add8e6", fg="red", font=("Roboto", 12, "bold"))
label_mensagem_reset.grid(row=5, column=0, columnspan=2, padx=(20, 20), pady=5, sticky="n")


root.mainloop()