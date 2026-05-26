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
HEIGHT   = 740
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
        self.active       = True   # False → ignora todos los eventos

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
        if not self.active:
            return None

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
    def __init__(self, x, y, titulo, valor_inicial, paramCambio, unidad, callback_cambio, manager, panel=None, width = 400,sum=0.1):
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

        self.tWidth = width
        self.tHeight = 100
        self.sum = sum

        # Contenedor del panel
        if self.panel is None:
            self.panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((x-self.tWidth/2, y), (self.tWidth, self.tHeight)),
                manager=manager,
            )
        else:
            # Si se pasa un panel existente, se usan sus coordenadas relativas
            print (self.tWidth)
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
            relative_rect=pygame.Rect((240, 30), (40, 40)),
            text="-",
            manager=manager,
            container=self.panel,
        )

        # Botón sumar
        self.bton_mas = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 30), (40, 40)),
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
                self.valor -= self.sum
                print ("actualizando valor")
                self._actualizar()
            elif event.ui_element == self.bton_mas:
                self.valor += self.sum
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

    # ControlPanel crea un sub-panel de tWidth=400 px.
    # Pasando cx como x y dejando que el constructor haga x - tWidth/2
    # el panel queda centrado en pantalla.
    gravedad_panel = ControlPanel(cx, 350, "Gravedad (m/s²)", params["gravedad"],
                                  "gravedad", "m/s²", actualizar_gravedad, manager)
    viento_panel   = ControlPanel(cx, 475, "Viento (m/s)",    params["velocidad_del_viento"],
                                  "velocidad_del_viento", "m/s", actualizar_viento, manager)

    x0 = cx - CP_WIDTH // 2

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
        "gravedad_panel":  gravedad_panel,
        "viento_panel":    viento_panel,
        "button_continue": button_continue,
        "status_label":    status_label,
    }



def panelDeParametros(manager):
    """Panel izquierdo de la pantalla de inicio (no usado activamente)."""
    cx = 0
    angulo = ControlPanel(cx , 350, "Gravedad", params["gravedad"],"gravedad", "m/s²", actualizar_gravedad, manager)
    fuerza = ControlPanel(cx , 475, "Viento (m/s)", params["velocidad_del_viento"], "velocidad_del_viento", "m/s", actualizar_viento, manager)


# ══════════════════════════════════════════════════════════════
# PANEL LATERAL DE SIMULACIÓN
# Ancho fijo de 500 px, pegado al borde izquierdo.
# Contiene: ángulo, fuerza, cantidad de proyectiles y
# tres botones de acción (Lanzar, Pausar, Reiniciar).
# ══════════════════════════════════════════════════════════════
SIM_PANEL_W = 400

# Dimensiones de los botones de acción
SIM_BTN_W   = 440
SIM_BTN_H   = 52
SIM_BTN_IMG = 48   # tamaño reservado para icono a la izquierda
SIM_BTN_GAP = 12   # separación vertical entre botones

def actualizar_angulo(nuevo_valor):
    global params
    print(f"Ángulo actualizado: {params['angulo']:.1f}°")
    # Sincronizar con el proyectil seleccionado
    for p in proyectiles:
        if p.select:
            p.fisicas.angulo = params["angulo"]

def actualizar_fuerza(nuevo_valor):
    global params
    print(f"Fuerza actualizada: {params['newtons']:.1f} N")
    # Sincronizar con el proyectil seleccionado
    for p in proyectiles:
        if p.select:
            p.fisicas.fuerza = params["newtons"]

def actualizar_masa(nuevo_valor):
    """Actualiza la masa (kg) del proyectil seleccionado."""
    global params
    # La masa no puede ser menor a 0.1 kg
    if params["masa"] < 0.1:
        params["masa"] = 0.1
    nueva_masa = params["masa"]
    print(f"Masa actualizada: {nueva_masa:.1f} kg")
    for p in proyectiles:
        if p.select:
            p.masa         = nueva_masa
            p.fisicas.masa = nueva_masa

