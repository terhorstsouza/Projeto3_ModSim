#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:18:40 2018

Projeto 3 de ModSim

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

''' Dados do Salto '''
Ts = [0, 9.375, 18.75, 26.875, 33.75, 40.000000000000014, 47.5, 53.75, 
      60.625000000000014, 68.12500000000001, 76.25000000000001, 
      85.00000000000001, 95.00000000000004, 106.87500000000001,
      119.37500000000001, 134.375, 151.875, 166.25000000000006, 
      183.75000000000006, 209.37500000000006, 226.25000000000006, 
      245.62500000000006, 265.00000000000006, 286.8750000000001]

S = [39056.6037735849, 38773.58490566038, 37452.83018867925, 35754.71698113207,
     33962.264150943396, 31981.132075471694, 29339.62264150943, 
     27358.490566037734, 25094.33962264151, 23018.867924528302,
     21037.735849056604, 19339.62264150943, 17641.509433962263,
     15943.396226415094, 14528.301886792455, 12924.528301886796,
     11320.754716981133, 10188.67924528302, 8867.92452830189, 7075.471698113208,
     6037.735849056611, 4905.660377358494, 3867.9245283018827,
     2641.5094339622665]

Tv = [0, 3.115264797507784, 5.607476635514018, 8.099688473520253, 
     10.59190031152648, 13.084112149532714, 15.576323987538949,
     18.691588785046733, 21.183800623052967, 24.29906542056076, 
     27.414330218068535, 31.77570093457944, 34.89096573208723,
     39.875389408099686, 46.72897196261683, 54.82866043613708, 
     60.436137071651096, 64.797507788162, 69.15887850467291, 74.14330218068537, 
     80.37383177570095, 87.2274143302181, 95.95015576323988, 107.16510903426791,
     122.1183800623053, 139.56386292834893, 158.8785046728972,
     179.43925233644862, 199.37694704049846, 218.69158878504675, 
     238.62928348909662, 260.43613707165116, 282.86604361370723] 

V = [0, 26.506024096385545, 51.80722891566268, 79.51807228915663,
     101.20481927710841, 125.30120481927713, 150.6024096385542,
     179.51807228915663, 203.6144578313253, 228.91566265060237,
     255.42168674698792, 283.13253012048193, 304.8192771084337,
     327.71084337349396, 342.16867469879514, 327.71084337349396,
     302.4096385542168, 279.5180722891566, 254.2168674698795,
     225.30120481927707, 197.59036144578312, 172.28915662650599,
     148.19277108433732, 127.71084337349396, 108.43373493975906,
     93.97590361445788, 81.92771084337352, 73.49397590361451,
     67.46987951807228, 62.650602409638566, 59.03614457831327,
     55.42168674698797, 51.80722891566268]


''' Parâmetros '''

# Encontrado na literatura:
peso_pessoa = 73 #kg

peso_traje = 45 #kg

peso = peso_pessoa + peso_traje # Massa total do Felix Baumgartner

# Encontrado na Literatura
area_pessoa = 0.18 # Mergulhando de cabeça

area_paraquedas = 25 # Informação encontrada em Red Bull Stratos

altura_inicial = 39014 # altitude do pulo original

altura_paraquedas = 1524 # altitude na qual Felix Baumgartner abriu o paraquedas

v_inicial = 0 # Velocidade inicial

# Calculando a Força de Resistência do Ar
def drag(sy, d, velocidade):
    # Os valores de Cd foram encontrados na Literatura
    if sy > altura_paraquedas:
        Cd = 0.5 # Coeficiente de arrasto de uma pessoa
        area = area_pessoa
    else:
        Cd = 0.75 # Coeficiente de arrasto do paraquedas
        area = area_paraquedas 
    Far = Cd * ((d * velocidade ** 2) / 2) * area
    return Far

# Calculando a aceleração da gravidade
def k_gravidade(altitude):
    # Linha de tendência dos pontos encontrados na Literatura
    # Para a faixa trabalhada podemos assumir que é uma reta
    gravidade = (-0.0000030646) * altitude + 9.8066215751
    return gravidade

