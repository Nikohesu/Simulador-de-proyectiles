import pygame
import sys

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arrastrar objeto con el mouse")
reloj = pygame.time.Clock()

# Definimos el objeto (un cuadrado de 100x100 píxeles)
objeto_rect = pygame.Rect(350, 250, 100, 100)
color = (100, 250, 100)

# Variables de control para el arrastre
se_esta_arrastrando = False
desfase_x = 0
desfase_y = 0

while True:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Al presionar el botón del mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Clic izquierdo
                # Si el clic fue DENTRO del objeto, activamos el arrastre
                if objeto_rect.collidepoint(mouse_pos):
                    se_esta_arrastrando = True
                    # Calculamos la distancia entre el mouse y la esquina del objeto
                    desfase_x = objeto_rect.x - mouse_pos[0]
                    desfase_y = objeto_rect.y - mouse_pos[1]

        # Al soltar el botón del mouse
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                se_esta_arrastrando = False

    # Si el arrastre está activo, actualizamos la posición del objeto
    if se_esta_arrastrando:
        objeto_rect.x = mouse_pos[0] + desfase_x
        objeto_rect.y = mouse_pos[1] + desfase_y

    # Dibujar en pantalla
    pantalla.fill((30, 30, 30))
    pygame.draw.rect(pantalla, color, objeto_rect)
    pygame.display.flip()
    
    reloj.tick(60)