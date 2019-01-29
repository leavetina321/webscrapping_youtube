#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 15:15:38 2018

@author: yewanxin
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv('youtube_clean.csv')


app.layout = html.Div([
    dcc.Graph(
        id='youtube',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['channel_type'] == i]['age'],
                    y=df[df['channel_type'] == i]['v_per_view'],
                    text=df[df['channel_type'] == i]['age'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.channel_type.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'subscribers'},
                yaxis={'title': 'estimated monthly earnings'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()
