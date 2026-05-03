import pygame
import sys
import widgets

pygame.init()
time = pygame.time.Clock()
dtime = 0
screenwidth,screenheight = 800,500
screen = pygame.display.set_mode((800,500),pygame.RESIZABLE)
pygame.display.set_caption("simulador de lanzamiento de proyectiles")
newtons = 0
gravedad = 9.8

running = True
fisicsrunning = False
escala = 10 #10 pixeles equivale a 1 metro

imghumano = pygame.image.load("assets/img/humano.png").convert_alpha()
imgpiedra = pygame.image.load("assets/img/piedra.png").convert_alpha()
imgnave = pygame.image.load("assets/img/nave.png").convert_alpha()

pygame.display.set_icon(imgnave)

class proyectil:#separacion en clases, procesar por separado las fisicas y los graficos, luego se unen con una clase principal
    def __init__(self,screen,x,y,width,height,masa,color,img):
        self.screen = screen
        self.posicion = pygame.math.Vector2(x,y)
        self.tamaño = pygame.math.Vector2(width,height)
        self.masa = masa
        self.color = color
        self.img = pygame.transform.scale(img, (self.tamaño.x*(escala), self.tamaño.y*(escala))) if img else False

        self.fisicas = fsproyecctil(self.posicion,self.tamaño,self.masa,self.screen)
        self.graficos = grproyectil(self.color,escala)
    def draw(self):
        if self.img:
            if lanzar.estado():
                self.graficos.dibujarConImagen(self.screen,self.fisicas.actualizar(),self.tamaño,self.img)
            else:
                self.graficos.dibujarConImagen(self.screen,self.posicion,self.tamaño,self.img)
        else:
            if lanzar.estado():
                self.graficos.dibujar(self.screen,self.fisicas.actualizar(),self.tamaño,self.color)
            else:
                self.graficos.dibujar(self.screen,self.posicion,self.tamaño,self.color)
    
class fsproyecctil:
    def __init__ (self,posicion,tamaño,masa,mundo):
        self.posicion = posicion
        self.tamaño = tamaño
        self.masa = masa
        self.mundo = mundo# el mundo es la pantalla pero desde la perspectiva fisica
        self.suelo = False
        self.velocidad = pygame.math.Vector2(0,0)

    def fuerzax(self,fuerza):
        self.velocidad.x += (fuerza/self.masa)
    def fuerzay(self,fuerza):
        self.velocidad.y -= (fuerza/self.masa)
        self.suelo = False


    def apigravedad(self):#estoy pensando en separar las principales caracteristicas fisicar en distintos modulos para mejor depuracion del simulardor
        limite_suelo = self.mundo.get_height() / escala

        if not self.suelo:
            self.velocidad.y += gravedad*dtime
            self.posicion += self.velocidad * dtime

        if self.posicion.y + self.tamaño.y >= limite_suelo:
            self.posicion.y = limite_suelo - self.tamaño.y
            self.velocidad.y = 0
            self.suelo = True
        else:
            self.suelo = False

    def actualizar(self):
        self.apigravedad()
        return self.posicion
class grproyectil:
    def __init__(self,color,escala):
        self.color = color
        self.escala = escala
    def dibujar(self,screen,posicion,tamaño,color):
        pygame.draw.rect(screen,color,rect=[posicion.x*self.escala,posicion.y*self.escala,tamaño.x*self.escala,tamaño.y*self.escala])

    def dibujarConImagen(self,screen,posicion,tamaño,img):
        rect = (posicion.x*self.escala,posicion.y*self.escala)
        screen.blit(img, rect)



proyectilv1 = proyectil(screen,4,46,4,4,1,(250,0,0),False)#inicializo el v1 (pantalla,x(metro respecto al origen),y(metros respecto al origen),width(m),height(m),masa(kg),)
proyectilv2 = proyectil(screen,4,46,4,4,2,(0,0,250),imgpiedra)
lanzar = widgets.boton(screen,screenwidth, screenheight, 150, 50, (0, 250, 0),(250, 0, 0), "Lanzar","Parar", (255, 255, 255),False,False)


while running:
    screen.fill((250,250,250))
    dtime = 1/time.get_fps() if time.get_fps() >0 else 0

    proyectilv1.draw()
    proyectilv2.draw()

    lanzar.dibujar()


    pygame.display.flip()
    screen.get_height()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    
                newtons += 1
                print(f"Valor de fuerza: {newtons}")
            if event.key == pygame.K_DOWN:  
                newtons -= 1
                print(f"Valor de fuerza: {newtons}")
            if event.key == pygame.K_RIGHT:    
                gravedad += 1
                print(f"Valor de gravedad: {gravedad}")
            if event.key == pygame.K_LEFT:  
                gravedad -= 1
                print(f"Valor de gravedad: {gravedad}")

        lanzar.presionado(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
    time.tick(60)