# Calculando a densidade do ar
def dAr(altitude):
    # Linha de tendência dos pontos encontrados na Literatura
    # Para a faixa trabalhada podemos assumir que é exponencial
    densidade = 14.9812604381766 * np.exp(-0.00014471277003936 * altitude)
    return densidade

# Calculando a velocidade do som
def Vsom(altitude):
    # Linha de tendência dos pontos encontrados na Literatura
    # Para a faixa trabalhada podemos assumir que é linear
    v_som = -0.004035 * altitude + 343
    return v_som

delta_t = 0.01

t = np.arange(0, 1000 + delta_t, delta_t)

Ci = [altura_inicial, v_inicial]

def EqDif(Ci, t):
    sy = Ci[0]
    vy = Ci[1]
    
    dsydt = vy
        
    dvydt = (-(peso * k_gravidade(sy)) + drag(sy, dAr(sy), vy)) / peso
    
    return dsydt, dvydt

resultado = odeint(EqDif, Ci, t)
posicao = []
for p in resultado[:,0]:
    if p >= 0:
        posicao.append(p)
    else:
        posicao.append(0)

velocidade = []       
for i in range(len(resultado[:,1])):
    if resultado[:,0][i] >= 0:
        velocidade.append(-resultado[:,1][i])
    else:
        velocidade.append(0)
