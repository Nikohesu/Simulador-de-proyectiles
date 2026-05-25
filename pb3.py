import pygame
import pygame_gui

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


# --- CONFIGURACIÓN DE PYGAME ---
pygame.init()
pygame.display.set_caption("Control de Parámetros con Temas JSON")
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#05050a'))

manager = pygame_gui.UIManager((800, 600), 'styles3.json')

# --- VARIABLES GLOBALES DEL JUEGO ---
# Estado que tus físicas o simulaciones van a leer
variables_entorno = {
    "gravedad": 9.8,
    "viento": 2.5
}

# --- FUNCIONES CALLBACK ---
# Estas funciones se ejecutan automáticamente cuando tocas los botones + o -
def actualizar_gravedad(nuevo_valor):
    variables_entorno["gravedad"] = nuevo_valor
    print(f"Gravedad actualizada en el motor: {variables_entorno['gravedad']:.1f}")

def actualizar_viento(nuevo_valor):
    variables_entorno["viento"] = nuevo_valor
    print(f"Viento actualizado en el motor: {variables_entorno['viento']:.1f}")


# --- INSTANCIACIÓN DE LOS OBJETOS ---
# Creamos el panel de Gravedad
panel_gravedad = ControlPanel(
    x=200, y=150, 
    titulo="GRAVEDAD", 
    valor_inicial=variables_entorno["gravedad"], 
    unidad="M/S²", 
    callback_cambio=actualizar_gravedad, 
    manager=manager
)

# Creamos el panel de Viento (desplazado en Y hacia abajo)
panel_viento = ControlPanel(
    x=200, y=300, 
    titulo="VIENTO", 
    valor_inicial=variables_entorno["viento"], 
    unidad="M/S", 
    callback_cambio=actualizar_viento, 
    manager=manager
)


# --- BUCLE PRINCIPAL ---
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
        # Pasamos los eventos a cada panel para que controlen sus respectivos botones
        panel_gravedad.procesar_evento(event)
        panel_viento.procesar_evento(event)
                
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()