def actualizar_posicion_y(nuevo_valor):
    """Mueve el proyectil seleccionado a la nueva posición X (en metros).
    Actualiza posicion, fisicas.posicion e initial_posicion para que
    Reiniciar también vuelva al lugar correcto. Solo actúa con física inactiva."""
    global params
    nueva_y = params["pos_y"]
    print(f"Posición Y actualizada: {nueva_y:.1f} m")
    for p in proyectiles:
        if p.select and not p.runningFisica:
            p.posicion.y          = nueva_y
            p.fisicas.posicion.y  = nueva_y
            p.initial_posicion.y  = nueva_y
            # Actualizar rect de colisión
            p.rect.y = int(nueva_y * escala)


def simulacion(manager):
    """Crea y devuelve todos los widgets del panel lateral de simulación."""

    # ── Panel contenedor principal ─────────────────────────────
    panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, 0), (SIM_PANEL_W, HEIGHT)),
        manager=manager,
        object_id="#panel_simulacion",
    )

    panel_w = SIM_PANEL_W  # 500 px

    # ── Subpanel de ángulo  (centrado dentro del panel) ────────
    # ControlPanel crea un sub-UIPanel de tWidth=400 px.
    # Para centrarlo: x = (panel_w - 400) // 2 = 50
    sub_x = (panel_w - 350) // 2   # 50

    panel_angulo = ControlPanel(
        sub_x, 30,
        "Ángulo", params["angulo"],
        "angulo", "°",
        actualizar_angulo,
        manager,
        panel=panel,
        width = 350,
        sum = 5 
    )
     # ajustar ancho para que quede centrado dentro del panel

    panel_fuerza = ControlPanel(
        sub_x, 155,
        "Fuerza", params["newtons"],
        "newtons", "N",
        actualizar_fuerza,
        manager,
        panel=panel,
        width = 350,
        sum = 1
    )

    panel_pos_y = ControlPanel(
        sub_x, 280,
        "Posición Y", params["pos_y"],
        "pos_y", "m",
        actualizar_posicion_y,
        manager,
        panel=panel,
        width = 350,
        sum = 1
    )

    panel_masa = ControlPanel(
        sub_x, 405,
        "Masa (kg)", params["masa"],
        "masa", "kg",
        actualizar_masa,
        manager,
        panel=panel,
        width = 350,
        sum = 0.5
    )

    # ── Botones de acción (Lanzar / Pausar / Reiniciar) ────────
    btn_x  = (panel_w - SIM_BTN_W) // 2   # 30
    btn_y0 = 540

    btn_lanzar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x+50, btn_y0), (SIM_BTN_W-100, SIM_BTN_H)),
        text="    🚀  Lanzar",
        manager=manager,
        container=panel,
        object_id="#btn_lanzar",
    )

    btn_pausar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x+50, btn_y0 + SIM_BTN_H + SIM_BTN_GAP), (SIM_BTN_W-100, SIM_BTN_H)),
        text="    ⏸  Pausar",
        manager=manager,
        container=panel,
        object_id="#btn_pausar",
    )

    btn_reiniciar = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((btn_x+50, btn_y0 + 2 * (SIM_BTN_H + SIM_BTN_GAP)), (SIM_BTN_W-100, SIM_BTN_H)),
        text="    🔄  Reiniciar",
        manager=manager,
        container=panel,
        object_id="#btn_reiniciar",
    )


    """"Implementacion del simulador, de aqui hasta el return se encuentran las funciones encargadas de ejecutar fisicas y graficos de la simulacion"""
    # Offset en metros para que los proyectiles aparezcan a la derecha del panel lateral (400px / 10px·m⁻¹ = 40m)
    offset_x = SIM_PANEL_W // escala + 5  # 45 m de margen
    proyectiles.append(proyectil(screen, offset_x, 30, 4, 4, 1, (250, 0,   0),   imghumano))
    proyectiles.append(proyectil(screen, offset_x, 30, 4, 4, 2, (0,   0,   250), imgpiedra))
    proyectiles.append(proyectil(screen, offset_x, 30, 4, 4, 1, (0,   250, 0),   imgnave))

    # Seleccionar el primer proyectil por defecto y sincronizar params
    if proyectiles:
        proyectiles[0].border = True
        proyectiles[0].select = True
        global active_proyectil
        active_proyectil = proyectiles[0]
        params["angulo"]  = proyectiles[0].fisicas.angulo
        params["newtons"] = proyectiles[0].fisicas.fuerza
        params["pos_y"]   = proyectiles[0].posicion.y
        params["masa"]    = proyectiles[0].fisicas.masa

    return {
        "panel":              panel,
        "panel_angulo":       panel_angulo,
        "panel_fuerza":       panel_fuerza,
        "panel_pos_y":        panel_pos_y,
        "panel_masa":         panel_masa,
        "btn_lanzar":         btn_lanzar,
        "btn_pausar":         btn_pausar,
        "btn_reiniciar":      btn_reiniciar,
    }


