import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from apps import linechart, home, tariff, about, help


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return home.layout
    elif pathname == '/linechart':
         return linechart.layout
    elif pathname == '/tariff':
         return tariff.layout
    elif pathname == '/about':
         return about.layout
    elif pathname == '/help':
         return help.layout
    else:
        return '404'

# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.callback(
    Output(f"navbar-collapse2", "is_open"),
    [Input(f"navbar-toggler2", "n_clicks")],
    [State(f"navbar-collapse2", "is_open")],
)(toggle_navbar_collapse)

server = app.server
# app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run_server(debug=True)
