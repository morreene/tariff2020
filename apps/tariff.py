import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import commonmodules
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3


from app import app

# Create connection with sqlite
cnx = sqlite3.connect('data.db')
importers = pd.read_sql_query("SELECT * FROM importers", cnx)
# member = pd.read_sql_query("SELECT * FROM all_mem", cnx)
# member_dict = dict(zip(member['MemberCode'], member['Member']))
importers_tuples = [tuple(x) for x in importers[['importerCode','importerName']].values]

exporters = pd.read_sql_query("SELECT * FROM exporters", cnx)
exporters_tuples = [tuple(x) for x in exporters[['exporterCode','exporterName']].values]

hs = pd.read_sql_query("SELECT * FROM hs", cnx)
hs_tuples = [tuple(x) for x in hs[['hs','hs_desc']].values]

page_content = html.Div([
                        # html.Br(),
                        # html.H3('This is tariff page'),
                        dbc.Row(
                            [
                                dbc.Col([
                                    html.P('Importer'),
                                    dcc.Dropdown(
                                        id='dropdown_1',
                                        # options=[{'label': i, 'value': i} for i in ['Select','China', 'Argentina', 'Belgium']],
                                        # options=[{'label': i, 'value': i} for i in [1,2,3]],
                                        options=[{'label': i[1], 'value': i[0]} for i in importers_tuples], # See above

                                        # multi=True,
                                        # value='0. summary',
                                        value='1. economic environment',
                                        clearable=False
                                    ),
                                    ], width=2, align="center"
                                ),
                                dbc.Col(
                                    [
                                    html.P('Exporter'),
                                    dcc.Dropdown(
                                        id='dropdown_2',
                                        # options=[{'label': i, 'value': i} for i in member_list],
                                        # options=[{'label': i, 'value': i} for i in [5,7,8]], # See above
                                        options=[{'label': i[1], 'value': i[0]} for i in exporters_tuples], # See above
                                        value='ALB',
                                        clearable=False
                                    ),
                                    ], width=2
                                ),
                                dbc.Col(
                                    [
                                    html.P('Products'),
                                    dcc.Dropdown(
                                        id='dropdown_2',
                                        # options=[{'label': i, 'value': i} for i in member_list],
                                        # options=[{'label': i, 'value': i} for i in [5,7,8]], # See above
                                        options=[{'label': i[1], 'value': i[0]} for i in hs_tuples], # See above
                                        value='ALB',
                                        clearable=False
                                    ),
                                    ], width=6
                                ),
                                dbc.Col(
                                    [
                                    html.P('Search'),
                                                            # dbc.Input(id="search-input", placeholder="Type something...", type="text", value=''),
                                                            # html.Span('  ', id="example-output", style={"vertical-align": "middle"}),
                                                            dbc.Button('Search', id="search-button", className="mr-2", color="info",),

                                    # dcc.Dropdown(
                                    #     id='dropdown_2',
                                    #     # options=[{'label': i, 'value': i} for i in member_list],
                                    #     options=[{'label': i, 'value': i} for i in [5,7,8]], # See above
                                    #     value='ALB',
                                    #     clearable=False
                                    # ),
                                    ], width=2
                                ),
                            ],
                        ),
                    html.Br(),
                    html.H5('This is tariff page'),
                    html.Div(id='table-container')
             ], className='container')

layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    page_content,
    ])
