# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask, send_from_directory
import os

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd
import calendar
import locale
from locale import atof

server = Flask(__name__, static_folder='static')
app = dash.Dash(__name__, server=server)
app.scripts.config.serve_locally = True

#develop offline
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

data = pd.read_csv('https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/722503/Monthly_museums_and_galleries_May_2018.csv', encoding='latin1')

# replace - with 0 and convert visit number strings to numeric - should fix this in CSV
data.loc[data.visits.isin(['-']), 'visits'] = '0'
data['visits'] = data['visits'].str.replace(',', '')
data['visits'] = data['visits'].astype(int)
data.loc[data['visits'] == 0,'visits'] = np.nan


#locale.setlocale(locale.LC_NUMERIC, '')
#data['visits'] = pd.DataFrame({'temp': data.visits}).applymap(atof)


museums_list = data.museum.unique()
years_list = data.year.unique()
data['day'] = 1
data['Month'] = pd.to_datetime(data[['month', 'year', 'day']])
raw_data = data.copy()
data = data.pivot(index='Month',columns='museum',values='visits')
data = data.reset_index()
for col in museums_list:
    data[col + '_MA'] = data.rolling(window=12)[col].mean()



# [x for x in museums_list if 'TOTAL' not in x]
museums_list_individual = {
 'BRITISH MUSEUM': ['WC1B 3DG', 51.518970, -0.126500],
 'GEFFRYE MUSEUM': ['E2 8EA', 51.531556, -0.076271],
 'HORNIMAN MUSEUM (Excluding visits to the Garden)': ['SE23 3PQ', 51.441131, -0.060762],
 'IWM LONDON': ['SE1 6HZ', 51.496008, -0.108353],
 'HMS BELFAST (IWM)': ['SE1 2JH', 51.506048, -0.081481],
 'CHURCHILL WAR ROOMS (IWM)': ['SW1A 2AQ', 51.501764, -0.129108],
 'IWM DUXFORD ': ['CB22 4QR', 52.094764, 0.128180],
 'IWM NORTH': ['M17 1TZ', 53.469713, -2.298734],
 'NATIONAL GALLERY': ['WC2N 5DN', 51.509097, -0.127683],
 '(NHM) SOUTH KENSINGTON': ['SW7 5BD', 51.496563, -0.176892],
 '(NHM) TRING': ['HP23 6AP', 51.791524, -0.660652],
 'ROYAL MUSEUMS GREENWICH ': ['SE10 9NF', 51.481154, -0.003746],
 'NATIONAL MUSEUMS LIVERPOOL': ['L3 1DG', 53.406165, -2.995119],
 'NATIONAL COAL MINING MUSEUM FOR ENGLAND': ['WF4 4RH', 53.643479, -1.619416],
 'SCIENCE MUSEUM GROUP SOUTH KENSINGTON ': ['SW7 2DD', 51.497295, -0.176503],
 'SCIENCE MUSEUM GROUP NATIONAL MEDIA MUSEUM': ['BD1 1NQ', 53.790557, -1.756460],
 'SCIENCE MUSEUM GROUP NATIONAL RAILWAY MUSEUM': ['YO26 4XJ', 53.960767, -1.096551],
 'SCIENCE MUSEUM GROUP  LOCOMOTION AT SHILDON': ['DL4 2RE'],
 'SCIENCE MUSEUM GROUP MUSEUM OF SCIENCE AND INDUSTRY, MANCHESTER': ['M3 4FP'],
 'SCIENCE MUSEUM GROUP SWINDON (WROUGHTON)': ['SN4 9LT'],
 'NATIONAL PORTRAIT GALLERY': ['WC2H 0HE'],
 '(RA) LEEDS': ['LS10 1LT'],
 '(RA) FORT NELSON ': ['PO17 6AN'],
 '(RA) WHITE TOWER (BASED AT THE TOWER OF LONDON) ': ['EC3N 4AB'],
 "SIR JOHN SOANE'S MUSEUM": ['WC2A 3BP'],
 'TATE BRITAIN ': ['SW1P 4RG'],
 'TATE MODERN  ': ['SE1 9TG'],
 'TATE LIVERPOOL': ['L3 4BB'],
 'TATE ST IVES': ['TR26 1TG'],
 '(V&A) SOUTH KENSINGTON': ['SW7 2RL'],
 '(V&A) MUSEUM OF CHILDHOOD, BETHNAL GREEN': ['E2 9PA'],
 '(V&A) BLYTHE HOUSE': ['W14 0QX'],
 'WALLACE COLLECTION': ['W1U 3BN'],
 '(T&W) ARBEIA': ['NE33 2BB'],
 '(T&W) DISCOVERY': ['NE1 4JA'],
 '(T&W) GREAT NORTH MUSEUM': ['NE2 4PT'],
 '(T&W) LAING': ['NE1 8AG'],
 '(T&W) WASHINGTON F PIT': ['NE37 1BN'],
 '(T&W) SEGEDUNUM': ['NE28 6HR'],
 '(T&W) SHIPLEY': ['NE8 4JB'],
 '(T&W) SOUTH SHIELDS': ['NE33 2JA'],
 '(T&W) HATTON GALLERY': ['NE1 7RU'],
 '(T&W) STEPHENSON ': ['NE29 8DX'],
 'MUSEUM OF LONDON': ['EC2Y 5HN'],
 'MUSEUM IN DOCKLANDS': ['E14 4AL'],
}

