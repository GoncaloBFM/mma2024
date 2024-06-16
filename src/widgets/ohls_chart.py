import dash
from dash import dcc
import plotly.graph_objects as go
import pandas as pd

def create_ohlc_chart(data):
    fig = go.Figure(data=[go.Ohlc(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green', decreasing_line_color='red'
    )])

    fig.update_layout(
        title='OHLC Chart',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return dcc.Graph(figure=fig)
