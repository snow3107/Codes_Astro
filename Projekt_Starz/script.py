# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:09:01 2025

@author: truej
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Création de données fictives
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.uniform(-10, 10, 100),
    'y': np.random.uniform(-10, 10, 100),
    'z': np.random.uniform(-10, 10, 100),
    'id': np.arange(100),
    'value': np.random.uniform(1, 5, 100)
})

# Initialisation de l'application Dash avec Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout de l'application
app.layout = dbc.Container([
    html.H1("Interaction avec un nuage de points 3D"),

    # Stockage de l'état d'affichage du second graphique
    dcc.Store(id="show-second-plot", data=False),

    # Conteneur global des deux graphiques
    html.Div([
        # Premier graphique (par défaut pleine largeur)
        html.Div(
            dcc.Graph(
                id='scatter-3d',
                style={'height': '80vh'}
            ),
            id="col-left",
            style={"width": "100%", "transition": "width 0.5s ease-in-out"}
        ),

        # Deuxième graphique + bouton "Fermer" (initialement caché)
        html.Div([
            html.Div([
                dcc.Graph(id='dynamic-3d-plot', style={'height': '70vh'}),

                # Bouton "Fermer" en premier plan
                dbc.Button("Fermer", id="close-button", color="danger",
                           className="mt-2",
                           style={'position': 'absolute', 'z-index': '10', 'right': '10px', 'top': '10px'}
                )
            ], style={'position': 'relative'})
        ], id="col-right", style={'width': '0%', 'overflow': 'hidden', 'transition': 'width 0.5s ease-in-out'})
    ], id="main-row", style={'display': 'flex'})  # Flexbox pour aligner les graphiques côte à côte
], fluid=True)

# Callback pour générer et redimensionner le premier graphique
@app.callback(
    Output("scatter-3d", "figure"),
    Input("show-second-plot", "data")
)
def update_scatter(show_plot):
    fig = go.Figure(
        data=[go.Scatter3d(
            x=df['x'], y=df['y'], z=df['z'],
            mode='markers',
            marker=dict(size=5, color=df['value'], colorscale='Viridis'),
            text=df['id'],
            customdata=df[['id', 'value']],
            hoverinfo='text'
        )]
    )

    # Taille dynamique en fonction de la disposition
    fig.update_layout(
        autosize=False,
        width=800 if show_plot else 1600,  # Change la largeur
        height=1000
    )

    return fig

# Callback pour basculer l'affichage du second graphique
@app.callback(
    Output("show-second-plot", "data"),
    [Input("scatter-3d", "clickData"), Input("close-button", "n_clicks")],
    [State("show-second-plot", "data")],
    prevent_initial_call=True
)
def toggle_display(clickData, n_clicks, show_plot):
    triggered_id = ctx.triggered_id  # Vérifie l'élément déclencheur

    if triggered_id == "close-button":
        return False  # Fermer le second graphique

    if clickData:
        return True  # Ouvrir le second graphique

    return show_plot  # Ne rien changer si aucun clic

# Callback pour ajuster la disposition en fonction de l'état `show-second-plot`
@app.callback(
    [Output("col-left", "style"),
     Output("col-right", "style")],
    Input("show-second-plot", "data")
)
def update_layout(show_plot):
    if show_plot:
        return {"width": "50%", "transition": "width 0.5s ease-in-out"}, {"width": "50%", "transition": "width 0.5s ease-in-out"}
    return {"width": "100%", "transition": "width 0.5s ease-in-out"}, {"width": "0%", "overflow": "hidden", "transition": "width 0.5s ease-in-out"}

# Callback pour mettre à jour le second graphique
@app.callback(
    Output('dynamic-3d-plot', 'figure'),
    Input("scatter-3d", "clickData"),
    prevent_initial_call=True
)
def update_graph(clickData):
    if clickData is None:
        return go.Figure()  # Retourne un graphique vide au démarrage

    point_id = clickData['points'][0]['customdata'][0]
    point_value = clickData['points'][0]['customdata'][1]

    # Création d'un graphique 3D associé au point sélectionné
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 50)
    x = point_value * np.outer(np.cos(theta), np.sin(phi))
    y = point_value * np.outer(np.sin(theta), np.sin(phi))
    z = point_value * np.outer(np.ones(np.size(theta)), np.cos(phi))

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Viridis')])
    fig.update_layout(title=f"Graphique 3D associé au point {point_id}")

    return fig

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)


