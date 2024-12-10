import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, Field
import config

# Pydantic models
class DropdownOption(BaseModel):
    """
    Model representing a dropdown option with label and value.
    
    Attributes:
        label (str): The label displayed for the option.
        value (str): The value associated with the option.
    """
    label: str
    value: str


class DropdownInputs(BaseModel):
    """
    Model representing the inputs required for dropdowns in the Dash app.
    
    Attributes:
        type (str): Selected fuel type ('Fossiles' or 'Organiques').
        state (str): Selected state of the fuel.
        unity (str): Selected unit of measurement.
        combustible (str): Selected combustible type.
    """
    type: str
    state: str
    unity: str
    combustible: str


# Initialize Dash app
app = dash.Dash(__name__)

# getting engine
engine = create_engine(config.DATABASE_URL)

df_elt = pd.read_sql("""
    SELECT *
    FROM public.donnees_emissions
    WHERE "Statut de l'élément" IN ('Valide générique', 'Valide spécifique')
    AND "code1" = 'Combustibles'
    AND "Sous-localisation géographique français" = 'France continentale'
    AND "Type Ligne" = 'Elément'
""", con=engine)

df_poste = pd.read_sql("""
    SELECT *
    FROM public.donnees_emissions
    WHERE "Statut de l'élément" IN ('Valide générique', 'Valide spécifique')
    AND "code1" = 'Combustibles'
    AND "Sous-localisation géographique français" = 'France continentale'
    AND "Type Ligne" = 'Poste'
""", con=engine)

# Create 'Nom complet' column in both DataFrames
df_elt['Nom complet'] = df_elt['Nom base français'].fillna('') + ' ' + df_elt['Nom attribut français'].fillna('')
df_poste['Nom complet'] = df_poste['Nom base français'].fillna('') + ' ' + df_poste['Nom attribut français'].fillna('')



