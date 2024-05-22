import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import pandas as pd
from src.Dataset import Dataset


def create_histogram(selected_data=None):
    histogram = draw_histogram(selected_data)
    return html.Div([
        dcc.Graph(figure=histogram, 
                config={
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['zoom', 'pan', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']
                }, 
                id='histogram', 
                clear_on_unhover=True),
        dcc.Tooltip(id="histogram-tooltip", 
                    loading_text="LOADING"),
    ], className='border-widget stretchy-widget', id='histogram-container')


def draw_histogram(selected_data):
    if selected_data is None or len(selected_data) == 0:
        fig = go.Figure()

    # Add only layout information
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[
                dict(
                    text="Select data on the scatterplot",
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=28, color="gray")
                )
            ],
            margin=dict(b=0, l=0, r=0, t=100)  # Adjust margins to ensure the text is visible
        )

        return fig
    

    df = Dataset.get().loc[selected_data.index]

    # Grouping and counting occurrences
    class_counts = df['class_name'].value_counts().reset_index()
    class_counts.columns = ['class_name', 'count']

    # Plotting with Plotly Express
    fig = px.histogram(class_counts, x='class_name', y='count')
    fig.update_xaxes(categoryorder='total descending')  # Sort categories by count

    fig.update_layout(
        xaxis=dict(
            side='top', 
            tickangle=280, 
            automargin=False, 
            fixedrange=True
        ),
        yaxis=dict(
            visible=False, 
            automargin=False, 
            fixedrange=True
        ), 
        # title={'text': 'Histogram of Sample Data', 'y': 0.1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},

        margin=dict(l=50, r=50, t=150, b=150))
    
    return fig

def create_histogram_children(image_paths, class_names):
    with open(image_paths[0], 'rb') as f:
                image = f.read()
    return image


