# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 23:23:25 2025

@author: truej
"""

import Projekt_Starz_Extract_data as exdat
import Projekt_Starz_Affichage as aff

file_path = "exoplanet.eu_catalog_26-03-25_23_36_03.dat"

df_filtered = exdat.extract_data_optimized(file_path, attributes=["star_name", "orbital_period", "ra", "dec", "star_distance", "mag_v", "star_teff", 'name', "semi_major_axis", "eccentricity", "inclination"], double_cols=None)

aff.run_dash_app(df=df_filtered.loc[(df_filtered['star_distance'] < 100) ])