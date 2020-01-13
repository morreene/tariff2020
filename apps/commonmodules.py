import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

def get_header():
    header = html.Div([
                html.Div([
                    html.H1(
                        'Dash Boiler Plate')
                ], className="twelve columns padded"),
            ], className="row gs-header gs-text-header")
    return header

def get_menu():
    nav_item_1 = dbc.NavItem(dbc.NavLink("Home", href="/"))
    nav_item_2 = dbc.NavItem(dbc.NavLink("Line Chart", href="/linechart"))
    nav_item_3 = dbc.NavItem(dbc.NavLink("Tariff", href="/tariff"))
    nav_item_4 = dbc.NavItem(dbc.NavLink("About", href="/about"))
    nav_item_5 = dbc.NavItem(dbc.NavLink("Help", href="/help"))
    nav_item_6 = dbc.NavItem(dbc.NavLink("Search[fater]", href="/search"))

    logo = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Find Tariff", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://plot.ly",
                ),
                dbc.NavbarToggler(id="navbar-toggler2"),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item_1, nav_item_2, nav_item_3, nav_item_4, nav_item_5, nav_item_6], className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ]
        ),
        # color="dark",
        # dark=True,
        className="mb-5",
    )
    return logo
