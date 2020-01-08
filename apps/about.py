import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import commonmodules

from app import app


page_content = html.Div([
                html.Br(),
                html.H3('This is About page'),
             ], className='container')

layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    page_content,
    ])
