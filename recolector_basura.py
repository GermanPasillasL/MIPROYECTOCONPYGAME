# ============================================================
# RECOLECTOR DE BASURA - Introducción a Pygame
# Autor: German Pasillas Lizarraga
# Materia: Lógica de Programación - CESUN Universidad
# ============================================================
# Descripción: el jugador agarra las bolsas de basura que hay en
# el parque y las lleva al camión que espera en la calle. Cada
# camión pide cierta cantidad de bolsas y en el parque solo hay
# las necesarias para completarlo. Al llenar el camión se ganan
# monedas, el camión se va y llega uno nuevo que pide 2 bolsas
# más. Con las monedas se compran mejoras en la tienda.
# Controles: flechas o WASD = mover | T = tienda | ESC = salir
# ============================================================

import pygame
import random

# ------------------------------------------------------------
# 1. INICIALIZACIÓN
# ------------------------------------------------------------
pygame.init()

ANCHO = 800
ALTO = 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recolector de Basura")

reloj = pygame.time.Clock()   # controla los FPS
FPS = 60

fuente = pygame.font.SysFont("arial", 20)
fuente_chica = pygame.font.SysFont("arial", 17)
fuente_grande = pygame.font.SysFont("arial", 28, bold=True)

# Colores (R, G, B)
COLOR_PASTO = (120, 175, 100)
COLOR_CALLE = (70, 70, 75)
COLOR_LINEA = (240, 220, 90)
COLOR_JUGADOR = (50, 90, 220)
COLOR_CABEZA = (255, 215, 150)
COLOR_BOT = (240, 140, 40)
COLOR_BOLSA = (35, 35, 40)
COLOR_BARRA = (30, 30, 35)
COLOR_TIENDA = (245, 235, 200)
COLOR_BORDE_TIENDA = (120, 90, 40)
COLOR_TEXTO_TIENDA = (90, 60, 20)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Medidas de la pantalla
ALTO_CALLE = 125    # la calle ocupa la parte de arriba
ALTO_BARRA = 40     # barra de información en la parte de abajo
# Por donde puede caminar el jugador
AREA_JUEGO = pygame.Rect(0, 0, ANCHO, ALTO - ALTO_BARRA)
# Donde aparece la basura (el pasto)
AREA_PASTO = pygame.Rect(0, ALTO_CALLE, ANCHO, ALTO - ALTO_CALLE - ALTO_BARRA)

# Jugador (un rectángulo: sirve para dibujar y para detectar colisiones)
jugador = pygame.Rect(100, 300, 36, 36)
velocidad = 1       # sube con las botas de la tienda
capacidad = 1        # cuántas bolsas puede cargar (sube con la mochila)
llevando = 0         # cuántas bolsas lleva cargando ahorita

# Compañero (bot) que se compra en la tienda
tiene_bot = False
bot = pygame.Rect(0, 0, 30, 30)
VELOCIDAD_BOT = 2
bot_lleva = False

# Camión
LUGAR_CAMION = ANCHO - 260   # posición x donde el camión se estaciona
VEL_CAMION = 6
camion_x = LUGAR_CAMION
camion = pygame.Rect(camion_x, 20, 152, 95)   # zona donde se entrega la basura
estado_camion = "esperando"  # puede ser: "esperando", "saliendo", "llegando"
numero_camion = 1
meta = 5                     # bolsas que pide el camión actual
entregadas = 0               # bolsas que ya están dentro del camión
monedas = 0

# Tienda: cada artículo es un diccionario con sus datos
tienda_abierta = False
articulos = [
    {"nombre": "Botas rápidas", "descripcion": "+1 de velocidad",
     "precio": 10, "comprados": 0, "maximo": 3},
    {"nombre": "Mochila grande", "descripcion": "+1 bolsa de capacidad",
     "precio": 20, "comprados": 0, "maximo": 2},
    {"nombre": "Compañero recolector", "descripcion": "Un bot que recoge y entrega bolsas solo",
     "precio": 60, "comprados": 0, "maximo": 1},
]

# Mensaje temporal en pantalla
mensaje = ""
mensaje_frames = 0


