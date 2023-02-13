# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
pd.set_option('display.max_columns', 40)
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df['class_name']=spacex_df.loc[:, 'class']
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#launch sites names
launch_sites_names=spacex_df['Launch Site'].unique()
opciones=[]
opciones.append({'label':'All','value':'All'})
for name in launch_sites_names:
    opciones.append({'label':name,'value':name})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                    options=opciones,
                                    value='All',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id=
                                'id-slider',
                                    min=0, max=10000, step=10,
                                    marks={min_payload: min_payload,
                                    max_payload:  max_payload},
                                    value=[min_payload, max_payload])
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input('id-slider', 'value'),
              ])
def get_pie_chart(entered_site,payloads):
    print ("payload: ", payloads)
    filtered_df=spacex_df[(spacex_df['class']==1) & (spacex_df['Payload Mass (kg)']>=payloads[0]) & (spacex_df['Payload Mass (kg)']<= payloads[1])   ]
    if entered_site == 'All':
        print (filtered_df)

        fig = px.pie(filtered_df, values='class', 
        names= 'Launch Site',
        title='All Sites')
        return fig
    else:
        print ("entered_site",entered_site)
        #filtered=spacex_df[(spacex_df['Launch Site']==entered_site) ]
        
        #filtered_df=spacex_df[(spacex_df['Launch Site']==entered_site)& (spacex_df['Payload Mass (kg)']>=payloads[0]) & (spacex_df['Payload Mass (kg)']<= payloads[1]) ].groupby(['class_name']).count()
        filtered_site=spacex_df[ (spacex_df['Payload Mass (kg)']>=payloads[0]) & (spacex_df['Payload Mass (kg)']<= payloads[1])   ].groupby(['class_name']).count()
        print (spacex_df[ (spacex_df['Payload Mass (kg)']>=payloads[0]) & (spacex_df['Payload Mass (kg)']<= payloads[1])   ])
        print (filtered_site)
        max_i=payloads[1]
        min_i=payloads[0]
    
        
        
        
        #print (filtered_df)
        fig = px.pie(filtered_site, values='class', 
        names=filtered_site.index,
        title=entered_site+ '['+str(min_i) + ' , ' +str(max_i) + ']')
        return fig

        pass
        # return the outcomes piechart for a selected site





# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input('id-slider', 'value'),
              ])
def get_scatter_chart(entered_site,payloads):
    filtered_df=spacex_df[(spacex_df['Payload Mass (kg)']>=payloads[0]) & (spacex_df['Payload Mass (kg)']<= payloads[1])   ]
    if entered_site == 'All':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return fig
    else:
        filtered_df=filtered_df[(filtered_df['Launch Site']==entered_site) ]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category")
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