'''
# Gráfico que compara as posições do saltador em função do tempo geradas pelo
# modelo com os dados do salto
plt.plot(t, posicao, label = 'Modelo', lw = 2.5)
plt.scatter(Ts, S, label = 'Dados do Salto', marker = 'o', color = 'black')
plt.legend(fontsize = 14)
plt.grid(True)
plt.title('Altitude em Função do Tempo', size = 14)
plt.xlabel('Tempo (s)', size = 14)
plt.ylabel('Altitude (m)', size = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

# Gráfico que compara as velocidades do saltador em função do tempo geradas pelo
# modelo com os dados do salto
plt.plot(t, velocidade, label = 'Modelo', lw = 2.5)
plt.scatter(Tv, V, label = 'Dados do Salto', marker = 'o', color = 'black')
plt.legend(fontsize = 14)
plt.grid(True)
plt.title('Velocidade em Função do Tempo', size = 14)
plt.xlabel('Tempo (s)', size = 14)
plt.ylabel('Velocidade (m/s)', size = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

EC = []
EG = []
EM = []
TD = [0]

# Analisamos a Energia Mecânica e o Trabalho da Resist. do Ar antes da abertura
# do paraquedas
t = np.arange(0, 290 + delta_t, delta_t)

p_validacao = []
v_validacao = []
for i in range(len(t)):
    p_validacao.append(posicao[i])
    v_validacao.append(velocidade[i])
    
for h in p_validacao: 
    EG.append(peso * k_gravidade(h) * h) # Energia Potencial Gravitacional

for v in v_validacao:
    EC.append((peso * v ** 2) / 2) # Energia Cinética
    
for e in range(len(EC)):
    EM.append(EC[e] + EG[e]) # Energia Mecânica
    
for i in range(1, len(p_validacao)):
    # Trabalho da Resistência do Ar
    TD.append(drag(p_validacao[i], dAr(p_validacao[i]),
                   v_validacao[i]) * (p_validacao[i-1] - p_validacao[i]))
    
delta_EM = []
validacao = [0]

for i in range(1, len(TD)):
    delta_EM.append(EM[i] - EM[i-1]) # ∆ Energia Mecânica
    validacao.append(TD[i-1] + delta_EM[i-1]) # ∆ Energia Mecância - Trabalho Far

# Gráfico de Validação    
plt.plot(t[1:], delta_EM, label = '∆EM', lw = 4.5) 
plt.plot(t, TD, label = 'Trabalho Drag', lw = 4.5)
plt.plot(t, validacao, label = '∆EM - Trabalho Drag', lw = 4.5)
plt.legend(fontsize = 14)
plt.grid(True)
plt.title('Validação', size = 14)
plt.xlabel('Tempo (s)', size = 14)
plt.ylabel('Energia (J)', size = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

# Levando em consideração a variação de massa
def EqDif2(Ci, t, m):
    sy = Ci[0]
    vy = Ci[1]
    
    dsydt = vy
        
    dvydt = (-(m * k_gravidade(sy)) + drag(sy, dAr(sy), vy)) / peso
    
    return dsydt, dvydt

lista_altitudes = np.arange(27000, 32001, 25)
lista_massa = np.arange(60, 121, 15)

# O ponto de velocidade máxima ocorre antes dos primeiros 200 segundos
t = np.arange(0, 200 + delta_t, delta_t)
for massa in lista_massa:
    resultados_velox = []
    resultados_posic = []
    velocidade2 = []
    posic_vmax = []
    m = massa + peso_traje  
    # Encontrando as velocidades máximas em função da altitude inicial
    for alts in lista_altitudes:
        CI = [alts, v_inicial]
        solucao = odeint(EqDif2,CI,t, args = (m,))
        
          
        for i in range(len(solucao[:,1])):
            if solucao[:,0][i] >= 0:
                velocidade2.append(-solucao[:,1][i])
                if velocidade2[i] > velocidade2[i-1]:
                    indice_max = i
            else:
                velocidade2.append(0)
                
        posic_vmax.append(solucao[:,0][indice_max]) # Lista de posição no instante de velocidade máxima para cada altitude inicial
        resultados_velox.append(max(velocidade2)) # Lista de velocidade máxima para cada altitude inicial
        resultados_posic.append(max(solucao[:,0]) / 1000) # Lista de altitudes iniciais
        
    # Encontrando a altitude mínima para se alcançar a velocidade do som
    for e in range(len(resultados_velox)):
        if resultados_velox[e] >= Vsom(posic_vmax[e]):
            posic = resultados_posic[e]        
            plt.plot(posic, resultados_velox[e],
                     marker = 'o', color = 'black')
            if massa == 120:
                print('Uma pessoa de 120 kg teria que pular de {0} para \
                      atingir a velocidade do som.'.format(posic))
            break
        
# Plotando o gráfico que responde a pergunta
    plt.plot(resultados_posic, resultados_velox,
             label = 'm = {0}kg'.format(massa), lw = 2)
plt.grid(True)
plt.legend(fontsize = 10)
plt.title('Altitude do Salto x Velocidade Máxima', size = 14)
plt.xlabel('Altitude Inicial (km)', size = 14)
plt.ylabel('Velocidade Máxima (m/s)', size = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()

# Aumentamos o escopo do estudo e analisamos massas maiores para ver como a
# altitude inicial para atingir 330 m/s varia em função da massa
lista_massa = np.arange(100, 1001, 50)
lista_altitudes = np.arange(13500, 28501, 150)

# Repetimos os passos que encontram a velocidade máxima e a altitude mínima para
# atingir a velocidade do som
for massa in lista_massa:
    resultados_velox = []
    resultados_posic = []
    velocidade2 = []
    posic_vmax = []
    m = massa + peso_traje    
    for alts in lista_altitudes:
        CI = [alts, v_inicial]
        solucao = odeint(EqDif2,CI,t, args = (m,))
        
          
        for i in range(len(solucao[:,1])):
            if solucao[:,0][i] >= 0:
                velocidade2.append(-solucao[:,1][i])
                if velocidade2[i] > velocidade2[i-1]:
                    indice_max = i
            else:
                velocidade2.append(0)

        posic_vmax.append(solucao[:,0][indice_max]) # Lista de posição no instante de velocidade máxima para cada altitude inicial
        resultados_velox.append(max(velocidade2)) # Lista de velocidade máxima para cada altitude inicial
        resultados_posic.append(max(solucao[:,0])) # Lista de altitudes iniciais
    
    for e in range(len(resultados_velox)):
        if resultados_velox[e] >= Vsom(posic_vmax[e]):
            posic = resultados_posic[e] / 1000  
            # Gráfico Conclusivo
            plt.plot(massa, posic, marker = 'o', color = 'darkblue')
            break
plt.grid(True)
plt.title('Gráfico Conclusivo - Altitude Inicial x Massa', size = 14)
plt.xlabel('Massa (kg)', size = 14)
plt.ylabel('Altitude Inicial (km)', size = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.show()
'''
''' ANIMAÇÃO '''