# ------------------------------------------------------------
# FUNCIONES
# ------------------------------------------------------------
def crear_nivel(cantidad):
    """Crea la lista con la cantidad exacta de bolsas que pide el camión."""
    lista = []
    while len(lista) < cantidad:
        x = random.randint(AREA_PASTO.left + 20, AREA_PASTO.right - 46)
        y = random.randint(AREA_PASTO.top + 20, AREA_PASTO.bottom - 46)
        bolsa = pygame.Rect(x, y, 26, 26)
        if bolsa.colliderect(jugador.inflate(80, 80)):
            continue                      # muy cerca del jugador, se intenta otra vez
        if bolsa.inflate(20, 20).collidelist(lista) != -1:
            continue                      # encima de otra bolsa, se intenta otra vez
        lista.append(bolsa)
    return lista


def distancia(a, b):
    """Distancia aproximada entre los centros de dos rectángulos."""
    return abs(a.centerx - b.centerx) + abs(a.centery - b.centery)


def mover_hacia(rect, destino, vel):
    """Mueve un rectángulo un paso en dirección al rectángulo destino."""
    if rect.centerx < destino.centerx - vel:
        rect.x += vel
    elif rect.centerx > destino.centerx + vel:
        rect.x -= vel
    if rect.centery < destino.centery - vel:
        rect.y += vel
    elif rect.centery > destino.centery + vel:
        rect.y -= vel


def precio_de(articulo):
    """El precio sube cada vez que se compra el mismo artículo."""
    return articulo["precio"] * (articulo["comprados"] + 1)


def dibujar_camion(x):
    """Dibuja el camión de basura con su esquina izquierda en x."""
    y = 20
    pygame.draw.rect(pantalla, (235, 235, 235), (x, y, 110, 80), border_radius=6)   # caja
    pygame.draw.rect(pantalla, (40, 150, 70), (x, y, 110, 14), border_radius=6)     # franja
    pygame.draw.rect(pantalla, (200, 60, 50), (x + 110, y + 25, 42, 55), border_radius=6)  # cabina
    pygame.draw.rect(pantalla, (170, 220, 250), (x + 128, y + 32, 20, 18))          # ventana
    for rueda_x in (x + 25, x + 85, x + 132):                                       # ruedas
        pygame.draw.circle(pantalla, NEGRO, (rueda_x, y + 82), 12)
        pygame.draw.circle(pantalla, (160, 160, 160), (rueda_x, y + 82), 5)


def dibujar_texto(texto, fuente_usada, color, centro):
    """Escribe un texto centrado en la posición indicada."""
    imagen = fuente_usada.render(texto, True, color)
    pantalla.blit(imagen, imagen.get_rect(center=centro))


# Al inicio hay en el parque exactamente las bolsas que pide el primer camión
bolsas = crear_nivel(meta)

