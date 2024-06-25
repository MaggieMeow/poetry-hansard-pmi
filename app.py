import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

viz_df = pd.read_csv('pmi_scores_by_year.csv')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("PMI Scores Dashboard"),
    dcc.Dropdown(
        id='placename-dropdown',
        options=[{'label': placename, 'value': placename} for placename in sorted(viz_df['Placename'].unique())],
        placeholder='Select a Placename'
    ),
    dcc.Dropdown(
        id='year-dropdown',
        placeholder='Select a Year'
    ),
    html.Br(),
    html.Div([
        html.Label("Minimum PMI Score:"),
        dcc.Input(id='pmi-threshold', type='number', value=-10, step=0.1)  # Adjustable step
    ]),
    dcc.Graph(id='pmi-graph')
])

@app.callback(
    Output('year-dropdown', 'options'),
    Input('placename-dropdown', 'value')
)
def update_year_options(selected_placename):
    if selected_placename:
        filtered_df = viz_df[viz_df['Placename'] == selected_placename]
        years = sorted(filtered_df['Year'].dropna().unique())
        return [{'label': int(year), 'value': int(year)} for year in years]
    return []

@app.callback(
    Output('year-dropdown', 'value'),
    Input('year-dropdown', 'options')
)
def set_default_year(options):
    if options:
        return options[0]['value']
    return None

@app.callback(
    Output('pmi-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('placename-dropdown', 'value'),
     Input('pmi-threshold', 'value')]
)
def update_graph(selected_year, selected_placename, pmi_threshold):
    if selected_year and selected_placename:
        filtered_df = viz_df[(viz_df['Year'] == selected_year) & (viz_df['Placename'] == selected_placename) & (viz_df['PMI'] >= pmi_threshold)]
        fig = px.bar(filtered_df, x='Word', y='PMI', title=f'PMI Scores for {selected_placename} in {selected_year}')
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},  # Ensure all labels are shown
            yaxis_tickmode='linear',  # Force showing all ticks
            height=800
        )
        return fig
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)