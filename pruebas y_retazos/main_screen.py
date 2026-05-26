import pygame
import pygame_gui
import math
import random
import os

# ══════════════════════════════════════════════════════════════
# RUTA BASE
# Se usa para resolver rutas de assets (imágenes) relativas
# al directorio donde vive este archivo.
# ══════════════════════════════════════════════════════════════
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ══════════════════════════════════════════════════════════════
# VENTANA
# ══════════════════════════════════════════════════════════════
WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TITLE    = "🚀 Simulador de Proyectil Planetario"
BG_COLOR = (5, 5, 18)


# ══════════════════════════════════════════════════════════════
# ESTRELLAS
# count       → cantidad total generada al inicio
# R_MIN/MAX   → rango de radios en px
# A_MIN/MAX   → rango de brillo base (0-255)
# FLICK_SPD   → velocidad de la oscilación seno
# FLICK_LO/HI → lo + hi*sin() define el rango del titileo
# ══════════════════════════════════════════════════════════════
STAR_COUNT     = 260
STAR_R_MIN     = 1
STAR_R_MAX     = 3
STAR_A_MIN     = 140
STAR_A_MAX     = 255
STAR_FLICK_SPD = 2.0
STAR_FLICK_LO  = 0.75
STAR_FLICK_HI  = 0.25


# ══════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL  (renderizado manual con pygame.font)
# ══════════════════════════════════════════════════════════════
TITLE_TEXT        = "SIMULADOR DE PROYECTIL"
TITLE_FONT        = "Arial"
TITLE_FONT_SIZE   = 42
TITLE_BOLD        = True
TITLE_COLOR       = (200, 220, 255)
TITLE_Y           = 10
DIVIDER_COLOR     = (80, 120, 220)
DIVIDER_Y         = 68
DIVIDER_HALF_W    = 300
DIVIDER_THICKNESS = 2


# ══════════════════════════════════════════════════════════════
# IMÁGENES DECORATIVAS DE FONDO
# Tierra a la izquierda, Marte a la derecha.
# center → (x, y) donde se centra el sprite
# size   → lado en px al que se escala el PNG
# ══════════════════════════════════════════════════════════════
DECO_LEFT_PATH   = "assets/img/tierra.png"
DECO_LEFT_CENTER = (110, 130)
DECO_LEFT_SIZE   = 160

DECO_RIGHT_PATH   = "assets/img/marte.png"
DECO_RIGHT_CENTER = (1170, 590)
DECO_RIGHT_SIZE   = 140


# ══════════════════════════════════════════════════════════════
# SELECTOR VISUAL DE PLANETAS
# Fila de tarjetas centrada horizontalmente.
# Cada tarjeta tiene tres estados: normal / hover / seleccionada.
# ══════════════════════════════════════════════════════════════
PS_TITLE_TEXT    = "Selecciona el planeta de lanzamiento"
PS_TITLE_Y       = 100
PS_TITLE_COLOR   = (180, 210, 255)
PS_TITLE_FONT_SZ = 22

PS_CARD_W    = 130   # ancho de cada tarjeta en px
PS_CARD_H    = 155   # alto de cada tarjeta en px
PS_IMG_SIZE  = 90    # lado del sprite escalado dentro de la tarjeta
PS_NAME_H    = 28    # altura reservada para el nombre al pie
PS_NAME_FONT_SZ = 16
PS_CARDS_Y   = 145   # Y del borde superior de la fila
PS_CARDS_GAP = 20    # separación horizontal entre tarjetas
PS_BORDER_R  = 14    # radio de esquinas redondeadas
PS_BORDER_T  = 2     # grosor del borde

# Colores por estado de tarjeta
PS_COLOR_NORMAL_BG      = (20,  30,  60)
PS_COLOR_NORMAL_BORDER  = (50,  80,  140)
PS_COLOR_HOVER_BG       = (30,  50,  90)
PS_COLOR_HOVER_BORDER   = (100, 160, 255)
PS_COLOR_SEL_BG         = (20,  60,  120)
PS_COLOR_SEL_BORDER     = (80,  200, 255)
PS_COLOR_NAME_NORMAL    = (180, 200, 240)
PS_COLOR_NAME_SELECTED  = (80,  200, 255)


