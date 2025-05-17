# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:54:06 2024

@author: legen
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_orbits_3d(a1, e1, i1, a2, e2, i2, num_points=1000):
    """
    Trace les orbites de deux corps autour d'un corps central en 3D sur un fond noir.
    
    Paramètres:
    -----------
    a1, a2 : float
        Demi-grand axe des orbites des corps 1 et 2 (en unités arbitraires).
    e1, e2 : float
        Excentricité des orbites des corps 1 et 2.
    i1, i2 : float
        Inclinaison des orbites des corps 1 et 2 (en degrés).
    num_points : int
        Nombre de points à utiliser pour tracer les orbites (plus il y a de points, plus la courbe est lisse).
    
    Returns:
    --------
    None (affiche le tracé 3D des orbites).
    """
    
    # Convertir l'inclinaison en radians
    i1 = np.radians(i1)
    i2 = np.radians(i2)
    
    # Calculer l'angle vrai à partir de l'anomalie excentrique pour une orbite elliptique
    theta = np.linspace(0, 2 * np.pi, num_points)
    
    # Calculer la position en 2D (dans le plan orbital)
    r1 = a1 * (1 - e1**2) / (1 + e1 * np.cos(theta))
    r2 = a2 * (1 - e2**2) / (1 + e2 * np.cos(theta))
    
    # Coordonnées en 2D dans le plan orbital
    x1_orbit = r1 * np.cos(theta) - a1 * e1  # Décalage pour positionner le corps central au foyer
    y1_orbit = r1 * np.sin(theta)
    x2_orbit = r2 * np.cos(theta) - a2 * e2  # Décalage pour positionner le corps central au foyer
    y2_orbit = r2 * np.sin(theta)
    
    # Appliquer l'inclinaison pour obtenir les coordonnées 3D
    x1 = x1_orbit * np.cos(i1)
    y1 = y1_orbit
    z1 = -x1_orbit * np.sin(i1)
    
    x2 = x2_orbit * np.cos(i2)
    y2 = y2_orbit
    z2 = -x2_orbit * np.sin(i2)
    
    # Diviser l'orbite du 2e objet en 4 saisons de périodes égales
    demiquarter = num_points // 8
    seasons = [
        (np.concatenate((x2[-demiquarter:], x2[:demiquarter])), np.concatenate((y2[-demiquarter:], y2[:demiquarter])), np.concatenate((z2[-demiquarter:], z2[:demiquarter]))),
        (x2[demiquarter:3*demiquarter], y2[demiquarter:3*demiquarter], z2[demiquarter:3*demiquarter]),
        (x2[3*demiquarter:5*demiquarter], y2[3*demiquarter:5*demiquarter], z2[3*demiquarter:5*demiquarter]),
        (x2[5*demiquarter:-demiquarter], y2[5*demiquarter:-demiquarter], z2[5*demiquarter:-demiquarter])
    ]
    
    # Tracer les orbites en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Tracer l'orbite du corps 1
    ax.plot(x1, y1, z1, label='Orbite du corps 1', color='cyan')
    
    # Tracer les saisons de l'orbite du corps 2 avec des couleurs différentes
    season_colors = ['magenta', 'yellow', 'green', 'orange']
    for idx, season in enumerate(seasons):
        ax.plot(season[0], season[1], season[2], label=f'Saison {idx + 1}', color=season_colors[idx])
    
    
    # Tracer le corps central
    ax.scatter(0, 0, 0, color='yellow', s=100, label='Corps central')
    
    # Ajouter le plan xy (d'un quadrilatère)
    xy_plane_size = (max(a1 * (1 + e1), a2 * (1 + e2)) + min(a1 * (1 + e1), a2 * (1 + e2))) * 1.5/2  # Taille du plan pour couvrir les orbites
    xx, yy = np.meshgrid(
        np.linspace(-xy_plane_size, xy_plane_size, 10), 
        np.linspace(-xy_plane_size, xy_plane_size, 10)
    )
    zz = np.zeros_like(xx)
    
    ax.plot_surface(xx, yy, zz, color='white', alpha=0.2)  # Plan blanc semi-transparent
    
    # Ajouter des labels et une légende
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')
    ax.legend()

    # Configurer l'échelle des axes pour être égale
    ax.set_box_aspect([1, 1, 1])
    
    # Changer la couleur des labels
   
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

a2 = 4.84814e-6*2.846e+6
#a2=4.267e+15*7.12676e-6*6.68459e-9

# Exemple d'utilisation
plot_orbits_3d(a1=2.044, e1=0.115, i1=0, a2=a2, e2=0.411, i2=119.3)
