# Recolector de Basura 🗑️🚚

Videojuego hecho con **Pygame** donde el jugador recoge las bolsas de basura que hay en un parque y las lleva a un camión que espera en la calle.

- **Autor:** German Pasillas Lizarraga
- **Institución / materia:** CESUN Universidad — Lógica de Programación
- **Objetivo general del juego:** llenar camiones de basura entregando exactamente las bolsas que cada uno pide. Cada camión lleno da monedas, se va, y llega otro que pide 2 bolsas más. Con las monedas se compran mejoras en la tienda (botas rápidas, mochila grande y un compañero bot que recolecta solo).

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python recolector_basura.py
```

**Controles:** flechas o WASD para moverse · `T` abre/cierra la tienda · `1`, `2`, `3` compran · `ESC` sale.

---

# Investigación sobre Pygame

## 1. ¿Qué es Pygame y para qué se utiliza?

Pygame es un conjunto de módulos de Python para hacer videojuegos y otras aplicaciones multimedia (gráficos, sonido, teclado, mouse, joystick). No es un motor de juegos completo como Unity o Godot: es una librería que te da las herramientas básicas (abrir una ventana, dibujar, leer eventos, medir el tiempo) y tú escribes la lógica del juego con tu propio código.

Por dentro funciona como una "envoltura" (wrapper) de **SDL** (Simple DirectMedia Layer), una librería en C que se encarga de hablar con la pantalla, el audio y los dispositivos de entrada en Windows, Mac y Linux. Gracias a eso, el mismo código de Python corre en varios sistemas operativos. Fue creada por Pete Shinners, nació en el año 2000 como sucesora de PySDL, es software libre bajo licencia LGPL y hoy la mantiene una comunidad de voluntarios. Existe también un fork llamado *pygame-ce* (Community Edition) que sigue el mismo estilo de uso. Yo trabajé con la versión 2.6.1.

Se usa mucho para **aprender a programar** (porque los resultados se ven en pantalla al instante), para prototipos, proyectos escolares y juegos 2D pequeños.

## 2. ¿Cómo se relaciona Pygame con los temas vistos en clase?

Lo que más me sorprendió es que Pygame no trae "magia" nueva: casi todo lo que usé son los mismos temas de clase aplicados a un juego. Estos son ejemplos reales de mi código `recolector_basura.py`:

| Tema de clase | Cómo aparece en mi juego |
|---|---|
| **Variables y constantes** | `ANCHO`, `ALTO`, `FPS` (constantes); `monedas`, `llevando`, `entregadas`, `meta` (variables que cambian mientras se juega). |
| **Ciclos** | El *game loop* es un `while corriendo:` que se repite 60 veces por segundo. Dentro uso `for` para recorrer las bolsas, dibujar la tienda o revisar eventos. |
| **Eventos** | `pygame.event.get()` me da los eventos (cerrar ventana, tecla `T`, teclas `1/2/3`, `ESC`). También leo teclas mantenidas con `pygame.key.get_pressed()` para mover al jugador. |
| **Condicionales** | `if llevando < capacidad` decide si puedo agarrar otra bolsa; `if monedas < precio` decide si alcanza para comprar; `if/elif/else` para los estados del camión. |
| **Estructuras de datos** | Una **lista** de `pygame.Rect` guarda las bolsas del parque; una **lista de diccionarios** guarda los artículos de la tienda (nombre, precio, comprados, máximo). |
| **Funciones** | `crear_nivel()`, `distancia()`, `mover_hacia()`, `precio_de()`, `dibujar_camion()` y `dibujar_texto()` separan tareas para no repetir código. |
| **Estados** | `estado_camion` puede ser `"esperando"`, `"saliendo"` o `"llegando"`; según su valor el programa hace cosas distintas. |

Además, Pygame aporta cosas propias que se apoyan en esos temas: `pygame.Rect` (rectángulos para posición y **colisiones** con `colliderect`), `pygame.draw` (dibujar figuras), `pygame.font` (texto) y `pygame.time.Clock` (controlar los cuadros por segundo).

La estructura de todo programa en Pygame es siempre la misma, y la sigo en mi código:

1. **Inicialización** (`pygame.init()`, crear la ventana).
2. **Bucle principal**: (A) manejar eventos → (B) actualizar el estado → (C) dibujar → `display.flip()` + `clock.tick(FPS)`.
3. **Cierre** (`pygame.quit()`).

## 3. ¿Qué significa que Pygame permite "tomar mucho o poco" de la librería?

Significa que Pygame es **modular**: está dividido en módulos independientes (`display`, `draw`, `event`, `key`, `font`, `time`, `image`, `mixer`, `sprite`, `mask`, etc.) y el programador decide cuáles usar. No te obliga a usar una estructura o clases específicas; puedes quedarte solo con lo mínimo (abrir ventana, leer teclado y dibujar figuras) o ir aprovechando más herramientas (imágenes, sonido, sprites, detección de colisiones por máscara) conforme el proyecto lo pida.

Mi juego es un ejemplo de "tomar poco": solo uso `display`, `draw`, `event`, `key`, `font`, `time` y `Rect`. No uso imágenes externas, sonido (`mixer`) ni la clase `Sprite`, porque dibujo todo con rectángulos y círculos. Eso me permitió concentrarme en la lógica (ciclos, listas, funciones) en lugar de aprender toda la librería de golpe. Más adelante, si el proyecto crece, podría "tomar más": sustituir los rectángulos por imágenes con `pygame.image`, agregar efectos con `pygame.mixer` u organizar los objetos con `Sprite`.

## Fuentes consultadas

- Documentación oficial de Pygame: <https://www.pygame.org/docs/>
- Sitio oficial: <https://www.pygame.org>
- Repositorio oficial: <https://github.com/pygame/pygame>
- Ejemplos y estructura vistos en clase (Lógica de Programación, CESUN).

---

# Organización del repositorio

| Rama | Contenido |
|---|---|
| `main` | Versión estable del proyecto (solo recibe merges de `v01` ya probados). |
| `v01` | Rama de integración: aquí se juntan las actividades y se prueba antes de pasar a `main`. |
| `actividad1` | Primera sesión de Pygame: escena base con jugador, bolsas y camión. |
| `actividad2` | Segunda sesión: tienda con mejoras y compañero recolector. |

El detalle del flujo de trabajo está en [FLUJO.md](FLUJO.md).
