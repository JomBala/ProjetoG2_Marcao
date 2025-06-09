# --- Importações ---
import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
import sys
import json
# Importa a nova função que vamos criar
from recursos.utilidades import get_timestamp_formatado

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

        # --- SUAS CORES PERSONALIZADAS (MANTIDAS) ---
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.CIANO_KONAN = (210, 239, 246)
        self.AZUL_ESCURO = (8, 39, 76)
        self.COR_BOTAO = (28, 63, 90) # Renomeei 'cor_botao' para ser mais claro
        self.AZUL_CHUVA = (14, 34, 47)
        self.NEON = (0, 255, 255)
        
        # --- Setup da Tela ---
        self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption("Paper Run: Konan Edition")
        self.relogio = pygame.time.Clock()
        
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
            self.fundoDead = pygame.image.load(os.path.join(caminho_recursos, "fundoDead.jpg"))
            
            self.konan_img = pygame.image.load(os.path.join(caminho_recursos, "konan.gif")).convert_alpha()
            self.obito_img = pygame.image.load(os.path.join(caminho_recursos, "obito_atacando.gif")).convert_alpha()
            self.fogo_img = pygame.image.load(os.path.join(caminho_recursos, "bola_de_fogo.png")).convert_alpha()
            
            self.som_entrada = pygame.mixer.Sound(os.path.join(caminho_recursos, "entradasound.mp3"))
            self.som_instrucoes = pygame.mixer.Sound(os.path.join(caminho_recursos, "instrucoes.mp3"))
            self.musica_jogo_path = os.path.join(caminho_recursos, "musicaPrincipal.mp3")
            
            self.fonteTexto = pygame.font.Font(os.path.join(caminho_recursos, "Audiowide-Regular.ttf"), 16)
            self.fonteMenu = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 20)
            self.fonteMenuMaior = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 35)
            self.fonte_game_over = pygame.font.Font(None, 74)
            self.fonte_placar = pygame.font.Font(None, 28)

        except Exception as e:
            print(f"Erro ao carregar um ou mais assets: {e}")
            pygame.quit()
            sys.exit()

    def show_start_screen(self):
        # (Esta função permanece exatamente como a sua versão, sem alterações)
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
        # (Esta função permanece exatamente como a sua versão, sem alterações)
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
        # (Esta função permanece exatamente como a sua versão, sem alterações)
        self.som_instrucoes.play()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.tela.blit(self.fundoInstrucoes, (0, 0))
            texto_bem_vindo = self.fonteMenuMaior.render("Bem-vindo", True, self.CIANO_KONAN)
            rect_bem_vindo = texto_bem_vindo.get_rect(center=(self.LARGURA_TELA // 2, 300))
            texto_nome = self.fonteMenuMaior.render(f"{player_name}", True, self.CIANO_KONAN)
            rect_nome = texto_nome.get_rect(centerx=rect_bem_vindo.centerx, top=rect_bem_vindo.bottom + 15)
            instrucao1 = self.fonteMenu.render("Use as setas para desviar dos mísseis", True, self.CIANO_KONAN)
            rect_instrucao1 = instrucao1.get_rect(centerx=rect_nome.centerx, top=rect_nome.bottom + 40)
            instrucao2 = self.fonteMenu.render("Pressione ESPAÇO para pausar o jogo", True, self.CIANO_KONAN)
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
    
    # --- INÍCIO DAS NOVAS FUNCIONALIDADES ---

    # Dentro da sua classe Game, substitua o método antigo por este:

    def registrar_partida(self, player_name, pontos):
        """
        Registra a pontuação, nome e o timestamp em log.dat (VERSÃO CORRIGIDA E SEGURA).
        """
        timestamp = get_timestamp_formatado()
        log_entry = {
            "nome": player_name,
            "pontos": pontos,
            "timestamp": timestamp
        }
        
        logs = [] # Começa com uma lista vazia
        
        # Tenta ler o arquivo de log existente
        if os.path.exists("log.dat"):
            try:
                with open("log.dat", "r", encoding="utf-8") as f:
                    dados_carregados = json.load(f)
                    # VERIFICAÇÃO DE SEGURANÇA: Garante que os dados são uma lista
                    if isinstance(dados_carregados, list):
                        logs = dados_carregados
            except (json.JSONDecodeError, FileNotFoundError):
                # Se o arquivo estiver corrompido ou não for encontrado, ignora e usa a lista vazia
                print("Arquivo de log corrompido ou não encontrado. Criando um novo.")
                logs = []

        # Adiciona a nova entrada à lista
        logs.append(log_entry)
        
        # Salva a lista inteira de volta no arquivo
        try:
            with open("log.dat", "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao escrever no arquivo de log: {e}")

    def show_pause_overlay(self):
        """Desenha uma camada escura e o texto de PAUSADO."""
        overlay = pygame.Surface((self.LARGURA_TELA, self.ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.tela.blit(overlay, (0, 0))
        
        texto_pausa = self.fonte_game_over.render("PAUSADO", True, self.BRANCO)
        rect_pausa = texto_pausa.get_rect(center=(self.LARGURA_TELA / 2, self.ALTURA_TELA / 2))
        self.tela.blit(texto_pausa, rect_pausa)
    
    def show_game_over_screen(self):
        """TELA DE GAME OVER ATUALIZADA: Mostra 'Você Morreu' e os 5 últimos scores."""
        ultimos_scores = []
        try:
            with open("log.dat", "r", encoding="utf-8") as f:
                logs = json.load(f)
                ultimos_scores = sorted(logs, key=lambda x: x.get('pontos', 0), reverse=True)[:5]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Arquivo de log não encontrado ou vazio.")
        
        self.tela.blit(self.fundoDead, (0, 0))
        
        texto_voce_morreu = self.fonte_game_over.render("VOCÊ MORREU", True, self.BRANCO)
        rect_voce_morreu = texto_voce_morreu.get_rect(center=(self.LARGURA_TELA / 2, self.ALTURA_TELA / 4))
        self.tela.blit(texto_voce_morreu, rect_voce_morreu)

        texto_titulo_scores = self.fonteMenuMaior.render("Melhores Pontuações:", True, self.BRANCO)
        rect_titulo_scores = texto_titulo_scores.get_rect(centerx=self.LARGURA_TELA / 2, top=rect_voce_morreu.bottom + 50)
        self.tela.blit(texto_titulo_scores, rect_titulo_scores)

        pos_y_score = rect_titulo_scores.bottom + 20
        for i, entrada in enumerate(ultimos_scores):
            texto_score = f"{i+1}. {entrada['nome']} - {entrada['pontos']} pontos ({entrada['timestamp']})"
            score_surface = self.fonteMenu.render(texto_score, True, self.BRANCO)
            score_rect = score_surface.get_rect(centerx=self.LARGURA_TELA / 2, top=pos_y_score)
            self.tela.blit(score_surface, score_rect)
            pos_y_score += 35

        pygame.display.flip()
        pygame.time.wait(5000)
        self.show_start_screen()

    def run_game_loop(self, player_name):
        """O loop principal onde o jogo acontece, agora com PAUSA."""
        todos_sprites = pygame.sprite.Group()
        projeteis = pygame.sprite.Group()
        konan = Player(self.konan_img, self.ALTURA_TELA)
        obito = Enemy(self.obito_img, self.LARGURA_TELA, self.ALTURA_TELA)
        todos_sprites.add(konan, obito)
        chuva = [GotaDeChuva(self.LARGURA_TELA, self.ALTURA_TELA) for _ in range(200)]
        EVENTO_TIRO_OBITO = pygame.USEREVENT + 1
        pygame.time.set_timer(EVENTO_TIRO_OBITO, 700)
        
        pygame.mixer.music.load(self.musica_jogo_path)
        pygame.mixer.music.play(-1)
        
        pontos = 0
        pausado = False # Variável para controlar o estado de pausa
        
        while True:
            self.relogio.tick(self.FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Só processa tiros se o jogo não estiver pausado
                if evento.type == EVENTO_TIRO_OBITO and not pausado:
                    obito.atirar(todos_sprites, projeteis, self.fogo_img)
                
                # --- LÓGICA DE PAUSA ---
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        pausado = not pausado
                        if pausado:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            # --- Lógica do Jogo (Só roda se NÃO estiver pausado) ---
            if not pausado:
                todos_sprites.update()
                pontos += 1
                if pygame.sprite.spritecollide(konan, projeteis, True):
                    pygame.mixer.music.stop()
                    self.registrar_partida(player_name, pontos // 10)
                    self.show_game_over_screen()
                    return

            # --- Desenho na Tela ---
            self.tela.blit(self.fundoJogo, (0, 0))
            for gota in chuva:
                if not pausado: gota.cair()
                gota.desenhar(self.tela, self.AZUL_CHUVA)
            todos_sprites.draw(self.tela)
            
            texto_pontos = self.fonteMenu.render(f"Pontos: {pontos // 10}", True, self.BRANCO)
            self.tela.blit(texto_pontos, (15, 15))
            texto_aviso_pausa = self.fonteTexto.render("Pressione ESPACO para pausar", True, self.BRANCO)
            self.tela.blit(texto_aviso_pausa, (self.LARGURA_TELA - texto_aviso_pausa.get_width() - 15, 15))
            
            # Se o jogo estiver pausado, desenha a tela de pausa por cima de tudo
            if pausado:
                self.show_pause_overlay()

            pygame.display.flip()
            
# --- Classes de Sprites do Jogo (sem alterações) ---
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
    def __init__(self, enemy_img, screen_width, screen_height):
        super().__init__()
        self.image = pygame.transform.scale(enemy_img, (70, 90))
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.centerx = self.screen_width - 100
        self.rect.centery = random.randint(50, self.screen_height - 50)

    def atirar(self, all_sprites, projectiles_group, projectile_img):
        self.rect.centery = random.randint(50, self.screen_height - 50)
        bola_de_fogo = Projectile(self.rect.center, projectile_img)
        all_sprites.add(bola_de_fogo)
        projectiles_group.add(bola_de_fogo)

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
        """Recorta o sprite sheet da bola de fogo."""
        
        # --- CONFIGURAÇÃO PARA O SEU SPRITE SHEET DA BOLA DE FOGO ---
        NUMERO_DE_FRAMES = 5
        FRAME_LARGURA = 220  # (largura total) / 5 (frames)
        FRAME_ALTURA = 114  # Altura total da imagem

        # IMPORTANTE: Se o fundo do seu sprite sheet tiver uma cor sólida,
        # coloque o valor RGB exato dela aqui. Se já for transparente, não importa.
        COR_DO_FUNDO = (0, 0, 0) # Exemplo: preto

        for i in range(NUMERO_DE_FRAMES):
            # Recorta o quadro da imagem principal
            frame = spritesheet_img.subsurface(pygame.Rect(i * FRAME_LARGURA, 0, FRAME_LARGURA, FRAME_ALTURA))
            
            # Torna a cor de fundo transparente
            frame.set_colorkey(COR_DO_FUNDO)
            
            # Redimensiona o quadro para o tamanho final que ele terá no jogo
            # Ajuste (60, 60) para o tamanho que você preferir!
            frame_redimensionada = pygame.transform.scale(frame, (80, 42))
            self.frames.append(frame_redimensionada)

    def animar(self):
        """Controla a troca de quadros para criar a animação."""
        agora = pygame.time.get_ticks()
        if agora - self.last_update_time > self.animation_speed:
            self.last_update_time = agora
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            
            center_antigo = self.rect.center
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(center=center_antigo)

    def update(self):
        """Atualiza a posição e a animação da bola de fogo."""
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


# --- Ponto de Partida do Programa ---
if __name__ == "__main__":
    jogo = Game()
    jogo.show_start_screen()