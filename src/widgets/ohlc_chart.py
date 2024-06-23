import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc

def create_ohlc_chart(chart_data):
    fig = go.Figure(data=[go.Ohlc(x=chart_data['Date'],
                                  open=chart_data['Open'],
                                  high=chart_data['High'],
                                  low=chart_data['Low'],
                                  close=chart_data['Close'])])

    fig.update_layout(title='OHLC Chart',
                      xaxis_title='Date',
                      yaxis_title='Value')

    return html.Div(dcc.Graph(figure=fig))

# Sample data, replace with your actual data source
chart_data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Open': [30, 31, 32, 33, 30, 28, 29, 30, 31, 33, 34, 32, 31, 33, 35, 36, 37, 38, 39, 40, 39, 38, 37, 35, 34, 33, 32, 31, 30, 28],
    'High': [31, 32, 33, 34, 32, 29, 30, 32, 33, 35, 36, 34, 33, 35, 37, 38, 39, 40, 41, 42, 41, 40, 39, 37, 36, 35, 34, 33, 32, 30],
    'Low': [29, 30, 31, 32, 29, 27, 28, 29, 30, 32, 33, 31, 30, 32, 34, 35, 36, 37, 38, 39, 38, 37, 36, 34, 33, 32, 31, 30, 29, 27],
    'Close': [30, 31, 32, 31, 29, 28, 29, 31, 32, 34, 33, 32, 32, 34, 36, 37, 38, 39, 40, 39, 38, 37, 35, 36, 34, 33, 32, 31, 29, 28]
})
