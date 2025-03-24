# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/Users/elhamserahati/Documents/Data Science/IBM Data Science/Applied DS Capstone/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

spacex_df['success'] = spacex_df['class'].to_numpy()
spacex_df['fail']    = 1-spacex_df['class'].to_numpy()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([html.Label("Select Launch Site:"),
                                          dcc.Dropdown(id='site-dropdown',
                                                       options=[{'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                                {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                                                {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                                {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                                                ],
                                                        placeholder = 'Select a Launch Site',
                                                        value='Select Launch Site')]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #Add a division for pie chart display
                                html.Div(id='success-pie-chart', className='chart-grid', style={'display':'flex'}),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min_payload,max_payload,int(max_payload/10),value=[min_payload,max_payload],id='payload-slider'),
                                html.Div(id='output-container-range-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                # html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Div(id='success-payload-scatter-chart', className='chart-grid', style={'display':'flex'}),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value')])

def update_pie_chart(launch_site):
    Y_chart1 = dcc.Graph(figure=px.pie(spacex_df.groupby('Launch Site')['success'].sum().reset_index(),
                                        values='success',names='Launch Site',
                                            title='Total Successfull Launches for each Launch Site'))
    df_launch_site = spacex_df[spacex_df['Launch Site']==launch_site]
    Y_chart2 = dcc.Graph(figure=px.pie(values=[df_launch_site['success'].sum(),df_launch_site['fail'].sum()],
                                       names=['Success','Fail'],
                                       color_discrete_sequence=['#d62728','#2ca02c'],
                                       title='Successfull vs Failed Launches for Launch Site: {}'.format(launch_site)))
    return [html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'})]

# TASK 4:
@app.callback(
    Output('output-container-range-slider', 'children'),
    Input('payload-slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])

def update_scatterplot(launch_site,payload_range):
    data = spacex_df[spacex_df['Launch Site']==launch_site]
    if len(payload_range)==2:
        data = data[data['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
    fig = px.scatter(data, x='Payload Mass (kg)',y='success',title='Payload Mass and successfull Launch Correlation')
    fig.update_layout(
    yaxis=dict(
        ticktext=["Failure", "Success"],  # Labels for yticks
        tickvals=[0, 1]  # Corresponding y values for labels
        ))
    Y_chart3 = dcc.Graph(figure=fig)
    return [html.Div(className='chart-item', children=html.Div(children=Y_chart3),style={'display':'flex'})]

# Run the app
if __name__ == '__main__':
    app.run_server()
