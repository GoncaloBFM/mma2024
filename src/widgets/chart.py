from dash import dcc, html
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
import base64
import textwrap
import pandas as pd
import os

# Function to create the chart
def create_chart(code_str, dataset_name):
    try:
        # Load the dataset
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
        data_path = os.path.join(base_path, f'{dataset_name}.csv')
        data = pd.read_csv(data_path)

        # Clear any existing matplotlib figures
        plt.close('all')

        # Dedent the code string to handle leading whitespace
        code_str = textwrap.dedent(code_str)

        # Define a local namespace to execute the provided code string
        local_namespace = {
            'pd': pd,
            'plt': plt,
            'data': data
        }

        # Execute the provided code string to generate a matplotlib chart
        exec(code_str, {}, local_namespace)

        # Save the matplotlib figure to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        # Convert the buffer to a base64 string
        img_base64 = base64.b64encode(buf.read()).decode('ascii')
        buf.close()

        # Create a Plotly figure to display the matplotlib image
        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source='data:image/png;base64,' + img_base64,
                xref="paper", yref="paper",
                x=0, y=1,
                sizex=1, sizey=1,
                xanchor="left",
                yanchor="top",
                sizing="contain",
                layer="below"
            )
        )

        fig.update_xaxes(visible=False, range=[0, 1])
        fig.update_yaxes(visible=False, range=[0, 1])
        fig.update_layout(
            title="Chart",
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        return dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%', 'overflow': 'auto'})

    except Exception as e:
        error_message = f"An error occurred while plotting the chart: {str(e)}"
        return html.Div(error_message, style={'color': 'red', 'textAlign': 'center'})
