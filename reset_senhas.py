import pyautogui
import time
import os
import pandas as pd
import pyperclip
from tkinter import filedialog
import tkinter as tk
from tkinter import filedialog, messagebox

# Caminhos das imagens
IMAGEM_LOGIN_PATH = "D:\\estudo\\regradeacesso\\imagens\\login.png"
IMAGEM_SENHA_PATH = "D:\\estudo\\regradeacesso\\imagens\\senha.png"

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
                pyautogui.click(localizacao.x + offset[0], localizacao.y + offset[1])
                print(f"Clicou na imagem {imagem} em {localizacao} com offset {offset}")
                return True  # Retorna True se clicou na imagem
        except Exception as e:
            print(f"Erro ao procurar a imagem: {e}")

        if time.time() - start_time > timeout:
            print(f"Não foi possível encontrar a imagem {imagem} dentro do tempo limite.")
            break

        time.sleep(1)
    return False  # Retorna False se não encontrou a imagem dentro do tempo limite

def preencher_campo_login_excel(login):
    pyperclip.copy(login)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.7)

def processar_logins():
    global DF
    if not EXCEL_PATH:
        print("Por favor, selecione um arquivo Excel primeiro.")
        return

    DF = pd.read_excel(EXCEL_PATH)

    if not DF.empty:
        # Clicar na imagem login.png na primeira vez com offset (0, 30)
        clicou_login = clicar_na_imagem(IMAGEM_LOGIN_PATH, offset=(0, 20))
        time.sleep(0.4)
        preencher_campo_login_excel(DF.iloc[0]['Login'])

        for index, row in DF.iterrows():
            login = row['Login']

            if index > 0:  # Pular a primeira iteração, pois já processamos o primeiro login
                # Clicar na imagem senha.png
                clicou_senha = clicar_na_imagem(IMAGEM_SENHA_PATH)
                time.sleep(0.4)

                if not clicou_senha:
                    print("Não foi possível clicar na imagem de senha. Encerrando o processo.")
                    break

                # Pressionar shift + tab 12 vezes
                pyautogui.keyDown('shift')
                for _ in range(12):
                    pyautogui.press('tab')
                pyautogui.keyUp('shift')

                # Digitar o login
                preencher_campo_login_excel(login)

            # Atualizar status no DataFrame
            DF.at[index, 'Status'] = 'ok'
            DF.to_excel(EXCEL_PATH, index=False)
            print(f"Processado login {login}")

        # Clicar na imagem de senha após o último login
        clicar_na_imagem(IMAGEM_SENHA_PATH)
        print("Último login processado. Clicou na imagem de senha.")
        messagebox.showinfo("Último Login", "Todos os logins foram processados com sucesso.")


def selecionar_arquivo():
    global EXCEL_PATH
    EXCEL_PATH = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if EXCEL_PATH:
        print(f"Arquivo Excel selecionado: {EXCEL_PATH}")
        processar_logins()

imagem_login_completa = verificar_imagem(IMAGEM_LOGIN_PATH)
imagem_senha_completa = verificar_imagem(IMAGEM_SENHA_PATH)

