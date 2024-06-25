import os
import pyautogui
import time
import pyperclip
import sys
import keyboard
from clicar_recursos import clicar_pagina_x_usuarios
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import messagebox

# Configurações para o Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste o caminho conforme necessário

diretorio_atual = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
IMAGEM_PATH = os.path.join(diretorio_atual, "imagens")
primeira_vez = True
pause = False

def verificar_imagem(image_name):
    image_path = os.path.join(IMAGEM_PATH, image_name)
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Arquivo de imagem {image_path} não encontrado.")
    return image_path

def localizar_imagem(image_name, confidence=0.7):
    image_path = verificar_imagem(image_name)
    positions = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
    if positions:
        return pyautogui.center(positions[0])
    else:
        raise Exception(f"Imagem {image_path} não encontrada na tela.")

def ler_texto_da_imagem(imagem):
    try:
        return pytesseract.image_to_string(imagem)
    except Exception as e:
        print(f"Erro ao tentar ler texto da imagem: {e}")
        return ""

def toggle_pause():
    global pause
    pause = not pause
    if pause:
        print("Automação pausada. Pressione 'p' novamente para continuar.")
    else:
        print("Automação retomada.")

keyboard.add_hotkey('p', toggle_pause)

def tirar_screenshot(left, top, width, height):
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    #screenshot.show()
    return screenshot

# Função para verificar se o texto está na sugestão
def verificar_sugestao(texto, left, top, width, height):
    screenshot = tirar_screenshot(left, top, width, height)
    texto_screenshot = ler_texto_da_imagem(screenshot)
    return texto.lower() in texto_screenshot.lower()

# Exceção personalizada para quando o nome não é encontrado na sugestão após várias tentativas
class NomeNaoEncontradoException(Exception):
    pass

class ParametroNaoEncontradoException(Exception):
    pass

def escrever_texto(texto, press_tab=True, is_nome=False, is_parametro=False):
    global pause
    while pause:
        time.sleep(0.1)
    
    pyperclip.copy(texto)
    pyautogui.hotkey('ctrl', 'v')
    if not texto.isdigit() and texto.lower() != "estudo de custo versão2":
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        time.sleep(0.3)
        pyautogui.typewrite(texto[-2])
        if texto.lower() not in ["contratos", "estudo de custo versão 2", "gerente"]:
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(0.2)
    
    # Verifica se é o campo 'Nome' para tratar a sugestão
    if is_nome:
        # Coordenadas da região da sugestão
        sugestao_left = 450
        sugestao_top = 548
        sugestao_width = 351
        sugestao_height = 51

        tentativas = 0
        max_tentativas = 5  # Número máximo de tentativas

        # Verifica se o nome está na sugestão
        while tentativas < max_tentativas:
            if verificar_sugestao(texto, sugestao_left, sugestao_top, sugestao_width, sugestao_height):
                print(f"Sugestão encontrada: {texto}")
                break
            else:
                tentativas += 1
                print(f"Nome '{texto}' não encontrado na sugestão após tentativa {tentativas}.")
                
                # Tenta corrigir o nome
                pyautogui.hotkey('ctrl', 'a')  # Seleciona todo o texto
                pyautogui.hotkey('ctrl', 'v')  # Cola o texto novamente
                time.sleep(0.5)  # Espera a sugestão aparecer
                pyautogui.press('backspace')  # Apaga uma letra do final
                #pyautogui.typewrite(texto[-2])  # Escreve a última letra novamente
                time.sleep(0.5)  # Espera um pouco para a sugestão aparecer novamente

        if tentativas >= max_tentativas:
            raise NomeNaoEncontradoException(f"Limite de tentativas alcançado. Nome '{texto}' não encontrado na sugestão.")

    # Verifica se é o campo 'Parâmetro' para tratar a sugestão
    if is_parametro:
        # Coordenadas da região da sugestão
        sugestao_left = 450
        sugestao_top = 648
        sugestao_width = 351
        sugestao_height = 51

        tentativas = 0
        max_tentativas = 5  # Número máximo de tentativas

        # Verifica se o parâmetro está na sugestão
        while tentativas < max_tentativas:
            if verificar_sugestao(texto, sugestao_left, sugestao_top, sugestao_width, sugestao_height):
                print(f"Sugestão encontrada: {texto}")
                break
            else:
                tentativas += 1
                print(f"Parâmetro '{texto}' não encontrado na sugestão após tentativa {tentativas}.")
                
                # Tenta corrigir o parâmetro
                pyautogui.hotkey('ctrl', 'a')  # Seleciona todo o texto
                pyautogui.hotkey('ctrl', 'v')  # Cola o texto novamente
                time.sleep(0.5)  # Espera a sugestão aparecer
                pyautogui.press('tab')
                #pyautogui.press('backspace')  # Apaga uma letra do final
                #pyautogui.typewrite(texto[-2])  # Escreve a última letra novamente
                time.sleep(0.5)  # Espera um pouco para a sugestão aparecer novamente
                

        if tentativas >= max_tentativas:
            raise ParametroNaoEncontradoException(f"Limite de tentativas alcançado. Parâmetro '{texto}' não encontrado na sugestão.")

    if press_tab:
        if texto.lower() in ["contratos", "estudo de custo versão 2", "gerente"]:
            pyautogui.press('enter')
            pyautogui.press('tab')
        else:
            pyautogui.press('down')
            pyautogui.press('enter')
            time.sleep(0)
            pyautogui.press('tab')

