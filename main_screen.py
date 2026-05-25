import pygame
import pygame_gui
import math
import random
import json
import os

# ─────────────────────────────────────────────
# CARGA DE ESTILOS DESDE ARCHIVO EXTERNO
# Todos los valores visuales (colores, tamaños,
# posiciones, textos) viven en styles.json.
# ─────────────────────────────────────────────
_BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
_STYLES_PATH = os.path.join(_BASE_DIR, "styles.json")
with open(_STYLES_PATH, "r", encoding="utf-8") as _f:
    S = json.load(_f)

# Atajos a secciones del JSON
WIN      = S["window"]
STARS_S  = S["stars"]
TITLE_S  = S["title_bar"]
DECO_IMG = S["decorative_images"]
PS       = S["planet_selector"]   # configuración visual del selector de planetas
CP       = S["control_panel"]
PLANETS  = S["planets"]
DEFAULTS = S["defaults"]

WIDTH, HEIGHT = WIN["width"], WIN["height"]
FPS           = WIN["fps"]


# ─────────────────────────────────────────────
# CARGA Y ESCALADO DE IMÁGENES
# Devuelve un Surface escalado al tamaño pedido,
# o None si la ruta es null / el archivo no existe.
# convert_alpha() preserva la transparencia PNG.
# ─────────────────────────────────────────────
def load_image(rel_path, size):
    if not rel_path:
        return None
    abs_path = os.path.join(_BASE_DIR, rel_path)
    if not os.path.exists(abs_path):
        return None
    img = pygame.image.load(abs_path).convert_alpha()
    return pygame.transform.smoothscale(img, (size, size))


# ─────────────────────────────────────────────
# PRE-CARGA DE TODAS LAS IMÁGENES AL INICIO
# Se hace una sola vez para no releer disco
# en cada frame. Devuelve dos dicts:
#   planet_imgs  → nombre_planeta: Surface
#   deco_imgs    → "left"/"right": Surface
# ─────────────────────────────────────────────
def preload_assets():
    planet_imgs = {}
    for name, data in PLANETS.items():
        planet_imgs[name] = load_image(data.get("img"), PS["img_size"])

    deco_imgs = {
        "left":  load_image(DECO_IMG["left"]["path"],  DECO_IMG["left"]["size"]),
        "right": load_image(DECO_IMG["right"]["path"], DECO_IMG["right"]["size"]),
    }
    return planet_imgs, deco_imgs


# ─────────────────────────────────────────────
# GENERACIÓN Y DIBUJO DE ESTRELLAS
# Crea posiciones y radios aleatorios; el brillo
# oscila con seno para simular titileo estelar.
# ─────────────────────────────────────────────
def gen_stars(n=None):
    n = n or STARS_S["count"]
    return [
        (
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(STARS_S["radius_min"], STARS_S["radius_max"]),
            random.randint(STARS_S["alpha_min"],  STARS_S["alpha_max"]),
        )
        for _ in range(n)
    ]


def draw_stars(surface, stars, t):
    spd = STARS_S["flicker_speed"]
    lo  = STARS_S["flicker_min"]
    hi  = STARS_S["flicker_max"]
    for (x, y, r, base_a) in stars:
        flicker = int(base_a * (lo + hi * math.sin(t * spd + x)))
        pygame.draw.circle(surface, (flicker, flicker, flicker), (x, y), r)


# ─────────────────────────────────────────────
# DIBUJO DEL FONDO
# Rellena con color espacial, dibuja estrellas
# y coloca las imágenes decorativas (Tierra y
# Marte) centradas en las posiciones del JSON.
# ─────────────────────────────────────────────
def draw_background(screen, stars, time_elapsed, deco_imgs):
    screen.fill(tuple(WIN["background_color"]))
    draw_stars(screen, stars, time_elapsed)

    # Imagen decorativa izquierda (Tierra)
    img_l = deco_imgs.get("left")
    if img_l:
        cx, cy = DECO_IMG["left"]["center"]
        rect = img_l.get_rect(center=(cx, cy))
        screen.blit(img_l, rect)

    # Imagen decorativa derecha (Marte)
    img_r = deco_imgs.get("right")
    if img_r:
        cx, cy = DECO_IMG["right"]["center"]
        rect = img_r.get_rect(center=(cx, cy))
        screen.blit(img_r, rect)


