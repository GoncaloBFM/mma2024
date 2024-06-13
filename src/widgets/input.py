from dash import dcc, html

def create_input():
    return html.Div(
        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'},
        children=[
            html.Div(
                style={'width': '80%', 'marginBottom': '20px'},
                children=[
                    html.Label('Prompt:'),
                    dcc.Textarea(
                        id='prompt-input',
                        style={'width': '100%', 'height': '200px'},  # Adjusted height for larger input area
                        placeholder='Enter the prompt here...'
                    ),
                ]
            ),
            html.Div(
                style={'width': '80%', 'marginBottom': '20px'},
                children=[
                    html.Label('Answer:'),
                    dcc.Textarea(
                        id='answer-input',
                        value='''import matplotlib.pyplot as plt

# Example data for the pie chart
labels = ['Rent', 'Groceries', 'Utilities']
sizes = [1200, 300, 150]
colors = ['#ff9999','#66b3ff','#99ff99']
explode = (0.1, 0, 0)  # explode 1st slice (i.e. 'Rent')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("January Expenses")
plt.show()
''',  # Default value for the answer input
                        style={'width': '100%', 'height': '200px'},  # Adjusted height for larger input area
                        placeholder='Enter the answer here...',
                    ),
                ]
            ),
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]
    )
