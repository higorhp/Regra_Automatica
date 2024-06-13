import pyautogui
import time
import os
import pandas as pd
import pyperclip
from tkinter import filedialog
import tkinter as tk
import sys

# Obtém o diretório onde o executável está sendo executado
diretorio_atual = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
IMAGEM_PATH = os.path.join(diretorio_atual, "imagens")

# Caminhos das imagens
IMAGEM_LOGIN_PATH = os.path.join(IMAGEM_PATH, "login.png")
IMAGEM_MATRICULA_PATH = os.path.join(IMAGEM_PATH, "matricula.png")
IMAGEM_SENHA_PATH = os.path.join(IMAGEM_PATH, "senha.png")
IMAGEM_CARREGANDO_PATH = os.path.join(IMAGEM_PATH, "carregando.png")

EXCEL_PATH = ""
DF = pd.DataFrame()

def verificar_imagem(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Arquivo de imagem {image_path} não encontrado.")
    return image_path

def clicar_na_imagem(imagem, timeout=30, offset=(0, 0)):
    start_time = time.time()
    while True:
        try:
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)
            if localizacao is not None:
                localizacao = (localizacao[0] + offset[0], localizacao[1] + offset[1])
                pyautogui.click(localizacao)
                print(f"Clicou na imagem {imagem} em {localizacao} com offset {offset}")
                return localizacao  # Retorna a localização se clicou na imagem
        except Exception as e:
            print(f"Erro ao procurar a imagem: {e}")

        if time.time() - start_time > timeout:
            print(f"Não foi possível encontrar a imagem {imagem} dentro do tempo limite.")
            return None  # Retorna None se não encontrou a imagem dentro do tempo limite
        
        time.sleep(1)

def esperar_imagem_desaparecer(imagem):
    print(f"Aguardando a imagem {imagem} desaparecer...")
    while True:
        try:
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)
            if localizacao is None:
                print(f"A imagem {imagem} desapareceu.")
                return
        except pyautogui.ImageNotFoundException:
            print(f"A imagem {imagem} desapareceu.")
            return
        except Exception as e:
            print(f"Erro ao verificar a imagem: {e}")

        time.sleep(1)

def preencher_campo_login_excel(login):
    pyperclip.copy(login)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.7)

def processar_logins_matri():
    global DF
    if not EXCEL_PATH:
        print("Por favor, selecione um arquivo Excel primeiro.")
        return

    DF = pd.read_excel(EXCEL_PATH)

    if not DF.empty:
        # Clicar na imagem login.png na primeira vez com deslocamento (0, 30) e digitar o primeiro login
        clicou_login = clicar_na_imagem(IMAGEM_LOGIN_PATH, offset=(0, 10))
        time.sleep(0.4)
        preencher_campo_login_excel(DF.iloc[0]['Login'])

        for index, row in DF.iterrows():
            login = row['Login']
            matricula = row['Matricula']

            if index > 0:  # Pular a primeira iteração, pois já processamos o primeiro login
                # Digitar o login
                preencher_campo_login_excel(login)
                time.sleep(1.4)

            # Clicar na imagem matricula.png com deslocamento
            clicou_matricula = clicar_na_imagem(IMAGEM_MATRICULA_PATH, offset=(0, 40))
            if not clicou_matricula:
                print("Não foi possível clicar na imagem de matrícula. Encerrando o processo.")
                break
            pyautogui.doubleClick(clicou_matricula)
            time.sleep(0.3)
            # Digitar a matrícula do usuário
            pyperclip.copy(matricula)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

            # Clicar na imagem senha.png
            clicou_senha = clicar_na_imagem(IMAGEM_SENHA_PATH)
            if not clicou_senha:
                print("Não foi possível clicar na imagem de senha. Encerrando o processo.")
                break
            time.sleep(0.5)  # Pequeno atraso antes de clicar novamente

            # Clicar um pouco à esquerda da imagem de senha
            pyautogui.click(clicou_senha[0] - 16, clicou_senha[1])
            print(f"Clicou um pouco à esquerda da imagem de senha em {clicou_senha[0] - 16, clicou_senha[1]}")

            time.sleep(0.7)
            # Esperar a imagem carregando.png desaparecer
            esperar_imagem_desaparecer(IMAGEM_CARREGANDO_PATH)

            pyautogui.keyDown('shift')
            for _ in range(12):
                pyautogui.press('tab')
            pyautogui.keyUp('shift')
                    
            # Atualizar status no DataFrame
            DF.at[index, 'Status'] = 'ok'
            DF.to_excel(EXCEL_PATH, index=False)
            print(f"Processado login {login}")

def selecionar_arquivo_matri():
    global EXCEL_PATH
    EXCEL_PATH = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if (EXCEL_PATH):
        print(f"Arquivo Excel selecionado: {EXCEL_PATH}")
        processar_logins_matri()

imagem_login_completa = verificar_imagem(IMAGEM_LOGIN_PATH)
imagem_matricula_completa = verificar_imagem(IMAGEM_MATRICULA_PATH)
imagem_senha_completa = verificar_imagem(IMAGEM_SENHA_PATH)
imagem_carregando_completa = verificar_imagem(IMAGEM_CARREGANDO_PATH)