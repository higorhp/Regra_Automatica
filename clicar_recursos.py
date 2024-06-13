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
    "OCORRENCIA": ("ocorrencia.png", -300),
    "PONTO WEB": "ponto.png",
    "SISTEMA DE DOCUMENTOS": ("documentos.png", -800),
    "CONTRATOS": ("contratos.png", -800),
    "REVISÃO": ("revisao.png", -800),
    "SISTEMA DE BENEFÍCIOS": ("beneficios.png", -900),
    "EXPORTACAO": ("exportacao.png", -1750),
}

def clicar_pagina_x_usuarios(nome, sistemas):
    try:
        # Clica na imagem da página
        pagina_x_usuarios_pos = localizar_imagem("pagina.png", confidence=0.8)
        if pagina_x_usuarios_pos:
            pyautogui.click(pagina_x_usuarios_pos)
            print('Clicado na imagem "Pagina X Usuários".')
        else:
            print('Imagem "Pagina X Usuários" não encontrada.')
            return

        time.sleep(1)

        # Clica na imagem "Usuário"
        usuario_pos = localizar_imagem("usuario.png", confidence=0.8)
        if usuario_pos:
            pyautogui.click(usuario_pos)
            print('Clicado na imagem "Usuário".')
        else:
            print('Imagem "Usuário" não encontrada.')
            return

        # Escreve o nome do usuário
        nome = nome.strip()
        pyautogui.typewrite(nome)
        print(f'Nome "{nome}" escrito.')
        time.sleep(0.5)
        pyautogui.press('tab')
        print(f'Nome "{nome}" escrito e tecla "Tab" pressionada.')

        # Verifica se "EXPORTACAO" está na lista de sistemas
        exportacao_selecionado = "EXPORTACAO" in [sistema.upper() for sistema in sistemas]

        # Flag para controlar se o scroll de -1000 já foi realizado
        scroll_menos_mil_realizado = False

        # Realiza o scroll para sistemas diferentes de "EXPORTACAO"
        for sistema in sistemas:
            if sistema.upper() == "EXPORTACAO":
                continue
            imagem_scroll = SISTEMA_IMAGENS_SCROLL.get(sistema.upper())
            if imagem_scroll:
                if isinstance(imagem_scroll, tuple):
                    imagem, scroll = imagem_scroll
                else:
                    imagem = imagem_scroll
                    scroll = 0

                if scroll != 0:
                    if scroll == -800 and not scroll_menos_mil_realizado:
                        pyautogui.scroll(scroll)
                        print(f'Scroll de {scroll} realizado para o sistema "{sistema}".')
                        time.sleep(1)
                        scroll_menos_mil_realizado = True
                    elif scroll != -800:
                        pyautogui.scroll(scroll)
                        print(f'Scroll de {scroll} realizado para o sistema "{sistema}".')
                        time.sleep(1)

                imagem_pos = localizar_imagem(imagem, confidence=0.8)
                if imagem_pos:
                    pyautogui.click(imagem_pos)
                    print(f'Clicado na imagem "{imagem}".')
                    pyautogui.press('down')
                    time.sleep(0.5)
                    pyautogui.press('enter')
                    print(f'Tecla "Down" e "Enter" pressionadas após "{sistema}".')
                else:
                    print(f'Imagem "{imagem}" não encontrada para o sistema "{sistema}".')

                # Adiciona o scroll de 1000 após "REVISÃO"
                if sistema.upper() == "REVISÃO":
                    pyautogui.scroll(900)
                    print('Scroll de 1000 realizado após "REVISÃO".')
                    imagem_pos = localizar_imagem("anual.png", confidence=0.8)
                    if imagem_pos:
                        pyautogui.click(imagem_pos)
                        print('Clicado na imagem "anual.png".')
                        pyautogui.press('down')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        print('Tecla "Down" e "Enter" pressionadas após "ANUAL".')

                    # Adiciona o scroll de -1000 após "ANUAL"
                    pyautogui.scroll(-800)
                    print('Scroll de -1000 realizado após "ANUAL".')

                # Adiciona o scroll de 1000 após "CONTRATOS"
                if sistema.upper() == "CONTRATOS":
                    pyautogui.scroll(800)
                    print('Scroll de 1000 realizado após "CONTRATOS".')
                    imagem_pos = localizar_imagem("estudo.png", confidence=0.8)
                    if imagem_pos:
                        pyautogui.click(imagem_pos)
                        print('Clicado na imagem "estudo.png".')
                        pyautogui.press('down')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        print('Tecla "Down" e "Enter" pressionadas após "ESTUDO DE CUSTO".')

                    # Adiciona o scroll de -1000 após "ESTUDO DE CUSTO"
                    pyautogui.scroll(-800)
                    print('Scroll de -1000 realizado após "ESTUDO DE CUSTO".')

        # Realiza o scroll de -1750 se "EXPORTACAO" for o único sistema
        if exportacao_selecionado and len(sistemas) == 1:
            pyautogui.scroll(-1750)
            print(f'Scroll de -1750 realizado para o sistema "EXPORTACAO".')
            imagem_pos = localizar_imagem(SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0], confidence=0.8)
            if imagem_pos:
                pyautogui.click(imagem_pos)
                print(f'Clicado na imagem "{SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0]}".')
                pyautogui.press('down')
                time.sleep(0.5)
                pyautogui.press('enter')
                print(f'Tecla "Down" e "Enter" pressionadas após "EXPORTACAO".')
            else:
                print(f'Imagem "{SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0]}" não encontrada para o sistema "EXPORTACAO".')

        # Realiza um scroll adicional de -750 se "EXPORTACAO" estiver junto com outros sistemas
        elif exportacao_selecionado and len(sistemas) > 1:
            pyautogui.scroll(-100)
            print(f'Scroll adicional de -750 realizado para o sistema "EXPORTACAO".')
            time.sleep(1)
            imagem_pos = localizar_imagem(SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0], confidence=0.8)
            if imagem_pos:
                pyautogui.click(imagem_pos)
                print(f'Clicado na imagem "{SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0]}".')
                pyautogui.press('down')
                time.sleep(0.5)
                pyautogui.press('enter')
                print(f'Tecla "Down" e "Enter" pressionadas após "EXPORTACAO".')
            else:
                print(f'Imagem "{SISTEMA_IMAGENS_SCROLL["EXPORTACAO"][0]}" não encontrada para o sistema "EXPORTACAO".')

    except Exception as e:
        print(f"Erro ao tentar clicar na imagem 'Pagina X Usuários': {e}")
