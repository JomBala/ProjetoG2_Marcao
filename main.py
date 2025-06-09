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
azul_escuro = (8,39,76)
roxo_botao = (149, 61, 158) # Cor roxa para o botão, sem transparência

# --- Carregamento de Assets (Imagens, Fontes, Sons) ---
try:
    # Ícone
    icone = pygame.image.load("Recursos/assets/icone.png")
    pygame.display.set_icon(icone)
    
    # Imagens de Fundo
    fundoStart = pygame.image.load("Recursos/assets/fundoStart.png")
    fundoJogo = pygame.image.load("Recursos/assets/fundoJogo.png")
    fundoInstrucoes = pygame.image.load("Recursos/assets/instrucoes.jpg")
    fundoDead = pygame.image.load("Recursos/assets/fundoDead.png")
    
    # Sprites
    iron = pygame.image.load("Recursos/assets/iron.png")
    passaro = pygame.image.load("Recursos/assets/konan.gif")
    missel = pygame.image.load("Recursos/assets/missile.png")
    
    # Sons e Música
    pygame.mixer.init() # Inicializa o mixer SÓ UMA VEZ
    entrada_sound = pygame.mixer.Sound("Recursos/assets/entradasound.mp3")
    pygame.mixer.music.load("Recursos/assets/ironsound.mp3")
    
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
    pygame.mixer.music.stop() # Garante que a música de outras telas pare
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
    """Função que usa Tkinter para pedir o nome e, se conseguir, avança para a tela de instruções."""
    nome_coletado = None
    
    root = tk.Tk()
    root.title("Informe seu Nickname")
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
    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundoInstrucoes, (0, 0))

        # Textos de boas-vindas e instruções
        texto_bem_vindo = fonteMenuMaior.render("Bem-vindo", True, preto)
        rect_bem_vindo = texto_bem_vindo.get_rect(center=(tela.get_width() // 2, 45))
        
        texto_nome = fonteMenuMaior.render(f"{nome_jogador}", True, preto)
        rect_nome = texto_nome.get_rect(centerx=rect_bem_vindo.centerx, top=rect_bem_vindo.bottom + 10)
        
        instrucao1 = fonteMenu.render("Use as setas para desviar dos mísseis", True, branco)
        rect_instrucao1 = instrucao1.get_rect(centerx=rect_nome.centerx, top=rect_nome.bottom + 29)

        instrucao2 = fonteMenu.render("Pressione ESPAÇO para pausar o jogo", True, branco)
        rect_instrucao2 = instrucao2.get_rect(centerx=rect_instrucao1.centerx, top=rect_instrucao1.bottom + 10)

        tela.blit(texto_bem_vindo, rect_bem_vindo)
        tela.blit(texto_nome, rect_nome)
        tela.blit(instrucao1, rect_instrucao1)
        tela.blit(instrucao2, rect_instrucao2)
        
        # Botão para iniciar o jogo
        botao_iniciar_rect = pygame.Rect(0, 0, 200, 50)
        botao_iniciar_rect.center = (tela.get_width() // 2, 245)
        pygame.draw.rect(tela, roxo_botao, botao_iniciar_rect, border_radius=10)
        
        texto_botao = fonteMenu.render("Iniciar Jogo", True, branco)
        tela.blit(texto_botao, texto_botao.get_rect(center=botao_iniciar_rect.center))
        
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

def loop_principal_do_jogo(nome_jogador):
    """Função onde o jogo de desviar dos mísseis acontece."""
    em_pausa = False
    posicaoXPersona = 500
    posicaoYPersona = 500
    movimentoXPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pontos = 0
    
    # Lógica de som do jogo
    pygame.mixer.music.play(-1) # Toca a música do jogo em loop
    
    while True:
        # Lógica de eventos do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Seus eventos de KEYDOWN e KEYUP para mover o personagem
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
            if evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    movimentoXPersona = 0

        # Lógica de atualização de posição, colisão, etc.
        posicaoXPersona += movimentoXPersona
        # Aqui vai o resto da sua lógica de jogo que estava faltando:
        # limites de tela, movimento do míssil, verificação de colisão, etc.

        # Desenho na tela
        tela.blit(fundoJogo, (0, 0))
        tela.blit(iron, (posicaoXPersona, posicaoYPersona))
        tela.blit(missel, (posicaoXMissel, posicaoYMissel))
        
        texto_pontos = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto_pontos, (15, 15))

        pygame.display.update()
        relogio.tick(60)

# (A função 'dead()' não foi fornecida no seu último código, então não a incluí.
# Se precisar dela, pode colar aqui.)

# --- Ponto de Partida do Programa ---
# Começa o programa exibindo a tela de menu inicial.
start()