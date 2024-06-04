import os
import pyautogui
import time
import pyperclip
from clicar_recursos import clicar_pagina_x_usuarios

IMAGEM_PATH = "D:\\estudo\\regradeacesso\\imagens"
primeira_vez = True

def verificar_imagem(image_name):
    image_path = os.path.join(IMAGEM_PATH, image_name)
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Arquivo de imagem {image_path} não encontrado.")
    return image_path

def localizar_imagem(image_name, confidence=0.7):
    image_path = verificar_imagem(image_name)
    positions = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
    if positions:
        # Retorna o centro da primeira posição encontrada
        return pyautogui.center(positions[0])
    else:
        raise Exception(f"Imagem {image_path} não encontrada na tela.")

def executar_automacao(nome, sistema, nome_campo, parametro):
    global primeira_vez
    
    botao_inserir_pos = localizar_imagem("botao_inserir.png")
    pyautogui.click(botao_inserir_pos)
    print('Clicado no botão "Inserir".')
    time.sleep(2.5 if primeira_vez else 0.3)

    def escrever_texto(texto, press_tab=True):
        pyperclip.copy(texto)
        pyautogui.hotkey('ctrl', 'v')
        if not texto.isdigit() and texto.lower() != "estudo de custo versão2":
            pyautogui.press('backspace')
            pyautogui.press('backspace')
            time.sleep(0.3)
            pyautogui.typewrite(texto[-2])
            if texto.lower() not in ["contratos", "estudo de custo versão 2"]:  # Verifica se o texto não é "CONTRATOS"
                pyautogui.press('down')
                time.sleep(0)
        if press_tab:
            if texto.lower() == ["contratos","ESTUDO DE CUSTO VERSÃO 2"]:
                pyautogui.press('enter')  # Se for "CONTRATOS", pressiona "enter"
            else:
                pyautogui.press('enter')  # Pressiona "tab" para outros textos
                time.sleep(0)
                pyautogui.press('tab')

    campo_nome_pos = localizar_imagem("nome.png")
    pyautogui.click(campo_nome_pos)
    escrever_texto(nome)
    print(f'Nome "{nome}" escrito no campo "Nome".')
    time.sleep(0)

    
    escrever_texto(sistema, press_tab=False)
    print(f'Sistema "{sistema}" escrito no campo "Sistema".')
    pyautogui.press('tab')
    time.sleep(0)

 

    escrever_texto(nome_campo)
    print(f'Nome do Campo "{nome_campo}" escrito no campo "Nome do Campo".')
    time.sleep(0)

    escrever_texto(parametro)
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
        botao_salvar_pos = localizar_imagem("salvar.png")
        pyautogui.click(botao_salvar_pos)
        print('Clicado no botão "Salvar".')
        time.sleep(2)  # Espera 2 segundos antes de pressionar Enter
        pyautogui.press('enter')  # Pressiona Enter após clicar em Salvar
        print('Pressionado Enter após clicar no botão "Salvar".')
        time.sleep(2)  # Espera mais 2 segundos para finalizar

        # Salva o nome do colaborador e os sistemas associados
        with open("log_de_acesso.txt", "a") as log_file:
            log_file.write(f"Nome: {nome}\n")
            log_file.write("Sistemas:\n")
            for sistema in sistemas:
                log_file.write(f" - {sistema}\n")
            log_file.write("\n")
        print('Informações de acesso salvas no log_de_acesso.txt.')
    except Exception as e:
        print(f"Erro ao tentar salvar no final: {e}")