#from geopy.geocoders import GoogleV3
#from geopy.geocoders import Bing
#geolocator = GoogleV3()
#geolocator = Bing(api_key = 'As--8aijMhZO5UZPjONPEaePK5nn16TgjznsOZEYbDTEwgsaL3C364fnOIwzEg8N')
##api_key
#location = geolocator.geocode("BRITISH MUSEUM")
#print((location.latitude, location.longitude))
#geolocator.geocode("WC1B 3DG").latitude
#geolocator.geocode("YO26 4XJ").latitude
#geolocator.geocode("HORNIMAN MUSEUM (Excluding visits to the Garden)").longitude
#
#test = pd.DataFrame({
#    'mus': [x for x in museums_list if 'TOTAL' not in x]
#})
#
#mus_locs = pd.DataFrame.from_dict(museums_list_individual, orient='index')
#mus_locs['location'] = mus_locs[0].apply(geolocator.geocode)
#mus_locs['lon'] = mus_locs['location'].apply(lambda x: x.longitude)
#mus_locs['lat'] = mus_locs['location'].apply(lambda x: x.latitude)
#mus_locs.to_csv('mus_locs.csv')
mus_locs = pd.read_csv('mus_locs.csv', index_col=0)

musy = raw_data.copy()
today = max(musy.Month)
musy = musy.loc[(musy['Month'] > (today - pd.DateOffset(years=1))) & (musy['Month'] <= today)]
last_year = musy.groupby(['museum']).sum()
last_year = last_year.reset_index()
last_year = last_year.loc[last_year['visits'] > 0]

def format_nums(num):
    if num >= 999000:
        fnum = str(round(num / 1000000, 1)) + 'M'
    elif num >= 1000:
        fnum = str(int(round(num / 1000, 0))) + 'k'
    else:
        fnum = str(int(num))
    return(fnum)

last_year['visits_format'] = last_year['visits'].apply(format_nums)

# leaderboard df ---------------------------------------------------------------

leaderboard_mus = ['BRITISH MUSEUM',
 'IWM TOTAL',
 'NHM TOTAL',
 'SCIENCE MUSEUM GROUP TOTAL',
 '(RA) TOTAL',
 'TATE TOTAL',
 '(V&A) TOTAL',
 'TYNE & WEAR TOTAL',
 'HORNIMAN MUSEUM',
 'NATIONAL GALLERY',
 'NATIONAL PORTRAIT GALLERY']
leaderboard_df = last_year.loc[last_year['museum'].isin(leaderboard_mus)]
leaderboard_df = leaderboard_df.sort_values(by='visits', ascending=True)

#leaderboard_df = leaderboard_df[['museum', 'visits_format']]

leaderboard_figure={
        'data': [go.Bar(x=leaderboard_df['visits'], 
                        y=leaderboard_df['museum'],
                        text=leaderboard_df['visits_format'],
                        textposition = 'outside',
                        orientation='h',
                        marker=dict(
                            color='#d40072',
#                            width=3,
                        ),
                        width=0.5,
                        cliponaxis=False,
                        hoverinfo='none'),
                ],
        'layout': go.Layout(margin = dict(l=250, r=100, t=0, b=0, pad=2),
                            xaxis = dict(
                                showgrid=False,
                                zeroline=False,
                                showline=False,),
                            yaxis = dict(
                                showgrid=False,
                                zeroline=False,
                                showline=False,),
                            )
    }


# mapbox df --------------------------------------------------------------------

last_year_map = last_year.loc[last_year['museum'].isin(mus_locs.index)]
last_year_map = last_year_map.set_index(['museum'])

last_year_map['lat'] = mus_locs['lat']
last_year_map['lon'] = mus_locs['lon']

mymin = min(last_year_map['visits'])
mymax = max(last_year_map['visits'])
a = 10
b = 50
def scale_visits(x):
    return ((b-a) * (x - mymin) / (mymax - mymin)) + a

last_year_map['size'] = last_year_map['visits'].apply(scale_visits)

last_year_map['hovertext'] = last_year_map.index + '<br>' + last_year_map['visits_format'].astype(str)


mapbox_access_token = 'pk.eyJ1IjoibWF4d2VsbDg4ODgiLCJhIjoiY2pqcHJpbnF6MDhzMDN3cDRubGJuMzBsayJ9.bA38eIQYmV3OMpwgeeb2Dg'


