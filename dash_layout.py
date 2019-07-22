import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

#Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem(dbc.NavLink("Home", href="http://localhost:8050/")),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(dbc.NavLink("Crime Stats", href="http://localhost:8050/crimes")),
                dbc.DropdownMenuItem(dbc.NavLink("Mapping", href="http://localhost:8050/maps")),
            ],
        ),
    ],
    brand="Chicago Crime Analysis",
    # brand_href="#",
    sticky="top",
    # dark=True
)

#footer
footer = dbc.NavbarSimple(
    children=[
        dbc.Col([
            html.P("Made by Using Dash")
        ],
        width=12,
        align='end',
        style={'padding':'5px','left':'0','bottom':'0','width':'100%'})
])