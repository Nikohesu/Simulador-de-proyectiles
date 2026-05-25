import pygame
import sys
import widgets
import math

pygame.init()
time = pygame.time.Clock()
dtime = 0
screenwidth,screenheight = 800,500
screen = pygame.display.set_mode((800,500),pygame.RESIZABLE)
pygame.display.set_caption("simulador de lanzamiento de proyectiles")


#variables globales que afectan a todos los proyectiles
gravedad = 9.8
escala = 10 #10 pixeles equivale a 1 metro
viento = 3 #velocidad del viento m/s, no se tiene en cuenta el volumen de los proyectiles

#guarda los proyecctiles creados para luego poder reiniciarlos o editarlos
proyectiles = []
running = True

#assets
imghumano = pygame.image.load("assets/img/humano.png").convert_alpha()
imgpiedra = pygame.image.load("assets/img/piedra.png").convert_alpha()
imgnave = pygame.image.load("assets/img/nave.png").convert_alpha()

pygame.display.set_icon(imgnave)

#vairables de lanzamiento con inferencia global
angulo = 45 #angulo de lanzamiento
newtons = 10 #fuerza de lanzamiento
#son para evitar que se tengan que realizar multiples barras para cambio de variables
#estas versiones de la variables globales permiten tener una sola barra para cambiar el valor de las locales que son la que eestan en las clasesd

active_proyectil = None

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
        proyectil.fisicas.lanzamientoCA(angulo)

def lanzarActivo():
    if active_proyectil is not None:
        active_proyectil.fisicas.lanzamientoCA(angulo)



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

        global active_proyectil
        active_proyectil = self

    def draw(self):

        if lanzar.boton_state:
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
                    if self.select:
                        self.border = False
                        self.select = False
                        print("edicion desactivada para proyectil ")
                    else :
                        self.border = True
                        self.select = True
                        print("edicion activada para proyectil ")

class fsproyecctil:
    def __init__ (self,posicion,tamaño,masa,mundo):
        self.posicion = posicion
        self.tamaño = tamaño
        self.masa = masa
        self.mundo = mundo# el mundo es la pantalla pero desde la perspectiva fisica
        self.suelo = False
        self.velocidad = pygame.math.Vector2(0,0)


    def lanzamientoCA (self,angulo):
        print("lanzamiento ejecutado con angulo: ", angulo)
        angulo = math.radians(angulo)
        vx = (newtons / self.masa) * math.cos(angulo)
        vy = (newtons / self.masa) * math.sin(angulo)
        print ("velocidad en x: ",vx)
        print("velocidad en y:", vy)
        self.velocidad.x += vx
        self.velocidad.y -= vy
        self.suelo = False


    def apigravedad(self):#estoy pensando en separar las principales caracteristicas fisicar en distintos modulos para mejor depuracion del simulardor
        limite_suelo = self.mundo.get_height() / escala

        if not self.suelo:
            self.velocidad.y += gravedad*dtime
            self.velocidad.x -= viento*dtime

        if self.posicion.y + self.tamaño.y >= limite_suelo:
            self.posicion.y = limite_suelo - self.tamaño.y
            self.velocidad.x = 0
            self.suelo = True
        else:
            self.suelo = False

    def act_posicion (self):#funcion que actualiza las posiciones segun la velocidad actual
        self.posicion += self.velocidad*dtime

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

proyectiles.append(proyectil(screen,0,30,4,4,1,(250,0,0),imghumano))#inicializo el v1 (pantalla,x(metro respecto al origen),y(metros respecto al origen),width(m),height(m),masa(kg),)
proyectiles.append(proyectil(screen,0,45,4,4,2,(0,0,250),imgpiedra))
proyectiles.append(proyectil(screen, 0, 45, 4, 4, 1, (250, 0, 0),imgnave))

lanzar = widgets.boton(screen,1, 1, 150, 50, (0, 250, 0),(250, 0, 0), "Lanzar","Parar", (255, 255, 255),reiniciar,lanzarTodos)



while running:
    screen.fill((250,250,250))
    dtime = 1/time.get_fps() if time.get_fps() >0 else 0

    for i in range(len(proyectiles)):
        proyectiles[i].draw()

    lanzar.dibujar()
    lanzar.position_resize()


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
            if event.key == pygame.K_a:
                angulo += 5
                print(f"Valor del angulo : ", angulo)
            if event.key == pygame.K_d:
                angulo -= 5
                print(f"Valor del angulo : ", angulo)
            if event.key == pygame.K_w:
                viento += 1
                print(f"Valor del viento : ", viento)
            if event.key == pygame.K_s:
                viento -= 1
                print(f"Valor del viento : ", viento)
        lanzar.presionado(event)
        for i in range(len(proyectiles)):
            proyectiles[i].seleccionar(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
    time.tick(60)