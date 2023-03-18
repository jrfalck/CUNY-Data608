from dash import Dash, html, dcc
import dash
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import datetime as dt
import dash_bootstrap_components as dbc

#import geopandas
#import geoplot
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

# This will giver all count of all Boros and its tree count
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname,count(tree_id)' +\
        '&$group=boroname').replace(' ', '%20')
soql_treesB = pd.read_json(soql_url)

# This will give you all Tree species and its count
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=spc_common,count(tree_id)' +\
        '&$group=spc_common').replace(' ', '%20')
soql_treesT = pd.read_json(soql_url)

soql_treesT.dropna(inplace=True)
soql_treesT

# This will give you a count by Steward count
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,count(tree_id)' +\
        '&$group=steward').replace(' ', '%20')

soql_treesS = pd.read_json(soql_url)

soql_treesS.dropna(inplace=True)
soql_treesS

# This will give you a count by Health
soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$group=health').replace(' ', '%20')

soql_treesH = pd.read_json(soql_url)

soql_treesH.dropna(inplace=True)
soql_treesH

borolist = soql_treesB['boroname']
borolist

borolistdf = pd.DataFrame({
    'c' : borolist
})
borolistdf

optionsB = [ 
    {'label': i, 'value':i} for i in borolistdf['c']
]

optionsB

spclistdf = pd.DataFrame({
    'c' : soql_treesT['spc_common']
})

optionsSpc = [ 
    {'label': i, 'value':i} for i in spclistdf['c']
]

optionsSpc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
       dbc.Col([html.H1("Data608 HW4 NYC Trees")
       ])
    ], justify="center"),
    
    dbc.Row([dbc.Col(dcc.Dropdown( id = 'boroN',
        options = optionsB,
        value = 'Bronx')),
             
             dbc.Col(dcc.Dropdown( id = 'speciesN',
        options = optionsSpc,
        value = optionsSpc[0]["value"]))]),
    
    dbc.Row([dbc.Col(dcc.Graph(id = 'bar_plot')),
             
             dbc.Col(dcc.Graph(id = 'bar_plot2'))]),
    
    dbc.Row([dbc.Col(dcc.Graph(id = 'geo_plot1')),
             
             dbc.Col(dcc.Graph(id = 'geo_plot2'))]),

    dbc.Row([dbc.Col([dbc.Row(html.H4("Appendix 1")),
                      dbc.Row(dcc.Graph(id = 'table1'))]),
             
             dbc.Col([dbc.Row(html.H4("Appendix 2")),
                      dbc.Row(dcc.Graph(id = 'table2'))])]),

])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))

def graph_update(dBoro,dSpc):

    #NEW with variables
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=health,count(tree_id)' +\
        '&$where=boroname=\'{0}\' AND spc_common=\'{1}\'' +\
        '&$group=health').format(dBoro,dSpc).replace(' ', '%20')

    soql_trees1 = pd.read_json(soql_url)

    
    fig = px.histogram(soql_trees1, x="health", y="count_tree_id")

    fig.update_layout(
        title="Health of Trees by Species by Boro",
        xaxis_title="Health of Trees",
        yaxis_title="Number of Trees",
        legend_title="Health",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )

    return fig

@app.callback(Output(component_id='bar_plot2', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))

def graph_update2(dBoro,dSpc):

    #NEW with variables
    soql_url2 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=steward,count(tree_id)' +\
        '&$where=boroname=\'{0}\' AND spc_common=\'{1}\'' +\
        '&$group=steward').format(dBoro,dSpc).replace(' ', '%20')

    soql_trees2 = pd.read_json(soql_url2)

    fig2 = px.histogram(soql_trees2, x="steward", y="count_tree_id")
 
    fig2.update_layout(
        title="Steward of Trees by Species by Boro",
        xaxis_title="Steward of Trees",
        yaxis_title="Number of Trees",
        legend_title="Steward",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )

    return fig2


@app.callback(Output(component_id='geo_plot1', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))

def graph_update3(dBoro,dSpc):

    #NEW with variables
    soql_url3 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=10000&$offset=0' +\
        '&$where=boroname=\'{0}\' AND spc_common=\'{1}\'').format(dBoro,dSpc).replace(' ', '%20')
    soql_trees3 = pd.read_json(soql_url3)
  
    px.set_mapbox_access_token("pk.eyJ1IjoianJmYWxjayIsImEiOiJjbGZkYzRjZ28wZWttM3FycmV2dXhxZjByIn0.47UNH0enC4D63f7R9vgBMg")
    fig3 = px.scatter_mapbox(soql_trees3, lat="latitude", lon="longitude",color="health")
 
    fig3.update_layout(
        title="Location of Trees by Species by Boro",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )

    return fig3

@app.callback(Output(component_id='geo_plot2', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))

def graph_update4(dBoro,dSpc):

    #NEW with variables
    soql_url4 = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=10000&$offset=0' +\
        '&$where=boroname=\'{0}\' AND spc_common=\'{1}\'').format(dBoro,dSpc).replace(' ', '%20')
    soql_trees4 = pd.read_json(soql_url4)
  
    px.set_mapbox_access_token("pk.eyJ1IjoianJmYWxjayIsImEiOiJjbGZkYzRjZ28wZWttM3FycmV2dXhxZjByIn0.47UNH0enC4D63f7R9vgBMg")
    fig4 = px.scatter_mapbox(soql_trees4, lat="latitude", lon="longitude",color="steward")

    fig4.update_layout(
        title="Location of Trees by Species by Boro",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )
    
    return fig4


@app.callback(Output(component_id='table1', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))
def table_update1(dBoro,dSpc):

    #NEW with variables

    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=spc_common,count(tree_id)' +\
            '&$where=boroname=\'{0}\'' +\
            '&$group=spc_common').format(dBoro).replace(' ', '%20')


    soql_treesBC = pd.read_json(soql_url)

    soql_treesBC.sort_values(by=['count_tree_id'], ascending=False,inplace=True)
    

    fig5 = go.Figure(data=[go.Table(
    header=dict(values=list(soql_treesBC.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[soql_treesBC.spc_common, soql_treesBC.count_tree_id],
               fill_color='lavender',
               align='left'))
                          ])
    fig5.update_layout(
        title="Count of all trees by species in the Boro",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )

    return fig5


@app.callback(Output(component_id='table2', component_property= 'figure'),
              Input('boroN','value'),
              Input('speciesN','value'))

def table_update2(dBoro,dSpc):

    #NEW with variables

    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
            '$select=boroname,count(tree_id)' +\
            '&$where=spc_common=\'{0}\'' +\
            '&$group=boroname').format(dSpc).replace(' ', '%20')

    soql_treesBSN = pd.read_json(soql_url)
    soql_treesBSN.sort_values(by=['count_tree_id'], ascending=False,inplace=True)
    

    fig6 = go.Figure(data=[go.Table(
    header=dict(values=list(soql_treesBSN.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[soql_treesBSN.boroname,soql_treesBSN.count_tree_id],
               fill_color='lavender',
               align='left'))
                          ])

    fig6.update_layout(
        title="Count of trees of this species in all Boros",
        font=dict(
            family="Garamond",
            size=14,
            color="Black"
        )
    )
    
    return fig6


######################
if __name__ == '__main__': 
    app.run_server()