# ══════════════════════════════════════════════════════════════
# BUCLE PRINCIPAL
# Inicializa pygame y el UIManager, pre-carga los assets,
# construye el selector y los controles, luego itera:
#   eventos → update → draw
# Al presionar Continuar con campos válidos, retorna params.
# ══════════════════════════════════════════════════════════════
def reiniciar ():
        for proyectil in proyectiles:
            """proyectiles[i].fisicas.posicion = pygame.math.Vector2(0,45)
            proyectiles[i].fisicas.velocidad = pygame.math.Vector2(0,0)
            proyectiles[i].posicion = pygame.math.Vector2(0,45)"""

            proyectil.posicion = proyectil.initial_posicion.copy()
            proyectil.fisicas.posicion = proyectil.posicion
            proyectil.fisicas.velocidad = pygame.math.Vector2(0,0)
            proyectil.fisicas.suelo = False
            try:
                proyectil.graficos.clearTrayectoria()
            except Exception:
                pass    
def lanzarTodos():
    for proyectil in proyectiles:
        proyectil.fisicas.lanzamientoCA()

def lanzarActivo():
    if active_proyectil is not None:
        active_proyectil.fisicas.lanzamientoCA()
escala = 10 #10 pixeles equivale a 1 metro
proyectiles = []
active_proyectil = None
runningFisica = False

