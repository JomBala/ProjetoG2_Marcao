# --- Importações ---
import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
import sys

# --- Classe Principal do Jogo ---

class Game:
    def __init__(self):
        """
        Inicializador do jogo. Configura tela, relógio, carrega assets e define constantes.
        """
        pygame.init()
        pygame.mixer.init()

        # --- Constantes ---
        self.LARGURA_TELA = 1000
        self.ALTURA_TELA = 700
        self.FPS = 60
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AZUL_ESCURO = (8, 39, 76)
        self.CIANO_KONAN = (210, 239, 246)
        self.AZUL_CHUVA = (14, 34, 47)
        self.NEON= (0,255,255)
        

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
            
            # Ícone
            icone = pygame.image.load(os.path.join(caminho_recursos, "icone.png"))
            pygame.display.set_icon(icone)
            
            # Imagens de Fundo
            self.fundoStart = pygame.image.load(os.path.join(caminho_recursos, "fundoStart.png"))
            self.fundoJogo = pygame.image.load(os.path.join(caminho_recursos, "fundoJogo.png"))
            self.fundoInstrucoes = pygame.image.load(os.path.join(caminho_recursos, "instrucoes.png"))
            
            # --- Sprites (GIFs) ---
            # O Pygame vai carregar apenas o primeiro quadro do seu GIF.
            
            # *********** PASSO 2: COLOQUE O NOME DO SEU GIF DA KONAN AQUI! ***********
            # Troque "konan_voando.gif" pelo nome exato do seu arquivo.
            self.konan_img = pygame.image.load(os.path.join(caminho_recursos, "konan.gif")).convert_alpha()
            
            # Você ainda vai precisar dos outros GIFs quando for usá-los
            self.obito_img = pygame.image.load(os.path.join(caminho_recursos, "obito_atacando.gif")).convert_alpha()
            self.fogo_img = pygame.image.load(os.path.join(caminho_recursos, "bola_de_fogo.gif")).convert_alpha()
            
            # --- Sons e Música ---
            self.som_entrada = pygame.mixer.Sound(os.path.join(caminho_recursos, "entradasound.mp3"))
            self.som_instrucoes = pygame.mixer.Sound(os.path.join(caminho_recursos, "instrucoes.mp3"))
            # *********** TROQUE A MÚSICA DO JOGO AQUI SE QUISER ***********
            self.musica_jogo_path = os.path.join(caminho_recursos, "musicaPrincipal.mp3")
            
            # --- Fontes ---
            self.fonteTexto = pygame.font.Font(os.path.join(caminho_recursos, "Audiowide-Regular.ttf"), 16)
            self.fonteMenu = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 20)
            self.fonteMenuMaior = pygame.font.Font(os.path.join(caminho_recursos, "roguehero.ttf"), 35)
            self.fonte_game_over = pygame.font.Font(None, 74)

        except Exception as e:
            print(f"Erro ao carregar um ou mais assets: {e}")
            pygame.quit()
            sys.exit()

    def show_start_screen(self):
        """Mostra a tela de menu inicial."""
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
        """Usa Tkinter para pedir o nome do jogador."""
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
        """Mostra a tela de instruções."""
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
            pygame.draw.rect(self.tela, self.AZUL_CHUVA, botao_iniciar_rect, border_radius=10)
            
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

    def run_game_loop(self, player_name):
        """O loop principal onde o jogo acontece."""
        todos_sprites = pygame.sprite.Group()
        projeteis = pygame.sprite.Group()
        
        konan = Player(self.konan_img, self.ALTURA_TELA)
        obito = Enemy(self.obito_img, self.LARGURA_TELA, self.ALTURA_TELA)
        
        todos_sprites.add(konan, obito)
        chuva = [GotaDeChuva(self.LARGURA_TELA, self.ALTURA_TELA) for _ in range(200)]

        EVENTO_TIRO_OBITO = pygame.USEREVENT + 1
        pygame.time.set_timer(EVENTO_TIRO_OBITO, 700)
        
        # --- CORREÇÃO DA MÚSICA AQUI ---
        pygame.mixer.music.load(self.musica_jogo_path)
        pygame.mixer.music.play(-1)
        
        while True:
            self.relogio.tick(self.FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == EVENTO_TIRO_OBITO:
                    obito.atirar(todos_sprites, projeteis, self.fogo_img)

            todos_sprites.update()
            
            if pygame.sprite.spritecollide(konan, projeteis, True):
                print(f"GAME OVER, {player_name}!")
                pygame.mixer.music.stop()
                self.show_game_over_screen()
                return

            self.tela.blit(self.fundoJogo, (0, 0))
            for gota in chuva:
                gota.cair()
                gota.desenhar(self.tela, self.AZUL_CHUVA)
                
            todos_sprites.draw(self.tela)
            pygame.display.flip()

    def show_game_over_screen(self):
        """Mostra a tela de 'Você Morreu' e volta para o menu."""
        texto = self.fonte_game_over.render("VOCÊ MORREU", True, self.BRANCO)
        rect_texto = texto.get_rect(center=(self.LARGURA_TELA / 2, self.ALTURA_TELA / 2))
        self.tela.blit(texto, rect_texto)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.show_start_screen()

# --- Classes de Sprites do Jogo ---

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
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade_y
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade_y
            
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
    def __init__(self, pos, projectile_img):
        super().__init__()
        self.image = pygame.transform.scale(projectile_img, (40, 40))
        self.rect = self.image.get_rect(center=pos)
        self.velocidade_x = -10

    def update(self):
        self.rect.x += self.velocidade_x
        if self.rect.right < 0: self.kill()

class GotaDeChuva:
    """Classe para criar o efeito de chuva (VERSÃO CORRIGIDA)."""
    def __init__(self, screen_width, screen_height):
        # Guardamos as dimensões da tela DENTRO do objeto
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # O resto do código continua igual
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-100, -10)
        self.velocidade = random.randint(5, 15)
        self.comprimento = random.randint(10, 20)

    def cair(self):
        """
        Método cair corrigido para usar as variáveis salvas em 'self'.
        Não precisa mais de parâmetros.
        """
        self.y += self.velocidade
        # Agora ele verifica usando a altura que foi guardada
        if self.y > self.screen_height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, self.screen_width)

    def desenhar(self, surface, color):
        # Este método já estava correto
        pygame.draw.line(surface, color, (self.x, self.y), (self.x, self.y + self.comprimento), 2)

# --- Ponto de Partida do Programa ---
if __name__ == "__main__":
    jogo = Game()
    jogo.show_start_screen()