# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.scripts.config.serve_locally = True

data = pd.read_csv('https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/714411/Monthly_museums_and_galleries_April_2018.csv', encoding='latin1')
data['day'] = 1
data['Month'] = pd.to_datetime(data[['month', 'year', 'day']])
museums_list = data.museum.unique()
data = data.pivot(index='Month',columns='museum',values='visits')
data = data.reset_index()

data2

app.layout = html.Div(children=[
    html.H1(children='Museums Dashboard'),
    html.H2(children='Compare visits between museums')
    dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': i, 'value': i} for i in museums_list],
                value=['BRITISH MUSEUM', 'NATIONAL GALLERY', 'TATE TOTAL'],
                multi=True
            ),
    html.Div(id='my-div'),
    dcc.Graph(id='my-graph')
    html.H2(children='Compare seasons for a museum')
    dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': i, 'value': i} for i in museums_list],
                value=['BRITISH MUSEUM'],
            ),
    dcc.Graph(id='my-graph2')
    
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    traces = []

    for i, musy in enumerate(selected_dropdown_value):
        traces.append(go.Scatter(
            x=data.Month,
            y=data[selected_dropdown_value[i]],
            mode = 'lines+markers',
            name = musy,
#            line=dict(color='rgba(67,67,67,1)', width=3),
#            connectgaps=True,
        ))
        print(max(data.Month))
    
    
    data2 = traces
    layout = dict(
        #title='Compare visits between museums',
        xaxis=dict(
            range=['2003-12-01','2018-04-20'],
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(count=3,
                         label='3y',
                         step='year',
                         stepmode='backward'),
                    dict(count=5,
                         label='5y',
                         step='year',
                         stepmode='backward'),
                    dict(count=14*12+4,
                         label='All',
                         step='month',
                         stepmode='backward'),
                ])
            ),
            #rangeslider=dict(),
            type='date',
        )
    )
    return dict(data=data2, layout=layout)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)