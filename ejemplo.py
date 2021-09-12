#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import plotly.express as px
import pandas as pd
import yaml

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='demo-dropdown',
           component_property='value')])
def update_output(value):
    if value is None:
        value = "Apples"
    print("Callback got:", value)
    print("DF section:", df.loc[df['Fruit'] == value])
    fig = px.bar(df.loc[df['Fruit'] == value],
                 x="Fruit",
                 y="Amount",
                 color="City",
                 barmode="group")
    return fig

print(df)
value = "Apples"
fig = px.bar(df.loc[df['Fruit'] == value],
             x="Fruit",
             y="Amount",
             color="City",
             barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': lab, 'value': lab} for lab in df['Fruit'][0:3]]
    ),
    html.Div([
    dcc.Graph(id='example-graph', figure=fig)])
])


def main(cfgfile):
    with open(cfgfile, "r") as cfgf:
        cfg = yaml.safe_load(cfgf)

if __name__ == '__main__':
    app.run_server(debug=True)

    
