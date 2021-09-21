import dash,os
from layout import layout
from callbacks import register_callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://cdn.plot.ly/plotly-locale-nl-latest.js']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=external_scripts, url_base_pathname='/dash/')
app.layout = layout
#--! Set Dash to suppress callback exceptions, because some callbacks can only be made when the first callback in the main layout has been made.
app.config['suppress_callback_exceptions'] = False
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8050)