fig_geo = dict(
    data = [go.Scattermapbox(
        lat=last_year_map['lat'],
        lon=last_year_map['lon'],
        mode='markers',
        marker=dict(
            size=last_year_map['size'],
            color='#d40072',
        ),
#        hovertext='monkey',
        hoverinfo='text',
        hovertext=last_year_map['hovertext'],
    )
    ],

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=52.878051,
                lon=-2.035973
            ),
            pitch=0,
            zoom=5,
            style='mapbox://styles/maxwell8888/cjk150o1k2jho2soarb32una4'
        ),
        margin = dict(l=0, r=0, t=0, b=0),
    )
)



app.css.append_css({"external_url": "https://codepen.io/Maxwell8888/pen/gjGXje.css"})

# layout -----------------------------------------------------------------------

app.layout = html.Div([

    html.Div([
        html.Header([
                html.Div([
                    html.Img(src='https://churchill-beta.dwp.gov.uk/images/logo-gov-white.png', ),
                    html.Div(['Hello world'])], 
                className='header-content',
                ),
        ],
        className='header'
        ),
        
        html.Div([
            html.H1(children='DCMS Museum Visits (draft version)', className='myh1'),
            
            html.Div([
                html.H3(children='Visitor numbers in last 12 Months', className='myh3'),
    
                dcc.Graph(id='leaderboard', figure=leaderboard_figure, config={'displayModeBar': False, 'staticPlot': True}, className='lb'),
                    
                dcc.Graph(id='my-graph-geo', figure = fig_geo, config={'displayModeBar': False}, className='map'),    
            ],
            className='vn mysec',
            ),
            
            html.Div([
                html.H3(children='Time series', className='myh32'),
                
                # I beleive dash wraps the dropdown in a div when using the id property, but the class will be in the child, so need to wrap in another div to set a class for the css grid.
                html.Div([ 
                    dcc.Dropdown(
                                id='my-dropdown',
                                options=[{'label': i, 'value': i} for i in museums_list],
                                value=['BRITISH MUSEUM', 'IWM TOTAL'],
                                multi=True
                            ),
                ],
                className='dp1',
                ),
                
                html.Div([
                    html.Button('Actual', id='button-1', className='actual-bt'),
                    html.Button('Moving Average', id='button-2', className='ma-bt'),
                ],
                className='ts-bts',
                ),
                html.Div([dcc.Graph(id='my-graph', config={'displayModeBar': False})], className='graph1'),
            ],
            className='ts mysec',
            ),
    
            html.Div([
                html.H3(children='Seasonal comparison', className='myh33'),
                
                html.Div([
                    dcc.Dropdown(
                        id='my-dropdown2',
                        options=[{'label': i, 'value': i} for i in museums_list],
                        value='TOTAL VISITOR FIGURES')],
                className='dp2',
                ),
                html.Div([
                    dcc.Dropdown(
                        id='choose-years',
                        options=[{'label': i, 'value': i} for i in years_list],
                        value=[2016, 2017, 2018],
                        multi=True)],
                className='dp3'
                ),
            
                dcc.Graph(id='my-graph2', config={'displayModeBar': False}, className='graph2'),
            ],
            className='seasonal mysec',
            ),            
            
        ],
        className='main',
        ),
        html.Div(['this is my foot.'], className='footer'),
#        html.Div(['four'], className='sidebar'),
#        html.Div(['five'], className='five'),
#        html.Div(['six'], className='six'),
    ], 
    className='wrapper'
    ),
    
    html.Div('off', id = 'hidden-div1', style = {'display': 'none'}),
    html.Div('off', id = 'hidden-div2', style = {'display': 'none'}),

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


dcms_colours = ['#d40072', '#a03155', '#4c2c92', '#005ea5', '#792540']
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
                line=dict(color=colour_list[i % len(colour_list)]),
            ))    
        if but2 == 'on':
            traces.append(go.Scatter(
                x=data.Month,
                y=data[selected_dropdown_value[i] + '_MA'],
                mode = 'lines',
                name=musy+' (MA)',
                showlegend=False,
                hoverinfo='none',
                line=dict(color=colour_list[i % len(colour_list)], dash='dash'),
            ))
        if but1 == 'off' and but2 == 'on':
            traces.append(go.Scatter(
                x=data.Month,
                y=data[selected_dropdown_value[i] + '_MA'],
                mode = 'lines',
                name=musy+' (MA)',
                showlegend=True,
                line=dict(color=colour_list[i % len(colour_list)], dash='dash'),
            ))



    
    layout = dict(
        #title='Compare visits between museums',
        xaxis=dict(
            range=['2003-12-01','2018-05-20'],
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
                    dict(count=14*12+5,
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


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run_server(debug=True)
