import streamlit as st
import CoolProp.CoolProp as CP
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulador de Ciclos Termodinámicos")

st.write("Comparación entre ciclo Rankine y Ciclo de absorción")

def calcular_ciclo_rankine(T_ambiente):
    # Suposiciones
    P_alta = 8000e3  # Presión de caldera en Pa
    P_baja = 10e3    # Presión de condensador en Pa
    fluido = "Water"
    
    # Estado 1: Entrada a la turbina (suponiendo vapor saturado a P_alta)
    h1 = CP.PropsSI('H', 'P', P_alta, 'Q', 1, fluido)
    s1 = CP.PropsSI('S', 'P', P_alta, 'Q', 1, fluido)
    
    # Estado 2: Salida de la turbina (expansión isentrópica)
    h2s = CP.PropsSI('H', 'P', P_baja, 'S', s1, fluido)
    eta_turbina = 0.85  # Eficiencia de la turbina
    h2 = h1 - eta_turbina * (h1 - h2s)
    
    # Estado 3: Salida del condensador (líquido saturado a P_baja)
    h3 = CP.PropsSI('H', 'P', P_baja, 'Q', 0, fluido)
    
    # Estado 4: Bomba (compresión isentrópica)
    v3 = 1 / CP.PropsSI('D', 'P', P_baja, 'Q', 0, fluido)
    h4 = h3 + v3 * (P_alta - P_baja) / 0.85  # Suponiendo eficiencia de bomba 85%
    
    # Trabajo y eficiencia
    W_turbina = h1 - h2
    W_bomba = h4 - h3
    Q_caldera = h1 - h4
    eficiencia = (W_turbina - W_bomba) / Q_caldera
    
    return eficiencia * 100

def calcular_ciclo_absorcion(T_ambiente):
    # Simplificación: eficiencia basada en correlación empírica
    eficiencia = 0.3 + 0.0005 * (T_ambiente - 273.15)  # Depende de la temperatura ambiente
    return max(10, eficiencia * 100)  # Límite mínimo de 10%

