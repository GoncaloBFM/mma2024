from dash import dcc
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
import base64
import textwrap

# Function to create the chart
def create_chart(code_str):
    # Dedent the code string to handle leading whitespace
    code_str = textwrap.dedent(code_str)
    
    # Execute the provided code string to generate a matplotlib chart
    exec_globals = {}
    exec_locals = {}
    exec(code_str, exec_globals, exec_locals)
    
    # Save the matplotlib figure to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
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
            yanchor="top"
        )
    )
    
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        title="Chart",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '100%'})
