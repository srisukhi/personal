#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import getopt
import logging as l
import plotly.express as px
import pandas as pd
import sys
import yaml

extcss = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


# See https://dash.plotly.com/basic-callbacks for examples

class Pairs:
    def __init__(self, mydf):
        self.mydf = mydf
        self.xcol = mydf.columns[0]
        self.ycol = mydf.columns[-1]
        self.app = dash.Dash(__name__, external_stylesheets=extcss)
        self.callbacks()
        print("app type:", type(self.app))

    def callbacks(self):
        @self.app.callback(
            Output(component_id="scatter-graph", component_property="figure"),
            Input(component_id="x-dropdown", component_property="value"),
            Input(component_id="y-dropdown", component_property="value"),
        )
        def update_output(xvalue, yvalue):
            print(f"Callback: xvalue {xvalue}, yvalue {yvalue}")
            if xvalue is not None:
                self.xcol = xvalue
            if yvalue is not None:
                self.ycol = yvalue
            fig = px.scatter(self.mydf, x=self.xcol, y=self.ycol)
            return fig

    def run(self):
        fig = px.scatter(self.mydf, x=self.xcol, y=self.ycol, height=600)
        intlabels = pd.DataFrame(self.mydf.columns).reset_index().\
            set_index(0).astype('str').to_dict()['index']
        matrix = px.scatter_matrix(self.mydf, height=900)
        matrix.update_layout(font={'size': 1})
        matrix.update_traces(showupperhalf=False, diagonal_visible=False)

        self.app.layout = html.Div(
            children=[
                html.H1(children="Pairs"),
                html.Div(
                    children="A statistical tool to visualize "
                    "pairs of fields in a table"
                ),
                html.Div([
                    dcc.Dropdown(
                        id="x-dropdown",
                        options=[{"label": lab, "value": lab} for lab in self.mydf.columns],
                        placeholder="Choose X axis"
                    )],
                    style={'width': '40%', 'display': 'inline-block'},
                ),
                html.Div([
                    dcc.Dropdown(
                        id="y-dropdown",
                        options=[{"label": lab, "value": lab} for lab in self.mydf.columns],
                        placeholder="Choose Y axis"
                    )],
                    style={'width': '40%', 'display': 'inline-block'},
                ),
                html.Div([dcc.Graph(id="scatter-graph", figure=fig)]),
                html.Div([dcc.Graph(id="scatter-matrix", figure=matrix)]),
            ]
        )
        self.app.run_server(debug=True, host='0.0.0.0')


def main(argv):
    cfgfile = None
    exit_code = None
    try:
        opts, args = getopt.getopt(argv[1:], "hc:", ["cfgfile="])
    except getopt.GetoptError:
        opts = [("-h", "")]
        exit_code = 2

    if len(opts) == 0:
        opts = [("-h", "")]

    for opt, arg in opts:
        if opt == "-h":
            print(f"Usage: {argv[0]} -c <cfgfile>")
            sys.exit(exit_code)
        elif opt in ("-c", "--cfgfile"):
            cfgfile = arg
    print("Input file:", cfgfile)

    with open(cfgfile, "r") as cfgf:
        cfg = yaml.safe_load(cfgf)

    cfgts = cfg["type-specific"]
    if cfg["type"] == "xlsx":
        xlfile = cfgts["xlfile"]
        sheet = cfgts["sheet"]
        mydf = pd.read_excel(xlfile, sheet)
    elif cfg["type"] == "csv":
        csvfile = cfgts["csvfile"]
        mydf = pd.read_csv(csvfile)

    print(mydf.head(2))
    pairs = Pairs(mydf)
    pairs.run()


if __name__ == "__main__":
    main(sys.argv)