# ══════════════════════════════════════════════════════════════
# PANEL DE CONTROLES NUMÉRICOS  (widgets pygame_gui)
# CP_WIDTH → ancho del bloque, centrado en pantalla.
# Cada campo: _Y = Y absoluta del widget, _H = alto en px.
# ══════════════════════════════════════════════════════════════
CP_WIDTH = 360

# Título decorativo del bloque
CP_TITLE_OFFSET_Y = 60
CP_TITLE_W        = 520
CP_TITLE_H        = 55
CP_TITLE_TEXT     = "🪐  SIMULADOR DE PROYECTIL PLANETARIO"

# Velocidad inicial
CP_V0_LABEL_Y    = 340
CP_V0_LABEL_H    = 28
CP_V0_ENTRY_Y    = 372
CP_V0_ENTRY_H    = 40

# Ángulo de lanzamiento
CP_ANGLE_LABEL_Y    = 430
CP_ANGLE_LABEL_H    = 28
CP_ANGLE_LABEL_TEXT = "Ángulo inicial (grados):"
CP_ANGLE_ENTRY_Y    = 462
CP_ANGLE_ENTRY_H    = 40

# Velocidad del viento
CP_WIND_LABEL_Y    = 520
CP_WIND_LABEL_H    = 28
CP_WIND_LABEL_TEXT = "Velocidad del viento (m/s):"
CP_WIND_ENTRY_Y    = 552
CP_WIND_ENTRY_H    = 40

# Botón continuar
CP_BTN_Y    = 618
CP_BTN_H    = 52
CP_BTN_TEXT = "Continuar  ▶️"

# Etiqueta de estado / feedback
CP_STATUS_Y            = 680
CP_STATUS_H            = 30
CP_STATUS_TEXT_DEFAULT = "Seleccione los datos y presione Continuar"
CP_STATUS_TEXT_ERROR   = "Error: ingrese valores numéricos válidos."


# ══════════════════════════════════════════════════════════════
# DATOS DE PLANETAS
# g      → gravedad en m/s²
# sky    → color del cielo en la simulación (RGB)
# ground → color del suelo en la simulación (RGB)
# img    → ruta relativa al sprite del selector
# ══════════════════════════════════════════════════════════════
PLANETS = {
    "Tierra":  {"g": 9.81,  "sky": (30,  80,  160), "ground": (34,  139, 34),  "img": "assets/img/tierra.png"},
    "Luna":    {"g": 1.62,  "sky": (10,  10,  30),  "ground": (120, 120, 120), "img": "assets/img/luna.png"},
    "Marte":   {"g": 3.72,  "sky": (160, 60,  20),  "ground": (140, 50,  10),  "img": "assets/img/marte.png"},
    "Júpiter": {"g": 24.79, "sky": (100, 70,  40),  "ground": (180, 120, 60),  "img": "assets/img/jupiter.png"},
    "Venus":   {"g": 8.87,  "sky": (160, 110, 30),  "ground": (200, 140, 40),  "img": "assets/img/venus.png"},
    "Saturno": {"g": 10.44, "sky": (100, 90,  60),  "ground": (170, 150, 100), "img": "assets/img/saturno.png"},
}

# Valores por defecto del formulario al abrir la pantalla
DEFAULT_PLANET = "Tierra"
DEFAULT_GRAVEDAD = PLANETS[DEFAULT_PLANET]["g"]
DEFAULT_VIENTO = 0.0


