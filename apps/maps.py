import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from  dash.dependencies import Input,Output

from dash_layout import navbar,footer
from app import app

import pandas as pd
community_area = pd.read_csv('apps/data/community_areas.csv')

"""
Card Area
"""
ca_table = dbc.Table.from_dataframe(community_area[['Community Area','Community Name','Number of Crimes']], striped=True, bordered=True, hover=True,size='sm',responsive ='sm')
ca_card = dbc.Col([
        dbc.CardHeader(html.H4("Community Area Information Table")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.Row(ca_table,style={'height':'400px','align-content': 'right','overflow-y': 'scroll'}),
                    width=9
                ),
                dbc.Col([
                    html.P(
                        """
                        This table displays the information about Community Area Code, name, and its crime number.
                        """
                    ),
                    html.P(
                        """
                        The highest number of crime are found in Near North Side with 9488 incidents, followed by Austin with 9129 incidents, and Loop area with 8022 incidents.
                        """
                    )
                ],width=3)
            ])
        ])
    ])

# Tabs
tabs = dbc.Col(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Choropleth Map", tab_id="tab-1"),
                dbc.Tab(label="Community Area", tab_id="tab-2"),
                dbc.Tab(label="Heatmap", tab_id="tab-3"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

body = dbc.Container([
    dbc.Col([
            dbc.Row([
                dbc.Card(tabs),
            ],
            style={
                'widht':'100%',
                'margin':'10px'
            }),
            dbc.Row([
                dbc.Card(ca_card, color='light')
            ], style={
                'widht':'100%',
                'margin':'10px'
            }),
            dbc.Row([
                dbc.Col(width=12)
            ],
            style={'padding':'10px'})
        ])
    ],
    className="mt-4",
    style={'width':'80%'}
)

layout = html.Div([navbar, body, footer])
@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-2":
        tab2_content = dbc.Row([
            dbc.Col(
                html.Iframe(
                    id='basemap', 
                    srcDoc=open('maps/basemap.html','r').read(), 
                    width='100%', height='600',
                    style={'border': 'none', 'border-radius': '5px 5px 5px 5px', 'margin-left':'0px'}),
                width=9,
                style={'padding-left':'0px'}
               
            ),
            dbc.Col([
                dbc.Row(
                    html.H2("Community Area Information"),
                    align="start"
                ),
                dbc.Row([
                    html.P(
                        """
                        This map displays information of each community areas which consist of the name and community area code. 
                        """
                    ),
                      html.P(
                        """
                        Click the marker to display the crime number.
                        """
                    ),
                ], 
                align="end")
            ],width=3)
        ],
            style={'margin-left':'0px'}
        )
        return tab2_content
    elif at == "tab-1":
        tab1_content = dbc. Row([
            dbc.Col(
                html.Iframe(
                    id='chicago_choropleth', 
                    srcDoc=open('maps/chicago_coropleth.html','r').read(), 
                    width='100%', height='600',
                    style={'border': 'none', 'border-radius': '5px 5px 5px 5px', 'margin-left':'0px'}),
                width=9,
                style={'padding-left':'0px'}
            ),
            dbc.Col([
                dbc.Row(
                    html.H2("Choropleth Map of Chicago Crime"),
                    align="center"
                ),
                dbc.Row([
                    html.P(
                        """
                        This map displays the proportions of crime in each community area. 
                        """
                    ),
                      html.P(
                        """
                        From this map we can see that the crime numbers are higher in the eastern and western middle part of city.
                        """
                    ),
                ], 
                align="end")
            ],width=3)
        ],
            style={'margin-left':'0px'}
        )
        return tab1_content
    elif at == "tab-3":
        tab3_content = dbc. Row([
            dbc.Col(
                html.Iframe(
                    id='crime_map', 
                    srcDoc=open('maps/crime_map.html','r').read(), 
                    width='100%', height='600',
                    style={'border': 'thin lightgrey solid', 'border-radius': '5px 5px 5px 5px'}),
                width=9,
                style={'padding-left':'0px'}
               
            ),
            dbc.Col([
                dbc.Row(
                    html.H2("Chicago Crime Heatmap"),
                    align="start"
                ),
                dbc.Row([
                    html.P(
                        """
                        This a heatmap display that displays the cluster points of every 100 crimes nearby. 
                        The more clusters overlap, the more red-ish the color.  
                        """
                    ),
                      html.P(
                        """
                        Zoom the map to pinpoint the center position of
                        the cluster.
                        """
                    ),
                ])
            ],width=3)
        ], 
            style={'margin-left':'0px'}
        )
        return tab3_content
    else:
        return "This should't have happened..."

# if __name__ == "__main__":
#     app.run_server(debug=True)