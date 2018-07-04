import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd
import calendar
import locale
from locale import atof

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.scripts.config.serve_locally = True

data = pd.read_csv('https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/714411/Monthly_museums_and_galleries_April_2018.csv', encoding='latin1')

# replace - with 0 and convert visit number strings to numeric - should fix this in CSV
locale.setlocale(locale.LC_NUMERIC, '')
data.loc[data.visits.isin(['-']), 'visits'] = '0'
data['visits'] = pd.DataFrame({'temp': data.visits}).applymap(atof)

raw_data = data.copy()
museums_list = data.museum.unique()
years_list = data.year.unique()
data['day'] = 1
data['Month'] = pd.to_datetime(data[['month', 'year', 'day']])
data = data.pivot(index='Month',columns='museum',values='visits')
data = data.reset_index()
for col in museums_list:
    data[col + '_MA'] = data.rolling(window=12)[col].mean()

app.layout = html.Div(children=[
    
    html.H1(children='Museums Dashboard fdfa'),
    html.H2(children='Compare visits between museums'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                        id='my-dropdown',
                        options=[{'label': i, 'value': i} for i in museums_list],
                        value=['BRITISH MUSEUM', 'IWM TOTAL'],
                        multi=True
                    ),
        ],
        className="six columns"
        ),
        html.Div([
            html.Button('Absolute Values', id='button-1'),
            html.Button('MA', id='button-2'),
        ],
        className="six columns"        
        ),
    ],
    #style={'columnCount': 2}
    className='row'
    ),
    
    html.Div(id='my-div'),
    html.Div('off', id = 'hidden-div1', style = {'display': 'none'}),
    html.Div('off', id = 'hidden-div2', style = {'display': 'none'}),
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


# we need seperate callbacks so that we can update the hidden div
@app.callback(
    Output('hidden-div1', 'children'),
    [Input('button-1', 'n_clicks')],
    [State('hidden-div1', 'children')])
def get_selected_data1(clicks, state):
    mystr = 'on'
    if state == 'on':
        mystr = 'off'
    return mystr

@app.callback(
    Output('hidden-div2', 'children'),
    [Input('button-2', 'n_clicks')],
    [State('hidden-div2', 'children')])
def get_selected_data2(clicks, state):
    mystr = 'on'
    if state == 'on':
        mystr = 'off'
    return mystr


colour_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'), Input('hidden-div1', 'children'), Input('hidden-div2', 'children')])
def update_graph(selected_dropdown_value, but1, but2):
    traces = []
    
    for i, musy in enumerate(selected_dropdown_value):
        if but1 == 'on':
            traces.append(go.Scatter(
                x=data.Month,
                y=data[selected_dropdown_value[i]],
                mode = 'lines+markers',
                name = musy,
                line=dict(color=colour_list[i % len(colour_list)], width=3),
    #            connectgaps=True,
            ))    
        if but2 == 'on':
            traces.append(go.Scatter(
                x=data.Month,
                y=data[selected_dropdown_value[i] + '_MA'],
                mode = 'lines',
                showlegend=False,
                line=dict(color=colour_list[i % len(colour_list)], dash='dash', width=3),
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
    app.run_server(debug=True)