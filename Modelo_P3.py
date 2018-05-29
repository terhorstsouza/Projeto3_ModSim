#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:18:40 2018

Projeto 3 de ModSim

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

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

delta_t = 0.01

t = np.arange(0, 1000 + delta_t, delta_t)

Ci = [altura_inicial, v_inicial]

def drag(parachute, d, velocidade):
    if not parachute:
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

def EqDif(Ci, t):
    sy = Ci[0]
    vy = Ci[1]
    
    if sy > altura_paraquedas:
        parachute = False
    else:
        parachute = True
    
    dsydt = -vy
        
    dvydt = k_gravidade(sy) - (drag(parachute, dAr(sy), vy) / peso)
    
    if sy + dsydt < 0:
        
        dsydt = 0 - sy
        
        dvydt = 0 - vy
    
    return dsydt, dvydt

resultado = odeint(EqDif, Ci, t)

plt.plot(t, resultado[:,0])
plt.grid(True)
plt.title('Altitude em Função do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Altitude (m)')
plt.show()

plt.plot(t, resultado[:,1])
plt.grid(True)
plt.title('Velocidade em Função do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.show()

print (max(resultado[:,1]))
    
    
    


