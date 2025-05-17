# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 07:51:18 2024

@author: legen
"""

import numpy as np
import matplotlib.pyplot as plt

class ETOILE :
    def __init__(self, TS, RS, name):
        self.TS = TS
        self.RS = RS
        self.name = name

class ORBITAL_OBJ :
    def __init__(self, a, e, i, p, alpha, epsilon, name):
        self.a = a
        self.e = e
        self.i = i
        self.p = p
        self.alpha = alpha
        self.epsilon = epsilon
        self.name = name
        
    def get_temp(self, D, Etoile):
        return Etoile.TS * np.sqrt(Etoile.RS * np.sqrt((1-self.alpha)/self.epsilon)/ (2*D))
    
    def position_at_time(self, t):
        # Anomalie moyenne
        M = 2 * np.pi * (t / self.p)  # M = 2π(t / P)
        
        # Approximation de l'anomalie excentrique par méthode de Newton-Raphson
        E = M  # Initial guess for E
        for _ in range(10):
            E = M + self.e * np.sin(E)
        
        # Anomalie vraie
        theta = 2 * np.arctan2(np.sqrt(1 + self.e) * np.sin(E/2), np.sqrt(1 - self.e) * np.cos(E/2))
        
        # Rayon
        r = self.a * (1 - self.e**2) / (1 + self.e * np.cos(theta))
        
        # Position dans le plan orbital
        x = r * np.cos(theta)# - self.a * self.e
        y = r * np.sin(theta)
        
        # Inclinaison (rotation autour de l'axe x)
        z = -x * np.sin(self.i)
        x = x * np.cos(self.i)
        
        return x, y, z
    
    def get_orbit(self, precision, tol):        
        p = np.round(self.p, tol)
        
        N = precision*int(p)
        
        time_points = np.linspace(0, p, N)
        distances = np.zeros_like(time_points)
        X, Y, Z = np.zeros(N), np.zeros(N), np.zeros(N)
        
        for i, t in enumerate(time_points):
            X[i], Y[i], Z[i] = self.position_at_time(t)
        
        return time_points, X, Y, Z
    
    def get_distances(self, precision, tol):
        time_points, X, Y, Z = self.get_orbite(precision, tol)
        return time_points, np.sqrt(X**2 + Y**2 + Z**2)
    
class SYSTEME:
    def __init__(self, Etoile, Corps_List):
        self.Etoile = Etoile
        self.Corps_List = Corps_List # Liste de ORBITAL_OBJ
        
    def get_full_orbits(self, precision, tol):
        N_Orbits = len(self.Corps_List)
        L = [0 for i in range(N_Orbits)]
        for i in range(N_Orbits):
            time_points, X, Y, Z = self.Corps_List[i].get_orbit(precision, tol)
            L[i] = [time_points, X, Y, Z]
        return L
    
    def plot_system(self, precision, tol):
        N_Orbits = len(self.Corps_List)
        L = self.get_full_orbits(precision, tol)
        
        # Tracer les orbites en 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d', facecolor='black')
        cmap = plt.colormaps['Set3'].resampled(N_Orbits)
        for i in range (N_Orbits):
            color = cmap(i)
            ax.plot(L[i][1], L[i][2], L[i][3], '+-', color=color, label=f"Orbite de {self.Corps_List[i].name}")
        
        # Tracer le corps central
        ax.scatter(0, 0, 0, color='yellow', s=100, label=self.Etoile.name)
        
        # Ajouter le plan xy (d'un quadrilatère)
        Cordes = [self.Corps_List[i].a * (1 + self.Corps_List[i].e) for i in range(N_Orbits)]
        xy_plane_size = (max(Cordes) + min(Cordes)) * 0.75/2  # Taille du plan pour couvrir les orbites
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
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        plt.tight_layout()
        plt.show()

    def get_distances(self, i, j, precision, tol):
        p1 = np.round(self.Corps_List[i].p, tol)
        p2 = np.round(self.Corps_List[j].p, tol)
        
        i_approx = ORBITAL_OBJ(self.Corps_List[i].a, self.Corps_List[i].e, self.Corps_List[i].i, p1, self.Corps_List[i].alpha, self.Corps_List[i].epsilon, self.Corps_List[i].name)
        j_approx = ORBITAL_OBJ(self.Corps_List[j].a, self.Corps_List[j].e, self.Corps_List[j].i, p2, self.Corps_List[j].alpha, self.Corps_List[j].epsilon, self.Corps_List[j].name)        
        
        print(f"p1, p2 = {p1}, {p2}")
        
        T_max = ppcm(p1,p2)
        N = precision*int(T_max)
        print(f"T_max = {T_max} années")
        time_points = np.linspace(0, T_max, N)
        distances = np.zeros_like(time_points)
        X1, Y1, Z1 = np.zeros(N), np.zeros(N), np.zeros(N)
        X2, Y2, Z2 = np.zeros(N), np.zeros(N), np.zeros(N)
        
        for k, t in enumerate(time_points):
            x1, y1, z1 = i_approx.position_at_time(t)
            x2, y2, z2 = j_approx.position_at_time(t)
            
            X1[k], Y1[k], Z1[k] = x1, y1, z1
            X2[k], Y2[k], Z2[k] = x2, y2, z2
            
            # Calcul de la distance entre les deux corps
            distances[k] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        
        return time_points, distances, X1, Y1, Z1, X2, Y2, Z2
    

def binary_temp(Systeme, Etoile_2, index_etoile, index_planete, precision, tol):
        Planete = Systeme.Corps_List[index_planete]
        Etoile_1 = Systeme.Etoile
        time_points, distances, X1, Y1, Z1, X2, Y2, Z2 = Systeme.get_distances(index_planete, index_etoile, precision, tol)
        TE4 = ((1-Planete.alpha)/(4*Planete.epsilon)) * ( ((Etoile_1.RS/(np.sqrt(X1**2 + Y1**2 + Z1**2)*1.496e+11))**2)*(Etoile_1.TS**4) 
                                                       + ((Etoile_2.RS/(distances*1.496e+11))**2)*(Etoile_2.TS**4) )
        return time_points, TE4**0.25
    

def ppcm(p1,p2):
    if int(p1) != p1 and int(p2) != p2 :
        # Déterminer le facteur pour convertir les flottants en entiers
        facteur = 10 ** max(len(str(p1).split('.')[1]), len(str(p2).split('.')[1]))
        print(f"facteur = {facteur}")
        
        # Convertir en entiers
        int_p1 = int(p1 * facteur)
        int_p2 = int(p2 * facteur)
        
        # Calculer le PPCM des entiers
        ppcm = np.lcm(int_p1, int_p2)/facteur
    
    elif int(p1) != p1 :
        # Déterminer le facteur pour convertir les flottants en entiers
        facteur = 10 ** len(str(p1).split('.')[1])
        print(f"facteur = {facteur}")
        
        # Convertir en entiers
        int_p1 = int(p1 * facteur)
        int_p2 = int(p2 * facteur)
        
        # Calculer le PPCM des entiers
        ppcm = np.lcm(int_p1, int_p2)/facteur
        
    elif int(p2) != p2 :
        # Déterminer le facteur pour convertir les flottants en entiers
        facteur = 10 ** len(str(p2).split('.')[1])
        print(f"facteur = {facteur}")
        
        # Convertir en entiers
        int_p1 = int(p1 * facteur)
        int_p2 = int(p2 * facteur)
        
        # Calculer le PPCM des entiers
        ppcm = np.lcm(int_p1, int_p2)/facteur
        
    else : 
        ppcm = np.lcm(p1, p2)

    return ppcm
        

Gamma_Cephei_A = ETOILE(4792-62, 3.332e+9, "Gamma Cephei A") # Caractéristiques Réelles
Gamma_Cephei_B_e = ETOILE(3990, 0.4*6.96e+8, "Gamma Cephei B") # Caractéristiques Réelles

Tadmor = ORBITAL_OBJ(2.044 + 0.057, 0.115, 0, 902.9/365.25, 0.606, 1, "Tadmor")
Hypparcos = ORBITAL_OBJ(3.5, 0.315, np.radians(30), 3, 0.206, 0.85, "Hypparcos")
Gamma_Cephei_B_o = ORBITAL_OBJ((1.467-0.046)*4.84814e-6*2.846e+6, 0.411, np.radians(119.3), 67.5, 0.6, 1, "Gamma Cephei B")

Gamma_Cephei = SYSTEME(Gamma_Cephei_A, [Tadmor, Hypparcos, Gamma_Cephei_B_o])

Gamma_Cephei.plot_system(50, 1)

"""
time_points, distances, X1, Y1, Z1, X2, Y2, Z2 = Gamma_Cephei.get_distances(1, 2, 10, 1)
plt.figure(figsize=(10, 6))
plt.plot(time_points, distances, '+-')
plt.title('Distance entre les deux corps en fonction du temps')
plt.xlabel('Temps [Années]')
plt.ylabel('Distance [U.A]')
plt.show()
"""
"""
time_points, TE = binary_temp(Gamma_Cephei, Gamma_Cephei_B_e, 2, 0, 50, 1)
plt.figure(figsize=(10, 6))
plt.plot(time_points, TE, '+-')
plt.title('Températures moyennes sur Tadmor en fonction du temps')
plt.xlabel('Temps [Années]')
plt.ylabel('Température moyenne [°K]')
"""
#a2 = 4.84814e-6*2.846e+6
#a2 = 3
# Exécution du test
#plot_distance_between_bodies(a1=2.044, e1=0.115, inc1=0, p1=902.9/365.25, a2=a2, e2=0.411, inc2=np.radians(119.3), p2=67.5, tol = 1)
