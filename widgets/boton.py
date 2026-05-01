import pygame
import math

pygame.init()
screenwidth,screenheight = 800,500
fps = pygame.time.Clock()
screen = pygame.display.set_mode((screenwidth,screenheight))

color = [250,0,0]
screen.fill((250,250,250))

running = True

class boton:
    def __init__(self, x, y, width, height, color,hcolor, texto,htexto, ctexto):#hcolor es hover lo mismo con htexto
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hcolor = hcolor
        self.texto = texto
        self.htexto = htexto
        self.ctexto = ctexto
        self.bpresionado = False
        self.font = pygame.font.SysFont(None, 30)
        self.drawcolor = color
        self.drawtext = texto
        
    def dibujar(self, screen):
        pygame.draw.rect(screen, self.drawcolor, self.rect, 0, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0,), self.rect, 5, border_radius=20)
        
        texto_renderizar = self.font.render(self.drawtext, True, self.ctexto) #renderizar el texto
        
        texto_centrado = texto_renderizar.get_rect(center = self.rect.center) #centrar
        
        screen.blit(texto_renderizar, texto_centrado)
        
        
        
        
    def presionado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if not self.bpresionado:
                    self.drawcolor = self.hcolor
                    self.drawtext = self.htexto
                    self.bpresionado = 1
                else :
                    self.drawcolor=color
                    self.drawtext = self.texto
                    self.bpresionado = 0


        """if self.bpresionado:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print("1")
                    self.color = color
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.bpresionado = False

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print("2")
                    self.color = (0, 200, 0)
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.bpresionado = True"""


boton_1 = boton(screenwidth-150, screenheight-50, 150, 50, (255, 0, 0),(0,250,0), "Lanzar","Parar", (255, 255, 255))

while running:
    pygame.display.flip()
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(event.key)
        boton_1.presionado(event)
    boton_1.dibujar(screen)
        

    