# Layout
app.layout = html.Div(
    style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H3('Décomposition des émissions par combustible en France métropolitaine', style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Type de combustible
        html.Div(
            style={'marginBottom': '20px'},
            children=[
                html.H5('Type de combustible', style={'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='type',
                    options=[
                        {'label': 'Fossiles', 'value': 'Fossiles'},
                        {'label': 'Organiques', 'value': 'Organiques'}
                    ],
                    value='Fossiles',
                    placeholder='Sélectionner combustible fossile ou organique',
                    style={'width': '100%'}
                )
            ]
        ),
        
        # Etat du combustible
        html.Div(
            style={'marginBottom': '20px'},
            children=[
                html.H5('Etat du combustible', style={'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='state',
                    placeholder='Sélectionner un état',
                    style={'width': '100%'}
                )
            ]
        ),
        
        # Unité
        html.Div(
            style={'marginBottom': '20px'},
            children=[
                html.H5('Unité (attention certaines unités ne couvrent pas tous les combustibles)', style={'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='unity',
                    placeholder='Sélectionnez une unité',
                    style={'width': '100%'}
                )
            ]
        ),
        
        # Graph for histogram of state
        html.Div(
            style={'marginBottom': '40px'},
            children=[
                dcc.Graph(id='histogram_state')
            ]
        ),
        
        # Détail par combustible
        html.Div(
            style={'marginBottom': '20px'},
            children=[
                html.H3('Détail des émissions par combustible', style={'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='combustible',
                    placeholder='Sélectionnez un combustible',
                    style={'width': '100%'}
                )
            ]
        ),
        
        # Graphs for detailed emissions
        html.Div(
            style={'marginBottom': '40px'},
            children=[
                dcc.Graph(id='histogram_detail_emissions'),
                dcc.Graph(id='histogram_poste')
            ]
        )
    ]
)


@app.callback(
    Output('state', 'options'),
    Output('state', 'value'),
    Input('type', 'value')
)
def update_state_options(selected_type: str) -> Tuple[List[DropdownOption], str]:
    """
    Update the available state options based on the selected type.
    
    Args:
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
    
    Returns:
        Tuple[List[DropdownOption], str]: The list of state options and the default value.
    """
    filtered_df = df_elt[df_elt['code2'] == selected_type]
    state_options = [{'label': u, 'value': u} for u in filtered_df['code3'].unique()]
    default_value =  filtered_df['code3'].unique()[0]
    return state_options, default_value

@app.callback(
    Output('unity', 'options'),
    Output('unity', 'value'),
    Input('type', 'value'), 
    Input('state', 'value')
)
def update_unity_options(selected_type: str, selected_state: str) -> Tuple[List[DropdownOption], str]:
    """
    Update the available unit options based on the selected type and state.
    
    Args:
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
        selected_state (str): The selected state.
    
    Returns:
        Tuple[List[DropdownOption], str]: The list of unit options and the default unit.
    """
    filtered_df = df_elt[
        (df_elt['code2'] == selected_type) &            
        (df_elt['code3'] == selected_state)]
    unity_options = [{'label': u, 'value': u} for u in filtered_df['Unité français'].unique()]
    default_value = 'kgCO2e/GJ PCI' if 'kgCO2e/GJ PCI' in filtered_df['Unité français'].unique() else filtered_df['Unité français'].unique()[0]
    return unity_options, default_value


@app.callback(
    Output('histogram_state', 'figure'),
    Input('type', 'value'), 
    Input('state', 'value'),
    Input('unity', 'value')
)
def update_graph_per_state(selected_type: str, selected_state: str, selected_unity: str) -> Figure:
    """
    Generate a histogram for emission rates based on selected type, state, and unit.
    
    Args:
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
        selected_state (str): The selected state.
        selected_unity (str): The selected unit.
    
    Returns:
        Figure: A Plotly figure object for the histogram.
    """
    filtered_df = df_elt[
        (df_elt['code2'] == selected_type) & 
        (df_elt['code3'] == selected_state) & 
        (df_elt['Unité français'] == selected_unity)
    ]
    fig = px.histogram(
        filtered_df,
        x='Nom complet',
        y='Total poste non décomposé',
        histfunc='avg'
    )
    fig.update_layout(
        title={
            'text': f'Taux d\'émission en {selected_unity} des combustibles {selected_state}',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Combustible',
        yaxis_title=selected_unity
    )
    return fig

@app.callback(
    Output('combustible', 'options'),
    Output('combustible', 'value'),
    Input('type', 'value'), 
    Input('state', 'value'),
    Input('unity', 'value')
)
def update_combustible_options(selected_type: str, selected_state: str, selected_unity: str) -> Tuple[List[DropdownOption], str]:
    """
    Update the available combustible options based on selected type, state, and unit.
    
    Args:
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
        selected_state (str): The selected state.
        selected_unity (str): The selected unit.
    
    Returns:
        Tuple[List[DropdownOption], str]: The list of combustible options and the default combustible.
    """
    filtered_df = df_elt[
        (df_elt['code2'] == selected_type) & 
        (df_elt['code3'] == selected_state) & 
        (df_elt['Unité français'] == selected_unity)
    ]
    combustible_options = [{'label': u, 'value': u} for u in filtered_df['Nom complet'].unique()]
    default_value = combustible_options[0]['value']
    return combustible_options, default_value

@app.callback(
    Output('histogram_detail_emissions', 'figure'),
    Input('type', 'value'), 
    Input('state', 'value'),
    Input('unity', 'value'),
    Input('combustible', 'value')
)
def update_histogram_detail_emissions(selected_type: str, selected_state: str, selected_unity: str, selected_combustible: str) -> Figure:
    """
    Generate a histogram for detailed emissions based on selected combustible, type, state, and unit.
    
    Args:
        selected_combustible (str): The selected combustible.
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
        selected_state (str): The selected state.
        selected_unity (str): The selected unit.
    
    Returns:
        Figure: A Plotly figure object for the detailed emissions histogram.
    """
    filtered_df = df_elt[
        (df_elt['code2'] == selected_type) & 
        (df_elt['code3'] == selected_state) & 
        (df_elt['Unité français'] == selected_unity) &
        (df_elt['Nom complet'] == selected_combustible)
    ]
    print(filtered_df)
    row = filtered_df.iloc[0]
    columns_to_plot = ['Total poste non décomposé', 'CO2f', 'CH4f', 'CH4b', 'N2O','Autres GES', 'CO2b']
    selected_row = row[columns_to_plot]
    long_df = selected_row.reset_index() 
    long_df.columns = ['Category', 'Value']

    fig = px.histogram(
        long_df,
        x='Category',  # Categories (column names)
        y='Value',     # Values from the selected row
        title='Histogram for Selected Row and Columns',
        labels={'Category': 'Categories', 'Value': 'Values'}
    )
    fig.update_layout(
        title={
            'text': f'Détail des taux d\'émission en {selected_unity} de {selected_combustible}',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Type d\'émission',
        yaxis_title=selected_unity
    )
    return fig

@app.callback(
    Output('histogram_poste', 'figure'),
    Input('type', 'value'), 
    Input('state', 'value'),
    Input('unity', 'value'),
    Input('combustible', 'value')
)
def update_histogram_poste(selected_type: str, selected_state: str, selected_unity: str, selected_combustible: str) -> Figure:
    """
    Generate a histogram for poste emissions based on selected combustible, type, state, and unit.
    
    Args:
        selected_combustible (str): The selected combustible.
        selected_type (str): The selected type ('Fossiles' or 'Organiques').
        selected_state (str): The selected state.
        selected_unity (str): The selected unit.
    
    Returns:
        Figure: A Plotly figure object for the poste emissions histogram.
    """
    filtered_df = df_poste[
        (df_poste['code2'] == selected_type) & 
        (df_poste['code3'] == selected_state) & 
        (df_poste['Unité français'] == selected_unity) &
        (df_poste['Nom complet'] == selected_combustible)
    ]
    fig = px.histogram(
        filtered_df,
        x='Type poste',
        y='Total poste non décomposé',
        histfunc='avg'
    )
    fig.update_layout(
        title={
            'text': f'Taux par poste d\'émission en {selected_unity} de {selected_combustible}',
            'x': 0.5,  # Center the title
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Poste',
        yaxis_title=selected_unity
    )
    return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)