# ============================================================
# RECOLECTOR DE BASURA - Actividad 1: Introducción a Pygame
# Autor: German Pasillas Lizarraga
# Materia: Lógica de Programación - CESUN Universidad
# ============================================================
# Versión base: el jugador agarra las bolsas de basura del parque
# y las lleva al camión. Al llenar el camión llega otro que pide
# 2 bolsas más. (Todavía sin tienda ni compañero.)
# Controles: flechas o WASD = mover | ESC = salir
# ============================================================

import pygame
import random

pygame.init()

ANCHO = 800
ALTO = 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recolector de Basura")
reloj = pygame.time.Clock()
FPS = 60
fuente = pygame.font.SysFont("arial", 20)

COLOR_PASTO = (120, 175, 100)
COLOR_CALLE = (70, 70, 75)
COLOR_JUGADOR = (50, 90, 220)
COLOR_BOLSA = (35, 35, 40)
BLANCO = (255, 255, 255)

ALTO_CALLE = 125
AREA_JUEGO = pygame.Rect(0, 0, ANCHO, ALTO)
AREA_PASTO = pygame.Rect(0, ALTO_CALLE, ANCHO, ALTO - ALTO_CALLE)

jugador = pygame.Rect(100, 300, 36, 36)
velocidad = 3
llevando = 0

camion = pygame.Rect(ANCHO - 260, 20, 152, 95)
meta = 5
entregadas = 0


def crear_nivel(cantidad):
    """Crea la lista con la cantidad exacta de bolsas que pide el camión."""
    lista = []
    while len(lista) < cantidad:
        x = random.randint(AREA_PASTO.left + 20, AREA_PASTO.right - 46)
        y = random.randint(AREA_PASTO.top + 20, AREA_PASTO.bottom - 46)
        bolsa = pygame.Rect(x, y, 26, 26)
        if bolsa.colliderect(jugador.inflate(80, 80)):
            continue
        if bolsa.inflate(20, 20).collidelist(lista) != -1:
            continue
        lista.append(bolsa)
    return lista


bolsas = crear_nivel(meta)

corriendo = True
while corriendo:
    # A) Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            corriendo = False

    # B) Actualización
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jugador.x += velocidad
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        jugador.y += velocidad
    jugador.clamp_ip(AREA_JUEGO)

    for bolsa in bolsas[:]:
        if jugador.colliderect(bolsa) and llevando < 1:
            bolsas.remove(bolsa)
            llevando += 1

    if llevando > 0 and jugador.colliderect(camion):
        entregadas += llevando
        llevando = 0
        print("Camión:", entregadas, "/", meta)

    if entregadas >= meta:
        meta += 2
        entregadas = 0
        bolsas = crear_nivel(meta)
        print("¡Camión lleno! El siguiente pide", meta)

    # C) Dibujo
    pantalla.fill(COLOR_PASTO)
    pygame.draw.rect(pantalla, COLOR_CALLE, (0, 0, ANCHO, ALTO_CALLE))
    pygame.draw.rect(pantalla, (235, 235, 235), camion, border_radius=6)
    for bolsa in bolsas:
        pygame.draw.rect(pantalla, COLOR_BOLSA, bolsa, border_radius=8)
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador, border_radius=8)
    texto = fuente.render("Camión: " + str(entregadas) + "/" + str(meta) +
                          "   Llevas: " + str(llevando), True, BLANCO)
    pantalla.blit(texto, (12, ALTO - 30))

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
