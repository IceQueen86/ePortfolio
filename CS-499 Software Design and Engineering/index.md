---
layout: default
title: Artifact One Original C++ Code
---

# **Source.cpp** #

```py
# =============================================================================
# Created By  : Sabrina Ozburn
# File Name: AnimalShelter_Original.py    
# =============================================================================

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'slodoz96' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % ("aacuser","slodoz96","localhost",27017)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None:
            insert = self.database.animals.insert_one(data)  # data should be dictionary
            # Check insert for operation
            if insert!=0:
                return True
            else:
                # Default return
                return False    
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            
    # Create method to implement the R in CRUD.
    def read(self, criteria=None):
        if criteria is not None:
            data = self.database.animals.find(criteria)         
        else:
            data = self.database.animals.find({})
        # Return the dataset else let the error flow up
        return data
    
    # Create method to implement the U in CRUD.
    def update(self, criteria, updateData):
        if criteria is not None:
            result = self.database.animals.update_one(criteria, {"$set" : updateData})
        else:
           return"{}"
        return result.raw_result
    
    # Create method to implement the D in CRUD.
    def delete(self, deleteData):
        if deleteData is not None:
            result = self.database.animals.delete_one(deleteData)
        else:
           return"{}"
        return result.raw_result
        
# =============================================================================
# Created By  : Sabrina Ozburn
# File Name: Dashboard_Original.py    
# =============================================================================     

# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc, html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64
JupyterDash.infer_jupyter_proxy_config()

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bson.json_util import dumps


# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from AnimalShelter import AnimalShelter

###########################
# Data Manipulation / Model
###########################

shelter = AnimalShelter()

#class read method must support retun of cursor object
df = pd.DataFrame.from_records(shelter.read({}))
df.drop(columns=['_id'],inplace=True)

rescue_types = ['Water Rescue', 'Mountain or Wilderness Rescue', 'Disaster or Individual Tracking', 'Reset']


#########################
# Dashboard Layout / View
#########################

app = JupyterDash('Global Rain')

#Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    #Title and Image
     html.Center(children=[
        html.B(html.H1('SNHU CS-340 Dashboard')),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '300px'}),
        # Unique identifier
        html.Center(html.H4('Sabrina Ozburn 2025')),
    ]),
    html.Hr(),
    
    # Radio buttons for each type of rescue animal in the shelter
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
                         
                        #FIXME: Set up the features for your interactive data table to make it user-friendly for your client
                        editable = False,
                        filter_action = "native",
                        sort_action = "native",
                        sort_mode = "multi",
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
    
    #This sets up the dashboard so that your chart and your geolocation chart are side-by-side
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
              [Input('rescue-type-filter', 'value')])
def update_dashboard(filter_type):
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
        
    return dff.to_dict('records')

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# Pie Chart graph with the percentage os animal breed in the viewport data
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])

def update_graphs(viewData):
    dffPie = pd.DataFrame.from_dict(viewData)

    return [
        dcc.Graph(            
            figure = px.pie(dffPie, names='breed',)
        )    
    ]
    
# This callback will update the geo-location chart for the selected data entry
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data")])

def update_map(viewData):
    dff = pd.DataFrame.from_dict(viewData)
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id")] +
            # Marker with tool tip and popup
            [dl.Marker(position=[row['location_lat'],row['location_long']], children=[
                dl.Tooltip(row['breed']),
                dl.Popup([
                     html.H1("Animal Name"),
                     html.P(row['name'])
                ])
            ]) for index, row in dff.iterrows()]
        )
    ]

# Run app and display result in jupyterlab mode, note, if you have previously run a prior app, the default port of 8050 may not be available, if so, try setting an alternate port.
app.run_server()         

            
