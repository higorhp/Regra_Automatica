import os
import pyautogui
import time
import sys

diretorio_atual = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
IMAGEM_PATH = os.path.join(diretorio_atual, "imagens")

def verificar_imagem(image_name):
    image_path = os.path.join(IMAGEM_PATH, image_name)
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Arquivo de imagem {image_path} não encontrado.")
    return image_path

def localizar_imagem(image_name, confidence=0.7):
    image_path = verificar_imagem(image_name)
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if location is not None:
        return location
    else:
        raise Exception(f"Imagem {image_path} não encontrada na tela.")

SISTEMA_IMAGENS_SCROLL = {
    "MOVIMENTAÇÃO RECURSOS HUMANOS": ("mrh.png", 0),
    "ANUAL": ("anual.png", 0),
    "ESTUDO DE CUSTO": ("estudo.png", 0),
    "CONTROLE POLICIA FEDERAL": ("federal.png", 0),
    "TELEFONIA": ("telefonia.png", -300),
    "OCORRENCIA": ("ocorrencia.png", -700),
    "PONTO WEB": ("ponto.png", -900),
    "REVISÃO": ("revisao.png", -900),
    "CONTRATOS": ("contratos.png", -900),
    "SISTEMA DE DOCUMENTOS": ("documentos.png", -1200),
    "SISTEMA DE BENEFÍCIOS": ("beneficios.png", -1850),
    "ALTERAÇÃO CR": ("alteracao.png", -1850),
    "EXPORTACAO": ("exportacao.png", -1900),
    "VR": ("vr.png", -2200),
    "VT": ("vt.png", -2300),
    "AO": ("ao.png", -2400),
    "ADIMISSAO": ("admissao.png", -23550),
    "RESCISAO": ("rescisao.png", -23550),
    "FERIAS": ("ferias.png", -23550),
}