def executar_automacao(nome, sistema, nome_campo, parametro):
    global primeira_vez
    
    while pause:
        time.sleep(0.1)  # Espera enquanto está pausado
    
    botao_inserir_pos = localizar_imagem("botao_inserir.png")
    pyautogui.click(botao_inserir_pos)
    print('Clicado no botão "Inserir".')
    time.sleep(2.5 if primeira_vez else 0.3)

    campo_nome_pos = localizar_imagem("nome.png")
    pyautogui.click(campo_nome_pos)
    print(f'Campo "Nome" clicado em posição: {campo_nome_pos}')

    try:
        escrever_texto(nome, is_nome=True)
    except NomeNaoEncontradoException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", str(e))
        root.destroy()
        return
    
    print(f'Nome "{nome}" escrito no campo "Nome".')
    time.sleep(1)  # Aguarda a sugestão aparecer

    escrever_texto(sistema, press_tab=False)
    print(f'Sistema "{sistema}" escrito no campo "Sistema".')
    pyautogui.press('tab')
    time.sleep(0)

    escrever_texto(nome_campo)
    print(f'Nome do Campo "{nome_campo}" escrito no campo "Nome do Campo".')
    time.sleep(0)

    try:
        escrever_texto(parametro, is_parametro=True)
    except ParametroNaoEncontradoException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", str(e))
        root.destroy()
        return

    print(f'Parâmetro "{parametro}" escrito no campo "Parâmetro".')
    time.sleep(0)

    if sistema.lower() in ["contratos", "estudo de custo versão 2"]:
        tipo_acesso = "CORD"
    else:
        tipo_acesso = "USER"

    escrever_texto(tipo_acesso, press_tab=False)
    print(f'Tipo de Acesso preenchido com "{tipo_acesso}".')
    time.sleep(0)
    pyautogui.press('tab')
    time.sleep(0)
    pyautogui.press('enter')
    print('Tecla "Tab" e "Enter" pressionadas após preencher o tipo de acesso.')

    primeira_vez = False

def salvar_no_final(nome="", sistemas=[]):
    try:
        while pause:
            time.sleep(0.1)
        
        botao_salvar_pos = localizar_imagem("salvar.png")
        pyautogui.click(botao_salvar_pos)
        print('Clicado no botão "Salvar".')
        time.sleep(2)
        pyautogui.press('enter')
        print('Pressionado Enter após clicar no botão "Salvar".')
        time.sleep(2)

        with open("log_de_acesso.txt", "a") as log_file:
            log_file.write(f"Nome: {nome}\n")
            log_file.write("Sistemas:\n")
            for sistema in sistemas:
                log_file.write(f" - {sistema}\n")
            log_file.write("\n")
        print('Informações de acesso salvas no log_de_acesso.txt.')
    except Exception as e:
        print(f"Erro ao tentar salvar no final: {e}")