# ─────────────────────────────────────────────
# DIBUJO DEL TÍTULO PRINCIPAL
# Renderizado manual con pygame.font para control
# total del color. Línea decorativa debajo.
# ─────────────────────────────────────────────
def draw_title(screen, font_title):
    surf = font_title.render(TITLE_S["text"], True, tuple(TITLE_S["color"]))
    screen.blit(surf, surf.get_rect(centerx=WIDTH // 2, y=TITLE_S["position_y"]))

    cx   = WIDTH // 2
    half = TITLE_S["divider_half_width"]
    pygame.draw.line(
        screen,
        tuple(TITLE_S["divider_color"]),
        (cx - half, TITLE_S["divider_y"]),
        (cx + half, TITLE_S["divider_y"]),
        TITLE_S["divider_thickness"],
    )


# ─────────────────────────────────────────────
# SELECTOR VISUAL DE PLANETAS
# Dibuja una fila de "tarjetas" con imagen y
# nombre para cada planeta. Resalta la selección
# actual y detecta hover/click del ratón.
# Devuelve el nombre del planeta clickeado o None.
# ─────────────────────────────────────────────
class PlanetSelector:
    def __init__(self, planet_imgs, selected):
        self.planet_names = list(PLANETS.keys())
        self.planet_imgs  = planet_imgs
        self.selected     = selected
        self.hovered      = None

        # Calcular posición X inicial para centrar todas las tarjetas
        n          = len(self.planet_names)
        total_w    = n * PS["card_width"] + (n - 1) * PS["cards_gap"]
        self.start_x = (WIDTH - total_w) // 2

        # Fuente para los nombres de planeta
        self.font_name  = pygame.font.SysFont("Arial", PS["name_font_size"], bold=True)
        self.font_title = pygame.font.SysFont("Arial", PS["title_font_size"], bold=False)

        # Pre-calcular rectángulos de cada tarjeta para hit-testing
        self._build_rects()

    def _build_rects(self):
        """Calcula y almacena el Rect de cada tarjeta."""
        self.rects = []
        x = self.start_x
        for _ in self.planet_names:
            r = pygame.Rect(x, PS["cards_y"], PS["card_width"], PS["card_height"])
            self.rects.append(r)
            x += PS["card_width"] + PS["cards_gap"]

    def handle_event(self, event):
        """Procesa eventos de ratón; devuelve nombre seleccionado o None."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = None
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.hovered = self.planet_names[i]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected = self.planet_names[i]
                    return self.selected
        return None

    def draw(self, screen):
        """Dibuja el título del selector y todas las tarjetas."""
        # Título de la sección
        title_surf = self.font_title.render(
            PS["title_text"], True, tuple(PS["title_color"])
        )
        screen.blit(title_surf, title_surf.get_rect(centerx=WIDTH // 2, y=PS["title_offset_y"]))

        for i, name in enumerate(self.planet_names):
            rect = self.rects[i]
            is_selected = (name == self.selected)
            is_hovered  = (name == self.hovered)

            # Elegir colores según estado de la tarjeta
            if is_selected:
                bg_color     = tuple(PS["color_selected_bg"])
                border_color = tuple(PS["color_selected_border"])
                name_color   = tuple(PS["color_name_selected"])
            elif is_hovered:
                bg_color     = tuple(PS["color_hover_bg"])
                border_color = tuple(PS["color_hover_border"])
                name_color   = tuple(PS["color_name_normal"])
            else:
                bg_color     = tuple(PS["color_normal_bg"])
                border_color = tuple(PS["color_normal_border"])
                name_color   = tuple(PS["color_name_normal"])

            # Fondo de la tarjeta (con borde redondeado)
            pygame.draw.rect(screen, bg_color,     rect, border_radius=PS["border_radius"])
            pygame.draw.rect(screen, border_color, rect, PS["border_thickness"], border_radius=PS["border_radius"])

            # Imagen del planeta centrada en la parte superior de la tarjeta
            img = self.planet_imgs.get(name)
            img_size = PS["img_size"]
            img_y    = rect.y + (PS["card_height"] - PS["name_height"] - img_size) // 2
            if img:
                img_rect = img.get_rect(centerx=rect.centerx, y=img_y)
                screen.blit(img, img_rect)
            else:
                # Fallback: círculo gris si no hay imagen (ej. Luna)
                cx = rect.centerx
                cy = img_y + img_size // 2
                pygame.draw.circle(screen, (150, 150, 160), (cx, cy), img_size // 2)

            # Nombre del planeta en la parte inferior de la tarjeta
            name_surf = self.font_name.render(name, True, name_color)
            name_rect = name_surf.get_rect(
                centerx=rect.centerx,
                y=rect.bottom - PS["name_height"] - 4
            )
            screen.blit(name_surf, name_rect)

            # Indicador de selección: subrayado bajo el nombre
            if is_selected:
                uy = name_rect.bottom + 2
                pygame.draw.line(
                    screen, border_color,
                    (rect.centerx - 30, uy), (rect.centerx + 30, uy), 2
                )


# ─────────────────────────────────────────────
# CONSTRUCCIÓN DEL PANEL DE CONTROLES (pygame_gui)
# Crea los campos numéricos y botón usando las
# posiciones y textos del JSON (sin dropdown,
# ya que el planeta se elige con PlanetSelector).
# ─────────────────────────────────────────────


#panel de control para modificar varibles
class ControlPanel:
    def __init__(self, x, y, titulo, valor_inicial, unidad, callback_cambio, manager):
        """
        Clase para replicar paneles de control numérico.
        
        :param x: Posición X del panel.
        :param y: Posición Y del panel.
        :param titulo: Texto del título (ej. "GRAVEDAD").
        :param valor_inicial: Valor numérico inicial.
        :param unidad: String de la unidad (ej. "M/S²", "M/S", "M").
        :param callback_cambio: Función que se ejecuta al cambiar el valor.
        :param manager: El UIManager de pygame_gui.
        """
        self.valor = valor_inicial
        self.unidad = unidad
        self.callback_cambio = callback_cambio
        
        # Contenedor principal del panel
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((x, y), (400, 100)),
            manager=manager
        )
        
        # Etiqueta del Título
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 10), (120, 30)),
            text=titulo,
            manager=manager,
            container=self.panel,
            object_id="#title"
        )
        
        # Etiqueta del Valor
        self.valor_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 45), (150, 40)),
            text=f"{self.valor:.1f} {self.unidad}",
            manager=manager,
            container=self.panel
        )
        
        # Botón Menos
        self.bton_menos = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 30), (40, 40)),
            text="-",
            manager=manager,
            container=self.panel
        )
        
        # Botón Más
        self.bton_mas = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((335, 30), (40, 40)),
            text="+",
            manager=manager,
            container=self.panel
        )

    def procesar_evento(self, event):
        """Maneja el comportamiento de los botones internos."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.bton_menos:
                self.valor -= 0.1
                self.actualizar_interfaz()
                
            elif event.ui_element == self.bton_mas:
                self.valor += 0.1
                self.actualizar_interfaz()


    def actualizar_interfaz(self):
        """Actualiza el texto en pantalla y notifica el cambio al juego."""
        self.valor_label.set_text(f"{self.valor:.1f} {self.unidad}")
        # Ejecutamos la función externa pasando el nuevo valor
        self.callback_cambio(self.valor)


def build_controls(manager, params):
    center_x  = WIDTH // 2
    control_w = CP["width"]
    x0        = center_x - control_w // 2

    # Título del panel (etiqueta decorativa)
    ui = CP["ui_title"]
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(center_x + ui["offset_x"], ui["offset_y"], ui["width"], ui["height"]),
        text=ui["text"],
        manager=manager,
    )

    # Campo: velocidad inicial
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(x0, CP["v0_label"]["offset_y"], control_w, CP["v0_label"]["height"]),
        text=CP["v0_label"]["text"],
        manager=manager,
    )
    entry_v0 = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(x0, CP["v0_entry"]["offset_y"], control_w, CP["v0_entry"]["height"]),
        manager=manager,
    )
    entry_v0.set_text(str(params["v0"]))

    # Campo: ángulo de lanzamiento
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(x0, CP["angle_label"]["offset_y"], control_w, CP["angle_label"]["height"]),
        text=CP["angle_label"]["text"],
        manager=manager,
    )
    entry_angle = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(x0, CP["angle_entry"]["offset_y"], control_w, CP["angle_entry"]["height"]),
        manager=manager,
    )
    entry_angle.set_text(str(params["angle"]))

    # Campo: velocidad del viento
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(x0, CP["wind_label"]["offset_y"], control_w, CP["wind_label"]["height"]),
        text=CP["wind_label"]["text"],
        manager=manager,
    )
    entry_wind = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(x0, CP["wind_entry"]["offset_y"], control_w, CP["wind_entry"]["height"]),
        manager=manager,
    )
    entry_wind.set_text(str(params["wind"]))

    # Botón continuar
    btn = CP["continue_button"]
    button_continue = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(x0, btn["offset_y"], control_w, btn["height"]),
        text=btn["text"],
        manager=manager,
    )

    # Etiqueta de estado/feedback
    sl = CP["status_label"]
    status_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(x0, sl["offset_y"], control_w, sl["height"]),
        text=sl["text_default"],
        manager=manager,
    )

    return {
        "entry_v0":       entry_v0,
        "entry_angle":    entry_angle,
        "entry_wind":     entry_wind,
        "button_continue": button_continue,
        "status_label":   status_label,
    }