def clicar_pagina_x_usuarios(nome, sistemas):
    try:
        # Clica na imagem da página
        pagina_x_usuarios_pos = localizar_imagem("pagina.png", confidence=0.8)
        pyautogui.click(pagina_x_usuarios_pos)
        print('Clicado na imagem "Pagina X Usuários".')

        time.sleep(1)

        # Clica na imagem "Usuário"
        usuario_pos = localizar_imagem("usuario.png", confidence=0.8)
        pyautogui.tripleClick(usuario_pos.x + 75,usuario_pos.y)
        print('Clicado na imagem "Usuário".')
        time.sleep(0.2)

        # Escreve o nome do usuário
        nome = nome.strip()
        pyautogui.typewrite(nome)
        print(f'Nome "{nome}" escrito.')
        time.sleep(0.5)
        pyautogui.press('tab')
        print(f'Nome "{nome}" escrito e tecla "Tab" pressionada.')
        time.sleep(0.3)

        
        # Realiza o scroll para sistemas diferentes de "EXPORTACAO"
        for sistema in sistemas:
            imagem_scroll = SISTEMA_IMAGENS_SCROLL.get(sistema.upper())
            if imagem_scroll:
                if isinstance(imagem_scroll, tuple):
                    imagem, scroll = imagem_scroll
                else:
                    imagem = imagem_scroll
                    scroll = 0

                if scroll != 0:
                    pyautogui.scroll(scroll)
                    print(f'Scroll de {scroll} realizado para o sistema "{sistema}".')
                    time.sleep(1)

                imagem_pos = localizar_imagem(imagem, confidence=0.7)
                pyautogui.click(imagem_pos)
                print(f'Clicado na imagem "{imagem}".')
                pyautogui.press('down')
                time.sleep(0.5)
                
                # Define a imagem a ser clicada com base no sistema
                if sistema.upper() == "PONTO WEB":
                    imagem_para_clicar = "LEIT.png"
                elif sistema.upper() in ["CONTRATOS", "ESTUDO DE CUSTO"]:
                    imagem_para_clicar = "CORD.png"
                elif sistema.upper() == "TELEFONIA":
                    imagem_para_clicar = "GER.png"
                else:
                    imagem_para_clicar = "USER.png"
                    time.sleep(0.5)

                # Localiza e clica na imagem específica
                imagem_para_clicar_pos = localizar_imagem(imagem_para_clicar, confidence=0.8)
                pyautogui.click(imagem_para_clicar_pos)
                print(f'Clicado na imagem "{imagem_para_clicar}".')

                # Realiza um scroll de 1000 após encontrar a imagem do sistema
                pyautogui.scroll(2000)
                print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
                time.sleep(0.3)

                # Vinculação de "REVISÃO" com "ANUAL"
                if sistema.upper() == "REVISÃO":
                    imagem_pos = localizar_imagem(SISTEMA_IMAGENS_SCROLL["ANUAL"][0], confidence=0.8)
                    pyautogui.click(imagem_pos)
                    print(f'Clicado na imagem "{SISTEMA_IMAGENS_SCROLL["ANUAL"][0]}".')
                    pyautogui.press('down')
                    time.sleep(0.5)
                    
                    # Localiza e clica na imagem específica
                    imagem_para_clicar_pos = localizar_imagem("USER.png", confidence=0.8)
                    pyautogui.click(imagem_para_clicar_pos)
                    print('Clicado na imagem "USER.png".')
                    time.sleep(0.2)

                # Vinculação de "CONTRATOS" com "ESTUDO DE CUSTO"
                if sistema.upper() == "CONTRATOS":
                    imagem_pos = localizar_imagem(SISTEMA_IMAGENS_SCROLL["ESTUDO DE CUSTO"][0], confidence=0.8)
                    pyautogui.click(imagem_pos)
                    print(f'Clicado na imagem "{SISTEMA_IMAGENS_SCROLL["ESTUDO DE CUSTO"][0]}".')
                    pyautogui.press('down')
                    time.sleep(0.5)
                    
                    # Localiza e clica na imagem específica
                    imagem_para_clicar_pos = localizar_imagem("CORD.png", confidence=0.8)
                    pyautogui.click(imagem_para_clicar_pos)
                    print('Clicado na imagem "CORD.png".')
                    time.sleep(0.2)

    except Exception as e:
        print(f"Erro ao tentar clicar na imagem 'Pagina X Usuários': {e}")

def clicar_vr():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("VR")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "VR".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 30,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(3000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para VR, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em VR: {e}")

def clicar_vt():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("VT")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "VT".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 45,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(3000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para VT, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em VT: {e}")

def clicar_ao():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("AO")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "AO".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 40,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(3000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para AO, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em AO: {e}")


def clicar_fer():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("FERIAS")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "VR".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 30,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(70000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para VR, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em VR: {e}")

def clicar_resci():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("RESCISAO")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "VT".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 45,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(70000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para VT, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em VT: {e}")

def clicar_admissa():
    try:
        imagem_scroll = SISTEMA_IMAGENS_SCROLL.get("ADIMISSAO")
        if imagem_scroll:
            imagem, scroll = imagem_scroll
            if scroll != 0:
                pyautogui.scroll(scroll)
                print(f'Scroll de {scroll} realizado para o sistema "AO".')
                time.sleep(1)

            imagem_pos = localizar_imagem(imagem, confidence=0.7)
            pyautogui.doubleClick(imagem_pos.x - 40,imagem_pos.y)
            print(f'Clicado na imagem "{imagem}".')
            pyautogui.press('down')
            time.sleep(0.5)

            # Realiza um scroll de 1000 após encontrar a imagem do sistema
            pyautogui.scroll(70000)
            print('Scroll de 1000 realizado após encontrar a imagem do sistema.')
            time.sleep(0.3)
            
            # Aqui você pode adicionar lógica adicional específica para AO, se necessário

    except Exception as e:
        print(f"Erro ao tentar clicar em AO: {e}")


