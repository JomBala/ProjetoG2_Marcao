# --- Importações ---
import pygame
import random
import os
import tkinter as tk
import pyttsx3
from tkinter import messagebox
import sys
import json
import math 
# --- ALTERAÇÃO 1: Importar as novas funções ---
from recursos.utilidades import get_timestamp_formatado
from recursos.funcoes import registrar_partida, obter_ultimos_registros

# --- Classe Principal do Jogo ---

class Game:
    def __init__(self):
        """
        Inicializador do jogo. Configura tela, relógio, carrega assets e define constantes.
        """
        pygame.init()
        pygame.mixer.init()

        # --- Constantes e Configurações ---
        self.LARGURA_TELA = 1000
        self.ALTURA_TELA = 700
        self.FPS = 60

        # --- CORES PERSONALIZADAS ---
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.CIANO_KONAN = (210, 239, 246)
        self.AZUL_ESCURO = (8, 39, 76)
        self.COR_BOTAO = (28, 63, 90) 
        self.AZUL_CHUVA = (14, 34, 47)
        self.NEON = (0, 255, 255)
        
        
        # --- Setup da Tela ---
        self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption("Paper Run: Konan Edition")
        self.relogio = pygame.time.Clock()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # --- Carregamento de Assets ---
        self.carregar_assets()

    def carregar_assets(self):
        """Carrega todas as imagens, fontes e sons em um só lugar."""
        try:
            caminho_recursos = "Recursos/assets/"
            self.icone = pygame.image.load(os.path.join(caminho_recursos, "icone.png"))
            pygame.display.set_icon(self.icone)
            
            self.fundoStart = pygame.image.load(os.path.join(caminho_recursos, "fundoStart.png"))
            self.fundoJogo = pygame.image.load(os.path.join(caminho_recursos, "fundoJogo.png"))
            self.fundoInstrucoes = pygame.image.load(os.path.join(caminho_recursos, "instrucoes.png"))
            self.fundoDead = pygame.image.load(os.path.join(caminho_recursos, "fundoDead.png"))
            
            self.konan_img = pygame.image.load(os.path.join(caminho_recursos, "konan.png")).convert_alpha()
            self.obito_img = pygame.image.load(os.path.join(caminho_recursos, "obito_atacando.png")).convert_alpha()
            self.fogo_img = pygame.image.load(os.path.join(caminho_recursos, "bola_de_fogo.png")).convert_alpha()
            self.shuriken_img = pygame.image.load(os.path.join(caminho_recursos, "ataque_shuriken.png")).convert_alpha()
            self.sharingan_spritesheet = pygame.image.load(os.path.join(caminho_recursos, "sharingan.png")).convert_alpha()

            self.som_entrada = pygame.mixer.Sound(os.path.join(caminho_recursos, "entradasound.mp3"))
            self.som_instrucoes = pygame.mixer.Sound(os.path.join(caminho_recursos, "instrucoes.mp3"))
            self.musica_jogo_path = os.path.join(caminho_recursos, "musicaPrincipal.mp3")
            
            self.fonteTexto = pygame.font.Font(os.path.join(caminho_recursos, "Audiowide-Regular.ttf"), 16)
            self.fonteMenu = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 20)
            self.fonteMenuMaior = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 35)
            self.fonte_game_over = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 70)
            self.fonte_placar = pygame.font.Font(None, 28)

        except Exception as e:
            print(f"Erro ao carregar um ou mais assets: {e}")
            pygame.quit()
            sys.exit()
            
    def falar(self, texto):
        try:
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Erro ao usar o pyttsx3: {e}")

    def show_start_screen(self):
        
        pygame.mixer.music.stop() 
        self.som_entrada.play(-1)
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.tela.blit(self.fundoStart, (0, 0))
            botao_iniciar_rect = pygame.Rect(150, 320, 150, 40)
            botao_sair_rect = pygame.Rect(150, 390, 150, 40)
            pygame.draw.rect(self.tela, self.BRANCO, botao_iniciar_rect, border_radius=15)
            startTexto = self.fonteTexto.render("INICIAR GAME", True, self.AZUL_ESCURO)
            self.tela.blit(startTexto, startTexto.get_rect(center=botao_iniciar_rect.center))
            pygame.draw.rect(self.tela, self.BRANCO, botao_sair_rect, border_radius=15)
            quitTexto = self.fonteTexto.render("SAIR DO GAME", True, self.AZUL_ESCURO)
            self.tela.blit(quitTexto, quitTexto.get_rect(center=botao_sair_rect.center))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_iniciar_rect.collidepoint(mouse_pos):
                        self.som_entrada.stop()
                        self.get_player_name()
                    if botao_sair_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            self.relogio.tick(self.FPS)

    def get_player_name(self):

        nome_coletado = None
        root = tk.Tk()
        root.title("Informe seu Nome")
        root.withdraw()
        largura_janela = 300
        altura_janela = 120
        pos_x = (root.winfo_screenwidth() - largura_janela) // 2
        pos_y = (root.winfo_screenheight() - altura_janela) // 2
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
            self.show_instructions_screen(nome_coletado)
        else:
            self.show_start_screen()

    def show_instructions_screen(self, player_name):
        
        self.som_instrucoes.play()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.tela.blit(self.fundoInstrucoes, (0, 0))
            texto_bem_vindo = self.fonteMenuMaior.render("Bem-vindo", True, self.CIANO_KONAN)
            rect_bem_vindo = texto_bem_vindo.get_rect(center=(self.LARGURA_TELA // 2, 300))
            texto_nome = self.fonteMenuMaior.render(f"{player_name}", True, self.CIANO_KONAN)
            rect_nome = texto_nome.get_rect(centerx=rect_bem_vindo.centerx, top=rect_bem_vindo.bottom + 15)
            instrucao1 = self.fonteMenu.render("Use as SETAS para desviar dos ATAQUES do Obito", True, self.CIANO_KONAN)
            rect_instrucao1 = instrucao1.get_rect(centerx=rect_nome.centerx, top=rect_nome.bottom + 40)
            instrucao2 = self.fonteMenu.render("Pressione ESPACO para pausar o jogo", True, self.CIANO_KONAN)
            rect_instrucao2 = instrucao2.get_rect(centerx=rect_instrucao1.centerx, top=rect_instrucao1.bottom + 20)
            self.tela.blit(texto_bem_vindo, rect_bem_vindo)
            self.tela.blit(texto_nome, rect_nome)
            self.tela.blit(instrucao1, rect_instrucao1)
            self.tela.blit(instrucao2, rect_instrucao2)
            botao_iniciar_rect = pygame.Rect(0, 0, 200, 50)
            botao_iniciar_rect.center = (self.LARGURA_TELA // 2, rect_instrucao2.bottom + 50)
            pygame.draw.rect(self.tela, self.COR_BOTAO, botao_iniciar_rect, border_radius=10)
            texto_botao = self.fonteMenu.render("Iniciar Jogo", True, self.NEON)
            self.tela.blit(texto_botao, texto_botao.get_rect(center=botao_iniciar_rect.center))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_iniciar_rect.collidepoint(mouse_pos):
                        self.som_instrucoes.stop()
                        self.run_game_loop(player_name)
                        return
            pygame.display.update()
            self.relogio.tick(self.FPS)
    
    # --- ALTERAÇÃO 2: Remover o método registrar_partida daqui ---
    # def registrar_partida(self, player_name, pontos): -> ESTA FUNÇÃO FOI MOVIDA PARA funcoes.py

    def show_pause_overlay(self):
        overlay = pygame.Surface((self.LARGURA_TELA, self.ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.tela.blit(overlay, (0, 0))
        
        texto_pausa = self.fonte_game_over.render("PAUSE", True, self.BRANCO)
        rect_pausa = texto_pausa.get_rect(center=(self.LARGURA_TELA / 2, self.ALTURA_TELA / 2))
        self.tela.blit(texto_pausa, rect_pausa)
    
    def show_game_over_screen(self):
        self.falar("Não existe redenção, só existe o fim")
        
        # --- ALTERAÇÃO 3: Chamar a função importada para obter os scores ---
        ultimos_scores = obter_ultimos_registros(5)
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            self.tela.blit(self.fundoDead, (0, 0))
            
            texto_voce_morreu = self.fonte_game_over.render("OBITO TE DERROTOU", True, self.NEON)
            rect_voce_morreu = texto_voce_morreu.get_rect(center=(self.LARGURA_TELA / 2, self.ALTURA_TELA / 4))
            self.tela.blit(texto_voce_morreu, rect_voce_morreu)

            texto_titulo_scores = self.fonteMenuMaior.render("Melhores Pontuações:", True, self.CIANO_KONAN)
            rect_titulo_scores = texto_titulo_scores.get_rect(centerx=self.LARGURA_TELA / 2, top=rect_voce_morreu.bottom + 50)
            self.tela.blit(texto_titulo_scores, rect_titulo_scores)

            pos_y_score = rect_titulo_scores.bottom + 20
            for i, entrada in enumerate(ultimos_scores):
                texto_score = f"{i+1}. {entrada.get('nome','?')} - {entrada.get('pontos','?')} pts ({entrada.get('timestamp','?')})"
                score_surface = self.fonteMenu.render(texto_score, True, self.CIANO_KONAN)
                score_rect = score_surface.get_rect(centerx=self.LARGURA_TELA / 2, top=pos_y_score)
                self.tela.blit(score_surface, score_rect)
                pos_y_score += 35

            botao_rect = pygame.Rect(0, 0, 250, 50)
            botao_rect.center = (self.LARGURA_TELA // 2, self.ALTURA_TELA - 100)
            pygame.draw.rect(self.tela, self.COR_BOTAO, botao_rect, border_radius=10)
            
            texto_botao = self.fonteMenu.render("Jogar Novamente", True, self.NEON)
            self.tela.blit(texto_botao, texto_botao.get_rect(center=botao_rect.center))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_rect.collidepoint(mouse_pos):
                        self.show_start_screen()
                        return

            pygame.display.update()
            self.relogio.tick(self.FPS)


    def run_game_loop(self, player_name):
        todos_sprites = pygame.sprite.Group()
        projeteis = pygame.sprite.Group()
        konan = Player(self.konan_img, self.ALTURA_TELA)
        
        obito = Enemy(self.obito_img, self.fogo_img, self.shuriken_img, self.LARGURA_TELA, self.ALTURA_TELA)
        
        posicao_sharingan = (self.LARGURA_TELA - 70, 70)
        sharingan_decorativo = SharinganAnimado(posicao_sharingan, self.sharingan_spritesheet)
        todos_sprites.add(sharingan_decorativo)
        
        todos_sprites.add(konan, obito)
        chuva = [GotaDeChuva(self.LARGURA_TELA, self.ALTURA_TELA) for _ in range(200)]
        EVENTO_TIRO_OBITO = pygame.USEREVENT + 1
        
        intervalo_tiro_atual = 700  
        proximo_nivel_pontos = 100  
        
        pygame.time.set_timer(EVENTO_TIRO_OBITO, intervalo_tiro_atual) 
        
        pygame.mixer.music.load(self.musica_jogo_path)
        pygame.mixer.music.play(-1)
        
        pontos = 0
        pausado = False
        
        while True:
            self.relogio.tick(self.FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if evento.type == EVENTO_TIRO_OBITO and not pausado:
                    obito.atirar(todos_sprites, projeteis)
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        pausado = not pausado
                        if pausado:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            if not pausado:
                todos_sprites.update()
                pontos += 1

                if (pontos // 10) >= proximo_nivel_pontos:
                    intervalo_tiro_atual = int(intervalo_tiro_atual * 0.9)
                    
                    if intervalo_tiro_atual < 200:
                        intervalo_tiro_atual = 200
                    
                    pygame.time.set_timer(EVENTO_TIRO_OBITO, 0)
                    pygame.time.set_timer(EVENTO_TIRO_OBITO, intervalo_tiro_atual)

                    proximo_nivel_pontos += 100


                if pygame.sprite.spritecollide(konan, projeteis, True):
                    pygame.mixer.music.stop()
                    # --- ALTERAÇÃO 4: Chamar a função importada ---
                    registrar_partida(player_name, pontos // 10)
                    self.show_game_over_screen()
                    return

            self.tela.blit(self.fundoJogo, (0, 0))
            for gota in chuva:
                if not pausado: gota.cair()
                gota.desenhar(self.tela, self.AZUL_CHUVA)
            todos_sprites.draw(self.tela)
            
            texto_pontos = self.fonteMenu.render(f"Pontos: {pontos // 10}", True, self.BRANCO)
            self.tela.blit(texto_pontos, (15, 15))
            texto_aviso_pausa = self.fonteTexto.render("Pressione ESPACO para pausar", True, self.BRANCO)
            self.tela.blit(texto_aviso_pausa, (self.LARGURA_TELA - texto_aviso_pausa.get_width() - 15, 15))
            
            if pausado:
                self.show_pause_overlay()

            pygame.display.flip()
            
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, screen_height):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (60, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = screen_height // 2
        self.velocidade_y = 7
        self.screen_height = screen_height

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]: self.rect.y -= self.velocidade_y
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]: self.rect.y += self.velocidade_y
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > self.screen_height: self.rect.bottom = self.screen_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, spritesheet_img, fogo_img, shuriken_img, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fogo_img = fogo_img
        self.shuriken_img = shuriken_img

        self.frames = []; self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks(); self.animation_speed = 100
        self.carregar_frames(spritesheet_img)
        self.image = self.frames[self.current_frame]; self.rect = self.image.get_rect()
        self.reposicionar()

    def carregar_frames(self, spritesheet_img):
        NUM_COLUNAS, NUM_LINHAS = 5, 3
        FRAME_LARGURA = spritesheet_img.get_width() // NUM_COLUNAS
        FRAME_ALTURA = spritesheet_img.get_height() // NUM_LINHAS
        for y in range(NUM_LINHAS):
            for x in range(NUM_COLUNAS):
                frame = spritesheet_img.subsurface(pygame.Rect(x * FRAME_LARGURA, y * FRAME_ALTURA, FRAME_LARGURA, FRAME_ALTURA))
                frame.set_colorkey((0, 0, 0))
                self.frames.append(pygame.transform.scale(frame, (200, 100)))

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update_time > self.animation_speed:
            self.last_update_time = agora
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            center_antigo = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center_antigo)

    def reposicionar(self):
        self.rect.centerx = self.screen_width - 100
        self.rect.centery = random.randint(45, self.screen_height - 45)

    def update(self):
        self.animar()

    def atirar(self, all_sprites, projectiles_group):
        self.reposicionar()
        tipo_ataque = random.choice(['fogo', 'shuriken'])

        if tipo_ataque == 'fogo':
            novo_projetil = Projectile(self.rect.midleft, self.fogo_img)
        else:
            novo_projetil = ShurikenInimigo(self.rect.midleft, self.shuriken_img)

        all_sprites.add(novo_projetil)
        projectiles_group.add(novo_projetil)


class ShurikenInimigo(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_img):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed = 75

        self.carregar_frames(spritesheet_img)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.velocidade_x = -12

    def carregar_frames(self, spritesheet_img):
        NUMERO_DE_FRAMES = 3
        FRAME_LARGURA = spritesheet_img.get_width() // NUMERO_DE_FRAMES
        FRAME_ALTURA = spritesheet_img.get_height()

        for i in range(NUMERO_DE_FRAMES):
            frame = spritesheet_img.subsurface(pygame.Rect(i * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
            frame_redimensionada = pygame.transform.scale(frame, (40, 40))
            self.frames.append(frame_redimensionada)

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update_time > self.animation_speed:
            self.last_update_time = agora
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            center_antigo = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center_antigo)

    def update(self):
        self.animar()
        self.rect.x += self.velocidade_x
        if self.rect.right < 0:
            self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, bola_de_fogo_png):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed = 100

        self.carregar_frames(bola_de_fogo_png)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.velocidade_x = -10 

    def carregar_frames(self, spritesheet_img):
        
        NUMERO_DE_FRAMES = 5
        FRAME_LARGURA = 220
        FRAME_ALTURA = 114
        COR_DO_FUNDO = (0, 0, 0) 

        for i in range(NUMERO_DE_FRAMES):
            frame = spritesheet_img.subsurface(pygame.Rect(i * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
            frame.set_colorkey(COR_DO_FUNDO)
            frame_redimensionada = pygame.transform.scale(frame, (80, 42))
            self.frames.append(frame_redimensionada)

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.last_update_time > self.animation_speed:
            self.last_update_time = agora
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            center_antigo = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center_antigo)

    def update(self):
        self.animar()
        self.rect.x += self.velocidade_x
        
        if self.rect.right < 0:
            self.kill()

class GotaDeChuva:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-100, -10)
        self.velocidade = random.randint(5, 15)
        self.comprimento = random.randint(10, 20)

    def cair(self):
        self.y += self.velocidade
        if self.y > self.screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, self.screen_width)

    def desenhar(self, surface, color):
        pygame.draw.line(surface, color, (self.x, self.y), (self.x, self.y + self.comprimento), 2)

class SharinganAnimado(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_img):
        super().__init__()
        self.frames = []
        
        largura_total = spritesheet_img.get_width()
        altura_total = spritesheet_img.get_height()
        largura_frame = largura_total // 3
        
        for i in range(3):
            frame = spritesheet_img.subsurface((i * largura_frame, 0, largura_frame, altura_total))
            frame.set_colorkey((0, 0, 0))
            frame_redimensionado = pygame.transform.scale(frame, (80, 80))
            self.frames.append(frame_redimensionado)
            
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=pos)
        
        self.ultimo_update = pygame.time.get_ticks()
        self.velocidade_anim = 80

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update > self.velocidade_anim:
            self.ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            posicao_antiga = self.rect.center
            self.image = self.frames[self.frame_atual]
            self.rect = self.image.get_rect(center=posicao_antiga)


if __name__ == "__main__":
    jogo = Game()
    jogo.show_start_screen()
