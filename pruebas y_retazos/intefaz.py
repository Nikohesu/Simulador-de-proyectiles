import pygame
import pygame_gui
import math
import sys
import random

#  Configuración general 
WIDTH, HEIGHT = 1280, 720
FPS = 60

PLANETS = {
    "Tierra":  {"g": 9.81,  "sky": (30,  80,  160), "ground": (34,  139, 34)},
    "Luna":    {"g": 1.62,  "sky": (10,  10,  30),  "ground": (120, 120, 120)},
    "Marte":   {"g": 3.72,  "sky": (160, 60,  20),  "ground": (140, 50,  10)},
    "Júpiter": {"g": 24.79, "sky": (100, 70,  40),  "ground": (180, 120, 60)},
    "Venus":   {"g": 8.87,  "sky": (160, 110, 30),  "ground": (200, 140, 40)},
    "Saturno": {"g": 10.44, "sky": (100, 90,  60),  "ground": (170, 150, 100)},
}

GROUND_Y = HEIGHT - 80

SCENE_PARAMS = 0
SCENE_LAUNCH = 1

# Estrellas
def gen_stars(n=220):
    return [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
             random.randint(1, 3), random.randint(140, 255)) for _ in range(n)]

def draw_stars(surface, stars, t):
    for (x, y, r, base_a) in stars:
        flicker = int(base_a * (0.75 + 0.25 * math.sin(t * 2 + x)))
        col = (flicker, flicker, flicker)
        pygame.draw.circle(surface, col, (x, y), r)

#  Física 
def simulate(v0, angle_rad, wind, g, steps=3000, dt=0.04):
    vx = v0 * math.cos(angle_rad) + wind
    vy = v0 * math.sin(angle_rad)
    x, y = 0.0, 0.0
    pts = [(x, y)]
    y_max = 0.0
    for _ in range(steps):
        vy_new = vy - g * dt
        x += vx * dt
        y += vy_new * dt
        vy = vy_new
        if y < 0:
            if vy != 0:
                x += vx * (-y / vy) * dt
            pts.append((x, 0.0))
            break
        y_max = max(y_max, y)
        pts.append((x, y))
    return pts, y_max, pts[-1][0]

def world_to_screen(pts, x_max, y_max):
    margin_l, margin_r = 80, 80
    margin_top = 60
    avail_w = WIDTH - margin_l - margin_r
    avail_h = GROUND_Y - margin_top
    scale_x = avail_w / max(x_max, 1)
    scale_y = avail_h / max(y_max, 1)
    scale   = min(scale_x, scale_y)
    return [(margin_l + int(x * scale), GROUND_Y - int(y * scale)) for (x, y) in pts]

# Helpers UI
def kill_all(elements):
    for el in elements:
        if el is not None:
            el.kill()