# ─────────────────────────────────────────────
# BUCLE PRINCIPAL
# Inicializa pygame, pre-carga assets, construye
# el selector visual y los controles numéricos.
# Itera procesando eventos, actualizando la UI
# y dibujando cada frame.
# ─────────────────────────────────────────────
def main():
    pygame.init()
    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WIN["title"])
    clock   = pygame.time.Clock()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Fuente del título principal
    font_title = pygame.font.SysFont(
        TITLE_S["font_family"], TITLE_S["font_size"], bold=TITLE_S["bold"]
    )

    # Pre-carga de imágenes (planeta selector + decorativas)
    planet_imgs, deco_imgs = preload_assets()

    # Campo de estrellas y tiempo acumulado para el parpadeo
    stars        = gen_stars()
    time_elapsed = 0.0

    # Estado inicial desde el JSON
    params   = dict(DEFAULTS)
    selector = PlanetSelector(planet_imgs, params["planet"])
    widgets  = build_controls(manager, params)

    # ── Bucle de eventos ──────────────────────
    running = True
    while running:
        time_delta    = clock.tick(FPS) / 1000.0
        time_elapsed += time_delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # El selector consume el evento primero (hover + click de tarjeta)
            clicked = selector.handle_event(event)
            if clicked:
                params["planet"] = clicked  # actualizar planeta seleccionado
                print(f"Planeta seleccionado: {clicked}")
            # Botón "Continuar": leer campos y salir si son válidos
            

            if (
                event.type == pygame_gui.UI_BUTTON_PRESSED
                and event.ui_element == widgets["button_continue"]
            ):
                try:
                    params["v0"]      = float(widgets["entry_v0"].get_text())
                    params["angle"]   = float(widgets["entry_angle"].get_text())
                    params["wind"]    = float(widgets["entry_wind"].get_text())
                    params["gravity"] = PLANETS[params["planet"]].get("g", 9.8)

                    widgets["status_label"].set_text(
                        f"Planeta: {params['planet']}, v0={params['v0']}, "
                        f"ang={params['angle']}, viento={params['wind']}"
                    )
                    return  # Pasar a la pantalla de simulación
                except ValueError:
                    widgets["status_label"].set_text(CP["status_label"]["text_error"])

            manager.process_events(event)

        # ── Actualización de lógica de UI ─────
        manager.update(time_delta)

        # ── Dibujo del frame ──────────────────
        draw_background(screen, stars, time_elapsed, deco_imgs)
        draw_title(screen, font_title)
        selector.draw(screen)       # selector visual de planetas
        manager.draw_ui(screen)     # campos numéricos y botón (pygame_gui)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
