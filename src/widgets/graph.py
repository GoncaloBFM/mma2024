import networkx as nx
import plotly.graph_objects as go
from dash import dcc
import numpy as np

from src.Dataset import Dataset

def create_graph(selected_rows=None):
    graph_figure = draw_graph(selected_rows)
    return dcc.Graph(
        id="graph",
        figure=graph_figure,
        className="stretchy-widget border-widget",
        responsive=True,
        config = {
            'displaylogo': False,
            'modeBarButtonsToRemove': ['autoscale', 'lasso2d', 'select2d'], # look here to remove buttons
            'displayModeBar': True,
        }
    )

def draw_graph(selected_rows, valid_birds=None, drag_select=False):

    # Default to displaying Blank graph with message if nothing is selected
    if not selected_rows or len(selected_rows) == 0:
        fig = go.Figure()

        # Add only layout information
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[
                dict(
                    text="Select Data on the Scatterplot",
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=28, color="gray")
                )
            ],
            margin=dict(b=0, l=0, r=0, t=40),  # Adjust margins to ensure the text is visible
        )

        return fig

    bird_classes = [bird_details["class_name"] for bird_details in selected_rows] # selected_rows[0]["class_name"]
    bird_species = [bird_class.split(" ")[-1] for bird_class in bird_classes] # bird_class.split(" ")[-1]

    # Initialize a NetworkX graph
    G = nx.Graph()

    # Only look at selected species
    species_df = Dataset.data.loc[Dataset.data["species_name"].isin(bird_species)]
    # Filter out class names that are not in selected region
    if valid_birds is not None:
        species_df = species_df.loc[species_df["class_name"].isin(valid_birds)]
    selected_nodes = set(bird_classes)

    # Add nodes (all unique bird names)
    for bird_name in species_df['class_name']:
        G.add_node(bird_name)

    # Add edges (between birds of the same species)
    species_groups = species_df.groupby('species_name')['class_name'].apply(list)
    for birds in species_groups:
        for i, bird_a in enumerate(birds[:-1]):
            for bird_b in birds[i+1:]:
                if bird_a in selected_nodes or bird_b in selected_nodes:
                    G.add_edge(bird_a, bird_b)


    # Get positions of nodes using a layout
    k_value = 2/np.sqrt(G.number_of_nodes())
    pos = nx.spring_layout(G, scale=15, k=k_value)

    # Create edge traces
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    # Create node traces
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=20,
            colorscale='ylgnbu',
            line=dict(width=0, color='darkblue')
        )
    )

    node_colours = []
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)

        # Assign color based on whether the node is in the highlight list
        if node in bird_classes:
            node_colours.append('rgba(255, 0, 0, 0.5)'*(1-drag_select) + 'rgba(31, 119, 180, 0.5)'*drag_select)
        else:
            node_colours.append('rgba(31, 119, 180, 0.5)')

    # Add colors to nodes
    node_trace['marker']['color'] = node_colours

    # Create a figure
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        font=dict(size=16)
    )
    return go.Figure(data=[edge_trace, node_trace], layout=layout)

