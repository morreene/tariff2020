import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import commonmodules

from app import app


page_content = html.Div([
                    html.Br(),
                    html.H3('Line Chart'),
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [
                                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
                            ],
                            'layout': {
                                'title': 'Dash Data Visualization'
                            }
                        }
                    ),
             ], className='container')




layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    page_content
])
