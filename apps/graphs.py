import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from  dash.dependencies import Input,Output,State

import dash_table as dtable

from dash_layout import navbar,footer
from app import app

import pandas as pd
import numpy as np

"""
Processing Data
"""
crimes = pd.read_csv('apps/data/serious_crime.csv')

"""
Card Area
"""
#primary types
types=[]
instances=[]
for primary_type,instance in crimes.groupby('Primary Type'):
  types.append(primary_type)
  instances.append(len(instance))

primary_type_card = dbc.Card([
    dbc.CardHeader(html.H4("Crimes by Primary Type")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                    html.P(
                            """
                            This graph displays the number and the related types of crime.
                            """
                        ),
                        html.P(
                            """
                            Most common crimes are theft with 63 thousands incidents, battery with nearlt 50 thousands incidents, and followed by assault with 20 thousand insidents.
                            """
                        )
                ],width=3),
            dbc.Col([
                dbc.Row(
                dcc.Graph(
                    figure={
                        'data':[
                            {'x':types,'y':instances,'type': 'bar', 'marker':{
                                'color':'gray'
                            }}
                        ]
                    }
                )
                )
            ],width=9,style={'content-align':'center'})
        ])
    ])
])

#monthly types
crime_sums=[]
months=[]

for month,crime_sum in crimes.groupby('Month'):
  months.append(month)
  crime_sums.append(len(crime_sum))
month_list = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October','November','December']

for mo in range(0,len(months)):
    months[mo] = month_list[mo]

months_card = dbc.Card([
    dbc.CardHeader(html.H4("Monthly Crime Data")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Row(
                dcc.Graph(
                    figure={
                        'data':[
                            {'x':months,'y':crime_sums,'type': 'line', 'marker':{
                                'color':'gray'
                                }, 
                            }
                        ],
                    },
                )
            ), 
            ],width=9,style={'content-align':'center'}),
            dbc.Col([
                    html.P(
                            """
                            This graph displays the number throughout the year.
                            """
                        ),
                        html.P(
                            """
                            August has the highest number of crimes, while february has the lowest. This is quite interesting due February usually is the coldest month of the year and August is usually the warmest.
                            """
                        )
                ],width=3),
        ])
    ])
])

#day/night
nightday =[]
sum_crimes=[]

for zx,crime in crimes.groupby('DayFlag'):
    if zx == False:
        nightday.append('Night')
    elif zx == True:
        nightday.append('Day')
    sum_crimes.append(len(crime))

day_night_card = dbc.Card([
    dbc.CardHeader(html.H4("Crimes by Primary Type")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                    html.P(
                            """
                            This graph displays the numbers of crime differences between day and night.
                            """
                        ),
                        html.P(
                            """
                            From this data we can see that most of the crime was happened during the daylight (7AM to 7PM).
                            """
                        )
                ],width=3),
            dbc.Col([
                dbc.Row(
                dcc.Graph(
                    figure={
                        'data':[
                            {'x':nightday,'y':sum_crimes,'type': 'bar', 'marker':{
                                'color':'gray'
                            }}
                        ]
                    }
                )
                )
            ],width=9,style={'content-align':'center'})
        ])
    ])
])
    

#by location
locations=[]
instances2=[]

for location,crime in crimes.groupby('Location Description'):
  if len(crime) > 5000:
    locations.append(location)
    instances2.append(len(crime))

locational = dbc.Card([
    dbc.CardHeader(html.H4("Crime locations")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Row(
                dcc.Graph(
                    figure={
                        'data':[
                            {'x':locations,'y':instances2,'type': 'bar', 'marker':{
                                'color':'gray'
                            }}
                        ]
                    }
                )
            ), 
            ],width=9,style={'content-align':'center'}),
            dbc.Col([
                    html.P(
                            """
                            This graph displays where the locations of the crimes occured.
                            """
                        ),
                        html.P(
                            """
                            Most crimes take place in the streets, followed by apartment, residence, and sidewalk.
                            """
                        )
                ],width=3),
        ])
    ],style={'height':'600px'})
])


"""
Body Area
"""

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row(primary_type_card)
        ],style={'width':'100%','margin':'5px'}),
        dbc.Col([
            dbc.Row(months_card)
        ],style={'width':'100%','margin':'5px'}),
        dbc.Col([
            dbc.Row(day_night_card)
        ],style={'width':'100%','margin':'5px'}),
         dbc.Col([
            dbc.Row(locational)
        ],style={'width':'100%','margin':'5px'}),
        dbc.Row([
            dbc.Col(width=12)
        ],style={'padding':'10px'})
    ])
],
className="mt-4",
style={'width':'80%'}
)

layout = html.Div([navbar, body, footer])

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open