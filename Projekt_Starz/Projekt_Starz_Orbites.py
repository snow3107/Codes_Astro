# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 15:41:49 2025

@author: truej
"""

import numpy as np

def position_at_time(a, e, i, p, t):
    
    # Anomalie moyenne
    M = 2 * np.pi * (t / p)  # M = 2π(t / P)
    
    # Approximation de l'anomalie excentrique par méthode de Newton-Raphson
    E = M  # Initial guess for E
    for _ in range(10):
        E = M + e * np.sin(E)
    
    # Anomalie vraie
    theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E/2), np.sqrt(1 - e) * np.cos(E/2))
    
    # Rayon
    r = a * (1 - e**2)/(1 + e * np.cos(theta))
    
    # Position dans le plan orbital
    X = r * np.cos(theta)*np.cos(np.radians(i))
    Y = r * np.sin(theta)
    Z = -r*np.cos(theta)*np.sin(np.radians(i))
    
    return X, Y, Z

def get_full_orbit(a, e, i, p, n=100):
    
    time_points = np.linspace(0, p, n)
    
    x, y, z = position_at_time(a, e, i, p, time_points)
    
    return time_points, x, y, z

def get_orbit(a, e, i, n=100):
    
    # Anomalie vraie
    theta = 2 * np.linspace(0, 2*np.pi, n)
    
    # Rayon
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    
    # Position dans le plan orbital
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Inclinaison (rotation autour de l'axe x)
    z = -x * np.sin(i)
    x = x * np.cos(i)
    
    return x, y, z