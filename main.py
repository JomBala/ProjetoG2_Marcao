# --- Importações ---
import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
import json
import sys
import math


# --- Inicialização do Pygame e Variáveis Globais ---
pygame.init()
# inicializarBancoDeDados()

# Configurações da tela e relógio
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Paper Run: Konan Edition")
relogio = pygame.time.Clock()

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
ciano_claro = (170, 210, 220)
ciano_konan = (210,239,246)
azul_escuro = (8,39,76)
cor_botao = (28, 63, 90)
AZUL_CHUVA = (100, 110, 140)
COR_PLAYER = (150, 150, 255) # Placeholder para Konan
COR_INIMIGO = (255, 100, 0)   # Placeholder para Obito
COR_PROJETIL = (255, 50, 0)    # Placeholder para Bola de Fogo 

# --- Carregamento de Assets (Imagens, Fontes, Sons) ---
try:
    # Ícone
    icone = pygame.image.load("Recursos/assets/icone.png")
    pygame.display.set_icon(icone)
    
    # Imagens de Fundo
    fundoStart = pygame.image.load("Recursos/assets/fundoStart.png")
    fundoJogo = pygame.image.load("Recursos/assets/fundoJogo.png")
    fundoInstrucoes = pygame.image.load("Recursos/assets/instrucoes.png")
    fundoDead = pygame.image.load("Recursos/assets/fundoDead.png")
    
    # Sprites
    passaro = pygame.image.load("Recursos/assets/konan.gif")
    
    
    # Sons e Música
    pygame.mixer.init() 
    instrucoes_sound = pygame.mixer.Sound("Recursos/assets/instrucoes.mp3")
    entrada_sound = pygame.mixer.Sound("Recursos/assets/entradasound.mp3")
    
    
    # Fontes
    fonteTexto = pygame.font.Font("Recursos/assets/Audiowide-Regular.ttf", 16)
    fonteMenu = pygame.font.Font("Recursos/assets/roguehero.ttf", 20)
    fonteMenuMaior = pygame.font.Font("Recursos/assets/roguehero.ttf", 35)

except Exception as e:
    print(f"Erro ao carregar um ou mais assets: {e}")
    pygame.quit()
    sys.exit()

# --- Funções de Cada Tela do Jogo ---

def start():
    """Função da tela de menu inicial."""
    pygame.mixer.music.stop() 
    entrada_sound.play() # Toca o som de entrada do menu
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundoStart, (0, 0))

        # Definição dos retângulos dos botões
        botao_iniciar_rect = pygame.Rect(150, 320, 150, 40)
        botao_sair_rect = pygame.Rect(150, 390, 150, 40)
        
        # Desenha os botões
        pygame.draw.rect(tela, branco, botao_iniciar_rect, border_radius=15)
        startTexto = fonteTexto.render("INICIAR GAME", True, azul_escuro)
        tela.blit(startTexto, startTexto.get_rect(center=botao_iniciar_rect.center))

        pygame.draw.rect(tela, branco, botao_sair_rect, border_radius=15)
        quitTexto = fonteTexto.render("SAIR DO GAME", True, azul_escuro)
        tela.blit(quitTexto, quitTexto.get_rect(center=botao_sair_rect.center))
        
        # Lógica de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar_rect.collidepoint(mouse_pos):
                    entrada_sound.stop()
                    pedir_nome_e_avancar()
                if botao_sair_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        relogio.tick(60)

def pedir_nome_e_avancar():
    """Função que Avança para a tela de instruções."""

    nome_coletado = None
    
    root = tk.Tk()
    root.title("Informe seu Nome")
    root.withdraw()

    largura_janela = 300
    altura_janela = 120
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.deiconify()
    
    def obter_nome():
        nonlocal nome_coletado
        nome_coletado = entry_nome.get().strip()
        if not nome_coletado:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    label = tk.Label(root, text="Digite seu nome para continuar:")
    label.pack(pady=10)
    entry_nome = tk.Entry(root)
    entry_nome.pack(pady=5)
    botao = tk.Button(root, text="Confirmar", command=obter_nome)
    botao.pack(pady=10)
    
    root.mainloop()

    if nome_coletado:
        tela_boas_vindas(nome_coletado)
    else:
        print("Coleta de nome cancelada.")
        start() # Volta para o menu inicial

def tela_boas_vindas(nome_jogador):
    """Função que mostra a tela de instruções e boas-vindas."""

    pygame.mixer.music.stop()  # Garante que a música de outras telas pare
    instrucoes_sound.play()  # Toca o som de entrada do menu

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundoInstrucoes, (0, 0))

        # Movendo os textos um pouco mais para baixo
        deslocamento = 80  # Ajuste para abaixar tudo

        texto_bem_vindo = fonteMenuMaior.render("Bem-vindo", True, ciano_konan)
        rect_bem_vindo = texto_bem_vindo.get_rect(center=(tela.get_width() // 2, tela.get_height() // 3 + deslocamento))

        texto_nome = fonteMenuMaior.render(f"{nome_jogador}", True, ciano_konan)
        rect_nome = texto_nome.get_rect(center=(tela.get_width() // 2, rect_bem_vindo.bottom + 15))

        instrucao1 = fonteMenu.render("Use as setas para desviar dos mísseis", True, ciano_konan)
        rect_instrucao1 = instrucao1.get_rect(center=(tela.get_width() // 2, rect_nome.bottom + 30))

        instrucao2 = fonteMenu.render("Pressione ESPAÇO para pausar o jogo", True, ciano_konan)
        rect_instrucao2 = instrucao2.get_rect(center=(tela.get_width() // 2, rect_instrucao1.bottom + 30))

        # Desenhando textos na tela
        tela.blit(texto_bem_vindo, rect_bem_vindo)
        tela.blit(texto_nome, rect_nome)
        tela.blit(instrucao1, rect_instrucao1)
        tela.blit(instrucao2, rect_instrucao2)

        # Movendo o botão para abaixo dos textos
        botao_iniciar_rect = pygame.Rect(0, 0, 200, 50)
        botao_iniciar_rect.center = (tela.get_width() // 2, rect_instrucao2.bottom + 40)
        pygame.draw.rect(tela, cor_botao, botao_iniciar_rect, border_radius=10)

        texto_botao = fonteMenu.render("Iniciar Jogo", True, ciano_konan)
        tela.blit(texto_botao, texto_botao.get_rect(center=botao_iniciar_rect.center))

        # Lógica de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar_rect.collidepoint(mouse_pos):
                    loop_principal_do_jogo(nome_jogador)
                    return

        pygame.display.update()
        relogio.tick(60)


