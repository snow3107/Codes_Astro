# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 21:18:47 2025

@author: truej
"""

import numpy as np
import plotly.graph_objects as go
import Project_Stars_Extract_data as exdat
import plotly.io as pio

pio.renderers.default = "browser"

def plot(df, info, polar=["ra", "dec", "star_distance"], label="star_name"):
    
    # Données utiles :
    textinfo = ""
    for i, attr in enumerate(info) :
        if attr == "star_distance" :
            textinfo += "<br>Distance : %{customdata[" + str(i+1) + "]} pcs"
        elif attr == "star_teff" :
            textinfo += "<br>T_eff : %{customdata[" + str(i+1) + "]} K"
        else :
            textinfo += "<br>" + str(attr) + " : %{customdata[" + str(i+1) + "]}"
    textinfo += "<extra></extra>"
    
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=df[polar[2]]*np.cos(np.pi*df[polar[1]]/180)*np.cos(np.pi*df[polar[0]]/180), 
        y=df[polar[2]]*np.cos(np.pi*df[polar[1]]/180)*np.sin(np.pi*df[polar[0]]/180), 
        z=df[polar[2]]*np.sin(np.pi*df[polar[1]]/180),
        mode='markers+text',
        marker=dict(size=5, color=df[polar[2]], colorscale='Viridis_r', opacity=0.8),
        text=df[label],  # Légendes des points
        textposition="top center",
        customdata=df[[label] + info],
        hovertemplate="Système: %{customdata[0]}<br>X : %{x}<br>Y : %{y}<br>Z : %{z}" + textinfo
    ))

    fig.update_layout(
        paper_bgcolor="black",  # Fond global
        plot_bgcolor="black",   # Fond du graphe
        scene=dict(
            xaxis=dict(
                title="X", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black"
            ),
            yaxis=dict(
                title="Y", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black"
            ),
            zaxis=dict(
                title="Z", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black"
            )
        ),
        showlegend=True
    )
    return fig

