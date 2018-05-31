#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:18:40 2018

Projeto 3 de ModSim

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

''' Implementação do Modelo '''

# Encontrado na literatura:
peso_pessoa = 73 #kg

altura_pessoa = 170 #cm

peso_traje = 45 #kg

peso = peso_pessoa + peso_traje

# Encontrado na Literatura
area_pessoa = 0.18

area_paraquedas = 25 # Informação encontrada em Red Bull Stratos

altura_inicial = 39014 # altitude do pulo original

altura_paraquedas = 1524

v_inicial = 0

def drag(sy, d, velocidade):
    if sy > altura_paraquedas:
        Cd = 0.5 # Coeficiente de arrasto de uma pessoa => Literatura
        area = area_pessoa
    else:
        Cd = 0.75
        area = area_paraquedas
    Far = Cd * ((d * velocidade ** 2) / 2) * area
    return Far

def k_gravidade(altitude):
    gravidade = (-0.0000030646) * altitude + 9.8066215751
    return gravidade

def dAr(altitude):
    densidade = 14.9812604381766 * np.exp(-0.00014471277003936 * altitude)
    return densidade

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

plt.plot(t, posicao)
plt.grid(True)
plt.title('Altitude em Função do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Altitude (m)')
plt.show()

plt.plot(t, velocidade)
plt.grid(True)
plt.title('Velocidade em Função do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.show()

EC = []
EGP = []
EM = []
TD = [0]

tempo_validacao = int(290 / delta_t) + 1

t = np.arange(0, 290 + delta_t, delta_t)

p_validacao = []
v_validacao = []
for i in range(tempo_validacao):
    p_validacao.append(posicao[i])
    v_validacao.append(velocidade[i])
    
for h in p_validacao: 
    EGP.append(peso * k_gravidade(h) * h)
    
for i in range(1, len(p_validacao)):
    TD.append(TD[i-1] + drag(p_validacao[i], dAr(p_validacao[i]),
                   v_validacao[i]) * (p_validacao[i-1] - p_validacao[i]))

for v in v_validacao:
    EC.append((peso * v ** 2) / 2)
    
for e in range(len(EC)):
    EM.append(EC[e] + EGP[e])
    
plt.plot(t, EM, label = 'Energia Mecância')
plt.plot(t, TD, label = 'Trabalho Drag')
plt.legend()
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.title('Validação')
plt.grid(True)
plt.show()

somaTD = 0
somaEM = 0
validacao = []

for valor in TD:
    somaTD += valor
    somaEM += valor
    validacao.append(somaTD - somaEM)
    
plt.plot(t, validacao)
plt.grid(True)
plt.xlabel('Tempo (s)')
plt.ylabel('Energia Mecância - Trabalho Drag')
plt.show()


#GRÁFICO CONCLUSIVO
#Felix alcançou Mach 1.25 à 338 m/s
#A Velocidade do som é de 330 m/s


lista_altitudes = np.arange(38014,39015,1)


resultados_velox = []
resultados_posic = []
velocidade2 = []     
for alts in lista_altitudes:
    print(alts)
    CI = [alts, v_inicial]
    solucao = odeint(EqDif,CI,t)
    
      
    for i in range(len(solucao[:,1])):
        if solucao[:,0][i] >= 0:
            velocidade2.append(-solucao[:,1][i])
        else:
            velocidade2.append(0)
        
    resultados_velox.append(max(velocidade2))
    resultados_posic.append(max(solucao[:,0]))
    

for e in range(len(resultados_velox)):
    if resultados_velox[e] >= 330 and resultados_velox[e]<= 330.1:
        posic = resultados_posic[e]         
        print('A posição onde a Velocidade vale 330 é: {0}'.format(posic))
        break

plt.plot(resultados_velox,resultados_posic)
plt.plot(330,38253, 'go', label = 'Altitude mínima')
plt.grid(True)
plt.legend()
plt.title('Grafico Conclusivo - Altitude mínima para se alcançar a velocidade do som')
plt.xlabel('Velocidades')
plt.ylabel('Altitudes')
plt.show()




