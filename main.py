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
import calendar

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.scripts.config.serve_locally = True

data = pd.read_csv('https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/714411/Monthly_museums_and_galleries_April_2018.csv', encoding='latin1')
raw_data = data.copy()
museums_list = data.museum.unique()
years_list = data.year.unique()
data['day'] = 1
data['Month'] = pd.to_datetime(data[['month', 'year', 'day']])
data = data.pivot(index='Month',columns='museum',values='visits')
data = data.reset_index()


app.layout = html.Div(children=[
    html.H1(children='Museums Dashboard'),
    html.H2(children='Compare visits between museums'),
    dcc.Dropdown(
                id='my-dropdown',
                options=[{'label': i, 'value': i} for i in museums_list],
                value=['BRITISH MUSEUM', 'NATIONAL GALLERY', 'TATE TOTAL'],
                multi=True
            ),
    html.Div(id='my-div'),
    dcc.Graph(id='my-graph'),
    html.H2(children='Compare seasons for a museum'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='my-dropdown2',
                options=[{'label': i, 'value': i} for i in museums_list],
                value='BRITISH MUSEUM')],
            style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='choose-years',
                options=[{'label': i, 'value': i} for i in years_list],
                value=[2016, 2017, 2018],
                multi=True)],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
        ),

    ]),
    dcc.Graph(id='my-graph2'),
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
    return dict(data=traces, layout=layout)

@app.callback(Output('my-graph2', 'figure'), [Input('my-dropdown2', 'value'), Input('choose-years', 'value')])
def update_graph2(selected_dropdown_value, years):
    season_data = raw_data
    season_data = season_data.loc[season_data.museum == selected_dropdown_value]
#    season_data['month_name'] = season_data['month'].apply(lambda x: calendar.month_abbr[x])
    season_data = season_data.pivot(index='month',columns='year',values='visits')
    season_data = season_data.reset_index()
    season_data['day'] = 1
    season_data['year'] = 2018
    season_data['Month'] = pd.to_datetime(season_data[['month', 'year', 'day']])
#    season_data['Month'] = data.Month.apply(lambda x: x.strftime('%b'))

    traces = []
    for i in years:
        traces.append(go.Scatter(
            x=season_data.Month,
            y=season_data[i],
            name=str(i)
        ))
        
    layout = dict(
        xaxis=dict(
            #range=[4,5,6,7,8,9,10,11,12,1,2,3],
            #rangeslider=dict(),
            #type='category',
            tickformat= '%b'
        )
    )
    return dict(data=traces, layout=layout)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server()