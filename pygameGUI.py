import pygame
import pygame_gui as gui
import sys

pygame.init()
fps = pygame.time.Clock()
screenWidth, screenHeight = 800, 600

screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption('Pygame GUI ')


#Uso de la libreria del GUI
manager = gui.UIManager((screenWidth, screenHeight), "theme.json") #El segundo parametro es el tema, se puede crear uno personalizado o usar los que vienen por defecto
boton_test = gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 50), (200, 60)),
    text='Prueba',
    manager=manager,
    object_id='#mi_boton' # <--- Forzamos este ID
)

running = True
while running:

    # time_delta es el tiempo que pasó desde el último frame (útil para animaciones/updates)
    time_delta = fps.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        # Pasar los eventos al mánager para que detecte hovers, clics, etc.
        manager.process_events(event)
        
        # Detectar eventos específicos de la GUI (como una función callback en JS)
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == boton_test:
                print("¡Acción de guardar ejecutada!")
    manager.update(time_delta)
    # Dibujar la escena
    screen.fill((30, 30, 30)) # Fondo de la pantalla (background-color del body)
    
    manager.draw_ui(screen)   # Dibuja todas las capas de la GUI encima del fondo

    pygame.display.flip() # Actualiza la pantalla completa (similar a update() pero más eficiente para toda la pantalla)    
    #pygame.display.update()
    fps.tick(60)
            
        