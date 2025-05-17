# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 16:03:32 2025

@author: truej
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import Projekt_Starz_Orbites as orbit

def run_dash_app(df, info=["star_distance", "mag_v", "star_teff"], polar=["ra", "dec", "star_distance"], label="star_name"):
    """Lance l'application Dash avec l'affichage interactif du nuage de points."""
    
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container([
        html.H1(style={'color': 'white', 'textAlign': 'center'}),
    
        # Appliquer un fond noir à l’ensemble de l’application
        html.Div(style={'backgroundColor': 'black', 'padding': '20px', 'minHeight': '100vh'}, children=[
    
            dcc.Store(id="show-second-plot", data=False),
            dcc.Store(id="camera-store", data={}),
    
            html.Div([
                html.Div(
                    dcc.Graph(id='scatter-3d', style={'height': '80vh'}),
                    id="col-left",
                    style={"width": "100%", "transition": "width 0.5s ease-in-out"}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='dynamic-3d-plot', style={'height': '70vh'}),
                        dbc.Button("Fermer", id="close-button", color="danger",
                                   className="mt-2",
                                   style={'position': 'absolute', 'z-index': '10', 'right': '10px', 'top': '10px'})
                    ], style={'position': 'relative'})
                ], id="col-right", style={'width': '0%', 'overflow': 'hidden', 'transition': 'width 0.5s ease-in-out'})
            ], id="main-row", style={'display': 'flex'})
        ])
    ], 
    fluid=True,
    className='dashboard-container'
    )
    
    
    # Callback pour auvegarder l'état de la caméra à chaque interaction
    @app.callback(
        Output("camera-store", "data"),  # Stocke la caméra
        Input("scatter-3d", "relayoutData"),  # Capture les changements de vue
        prevent_initial_call=True
    )
    def save_camera_state(relayout_data):
        if relayout_data and "scene.camera" in relayout_data:
            return relayout_data["scene.camera"]  # Stocke la caméra actuelle
        return dash.no_update
    
    

    # Callback pour générer et redimensionner le premier graphique
    @app.callback(
        Output("scatter-3d", "figure"),
        Input("show-second-plot", "data"),
        State("scatter-3d", "figure"),
        State("camera-store", "data")  # Récupère la caméra stockée
    )
    def update_scatter(show_plot, current_figure, camera_data):
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
            title="Carte Stellaire",
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
                ),
                camera=camera_data if camera_data else {}
            ),
            showlegend=True,
            autosize=False,
            width=800 if show_plot else 1600,
            height=1000
        )
        return fig



    # Callback pour gérer l'affichage du second graphique
    @app.callback(
        Output("show-second-plot", "data"),
        [Input("scatter-3d", "clickData"), Input("close-button", "n_clicks")],
        [State("show-second-plot", "data")],
        prevent_initial_call=True
    )
    def toggle_display(clickData, n_clicks, show_plot):
        triggered_id = ctx.triggered_id
        if triggered_id == "close-button":
            return False
        if clickData:
            return True
        return show_plot



    # Callback pour ajuster la disposition des graphiques
    @app.callback(
        [Output("col-left", "style"), Output("col-right", "style")],
        Input("show-second-plot", "data")
    )
    def update_layout(show_plot):
        if show_plot:
            return {"width": "50%", "transition": "width 0.5s ease-in-out"}, {"width": "50%", "transition": "width 0.5s ease-in-out"}
        return {"width": "100%", "transition": "width 0.5s ease-in-out"}, {"width": "0%", "overflow": "hidden", "transition": "width 0.5s ease-in-out"}



    # Callback pour générer le second graphique
    @app.callback(
        Output('dynamic-3d-plot', 'figure'),
        Input("scatter-3d", "clickData"),
        prevent_initial_call=True
    )
    def update_graph(clickData):
        if clickData is None:
            return go.Figure()
    
        # Récupérer l'ID du point cliqué
        point_name = clickData['points'][0]['customdata'][0]
        point_value = clickData['points'][0]['customdata'][3]  # Caractéristique pour la couleur
    
        # Filtrer `df` pour récupérer TOUS les points ayant le même nom que celui cliqué
        subset_df = df[df['star_name'] == point_name]
    
        # Construire les courbes
        traces = []
        born = 0
        for _, row in subset_df.iterrows():
            t_vals, x_vals, y_vals, z_vals = orbit.get_full_orbit(row["semi_major_axis"], row["eccentricity"], row["inclination"], row["orbital_period"])
            bborn = 1.5*max(np.max(np.abs(x_vals)), np.max(np.abs(y_vals)), np.max(np.abs(z_vals)))
            R = np.sqrt((x_vals**2) + (y_vals**2) + (z_vals**2))
            if bborn > born :
                born = bborn
    
            traces.append(go.Scatter3d(
                x=x_vals, y=y_vals, z=z_vals,
                mode='markers+lines',
                text=[f"r = {r:.5f} AU<br>t = {t:.2f} days<br>i = {row['inclination']}°<br>a = {row['semi_major_axis']} AU<br>e = {row['eccentricity']}" for t, r in zip(t_vals, R)],
                hoverinfo="text",
                line=dict(width=3),
                marker=dict(size=3),
                name=f"Orbite de {row['name']}"  # Légende
            ))
    
        # Ajouter le point central en (0, 0, 0)
        traces.append(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=10, color=point_value, colorscale='Viridis'),
            name="Centre"
        ))
    
        # Créer la figure et appliquer le style
        fig = go.Figure(data=traces)
        fig.update_layout(
            title=f"Système planétaire autour de {point_name}",
            paper_bgcolor="black",
            plot_bgcolor="black",
            scene=dict(
                xaxis=dict(title="X", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black", type="linear", autorange=False, range=[-born, born]),
                yaxis=dict(title="Y", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black", type="linear", autorange=False, range=[-born, born]),
                zaxis=dict(title="Z", color="cyan", showgrid=False, showticklabels=False, showline=False, backgroundcolor="black", type="linear", autorange=False, range=[-born, born])
            ),
            showlegend=True
        )
    
        return fig


    # Lancer l'application Dash
    app.run(debug=True)
