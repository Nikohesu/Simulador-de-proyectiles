import pygame
class boton:
    def __init__(self,screen, x, y, width, height, color_off, color_on, text_off, text_on, color_text, def_off, def_on):#hcolor es hover lo mismo con htexto
        self.screen = screen
        self.rect = pygame.Rect(x-width, y-height, width, height)
        self.color_off = color_off
        self.color_on = color_on
        self.text_off = text_off
        self.text_on = text_on
        self.color_text = color_text
        self.boton_state = False
        self.font = pygame.font.SysFont(None, 30)
        self.drawcolor = color_off
        self.drawtext = text_off

        #funciones que se activan al presionar el boton
        self.def_on = def_on
        self.def_off = def_off
        self.fstate = False
        
    def dibujar(self):

        pygame.draw.rect(self.screen, self.drawcolor, self.rect, 0, border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0,), self.rect, 5, border_radius=20)
        #dejar en contenedores separados: uno para el background y uno para el borde
        
        texto_renderizar = self.font.render(self.drawtext, True, self.color_text) #renderizar el texto
        texto_centrado = texto_renderizar.get_rect(center = self.rect.center) #centrar
        
        self.screen.blit(texto_renderizar, texto_centrado)
        
    def presionado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if not self.boton_state:
                    self.drawcolor = self.color_on
                    self.drawtext = self.text_on
                    self.boton_state = True #cambia el estado general del boton a ON (encendido)
                    
                    if self.def_on:
                        self.def_on()
                    
                        

                else :
                    self.drawcolor=self.color_off
                    self.drawtext = self.text_off
                    self.boton_state = False
                    if self.def_off:
                        self.def_off()

    def estado (self):
        return self.boton_state                
  

