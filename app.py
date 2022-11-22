#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
sheet_inflow = "inflow"
sheet_outflow = "outflow"
url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZ8z6itG8nQZD67jMNQzHY_AGwZy4hchWg7gv1YWwrm1wDV-MC2actFWNc09khWq9t_2aTep77k7My/pub?gid=11819995&single=true&output=csv"
url_outflow = url= "https://docs.google.com/spreadsheets/d/e/2PACX-1vQf-6x9UNzaLvMYnLobX3YxLvV8lhoWWzRDaO4I5ettKf3jZ_Z4a6rGYEL59CQ7GUmJGGs5hTeEPsD_/pub?gid=542325911&single=true&output=csv"
df_inflow = pd.read_csv(url_inflow)
df_outflow = pd.read_csv(url_outflow)


#membangun komponen
header = html.H1("Menyajikan data")
inflow_fig = go.FigureWidget()
inflow_fig.add_scatter(name='Inflow', x=df_inflow['Waktu'], y=df_inflow['Data'])
inflow_fig.layout.title = 'Inflow'

outflow_fig = go.FigureWidget()
outflow_fig.add_scatter(name='Outflow', x=df_outflow['Waktu'], y=df_outflow['Data'])
outflow_fig.layout.title = 'Outflow'

simulation_fig = go.FigureWidget()
# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Waktu'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header]),
        dbc.Row([dbc.Col([dcc.Graph(figure=inflow_fig)]), dbc.Col([dcc.Graph(figure=outflow_fig)])]),
        html.Button('Run', id='run-button', n_clicks=0), 
        html.Div(id='output-container-button', children='Klik run untuk menjalankan simulasi.'),
        dbc.Row([dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])])
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection

    #program numerik ---start----
    inout = df_inflow["Data"].values - df_outflow["Data"].values
    N = len(inout)
    u = np.zeros(N)
    u0 = 4000
    u[0] = u0
    dt = 1

    #metode Euler
    for n in range(N-1):
        u[n + 1] = u[n] + dt*inout[n]
    #program numerik ---end----


    # the figure/plot created using the data filtered above 
    simulation_fig = go.FigureWidget()
    simulation_fig.add_scatter(name='Simulation', x=df_outflow['Waktu'], y=u)
    simulation_fig.layout.title = 'Simulation'

    return simulation_fig


#jalankan aplikasi
app.run_server(debug=True)
