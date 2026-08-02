import dash
import dash_leaflet as dl
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import base64
import os

# Load local secure environment configurations
from dotenv import load_dotenv
load_dotenv()

from AnimalShelter import AnimalShelter

from QuickSort import quicksort_records

###########################
# Data Manipulation / Model
###########################

shelter = AnimalShelter()

CSV_FILE_NAME = 'aac_shelter_outcomes.csv'

if os.path.exists(CSV_FILE_NAME):
    df = pd.read_csv(CSV_FILE_NAME)

if df.empty:
    df = pd.DataFrame(columns=['id', 'breed', 'sex_upon_outcome', 'age_upon_outcome_in_weeks', 'name', 'location_lat', 'location_long'])
elif '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

rescue_types = ['Water Rescue', 'Mountain or Wilderness Rescue', 'Disaster or Individual Tracking', 'Reset']

#########################
# Dashboard Layout / View
#########################

app = dash.Dash(__name__)
app.title = "Grazioso Salvare Dashboard"

# Grazioso Salvare’s logo layout configuration
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
     html.Center(children=[
        html.B(html.H1('Grazioso Salvare Dashboard')),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '300px'}),
        html.Center(html.H4('By: Sabrina Ozburn')),
    ]),
    html.Hr(),
    
    dcc.RadioItems(
                id='rescue-type-filter',
                options=[{'label': i, 'value': i} for i in rescue_types],
                value='Reset',
                labelStyle={'display': 'inline-block'}
            ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                        data=df.to_dict('records'),
                        editable = False,
                        filter_action = "native",
                    
                        sort_action = "custom",
                        sort_mode = "single",
                        sort_by = [],

                        column_selectable = "single",
                        row_selectable = "single",
                        row_deletable = False,
                        selected_columns = [],
                        selected_rows = [],
                        page_action = "native",
                        page_current = 0,
                        page_size = 10,
                        ),
    html.Br(),
    html.Hr(),
    
    html.Div(className='row',
         style={'display' : 'flex', 'justify-content':'center'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(Output('datatable-id','data'),
              [Input('rescue-type-filter', 'value'),
               Input('datatable-id', 'sort_by')])
def update_dashboard(filter_type, sort_by):
    if df.empty:
        return []

    if filter_type == 'Reset':
        dff = df
    elif filter_type == 'Water Rescue':
        dff = df[df.breed.isin(['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland'])
                & (df.sex_upon_outcome == 'Intact Female')
                & ((df.age_upon_outcome_in_weeks >= 26) & (df.age_upon_outcome_in_weeks <= 156))]
    elif filter_type == 'Mountain or Wilderness Rescue':
        dff = df[df.breed.isin(['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler'])
                & (df.sex_upon_outcome == 'Intact Male')
                & ((df.age_upon_outcome_in_weeks >= 26) & (df.age_upon_outcome_in_weeks <= 156))]
    elif filter_type == 'Disaster or Individual Tracking':
        dff = df[df.breed.isin(['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler'])
                & (df.sex_upon_outcome == 'Intact Male')
                & ((df.age_upon_outcome_in_weeks >= 20) & (df.age_upon_outcome_in_weeks <= 300))]
        
    records_to_process = dff.to_dict('records')

    if sort_by and len(sort_by) > 0:
        sort_field = sort_by[0]['column_id']
        is_descending = sort_by[0]['direction'] == 'desc'
        
        sorted_list = quicksort_records(records_to_process, sort_field)
        
        if is_descending:
            sorted_list.reverse()
            
        return sorted_list
        
    return records_to_process

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_graphs(viewData):
    if not viewData:
        return [html.Div("No active viewport records selected to compute chart distributions.")]
        
    dffPie = pd.DataFrame.from_dict(viewData)
    if dffPie.empty or 'breed' not in dffPie.columns:
        return [html.Div("Data array fields missing required criteria.")]
        
    return [
        dcc.Graph(            
            figure = px.pie(dffPie, names='breed',)
        )    
    ]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])
def update_map(viewData):
    if not viewData:
        return [html.Div("Select rows within the datatable grid component to populate geographical markers.")]
        
    dff = pd.DataFrame.from_dict(viewData)
    if dff.empty or 'location_lat' not in dff.columns:
        return [html.Div("Coordinate fields are unpopulated for current filter parameters.")]
        
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id")] +
            [dl.Marker(position=[row['location_lat'],row['location_long']], children=[
                dl.Tooltip(row['breed']),
                dl.Popup([
                     html.H1("Animal Name"),
                     html.P(row['name'])
                ])
            ]) for index, row in dff.iterrows()]
        )
    ]

if __name__ == '__main__':
    # Starts your local development environment server at http://127.0.0.1:8050
    app.run(debug=True)