class proyectil:#separacion en clases, procesar por separado las fisicas y los graficos, luego se unen con una clase principal
    def __init__(self,screen,x,y,width,height,masa,color,img):
        self.screen = screen
        self.posicion = pygame.math.Vector2(x,y)
        self.tamaño = pygame.math.Vector2(width,height)
        self.masa = masa
        self.color = color
        self.img = pygame.transform.scale(img, (self.tamaño.x*(escala), self.tamaño.y*(escala))) if img else False

        self.rect = pygame.Rect(self.posicion.x*escala,self.posicion.y*escala,self.tamaño.x*escala,self.tamaño.y*escala)

        self.initial_posicion = pygame.math.Vector2(x,y)
        #son para verificar sie el proyectil esta seleccionado
        self.border = False
        self.select = False

        #variables de lanzamiento que se editan en el lanzamiento

        self.fisicas = fsproyecctil(self.posicion,self.tamaño,self.masa,self.screen)
        self.graficos = grproyectil(self.color,escala)
        self.runningFisica = False

        global active_proyectil
        active_proyectil = self
        print ("proyectil creado con posicion: ", self.posicion, " y masa: ", self.masa)
    def actualizarFisica(self,val):
        self.runningFisica = val

    def draw(self):

        if self.runningFisica:
            pos = self.fisicas.actualizar()
            if self.img:
                self.graficos.dibujarConImagen(self.screen, pos, self.tamaño, self.img, self.border)
            else:
                self.graficos.dibujar(self.screen, pos, self.tamaño, self.color,self.border)
            self.graficos.dibujarTrayectoria(self.screen, pos)
        else:
            if self.img:
                self.graficos.dibujarConImagen(self.screen, self.posicion, self.tamaño, self.img,self.border)
            else:
                self.graficos.dibujar(self.screen, self.posicion, self.tamaño, self.color,self.border)


    def seleccionar(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    for i in range(len(proyectiles)):
                        proyectiles[i].border = False
                        proyectiles[i].select = False
                    print ("proyectil presionado")
                    params["angulo"]  = self.fisicas.angulo
                    params["newtons"] = self.fisicas.fuerza
                    params["pos_y"]   = self.posicion.y   # posición X en metros
                    params["masa"]    = self.fisicas.masa  # masa del proyectil
                    if self.select:
                        self.border = False
                        self.select = False
                        print("edicion desactivada para proyectil ")
                    else :
                        self.border = True
                        self.select = True
                        print("edicion activada para proyectil ")
        if self.select:
            self.fisicas.angulo = params["angulo"]
            self.fisicas.fuerza = params["newtons"]
            

class fsproyecctil:
    def __init__ (self,posicion,tamaño,masa,mundo):
        self.posicion = posicion
        self.tamaño = tamaño
        self.masa = masa
        self.mundo = mundo# el mundo es la pantalla pero desde la perspectiva fisica
        self.suelo = False
        self.velocidad = pygame.math.Vector2(0,0)
        #Para el lanzamiento
        self.angulo = 0
        self.fuerza = 0


    def lanzamientoCA (self):
        print("lanzamiento ejecutado con angulo: ", self.angulo)
        angulo = math.radians(self.angulo)
        vx = (self.fuerza / self.masa) * math.cos(angulo)
        vy = (self.fuerza / self.masa) * math.sin(angulo)
        print ("velocidad en x: ",vx)
        print("velocidad en y:", vy)
        self.velocidad.x += vx
        self.velocidad.y -= vy
        self.suelo = False


    def apigravedad(self):#estoy pensando en separar las principales caracteristicas fisicar en distintos modulos para mejor depuracion del simulardor
        limite_suelo = self.mundo.get_height() / escala

        if not self.suelo:
            self.velocidad.y += params["gravedad"]*time_delta
            self.velocidad.x -= params["velocidad_del_viento"]*time_delta

        if self.posicion.y + self.tamaño.y >= limite_suelo:
            self.posicion.y = limite_suelo - self.tamaño.y
            self.velocidad.x = 0
            self.suelo = True
        else:
            self.suelo = False

    def act_posicion (self):#funcion que actualiza las posiciones segun la velocidad actual
        self.posicion += self.velocidad*time_delta

    def actualizar(self):#Aqui solo van actualizaciones con velocidad o aceleracion contantes
        self.apigravedad()
        self.act_posicion()
        return self.posicion
    
    
class grproyectil:
    def __init__(self,color,escala):
        self.color = color
        self.escala = escala
        self.trayectoria = []
        self.sample_spacing = 6

    def dibujar(self,screen,posicion,tamaño,color):
        pygame.draw.rect(screen,color,rect=[posicion.x*self.escala,posicion.y*self.escala,tamaño.x*self.escala,tamaño.y*self.escala])

    def dibujarConImagen(self,screen,posicion,tamaño,img,border):
        rect = (posicion.x*self.escala,posicion.y*self.escala)
        screen.blit(img, rect)
        if border:
            pygame.draw.rect(screen,(255,0,0),rect=[posicion.x*self.escala,posicion.y*self.escala,tamaño.x*self.escala,tamaño.y*self.escala],width=4)

    def dibujarTrayectoria(self, screen, posicion):
        px = int(posicion.x * self.escala)
        py = int(posicion.y * self.escala)
        if not self.trayectoria:
            self.trayectoria.append((px, py))
        else:
            lx, ly = self.trayectoria[-1]
            dx = px - lx
            dy = py - ly
            if dx*dx + dy*dy >= self.sample_spacing * self.sample_spacing:
                self.trayectoria.append((px, py))
        for tx, ty in self.trayectoria:
            pygame.draw.rect(screen, self.color, (tx, ty, 2, 2))

    def clearTrayectoria(self):
        self.trayectoria.clear()


def main():
    global screen, imghumano, imgpiedra, imgnave

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    imghumano = pygame.image.load("assets/img/humano.png").convert_alpha()
    imgpiedra = pygame.image.load("assets/img/piedra.png").convert_alpha()
    imgnave = pygame.image.load("assets/img/nave.png").convert_alpha()
    pygame.display.set_caption("Simulador de Proyectiles")
    pygame.display.set_icon(imgnave)

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
        "angulo": 0,       # ángulo de lanzamiento
        "newtons": 0,      # fuerza de lanzamiento
        "masa": 1,         # masa del proyectil (kg)
        "pos_y": 0,        # posición Y del proyectil seleccionado (metros)
    }


    selector = PlanetSelector(planet_imgs, params["planet"])
    widgets  = build_controls(manager, params)
    sim_widgets = None   # se crea una sola vez al pasar a simulación

    runningHome = True
    runningSimulacion = False

    # ── Bucle de eventos ──────────────────────────────────────
    running = True
    while running:
        global time_delta
        time_delta    = clock.tick(FPS) / 1000.0
        time_elapsed += time_delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Selector de planetas (solo activo en pantalla de inicio)
            clicked = selector.handle_event(event)
            if clicked:
                params["planet"] = clicked
                print(f"Planeta seleccionado: {clicked}")
                params["gravedad"] = PLANETS[clicked]["g"]

            # Botón Continuar
            if (event.type == pygame_gui.UI_BUTTON_PRESSED
                    and event.ui_element == widgets["button_continue"]):
                print("Continuar presionado, iniciando simulacion.....")

                # Desactivar selector para que no siga capturando clics
                selector.active = False

                # Destruir widgets de la pantalla de inicio
                widgets["gravedad_panel"].kill()
                widgets["viento_panel"].kill()
                widgets["button_continue"].kill()
                widgets["status_label"].kill()

                runningHome       = False
                runningSimulacion = True

                # Crear widgets de simulación UNA SOLA VEZ
                sim_widgets = simulacion(manager)

            # Eventos para los paneles de la pantalla de inicio
            if runningHome:
                widgets["gravedad_panel"].procesar_evento(event)
                widgets["viento_panel"].procesar_evento(event)

            # Eventos para los paneles de la pantalla de simulación
            if runningSimulacion and sim_widgets:
                sim_widgets["panel_angulo"].procesar_evento(event)
                sim_widgets["panel_fuerza"].procesar_evento(event)
                sim_widgets["panel_pos_y"].procesar_evento(event)
                sim_widgets["panel_masa"].procesar_evento(event)
                for i in range(len(proyectiles)):
                    proyectiles[i].seleccionar(event)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == sim_widgets["btn_lanzar"]:
                        print("▶ Lanzar")
                        for p in proyectiles:
                            p.fisicas.lanzamientoCA()
                            p.runningFisica = True
                    elif event.ui_element == sim_widgets["btn_pausar"]:
                        print("⏸ Pausar")
                        for p in proyectiles:
                            p.runningFisica = not p.runningFisica
                    elif event.ui_element == sim_widgets["btn_reiniciar"]:
                        print("🔄 Reiniciar")
                        reiniciar()
                        for p in proyectiles:
                            p.runningFisica = False

            manager.process_events(event)

        manager.update(time_delta)

        # ── Dibujo del frame ──────────────────
        draw_background(screen, stars, time_elapsed, deco_imgs)

        if runningHome:
            draw_title(screen, font_title)
            selector.draw(screen)

        if runningSimulacion:
            for p in proyectiles:
                p.draw()

        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
