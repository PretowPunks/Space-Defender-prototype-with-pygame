import pygame
import random

pygame.init()

# tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Defender')

# cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# relógio
relogio = pygame.time.Clock()

# carregar e redimensionar imagens
imagem_jogador = pygame.image.load("player.png")
imagem_jogador = pygame.transform.scale(imagem_jogador, (50, 50))
imagem_inimigo = pygame.image.load("asteroide.png")
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (50, 50))

# obter retângulos de imagem
retangulo_jogador = imagem_jogador.get_rect()
retangulo_jogador.width = 50
retangulo_jogador.height = 50

retangulo_inimigo = imagem_inimigo.get_rect()
retangulo_inimigo.width = 50
retangulo_inimigo.height = 50

# funções
def desenhar_texto(tela, texto, tamanho, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    superficie_texto = fonte.render(texto, True, BRANCO)
    texto_rect = superficie_texto.get_rect(center=(x, y))
    tela.blit(superficie_texto, texto_rect)

def movimento_jogador(retangulo_jogador, velocidade):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        retangulo_jogador.x -= velocidade
    if teclas[pygame.K_RIGHT]:
        retangulo_jogador.x += velocidade
    if teclas[pygame.K_UP]:
        retangulo_jogador.y -= velocidade
    if teclas[pygame.K_DOWN]:
        retangulo_jogador.y += velocidade

    # Impede que a nave saia dos limites da tela
    if retangulo_jogador.left < 0:
        retangulo_jogador.left = 0
    if retangulo_jogador.right > largura:
        retangulo_jogador.right = largura
    if retangulo_jogador.top < 0:
        retangulo_jogador.top = 0
    if retangulo_jogador.bottom > altura:
        retangulo_jogador.bottom = altura

def atirar_projetil(projeteis, x, y):
    projetil = pygame.Rect(x, y, 5, 10)
    projeteis.append(projetil)

def gerar_inimigo(inimigos, tempo_jogo):
    taxa_spawn = max(1, 20 - tempo_jogo // 10)
    if random.randint(1, taxa_spawn) == 1:
        retangulo_inimigo = imagem_inimigo.get_rect(topleft=(random.randint(0, largura - 50), -50))
        inimigos.append(retangulo_inimigo)

def detectar_colisao(retangulo_jogador, inimigos, projeteis):
    global pontuacao
    for inimigo in inimigos[:]:
        if retangulo_jogador.colliderect(inimigo):
            return True
        for projetil in projeteis[:]:
            if projetil.colliderect(inimigo):
                inimigos.remove(inimigo)
                projeteis.remove(projetil)
                pontuacao += 10
    return False

def desenhar_imagem_jogador(tela):
    pos_x = largura // 2 - imagem_jogador.get_width() // 2
    pos_y = altura - imagem_jogador.get_height() - 20
    tela.blit(imagem_jogador, (pos_x, pos_y))

def menu_principal():
    global jogo_rodando
    jogo_rodando = True
    while jogo_rodando:
        tela.fill(PRETO)
        desenhar_texto(tela, "Space Defender", 64, largura // 2, altura // 4)
        desenhar_texto(tela, "Press Enter to Start", 32, largura // 2, altura // 2)
        desenhar_imagem_jogador(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jogo_rodando = False
                    loop_jogo()

        pygame.display.flip()

def loop_jogo():
    global pontuacao
    pontuacao = 0
    retangulo_jogador = imagem_jogador.get_rect(center=(largura // 2, altura - 50))
    projeteis = []
    inimigos = []
    tempo_inicio = pygame.time.get_ticks()

    jogando = True
    while jogando:
        tela.fill(PRETO)
        tela.blit(imagem_jogador, retangulo_jogador)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    atirar_projetil(projeteis, retangulo_jogador.centerx, retangulo_jogador.top)

        movimento_jogador(retangulo_jogador, 5)
        tempo_jogo = (pygame.time.get_ticks() - tempo_inicio) // 1000
        gerar_inimigo(inimigos, tempo_jogo)
        detectar_colisao(retangulo_jogador, inimigos, projeteis)

        for projetil in projeteis:
            projetil.y -= 5
            pygame.draw.rect(tela, BRANCO, projetil)
            if projetil.bottom < 0:
                projeteis.remove(projetil)

        for inimigo in inimigos:
            inimigo.y += 2
            tela.blit(imagem_inimigo, inimigo)
            if inimigo.top > altura:
                inimigos.remove(inimigo)

        desenhar_texto(tela, f"Score: {pontuacao}", 24, largura // 2, 10)
        pygame.display.flip()
        relogio.tick(60)

        if detectar_colisao(retangulo_jogador, inimigos, projeteis):
            jogando = False

    fim_de_jogo()

def fim_de_jogo():
    global jogo_rodando, pontuacao
    tela.fill(PRETO)
    desenhar_texto(tela, "Game Over", 64, largura // 2, altura // 4)
    desenhar_texto(tela, f"Final Score: {pontuacao}", 32, largura // 2, altura // 2)
    desenhar_texto(tela, "Press Enter to Restart", 32, largura // 2, altura // 1.5)
    desenhar_imagem_jogador(tela)

    pygame.display.flip()

    reiniciar = True
    while reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    reiniciar = False
                    menu_principal()


# Iniciar o menu principal
menu_principal()
