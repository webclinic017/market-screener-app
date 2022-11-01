
import dash
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import plotly.graph_objects as go
import yfinance as yf
from def_symbols import TIMEFRAMES, get_symbol_names
from screener import get_data, add_indicators, confluence, screener

# creates the Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) #dbc.themes.ZEPHYR]

test_png = 'Xavier_Mcallister.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

# creates the layout of the App
app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(test_base64),
            style={'height':'25%', 'width':'25%'}),
    
    html.H1(children = 'Market Screener',
    style={'margin-left': '15%', 
           'margin-right': '15%', 
           'margin-top': '20px',
           'text_align' : 'center',
           #'color' : '#ff0000',
           #'border': '1px solid red'
          }),
    
    html.Hr(), 
    
    html.Div(id='live-update-table',
            style={'margin-left': '15%', 
                   'margin-right': '15%', 
                   'margin-top': '20px',
                   'text_align' : 'center',
                   #'color' : '#ff0000',
                   #'border': '1px solid red',
                    "height": "90vh", "maxHeight": "900vh"
                  }),
    dcc.Interval(id='update', interval=20000, n_intervals=0),
    
])

@app.callback(Output('live-update-table', 'children'),
              Input('update', 'n_intervals'))

def update_table(n):
    #table = get_data("AUDUSD", mt5.TIMEFRAME_M5)
    table = screener()

    return [
            dbc.Container([
                dash_table.DataTable(table.to_dict('records'),[{"name": i, "id": i} for i in table.columns], id='tbl',
                fixed_rows={'headers': True},
                                     
            style_table={#"background-color": "#36454F", 
                         "height": "90vh", "maxHeight": "90vh", 'overflow':'hidden'}, #, 'align':'right'},
            style_cell={'textAlign': 'center',
                       #'backgroundColor': '#36454F',
                        'color': 'white'},

            style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white','fontWeight': 'bold'  }, 

            style_data={
                    'backgroundColor': '#000000',
                    'color': 'white'
                        },

            style_data_conditional=[
                        {
                        'if': {
                            'column_id': 'Currency'
                        },
                        'color': 'lightblue'
                        },
                {
                    'if': {
                        'filter_query': '{Rating} contains "Sell"'
                    },
                    'color': 'red'
                },

                        {
                    'if': {
                        'filter_query': '{Rating} contains "Buy"'
                    },
                    'color': 'green'
                },

                {
                    'if': {
                        'filter_query': '{Rating} contains "Neutral"'
                    },
                    'color': 'white'
                }

            ],
            style_as_list_view=True,

                )
               ])
                ]
           

if __name__ == '__main__':
    # starts the server
    app.run_server()

