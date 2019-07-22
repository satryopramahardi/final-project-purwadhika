import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from dash_layout import navbar,footer
from app import app

import pandas as pd
crimes = pd.read_csv('apps/data/serious_crime.csv')

headers = dbc.Col([
        dbc.Container(
            [
                html.Div([
                    html.H1("Crimes in Chicago",style={'color':'white','vertical-align':'bottom','font-size':'72px','margin':'25px'}),
                    html.Hr(className="my-2"),
                    html.Div(html.P("Chicago crimes analysis and clustering using machine learning",style={'color':'white','font-size':'18px'}),style={'right':0,'bottom':0,'position': 'absolute','margin-right':'25px'})
                    
                ],
                    style={'right': 0, 'bottom': 0, 'position': 'absolute'}
                )
            ], style={'width':'80%'})
],style={'background-image': "url('static/header.jpg')",'background-size': 'cover','background-repeat':' no-repeat','height':'400px'})

analisyss = dbc.Card([
    dbc.CardHeader(html.H2("Go to Analysis",style={'font-size':'36px'})),
    dbc.CardBody([
        html.P("Take a look at the crime stats to see descriptive analysis of the data, or go to the mapping page to see the data mapping and clustering"),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardImg(src='static/home3.png',style={'object-fit':'cover','height':'250px'}),            
                    dbc.CardLink("Crime Stats and Graph", href="http://localhost:8050/crimes"),
                ],style={'padding':'5px','text-align':'center'}),width = 6
            ),dbc.Col(
                dbc.Card([
                    dbc.CardImg(src='static/home2.jpg',style={'object-fit':'cover','height':'250px'}),            
                    dbc.CardLink("Mapping and Clustering", href="http://localhost:8050/maps"),
                ],style={'padding':'5px','text-align':'center'}),width = 6
            )
        ])
        
    ])
])

body = dbc.Container([
    dbc.Col([
        dbc.Card([
        dbc.Col([
            dbc.CardHeader(html.H1("Crimes in Chichago",style={'font-size':'36px'})),
            dbc.Row([
                dbc.Col([
                    html.P("""
                    An analysis project by using data from the Chicago Police Department. This experiment aims to provide information that may help the city police to alocate their forces by clustering past criminal incidents through the year 2018 with over 170 thousand records.
                    """,style={'text-align':'justify'}),
                    html.P("According to Chicago Police, serious offence includes: "),
                    html.Div([dcc.Markdown('''
                    * Homicide 1st & 2nd Degree 
                    * Criminal Sexual Assault 
                    * Robbery 
                    * Aggravated Assault
                    * Aggravated Battery 
                    * Burglary 
                    * Larceny 
                    * Motor Vehicle Theft 
                    * Arson 
                    ''')
                    ])
                ],width=6),
                dbc.Col([
                    dbc.Card(
                        dbc.CardImg(src="static/home1.jpg", top=True,style={'height':'350px','object-fit':'cover',}),
                        style={'margin':'10px'}
                    )
                ],width=6)
                ],style={'margin-top':'10px'})
            ])
        ], style={'margin':'10px'}),
        dbc.Col(analisyss,style={'margin-top':'10px'})
    ])
],className="mt-4")


layout=[navbar,headers,body,footer]