# ------------------------------------------------------------
# 2. BUCLE PRINCIPAL (game loop)
# ------------------------------------------------------------
corriendo = True
while corriendo:

    # --- A) Manejo de eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if tienda_abierta:
                    tienda_abierta = False            # ESC primero cierra la tienda
                else:
                    corriendo = False

            if evento.key == pygame.K_t:
                tienda_abierta = not tienda_abierta   # abre o cierra la tienda

            # Compras: teclas 1, 2 y 3 (solo si la tienda está abierta)
            if tienda_abierta and evento.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                numero = evento.key - pygame.K_1      # 0, 1 o 2
                articulo = articulos[numero]
                precio = precio_de(articulo)
                if articulo["comprados"] >= articulo["maximo"]:
                    mensaje = "Ya tienes el máximo de este artículo"
                elif monedas < precio:
                    mensaje = "No te alcanzan las monedas"
                else:
                    monedas -= precio
                    articulo["comprados"] += 1
                    if numero == 0:
                        velocidad += 1
                    elif numero == 1:
                        capacidad += 1
                    elif numero == 2:
                        tiene_bot = True
                        bot.center = jugador.center
                    mensaje = "Compraste: " + articulo["nombre"]
                mensaje_frames = 90

    # --- B) Actualización del estado (se detiene si la tienda está abierta) ---
    if not tienda_abierta:

        # Movimiento del jugador con flechas o WASD
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador.x -= velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador.x += velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jugador.y -= velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jugador.y += velocidad

        # Evita que el jugador salga del área de juego
        jugador.clamp_ip(AREA_JUEGO)

        # Agarrar basura: colisión del jugador con una bolsa
        # (se revisa una copia de la lista porque vamos a borrar elementos)
        for bolsa in bolsas[:]:
            if jugador.colliderect(bolsa):
                if llevando < capacidad:
                    bolsas.remove(bolsa)
                    llevando += 1
                    mensaje = "¡Bolsa agarrada! Llévala al camión"
                    mensaje_frames = 60
                    print("Bolsa agarrada. Llevas:", llevando, "/", capacidad)
                else:
                    mensaje = "¡Mochila llena! Llévala al camión"
                    mensaje_frames = 30

        # Lógica del camión según su estado
        if estado_camion == "esperando":

            # Entregar basura: colisión del jugador con el camión
            if llevando > 0 and jugador.colliderect(camion):
                entregadas += llevando
                mensaje = "¡Entregaste " + str(llevando) + " bolsa(s) al camión!"
                mensaje_frames = 60
                print("Entregaste", llevando, "bolsa(s). Camión:", entregadas, "/", meta)
                llevando = 0

            # Compañero (bot): busca una bolsa, la agarra y la lleva al camión
            if tiene_bot:
                if not bot_lleva:
                    if len(bolsas) > 0:
                        objetivo = bolsas[0]
                        for bolsa in bolsas:
                            if distancia(bot, bolsa) < distancia(bot, objetivo):
                                objetivo = bolsa      # la más cercana al bot
                        mover_hacia(bot, objetivo, VELOCIDAD_BOT)
                        if bot.colliderect(objetivo):
                            bolsas.remove(objetivo)
                            bot_lleva = True
                else:
                    mover_hacia(bot, camion, VELOCIDAD_BOT)
                    if bot.colliderect(camion):
                        entregadas += 1
                        bot_lleva = False

            # Si ya se entregó la meta, el camión se va y se ganan monedas
            if entregadas >= meta:
                premio = meta * 3
                monedas += premio
                estado_camion = "saliendo"
                mensaje = "¡Felicidades! Camión lleno: +" + str(premio) + " monedas"
                mensaje_frames = 120
                print("¡Felicidades! Camión lleno. Monedas:", monedas)

        elif estado_camion == "saliendo":
            camion_x += VEL_CAMION
            if camion_x > ANCHO:                      # ya salió de la pantalla
                numero_camion += 1
                meta += 2                             # el siguiente camión pide más
                entregadas = 0
                bolsas = crear_nivel(meta)            # nuevas bolsas, solo las necesarias
                camion_x = -160                       # aparece por la izquierda
                estado_camion = "llegando"

        elif estado_camion == "llegando":
            camion_x += VEL_CAMION
            if camion_x >= LUGAR_CAMION:              # ya llegó a su lugar
                camion_x = LUGAR_CAMION
                estado_camion = "esperando"

        camion.x = camion_x                           # la zona de entrega sigue al camión

    # El mensaje desaparece cuando se acaba su tiempo
    if mensaje_frames > 0:
        mensaje_frames -= 1
    else:
        mensaje = ""

    # --- C) Dibujo (renderizado) ---
    pantalla.fill(COLOR_PASTO)

    # Calle y líneas
    pygame.draw.rect(pantalla, COLOR_CALLE, (0, 0, ANCHO, ALTO_CALLE))
    for linea_x in range(10, ANCHO, 70):
        pygame.draw.rect(pantalla, COLOR_LINEA, (linea_x, ALTO_CALLE - 12, 40, 5))

    # Bolsas de basura que quedan en el parque
    for bolsa in bolsas:
        pygame.draw.rect(pantalla, COLOR_BOLSA, bolsa, border_radius=8)
        pygame.draw.rect(pantalla, (200, 200, 200), (bolsa.centerx - 3, bolsa.top - 4, 6, 6))

    # Camión (con el contador de bolsas entregadas escrito en la caja)
    dibujar_camion(camion_x)
    dibujar_texto(str(entregadas) + "/" + str(meta), fuente_grande,
                  (30, 30, 30), (camion_x + 55, 62))

    # Compañero (bot)
    if tiene_bot:
        pygame.draw.rect(pantalla, COLOR_BOT, bot, border_radius=6)
        pygame.draw.circle(pantalla, BLANCO, (bot.centerx, bot.top + 9), 6)
        if bot_lleva:
            bolsa_bot = (bot.centerx - 6, bot.top - 18, 12, 14)
            pygame.draw.rect(pantalla, COLOR_BOLSA, bolsa_bot, border_radius=4)

    # Jugador (cuerpo y cabeza) y las bolsas que carga arriba de la cabeza
    pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador, border_radius=8)
    pygame.draw.circle(pantalla, COLOR_CABEZA, (jugador.centerx, jugador.top + 10), 8)
    for i in range(llevando):
        bolsa_cargada = (jugador.left + i * 14, jugador.top - 20, 12, 14)
        pygame.draw.rect(pantalla, COLOR_BOLSA, bolsa_cargada, border_radius=4)

    # Tienda (se dibuja encima de todo cuando está abierta)
    panel = pygame.Rect(0, 0, 560, 300)
    panel.center = (ANCHO // 2, 250)
    if tienda_abierta:
        pygame.draw.rect(pantalla, COLOR_TIENDA, panel, border_radius=14)
        pygame.draw.rect(pantalla, COLOR_BORDE_TIENDA, panel, 4, border_radius=14)
        dibujar_texto("TIENDA", fuente_grande, COLOR_TEXTO_TIENDA, (ANCHO // 2, panel.top + 28))
        dibujar_texto("Tus monedas: " + str(monedas), fuente, COLOR_TEXTO_TIENDA,
                      (ANCHO // 2, panel.top + 62))
        for i in range(len(articulos)):
            articulo = articulos[i]
            y = panel.top + 95 + i * 55
            if articulo["comprados"] >= articulo["maximo"]:
                precio_texto = "AGOTADO"
            else:
                precio_texto = str(precio_de(articulo)) + " monedas"
            titulo = str(i + 1) + ") " + articulo["nombre"]
            pantalla.blit(fuente.render(titulo, True, COLOR_TEXTO_TIENDA), (panel.left + 25, y))
            pantalla.blit(fuente_chica.render(articulo["descripcion"], True, (130, 100, 60)),
                          (panel.left + 25, y + 24))
            cantidad = "  (" + str(articulo["comprados"]) + "/" + str(articulo["maximo"]) + ")"
            derecha = precio_texto + cantidad
            imagen = fuente.render(derecha, True, COLOR_TEXTO_TIENDA)
            pantalla.blit(imagen, (panel.right - imagen.get_width() - 25, y + 6))
        dibujar_texto("Presiona 1, 2 o 3 para comprar | T para cerrar", fuente_chica,
                      COLOR_TEXTO_TIENDA, (ANCHO // 2, panel.bottom - 20))

    # Mensaje temporal (debajo de la calle, o debajo de la tienda si está abierta)
    if mensaje != "":
        fondo = pygame.Rect(0, 0, 460, 40)
        if tienda_abierta:
            fondo.center = (ANCHO // 2, panel.bottom + 25)
        else:
            fondo.center = (ANCHO // 2, ALTO_CALLE + 30)
        pygame.draw.rect(pantalla, COLOR_BARRA, fondo, border_radius=10)
        dibujar_texto(mensaje, fuente, BLANCO, fondo.center)

    # Barra de información
    pygame.draw.rect(pantalla, COLOR_BARRA, (0, ALTO - ALTO_BARRA, ANCHO, ALTO_BARRA))
    info = "Camión #" + str(numero_camion) + "  Entregadas: " + str(entregadas) + "/" + str(meta)
    info = info + "  Llevas: " + str(llevando) + "/" + str(capacidad) + "  Monedas: " + str(monedas)
    pantalla.blit(fuente_chica.render(info, True, BLANCO), (12, ALTO - 28))
    ayuda = fuente_chica.render("T: tienda | ESC: salir", True, (170, 170, 170))
    pantalla.blit(ayuda, (ANCHO - ayuda.get_width() - 12, ALTO - 28))

    pygame.display.flip()     # muestra todo lo dibujado
    reloj.tick(FPS)           # limita el juego a 60 cuadros por segundo

# ------------------------------------------------------------
# 3. CIERRE
# ------------------------------------------------------------
pygame.quit()