# 
#  MAIN
# 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🚀 Simulador de Proyectil Planetario")
    clock  = pygame.time.Clock()

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    stars = gen_stars(260)
    t_star = 0.0

    font_title  = pygame.font.SysFont("Arial", 42, bold=True)
    font_label  = pygame.font.SysFont("Arial", 18, bold=True)
    font_small  = pygame.font.SysFont("Arial", 15, bold=True)
    font_info   = pygame.font.SysFont("Arial", 20, bold=True)

    #  Escenas
    scene       = SCENE_PARAMS
    params      = {"planet": "Tierra", "v0": 50.0, "angle": 45.0, "wind": 0.0}
    traj_screen = []
    y_max_val   = 0.0
    x_max_val   = 0.0
    simulated   = False
    anim_idx    = 0
    anim_run    = False
    ANIM_SPEED  = 4

    #  widgets
    widgets_s1 = []   # escena 1
    widgets_s2 = []   # escena 2

    
    #   ESCENA 1
    
    def build_scene1():
        nonlocal widgets_s1
        kill_all(widgets_s1)
        widgets_s1.clear()

        CX = WIDTH // 2   # centro horizontal
        W  = 360          # ancho de los controles
        x0 = CX - W // 2

        lbl_tit = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(CX - 260, 60, 520, 55),
            text="🪐  SIMULADOR DE PROYECTIL PLANETARIO",
            manager=manager
        )

        lbl_p = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(x0, 160, W, 28),
            text="Planeta del lanzamiento:",
            manager=manager
        )
        dd_planet = pygame_gui.elements.UIDropDownMenu(
            options_list=list(PLANETS.keys()),
            starting_option=params["planet"],
            relative_rect=pygame.Rect(x0, 192, W, 40),
            manager=manager
        )

        lbl_v = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(x0, 252, W, 28),
            text="Velocidad inicial (m/s):",
            manager=manager
        )
        ent_v0 = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(x0, 284, W, 40),
            manager=manager
        )
        ent_v0.set_text(str(params["v0"]))

        lbl_a = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(x0, 344, W, 28),
            text="Ángulo inicial (grados):",
            manager=manager
        )
        ent_ang = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(x0, 376, W, 40),
            manager=manager
        )
        ent_ang.set_text(str(params["angle"]))

        lbl_w = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(x0, 436, W, 28),
            text="Velocidad del viento (m/s):",
            manager=manager
        )
        ent_wind = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(x0, 468, W, 40),
            manager=manager
        )
        ent_wind.set_text(str(params["wind"]))

        btn_next = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(x0, 548, W, 52),
            text="Continuar  ▶️",
            manager=manager
        )

        widgets_s1 = [lbl_tit, lbl_p, dd_planet,
                      lbl_v, ent_v0,
                      lbl_a, ent_ang,
                      lbl_w, ent_wind,
                      btn_next]
        return dd_planet, ent_v0, ent_ang, ent_wind, btn_next

   
    #   ESCENA 2
    
    def build_scene2():
        nonlocal widgets_s2
        kill_all(widgets_s2)
        widgets_s2.clear()

        PANEL_W = 300
        px = WIDTH - PANEL_W + 10
        pw = PANEL_W - 20

        lbl_tit = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 14, pw, 36),
            text="🚀 PARÁMETROS",
            manager=manager
        )
        lbl_pla = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 60, pw, 26),
            text=f"🌍 Planeta: {params['planet']}",
            manager=manager
        )
        lbl_gra = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 90, pw, 26),
            text=f"⬇️  Gravedad: {PLANETS[params['planet']]['g']} m/s²",
            manager=manager
        )
        lbl_v0r = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 120, pw, 26),
            text=f"⚡ Vel. inicial: {params['v0']} m/s",
            manager=manager
        )
        lbl_angr = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 150, pw, 26),
            text=f"📐 Ángulo: {params['angle']}°",
            manager=manager
        )
        lbl_windr = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 180, pw, 26),
            text=f"💨 Viento: {params['wind']} m/s",
            manager=manager
        )

        sep = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 218, pw, 20),
            text="────────────────",
            manager=manager
        )

        btn_launch = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(px, 250, pw, 52),
            text="🚀  Lanzar proyectil",
            manager=manager
        )
        btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(px, 316, pw, 44),
            text="◀️  Volver",
            manager=manager
        )

        # Resultados (inicialmente vacíos)
        lbl_res_tit = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 390, pw, 26),
            text="── Resultados ──",
            manager=manager
        )
        lbl_ymax = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 422, pw, 26),
            text="Y máx: --",
            manager=manager
        )
        lbl_xmax = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(px, 454, pw, 26),
            text="Alcance: --",
            manager=manager
        )

        widgets_s2 = [lbl_tit, lbl_pla, lbl_gra, lbl_v0r, lbl_angr, lbl_windr,
                      sep, btn_launch, btn_back, lbl_res_tit, lbl_ymax, lbl_xmax]
        return btn_launch, btn_back, lbl_ymax, lbl_xmax

   
    #  Inicializar escena 1
 
    dd_planet, ent_v0, ent_ang, ent_wind, btn_next = build_scene1()
    btn_launch = btn_back = lbl_ymax = lbl_xmax = None

    #  Bucle principal
    running = True
    while running:
        dt_ms = clock.tick(FPS)
        dt_s  = dt_ms / 1000.0
        t_star += dt_s

        #  Eventos 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #  Botones 
            if event.type == pygame_gui.UI_BUTTON_PRESSED:

                # Escena 1 → 2
                if scene == SCENE_PARAMS and event.ui_element == btn_next:
                    # Leer parámetros
                    sel = dd_planet.selected_option
                    params["planet"] = sel[0] if isinstance(sel, (list, tuple)) else sel
                    try:
                        params["v0"]    = float(ent_v0.get_text())
                        params["angle"] = float(ent_ang.get_text())
                        params["wind"]  = float(ent_wind.get_text())
                    except ValueError:
                        pass
                    # Cambiar escena
                    kill_all(widgets_s1)
                    widgets_s1.clear()
                    btn_launch, btn_back, lbl_ymax, lbl_xmax = build_scene2()
                    scene     = SCENE_LAUNCH
                    simulated = False
                    traj_screen.clear()

                # Escena 2: lanzar
                elif scene == SCENE_LAUNCH and event.ui_element == btn_launch:
                    angle_rad = math.radians(params["angle"])
                    g = PLANETS[params["planet"]]["g"]
                    pts, y_max_val, x_max_val = simulate(
                        params["v0"], angle_rad, params["wind"], g)
                    if x_max_val > 0 and y_max_val > 0:
                        traj_screen[:] = world_to_screen(pts, x_max_val, y_max_val)
                    else:
                        traj_screen.clear()
                    lbl_ymax.set_text(f"Y máx: {y_max_val:.1f} m")
                    lbl_xmax.set_text(f"Alcance: {x_max_val:.1f} m")
                    simulated = True
                    anim_idx  = 0
                    anim_run  = True

                # Escena 2 → 1
                elif scene == SCENE_LAUNCH and event.ui_element == btn_back:
                    kill_all(widgets_s2)
                    widgets_s2.clear()
                    dd_planet, ent_v0, ent_ang, ent_wind, btn_next = build_scene1()
                    scene     = SCENE_PARAMS
                    simulated = False
                    traj_screen.clear()

            manager.process_events(event)

        manager.update(dt_s)

        
        #  Fondo negro
       
        screen.fill((5, 5, 18))   

        # ESCENA 1: fondo espacio
        if scene == SCENE_PARAMS:
            draw_stars(screen, stars, t_star)

            # Título decorativo
            title_surf = font_title.render("SIMULADOR DE PROYECTIL", True, (200, 220, 255))
            screen.blit(title_surf, title_surf.get_rect(centerx=WIDTH // 2, y=10))

            # Línea decorativa bajo el título
            pygame.draw.line(screen, (80, 120, 220),
                             (WIDTH // 2 - 300, 68), (WIDTH // 2 + 300, 68), 2)

            #  planetas pequeños
            pygame.draw.circle(screen, (30, 100, 200), (120, 130), 55)   # azul
            pygame.draw.circle(screen, (15, 60, 140),  (120, 130), 55, 3)
            pygame.draw.circle(screen, (200, 80, 20),  (1160, 580), 40)  # rojo
            pygame.draw.circle(screen, (120, 50, 10),  (1160, 580), 40, 3)

        # ESCENA 2: cielo y suelo del planeta 
        else:
            PANEL_W = 300
            pdata = PLANETS[params["planet"]]
            sky   = pdata["sky"]
            gnd   = pdata["ground"]

            # cielo
            view_w = WIDTH - PANEL_W
            for row in range(GROUND_Y):
                ratio = row / GROUND_Y
                r = int(sky[0] + (0 - sky[0]) * ratio * 0.6)
                g = int(sky[1] + (0 - sky[1]) * ratio * 0.6)
                b = int(sky[2] + (0 - sky[2]) * ratio * 0.6)
                pygame.draw.line(screen, (max(0,r), max(0,g), max(0,b)),
                                 (0, row), (view_w, row))

            # Suelo
            pygame.draw.rect(screen, gnd, (0, GROUND_Y, view_w, HEIGHT - GROUND_Y))
            pygame.draw.line(screen, (255, 255, 255), (0, GROUND_Y), (view_w, GROUND_Y), 2)

            # Panel lateral 
            panel_surf = pygame.Surface((PANEL_W, HEIGHT), pygame.SRCALPHA)
            panel_surf.fill((10, 10, 30, 210))
            screen.blit(panel_surf, (WIDTH - PANEL_W, 0))

            # Trayectoria 
            if simulated and len(traj_screen) > 1:
                # Línea fantasma completa
                pygame.draw.lines(screen, (180, 180, 180), False, traj_screen, 1)

                # Avanzar animación
                if anim_run:
                    anim_idx += ANIM_SPEED
                    if anim_idx >= len(traj_screen):
                        anim_idx = len(traj_screen) - 1
                        anim_run = False

                # Trayectoria animada
                if anim_idx > 1:
                    pygame.draw.lines(screen, (255, 220, 50), False,
                                      traj_screen[:anim_idx + 1], 3)

                # Proyectil
                px2, py2 = traj_screen[anim_idx]
                pygame.draw.circle(screen, (255, 80, 60), (px2, py2), 11)
                pygame.draw.circle(screen, (255, 210, 200), (px2, py2), 6)

                # Etiquetas finales
                if not anim_run:
                    top_pt = min(traj_screen, key=lambda p: p[1])
                    pygame.draw.line(screen, (100, 255, 180),
                                     (top_pt[0], GROUND_Y), top_pt, 1)
                    lbl = font_small.render(f"Ymax = {y_max_val:.1f} m",
                                            True, (100, 255, 180))
                    screen.blit(lbl, (top_pt[0] + 6, top_pt[1] - 18))

                    end_pt = traj_screen[-1]
                    lbl2 = font_small.render(f"Xmax = {x_max_val:.1f} m",
                                             True, (255, 210, 80))
                    screen.blit(lbl2, (max(4, end_pt[0] - 90), end_pt[1] - 22))

            # Info planeta arriba izq.
            info = font_info.render(
                f"{params['planet']}  |  g = {PLANETS[params['planet']]['g']} m/s²",
                True, (220, 230, 255))
            screen.blit(info, (10, 10))

        #  GUI encima 
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()