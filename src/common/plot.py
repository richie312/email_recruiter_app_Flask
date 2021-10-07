# -*- coding: utf-8 -*-

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from src.common.helper_functions import collect_location_wise_count,tenure_dict
from datetime import datetime
from dotenv import load_dotenv
import os

# loads the  env vars from the root project  folder
main_dir = os.getcwd()
load_dotenv(dotenv_path=os.path.join(main_dir, '../../.env'))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
url = os.getenv('url')

data = collect_location_wise_count(url,180)
months = list(set(data['month'].values.tolist()))    

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,suppress_callback_exceptions=True)
def app_layout():
    return(
            html.Div([
                    dcc.Dropdown(
                    id='demo-dropdown',
                    options=[
                        {'label': 'Last Six Months', 'value': 180},
                        {'label': 'Last 3 Months', 'value': 90},
                        {'label': 'Last One Month', 'value': 30},
                        {'label': 'Last One Week', 'value': 7},
                        {'label': 'Last 2 Days', 'value': 2},
                        
                    ],
                    value= 180
                ),
                html.Div(id='dd-output-container'),
                
        html.Div([html.H1("Application Descriptive Statistics - {}".format(datetime.now().year))], style={"textAlign": "center"}),
        dcc.Graph(id="my-graph"),html.Div(id='data_pass'),
        html.Div([dcc.Slider(id='month-selected', min=min(data['month']), max=max(data['month']), value=max(data['month']),
                             marks= tenure_dict(months))],
                 style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "65%", "margin-left": "auto",
                        "margin-right": "auto"}),
    
    ], className="container")
    )
app.layout=app_layout()

# call back function for dropdown
# =============================================================================
# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('demo-dropdown', 'value')])
# def update_output(value):
#     #data = collect_location_wise_count(url,value)
#     #months = list(set(data['month'].values.tolist()))
#     #data_updated = data.to_json()
#     return 'You have selected "{}"'.format(value)
# 
# =============================================================================

# call back function for locationwise plot
@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("month-selected","value")]
)  
def update_graph(selected):
    #data = pd.read_json(data_updated)
    return {
        "data": [go.Pie(labels=data['Location'][data['month'] == selected].values.tolist(), values=data['Group_Count'][data['month'] == selected].values.tolist(),
                        marker={'colors': ['#EF963B', '#C93277', '#349600', '#EF533B', '#57D4F1']}, textinfo='label')],
        "layout": go.Layout(title="Location wise Application History", margin={"l": 300, "r": 300, },
                            legend={"x": 1, "y": 0.7})}


# =============================================================================
# @app.callback(
#     dash.dependencies.Output("my-graph", "figure"),
#     [dash.dependencies.Input("month-selected", "value")]
# )
# def update_graph(selected):
#     return {
#         "data": [go.Pie(labels=data['Location'][data['month'] == selected].values.tolist(), values=data['Group_Count'][data['month'] == selected].values.tolist(),
#                         marker={'colors': ['#EF963B', '#C93277', '#349600', '#EF533B', '#57D4F1']}, textinfo='label')],
#         "layout": go.Layout(title="Location wise Application History", margin={"l": 300, "r": 300, },
#                             legend={"x": 1, "y": 0.7})}
# 
# =============================================================================
        
if __name__ == '__main__':
    app.server.run(host = '0.0.0.0',port = int(os.getenv('port')),debug = True)