# ══════════════════════════════════════════════════════════════
# CARGA DE IMÁGENES
# load_image  → carga un PNG con alpha y lo escala a (size, size).
#               Devuelve None si rel_path es None o no existe el
#               archivo; el caller muestra un fallback gris.
# preload_assets → carga todo una sola vez para no releer disco
#               en cada frame. Devuelve (planet_imgs, deco_imgs).
# ══════════════════════════════════════════════════════════════
def load_image(rel_path, size):
    if not rel_path:
        return None
    abs_path = os.path.join(_BASE_DIR, rel_path)
    if not os.path.exists(abs_path):
        return None
    img = pygame.image.load(abs_path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


def preload_assets():
    """Devuelve (planet_imgs, deco_imgs) como dicts nombre→Surface."""
    planet_imgs = {
        name: load_image(data["img"], PS_IMG_SIZE)
        for name, data in PLANETS.items()
    }
    deco_imgs = {
        "left":  load_image(DECO_LEFT_PATH,  DECO_LEFT_SIZE),
        "right": load_image(DECO_RIGHT_PATH, DECO_RIGHT_SIZE),
    }
    return planet_imgs, deco_imgs


# ══════════════════════════════════════════════════════════════
# FONDO ESTRELLADO
# gen_stars  → genera lista de tuplas (x, y, radio, alpha_base).
# draw_stars → oscila el brillo con sin() para producir titileo;
#              t es el tiempo total acumulado en segundos.
# ══════════════════════════════════════════════════════════════
def gen_stars():
    return [
        (
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(STAR_R_MIN, STAR_R_MAX),
            random.randint(STAR_A_MIN, STAR_A_MAX),
        )
        for _ in range(STAR_COUNT)
    ]


def draw_stars(surface, stars, t):
    for (x, y, r, base_a) in stars:
        flicker = int(base_a * (STAR_FLICK_LO + STAR_FLICK_HI * math.sin(t * STAR_FLICK_SPD + x)))
        pygame.draw.circle(surface, (flicker, flicker, flicker), (x, y), r)


# ══════════════════════════════════════════════════════════════
# DIBUJO DEL FONDO COMPLETO
# Rellena con BG_COLOR, dibuja estrellas titilantes y coloca
# las imágenes decorativas. Si una imagen no cargó, se omite.
# ══════════════════════════════════════════════════════════════
def draw_background(screen, stars, t, deco_imgs):
    screen.fill(BG_COLOR)
    draw_stars(screen, stars, t)

    img_l = deco_imgs.get("left")
    if img_l:
        screen.blit(img_l, img_l.get_rect(center=DECO_LEFT_CENTER))

    img_r = deco_imgs.get("right")
    if img_r:
        screen.blit(img_r, img_r.get_rect(center=DECO_RIGHT_CENTER))


# ══════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL
# Renderizado manual con pygame.font para control total del
# color. La línea divisoria separa visualmente el título del
# contenido del menú.
# ══════════════════════════════════════════════════════════════
def draw_title(screen, font):
    surf = font.render(TITLE_TEXT, True, TITLE_COLOR)
    screen.blit(surf, surf.get_rect(centerx=WIDTH // 2, y=TITLE_Y))

    cx = WIDTH // 2
    pygame.draw.line(
        screen, DIVIDER_COLOR,
        (cx - DIVIDER_HALF_W, DIVIDER_Y),
        (cx + DIVIDER_HALF_W, DIVIDER_Y),
        DIVIDER_THICKNESS,
    )


# ══════════════════════════════════════════════════════════════
# SELECTOR VISUAL DE PLANETAS
# Fila de tarjetas centrada en pantalla; cada tarjeta muestra
# el sprite del planeta y su nombre al pie.
# Los Rects de hit-testing se calculan una sola vez en __init__
# y se reusan en handle_event y draw cada frame.
# ══════════════════════════════════════════════════════════════
class PlanetSelector:
    def __init__(self, planet_imgs, selected):
        self.planet_names = list(PLANETS.keys())
        self.planet_imgs  = planet_imgs
        self.selected     = selected
        self.hovered      = None

        # Centrar el bloque de tarjetas horizontalmente
        n            = len(self.planet_names)
        total_w      = n * PS_CARD_W + (n - 1) * PS_CARDS_GAP
        self.start_x = (WIDTH - total_w) // 2

        self.font_title = pygame.font.SysFont("Arial", PS_TITLE_FONT_SZ)
        self.font_name  = pygame.font.SysFont("Arial", PS_NAME_FONT_SZ, bold=True)

        # Pre-calcular Rects para hit-testing (reusar cada frame)
        self._rects = []
        x = self.start_x
        for _ in self.planet_names:
            self._rects.append(pygame.Rect(x, PS_CARDS_Y, PS_CARD_W, PS_CARD_H))
            x += PS_CARD_W + PS_CARDS_GAP

    def handle_event(self, event):
        """Actualiza hover/selección. Devuelve nombre clickeado o None."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = None
            for i, rect in enumerate(self._rects):
                if rect.collidepoint(event.pos):
                    self.hovered = self.planet_names[i]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._rects):
                if rect.collidepoint(event.pos):
                    self.selected = self.planet_names[i]
                    return self.selected
        return None

    def draw(self, screen):
        # Título de la sección
        t_surf = self.font_title.render(PS_TITLE_TEXT, True, PS_TITLE_COLOR)
        screen.blit(t_surf, t_surf.get_rect(centerx=WIDTH // 2, y=PS_TITLE_Y))

        for i, name in enumerate(self.planet_names):
            rect        = self._rects[i]
            is_selected = name == self.selected
            is_hovered  = name == self.hovered

            # Colores según estado de la tarjeta
            if is_selected:
                bg, border, name_c = PS_COLOR_SEL_BG, PS_COLOR_SEL_BORDER, PS_COLOR_NAME_SELECTED
            elif is_hovered:
                bg, border, name_c = PS_COLOR_HOVER_BG, PS_COLOR_HOVER_BORDER, PS_COLOR_NAME_NORMAL
            else:
                bg, border, name_c = PS_COLOR_NORMAL_BG, PS_COLOR_NORMAL_BORDER, PS_COLOR_NAME_NORMAL

            # Fondo y borde de la tarjeta
            pygame.draw.rect(screen, bg,     rect, border_radius=PS_BORDER_R)
            pygame.draw.rect(screen, border, rect, PS_BORDER_T, border_radius=PS_BORDER_R)

            # Sprite del planeta centrado en la zona superior de la tarjeta
            img   = self.planet_imgs.get(name)
            img_y = rect.y + (PS_CARD_H - PS_NAME_H - PS_IMG_SIZE) // 2
            if img:
                screen.blit(img, img.get_rect(centerx=rect.centerx, y=img_y))
            else:
                # Fallback gris cuando no existe el archivo (ej. Luna)
                pygame.draw.circle(screen, (150, 150, 160),
                                   (rect.centerx, img_y + PS_IMG_SIZE // 2), PS_IMG_SIZE // 2)

            # Nombre al pie de la tarjeta
            n_surf = self.font_name.render(name, True, name_c)
            n_rect = n_surf.get_rect(centerx=rect.centerx, y=rect.bottom - PS_NAME_H - 4)
            screen.blit(n_surf, n_rect)

            # Subrayado indicador de selección
            if is_selected:
                uy = n_rect.bottom + 2
                pygame.draw.line(screen, border,
                                 (rect.centerx - 30, uy), (rect.centerx + 30, uy), 2)


# ══════════════════════════════════════════════════════════════
# PANEL DE CONTROL NUMÉRICO
# Encapsula UIPanel + etiqueta de título + etiqueta de valor
# + botones +/- para ajustar un parámetro con step = 0.1.
# ══════════════════════════════════════════════════════════════

class ControlPanel:
    def __init__(self, x, y, titulo, valor_inicial, paramCambio, unidad, callback_cambio, manager, panel=None):
        """
        :param x, y:            Posición del panel en pantalla.
        :param titulo:          Texto del encabezado (ej. "GRAVEDAD").
        :param valor_inicial:   Valor numérico de partida.
        :param paramCambio:     Nombre del parámetro que se va a cambiar.
        :param unidad:          String de la unidad (ej. "m/s²").
        :param callback_cambio: Función llamada al cambiar el valor.
        :param manager:         UIManager de pygame_gui.
        """
        self.valor           = valor_inicial
        self.unidad          = unidad
        self.callback_cambio = callback_cambio
        self.paramCambio = paramCambio#para actualizar al cambiar un planeta
        self.panel = panel #si se pasa un panel, se usan sus coordenadas relativas; sino, se crean nuevos con coordenadas absolutas

        self.tWidth = 400
        self.tHeight = 100

        # Contenedor del panel
        if self.panel is None:
            self.panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((x-self.tWidth/2, y), (self.tWidth, self.tHeight)),
                manager=manager,
            )
        else:
            # Si se pasa un panel existente, se usan sus coordenadas relativas
            self.panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((x, y), (self.tWidth, self.tHeight)),
                manager=manager,
                container=self.panel,
            )

        # Etiqueta del título del parámetro
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 10), (120, 30)),
            text=titulo,
            manager=manager,
            container=self.panel,
            object_id="#title",
        )

        # Etiqueta del valor numérico actual
        self.valor_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 45), (150, 40)),
            text=f"{self.valor:.1f} {self.unidad}",
            manager=manager,
            container=self.panel,
        )

        # Botón restar
        self.bton_menos = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 30), (40, 40)),
            text="-",
            manager=manager,
            container=self.panel,
        )

        # Botón sumar
        self.bton_mas = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((335, 30), (40, 40)),
            text="+",
            manager=manager,
            container=self.panel,
        )
    def kill(self):
        self.panel.kill()
    def procesar_evento(self, event):
        """Detecta clic en los botones y actualiza el valor."""
        if not self.valor == params[self.paramCambio]:
            print("diferencia de valores en comparacion ")
            self.valor = params[self.paramCambio]
            self._actualizar()
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.bton_menos:
                self.valor -= 0.1
                print ("actualizando valor")
                self._actualizar()
            elif event.ui_element == self.bton_mas:
                self.valor += 0.1
                print ("actualizando valor")
                self._actualizar()

    def _actualizar(self):
        global params
        params[self.paramCambio] = self.valor
        """Sincroniza la etiqueta y llama al callback externo."""
        self.valor_label.set_text(f"{params[self.paramCambio]:.1f} {self.unidad}")
        self.callback_cambio(self.valor)


# ══════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DE CONTROLES NUMÉRICOS  (pygame_gui)
# Crea etiquetas de campo, text entries y el botón Continuar.
# x0 es el borde izquierdo del bloque centrado en pantalla.
# ══════════════════════════════════════════════════════════════


def actualizar_gravedad(nuevo_valor):
    global params
    print (f"Gravedad actualizada en el motor: {params['gravedad']:.1f}")
def actualizar_viento(nuevo_valor):
    global params
    print (f"Viento actualizado en el motor: {params['velocidad_del_viento']:.1f}")

def build_controls(manager, params):
    cx = WIDTH // 2
    x0 = cx - CP_WIDTH // 2 #centro del centro jaja

    gravedad_panel = ControlPanel(cx , 350, "Gravedad (m/s²)", params["gravedad"],"gravedad", "m/s²", actualizar_gravedad, manager)
    viento_panel = ControlPanel(cx , 475, "Viento (m/s)", params["velocidad_del_viento"], "velocidad_del_viento", "m/s", actualizar_viento, manager)



    # ── Botón continuar ────────────────────────
    button_continue = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(x0, CP_BTN_Y, CP_WIDTH, CP_BTN_H),
        text=CP_BTN_TEXT,
        manager=manager,
    )

    # ── Etiqueta de estado / feedback ─────────
    status_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(x0, CP_STATUS_Y, CP_WIDTH, CP_STATUS_H),
        text=CP_STATUS_TEXT_DEFAULT,
        manager=manager,
    )

    return {
        "gravedad_panel": gravedad_panel,
        "viento_panel": viento_panel,
        "button_continue": button_continue,
        "status_label":   status_label,
    }



def panelDeParametros(manager):
    cx = 0 #totalmente a la izquierda
    angulo = ControlPanel(cx , 350, "Gravedad", params["gravedad"],"gravedad", "m/s²", actualizar_gravedad, manager)
    fuerza = ControlPanel(cx , 475, "Viento (m/s)", params["velocidad_del_viento"], "velocidad_del_viento", "m/s", actualizar_viento, manager)


def simulacion(manager):
    panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (500, HEIGHT)),
            manager=manager, object_id="#panel_simlacion"
        )
    panel_de_angulo = ControlPanel(0 , 0, "Ángulo", params["angulo"],"angulo", "°", lambda x: print(f"Ángulo actualizado: {x:.1f}°"), manager, panel = panel)
    panel_de_fuerza = ControlPanel(0 , 125, "Fuerza", params["newtons"],"newtons", "N", lambda x: print(f"Fuerza actualizada: {x:.1f} N"), manager, panel = panel)

# ══════════════════════════════════════════════════════════════
# BUCLE PRINCIPAL
# Inicializa pygame y el UIManager, pre-carga los assets,
# construye el selector y los controles, luego itera:
#   eventos → update → draw
# Al presionar Continuar con campos válidos, retorna params.
# ══════════════════════════════════════════════════════════════
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock   = pygame.time.Clock()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT),"theme.json")  # tema personalizado 

    # Fuente manual para el título (fuera de pygame_gui)
    font_title = pygame.font.SysFont(TITLE_FONT, TITLE_FONT_SIZE, bold=TITLE_BOLD)

    planet_imgs, deco_imgs = preload_assets()
    stars        = gen_stars()
    time_elapsed = 0.0
    global params
    # Estado inicial del formulario
    params = {
        #parametros globales
        "planet": DEFAULT_PLANET,
        "gravedad": DEFAULT_GRAVEDAD,
        "velocidad_del_viento": DEFAULT_VIENTO,

        #parametros por objeto
        "angulo": 0,#angulo de lanzamiento
        "newtons": 0,#fuerza de lanzamiento
        "masa": 0,#masa del proyectil
        #estos son globales y van a cambiar cada vez que se seleccione un proyectil nuevo
    }


    selector = PlanetSelector(planet_imgs, params["planet"])
    widgets  = build_controls(manager, params)

    runningHome = True
    runningSimulacion = False

    # ── Bucle de eventos 
    #encargado de elminar elmentos de la pantalla de inicio para mostrar los de simulacion
    def kill_all(elements):
        for el in elements:
            if el is not None:
                widgets[el].kill()


    running = True
    while running:
        time_delta    = clock.tick(FPS) / 1000.0
        time_elapsed += time_delta
        


        #capturando eventos de todo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Selector: hover + click de tarjeta
            #selector de los planetas
            clicked = selector.handle_event(event)
            if clicked:
                params["planet"] = clicked
                print(f"Planeta seleccionado: {clicked}")
                params["gravedad"] = PLANETS[clicked]["g"]
            #CLIKED ES el nombre de la varible que representa la presionada en cierto momento

            # Botón Continuar: validar y retornar
            if (event.type == pygame_gui.UI_BUTTON_PRESSED
                    and event.ui_element == widgets["button_continue"]):
                # se quita la validacion porque se limitan los valores a los que se puede acoger el usuario
                print ("Continuar presionado, iniciando simulacion.....")
                runningHome = False
                runningSimulacion = True

            manager.process_events(event)

            #paneles de control
            widgets["gravedad_panel"].procesar_evento(event)
            widgets["viento_panel"].procesar_evento(event)

        manager.update(time_delta)

        # ── Dibujo del frame ──────────────────
        draw_background(screen, stars, time_elapsed, deco_imgs)

        if runningHome:
            draw_title(screen, font_title)
            selector.draw(screen) 


        if runningSimulacion:
            #eliminar widgets de la pantalla de inicio
            widgets["gravedad_panel"].kill()
            widgets["viento_panel"].kill()
            widgets["button_continue"].kill()
            widgets["status_label"].kill()
            
            #agregar nuevos widgets para la pantalla de simulacion
            simulacion(manager)

        manager.draw_ui(screen)  # widgets pygame_gui

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
