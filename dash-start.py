import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()

# Title the app.
app.title = "Chicago Crime Analysis"

# Boostrap CSS.
app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})
app.css.append_css({
    "external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
app.scripts.append_script({
    "external_url": "https://code.jquery.com/jquery-3.2.1.min.js"
})
app.scripts.append_script({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
})

app.layout = html.Div([
    html.H1('Chicago Crime Analysis'),
    html.Iframe(id='basemap', srcDoc=open('maps/crime_map.html','r').read(), width='80%', height='600',style={'border': 'thin lightgrey solid', 'border-radius': '5px 5px 5px 5px'},)
])


if __name__ == '__main__':
    app.run_server(debug=True)