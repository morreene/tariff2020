# Compared to tariff.py, this module loads hs descriptions for the form from a dictioary in hsdesc.py
# directly, instead of from sqLite. This make the loading faster.

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import commonmodules
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
from apps.hsdesc import hs_dict, exporters_tuples
import dash_table
from app import app

importers_tuples = [('156','China'),('840', 'USA')]

# Create connection with sqlite
# cnx = sqlite3.connect('data.db')
# importers = pd.read_sql_query("SELECT * FROM importers", cnx)
# importers_tuples = [tuple(x) for x in importers[['importerCode','importerName']].values]
# exporters = pd.read_sql_query("SELECT * FROM exporters", cnx)
# exporters_tuples = [tuple(x) for x in exporters[['exporterCode','exporterName']].values]
# hs = pd.read_sql_query("SELECT * FROM hs", cnx)
# hs_tuples = [tuple(x) for x in hs[['hs','hs_desc']].values]
# cnx.close()

page_content = html.Div([
                        # html.Br(),
                        dbc.Row(
                            [
                                dbc.Col([
                                    html.Span('Importer'),
                                    dcc.Dropdown(
                                        id='dropdown_importer',
                                        # options=[{'label': i, 'value': i} for i in ['Select','China', 'Argentina', 'Belgium']],
                                        # options=[{'label': i, 'value': i} for i in [1,2,3]],
                                        options=[{'label': i[1], 'value': i[0]} for i in importers_tuples], # See above

                                        # multi=True,
                                        # value='0. summary',
                                        value='156',
                                        clearable=False,

                                    ),
                                    ], width=2, align="center"
                                ),
                                dbc.Col(
                                    [
                                    html.Span('Exporter'),
                                    dcc.Dropdown(
                                        id='dropdown_exporter',
                                        options=[{'label': i[1], 'value': i[0]} for i in exporters_tuples], # See above
                                        value='418',
                                        clearable=False
                                    ),
                                    ], width=2
                                ),
                                dbc.Col(
                                    [
                                    html.Span('Products'),
                                    dcc.Dropdown(
                                        id='dropdown_hs',
                                        options = hs_dict,
                                        value='100620',
                                        clearable=False
                                    ),
                                    ], width=7
                                ),
                                dbc.Col(
                                    [
                                    html.Span('\u00A0'),
                                    dbc.Button('Search', id="search-button", className="mr-2", color="info",),
                                    ], width=1
                                ),
                            ],
                        ),
                    html.Br(),html.Br(),
                    html.P('Testing variables: Importer: China; Exporter: Laos; Product: HS 100620'),
                    html.Div(id='search-result-container')
             ], className='container')

layout = html.Div([
    # commonmodules.get_header(),
    commonmodules.get_menu(),
    page_content,
    ])


@app.callback(
        # dash.dependencies.Output('result-container', 'children'),
        Output('search-result-container', 'children'),
        [Input('dropdown_importer', 'value'),
         Input('dropdown_exporter', 'value'),
         Input('dropdown_hs', 'value'),
         Input('search-button', 'n_clicks')]
        # [dash.dependencies.State('search-input', 'value')]
    )
def display_table(dropdown_value_1, dropdown_value_2, dropdown_value_3, n_clicks):
    # dff = df[(df['Cat'].str.contains(dropdown_value_1)) & (df['ConcernedCountriesCode'].str.contains(dropdown_value_2))]
    cnx = sqlite3.connect('data.db')
    data_rate = pd.read_sql_query("SELECT * FROM data_rate WHERE reporter='" + dropdown_value_1 + "' AND substr(hs,1,6)='" + dropdown_value_3 + "'", cnx)
    data_type = pd.read_sql_query("SELECT * FROM data_type WHERE reporter='" + dropdown_value_1 + "' AND partner in (" + dropdown_value_2 + ", '000')", cnx)
    dff = pd.merge(data_rate, data_type, on=['reporter','type_code'])
    cnx.close()

    return html.Div([
            dbc.Alert('Importer: '+ dropdown_value_1 + ' Exporter: ' + dropdown_value_2 + ' HS: ' + dropdown_value_3),
            dash_table.DataTable(
                    id='tab',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
                    ],
                    data = dff.to_dict('records'),
                    editable=False,
                    # filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable=False,
                    row_selectable=False,
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 20,
                    style_cell={
                    'height': 'auto',
                    'minWidth': '50px', 'maxWidth': '180px',
                    'whiteSpace': 'normal',
                    'textAlign': 'left',
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'Symbol'},
                         'width': '100px'},
                        {'if': {'column_id': 'Member'},
                         'width': '70px'},
                        {'if': {'column_id': 'ReportDate'},
                         'width': '90px'},
                        {'if': {'column_id': 'Topic'},
                         'width': '200px'},
                        {'if': {'column_id': 'ParaID'},
                         'width': '40px'},
                    ]
                )
])
