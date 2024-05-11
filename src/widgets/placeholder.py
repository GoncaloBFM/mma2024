from dash import dcc
import plotly.express as px

def create_placeholder():
    data_canada = px.data.gapminder()
    fig = px.bar(data_canada, x='year', y='pop')
    return dcc.Graph(
            figure=fig,
            id='placeholder',
            className='stretchy-widget',
            responsive=True,
        )