import pygame

import numpy as np

pygame.init()

nova_posicao = []

lista_veloks = velocidade

posics = np.arange(100001 - 20520, 0, -1)

comprimento_display = 602
altura_display = 603

tela = pygame.display.set_mode((comprimento_display, altura_display))
pygame.display.set_caption("Python/Pygame Animation")

relogio = pygame.time.Clock()

preto = (0,0,0)
branco = (255,255,255)

class Paraquedista(pygame.sprite.Sprite):

    andando_esquerda = [pygame.image.load('Bombas_05.png'),pygame.image.load('Bombas_06.png'),
    pygame.image.load('Bombas_07.png'),pygame.image.load('Bombas_05.png'),pygame.image.load('Bombas_06.png'),
    pygame.image.load('Bombas_07.png'),pygame.image.load('Bombas_05.png'),pygame.image.load('Bombas_06.png'),
    pygame.image.load('Bombas_07.png'),pygame.image.load('Bombas_05.png'),pygame.image.load('Bombas_06.png'),
    pygame.image.load('Bombas_07.png')]

    queda = pygame.image.load('Bombas_05.png')

    queda_paraquedas = pygame.image.load('Bombas_23.png')


    def __init__(self, x, y, width, height, end, velocity):
            pygame.sprite.Sprite.__init__(self)
            self.lista_veloks = velocity
            self.centerx = x
            self.bottomy = y
            self.width = width
            self.height = height
            self.end = end
            self.path = [self.centerx, self.end]
            self.walkCount = 0
            self.contador = 0
            self.vel = 6
            self.rect = self.andando_esquerda[self.walkCount].get_rect()
            self.rect.centerx = self.centerx
            self.rect.bottom = self.bottomy

    def draw(self,tela):


        self.move()
        if (self.walkCount + 1) >= 33:
            self.walkCount = 0   
        
        if self.vel > 0:
            tela.blit(self.andando_esquerda[self.walkCount //3], (self.centerx, self.bottomy))
            self.walkCount += 1



        else:
            velocityy = self.lista_veloks[self.contador]
            if velocityy >= 47:
                tela.blit(self.queda, (self.centerx, self.bottomy))
            else:
                tela.blit(self.queda_paraquedas, (self.centerx- 15, self.bottomy - 50))
        pygame.display.flip()
        tela_plano_de_fundo = pygame.image.load('BackgroundGrade.png')
        tela.blit(tela_plano_de_fundo,[0,0])
        

    def move(self):
        if self.contador >= 0:
            if self.vel > 0:
                if self.centerx > self.path[1]:
                    self.centerx -= self.vel
                if self.centerx <= self.path[1]:
                    self.vel = 0
            if self.vel == 0:
                if self.centerx <= self.path[1]:
                    velocityy = self.lista_veloks[self.contador]
                    print(velocityy)
                    self.bottomy += velocityy/9.1
                    self.contador += 1000


        self.rect.centerx = self.centerx
        self.rect.bottom = self.bottomy

saltador = pygame.sprite.Group()
vel = 0
def animacao():


    paraquedistaa = Paraquedista((comprimento_display / 2), 75, 25, 25,
                                 375, velocidade)
    saltador.add(paraquedistaa)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return -1
        
        paraquedistaa.draw(tela)

        paraquedistaa.update()

        saltador.update()

        relogio.tick(10)

def loop(estado):
    #enquanto o jogo esta aberto
    while estado != -1:
        if estado == 1:
            

            estado = animacao()

    


estado = 1
loop(estado)
pygame.quit()