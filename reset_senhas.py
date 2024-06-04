import pyautogui
import time
import os
import pandas as pd
import pyperclip
from tkinter import filedialog
import tkinter as tk

# Caminhos das imagens
IMAGEM_LOGIN_PATH = "D:\\estudo\\regradeacesso\\imagens\\login.png"
IMAGEM_SENHA_PATH = "D:\\estudo\\regradeacesso\\imagens\\senha.png"

EXCEL_PATH = ""
DF = pd.DataFrame()

def verificar_imagem(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Arquivo de imagem {image_path} não encontrado.")
    return image_path

def clicar_na_imagem(imagem, timeout=30):
    start_time = time.time()
    while True:
        try:
            localizacao = pyautogui.locateCenterOnScreen(imagem, confidence=0.8)
            if localizacao is not None:
                pyautogui.click(localizacao)
                print(f"Clicou na imagem {imagem} em {localizacao}")
                break
        except Exception as e:
            print(f"Erro ao procurar a imagem: {e}")

        if time.time() - start_time > timeout:
            print(f"Não foi possível encontrar a imagem {imagem} dentro do tempo limite.")
            break
        
        time.sleep(1)

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
        # Clicar na imagem login.png na primeira vez e digitar o primeiro login
        clicar_na_imagem(IMAGEM_LOGIN_PATH)
        time.sleep(0.4)
        preencher_campo_login_excel(DF.iloc[0]['Login'])
        
        for index, row in DF.iterrows():
            login = row['Login']
            
            if index > 0:  # Pular a primeira iteração, pois já processamos o primeiro login
                # Clicar na imagem senha.png
                clicar_na_imagem(IMAGEM_SENHA_PATH)
                time.sleep(0.4)

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

def selecionar_arquivo():
    global EXCEL_PATH
    EXCEL_PATH = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if EXCEL_PATH:
        print(f"Arquivo Excel selecionado: {EXCEL_PATH}")
        processar_logins()

imagem_login_completa = verificar_imagem(IMAGEM_LOGIN_PATH)
imagem_senha_completa = verificar_imagem(IMAGEM_SENHA_PATH)

root = tk.Tk()
root.title("Selecionar Arquivo Excel")

selecionar_button = tk.Button(root, text="Selecionar Arquivo Excel", command=selecionar_arquivo)
selecionar_button.pack(pady=20)

root.mainloop()
