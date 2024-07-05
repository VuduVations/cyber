# cyberchoicesmb 
# Author: S Halverson @vuduvations
# License: BSD 3-Clause

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64
import io

# Function to calculate ALE
def calculate_ale(pre_aro, post_aro, pre_sle, post_sle):
    ale_pre = pre_aro * pre_sle
    ale_post = post_aro * post_sle
    return ale_pre, ale_post

# Function to update DataFrame with CBA metrics
def update_cba_metrics(df):
    df['ALE_Pre'] = df['Pre ARO'] * df['Pre SLE']
    df['ALE_Post'] = df['Post ARO'] * df['Post SLE']
    df['ACS'] = df['Annual Maintenance Cost'] + df['Safeguard Cost']
    df['Savings'] = df['ALE_Pre'] - df['ALE_Post']
    df['Net Savings'] = df['Savings'] - df['ACS']
    df['Decision'] = np.where(df['Net Savings'] > 0, 'Go', 'No Go')
    return df

# Interactive plot using Plotly
def plot_interactive_cba_metrics(df):
    metrics = ['EF', 'Safeguard Cost', 'Pre ARO', 'Post ARO', 'Pre SLE', 'Post SLE', 'ALE_Pre', 'ALE_Post']

    # Plot for detailed metrics
    fig1 = go.Figure()
    for metric in metrics:
        fig1.add_trace(go.Bar(
            x=df['Application/Software Name'],
            y=df[metric],
            name=metric,
            marker_color=np.where(df['Decision'] == 'Go', 'green', 'red'),
            hovertext=df['Decision']
        ))

    fig1.update_layout(
        barmode='group',
        title='CBA Metrics by Asset',
        xaxis_title='Application/Software Name',
        yaxis_title='Value',
        legend_title='Metric'
    )

    # Plot for overall decision
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df['Application/Software Name'],
        y=[1] * len(df),  # Dummy value for height
        name='Decision',
        marker_color=np.where(df['Decision'] == 'Go', 'green', 'red'),
        hovertext=df['Decision']
    ))

    fig2.update_layout(
        title='Overall Go/No Go Decision by Asset',
        xaxis_title='Application/Software Name',
        yaxis_title='Decision',
        yaxis=dict(
            showticklabels=False,  # Hide the y-axis ticks
            showgrid=False,
            zeroline=False,
        ),
        showlegend=False
    )

    # Budget allocation plot
    fig3 = px.pie(df, values='ACS', names='Application/Software Name', title='Budget Allocation for Safeguards')

    # Cost-effectiveness plot
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df['Application/Software Name'],
        y=df['Net Savings'],
        mode='markers+text',
        marker=dict(color=np.where(df['Net Savings'] > 0, 'green', 'red')),
        text=df['Net Savings'],
        textposition='top center'
    ))
    fig4.update_layout(
        title='Cost Effectiveness of Safeguards',
        xaxis_title='Application/Software Name',
        yaxis_title='Net Savings'
    )

    # Heatmap for cost-benefit analysis
    heatmap_data = df.set_index('Application/Software Name')[['ALE_Pre', 'ALE_Post', 'ACS', 'Net Savings']]
    fig5 = px.imshow(heatmap_data.T, text_auto=True, aspect="auto", title='Cost-Benefit Analysis Heatmap')

    return fig1, fig2, fig3, fig4, fig5

# Dash app setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src='assets/logo.png', height='100px'), width='auto'),
        dbc.Col(html.H1("VuduVations CBA for the SMB- Cybersecurity Cost Benefits Analysis for Small and Medium Business"), className="text-center mt-4")
    ]),
    dbc.Row(dbc.Col(dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select a CSV File')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ), className="mb-4")),
    dbc.Row(dbc.Col(html.Div(id='output-data-upload'))),
    dbc.Row([
        dbc.Col(dcc.Graph(id='cba-metrics-plot', figure={}), width=6),
        dbc.Col(dcc.Graph(id='cba-decision-plot', figure={}), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='budget-allocation-plot', figure={}), width=6),
        dbc.Col(dcc.Graph(id='cost-effectiveness-plot', figure={}), width=6)
    ]),
    dbc.Row(dbc.Col(dcc.Graph(id='cost-benefit-heatmap', figure={}), width=12))
], style={'backgroundColor': 'white'})  # Set background to white

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df = update_cba_metrics(df)
            fig1, fig2, fig3, fig4, fig5 = plot_interactive_cba_metrics(df)
            return fig1, fig2, fig3, fig4, fig5
    except Exception as e:
        print(e)
        return {}, {}, {}, {}, {}

@app.callback(
    [Output('cba-metrics-plot', 'figure'),
     Output('cba-decision-plot', 'figure'),
     Output('budget-allocation-plot', 'figure'),
     Output('cost-effectiveness-plot', 'figure'),
     Output('cost-benefit-heatmap', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        fig1, fig2, fig3, fig4, fig5 = parse_contents(contents, filename)
        return fig1, fig2, fig3, fig4, fig5
    return {}, {}, {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True)
