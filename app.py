import dash
import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html

# print(dcc.__version__) # 0.6.0 or above is required

# app = dash.Dash()
# external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
#                 "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
#                 "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# server = app.server
app.config.suppress_callback_exceptions = True

# if __name__ == '__main__':
#     app.run_server(debug=True)
