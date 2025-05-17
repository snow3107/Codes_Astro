# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 22:28:56 2025

@author: truej
"""

import pandas as pd

def get_cols(file_path, attributes):
    # Lire la première ligne uniquement (noms des colonnes)
    with open(file_path, 'r') as f:
        headers = f.readline().strip().split()  # Suppression des espaces et split

    # Identifier les indices des colonnes à conserver
    cols = [i for i, col in enumerate(headers) if col in attributes]

    return cols



def extract_data_optimized(file_path, attributes, double_cols=["star_name"]):

    # Lire le fichier en ne chargeant que les colonnes utiles
    df = pd.read_csv(file_path, sep='\t', usecols=attributes, header=0)

    # Suppression des lignes contenant des valeurs manquantes
    df.dropna(inplace=True)

    # Suppression des doublons selon les colonnes spécifiées
    if double_cols != None :
        df.drop_duplicates(subset=double_cols, inplace=True)

    return df

