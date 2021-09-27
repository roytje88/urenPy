import dash_core_components as dcc
import dash_html_components as html
import dash_table, os
from database import readTable,dframes
from styles import layoutStyles
import pandas as pd

styling = layoutStyles()
database = 'urenPy.db'
if not os.path.isfile(database):
    from deploy import *
    
    createDB()
    print("No database file found. I've created an empty database file.")
    print("Now adding default data...")
    for i in [2021,2022,2023]:
        addKalenderdata(i)
    urensoorten = [['10000','Regulier'],
                   ['10000','Ziek'],
                   ['10000','Verlof'],
                   ['10000','Bijzonder verlof']]
    for i in urensoorten:
        addUrensoort(create_connection(database),i[0],i[1])

frames = dframes()

df = readTable('contracten')
layout = html.Div(
    style= styling['maindiv'],
    children = [
        html.Div(
            style={},
            children=[
                html.H1('Urenregistratie'),
                ]
            ),
        html.Div(
            children= [
                dcc.Tabs(
                    children =[
                        dcc.Tab(
                            label = 'Uren',
                            style = styling['tabs']
                            ),
                        dcc.Tab(
                            label = 'Personen',
                            style = styling['tabs'],
                            
                            children=[
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Geregistreerde personen'),
                                        dash_table.DataTable(
                                            id='personenTable',
                                            columns = [{'name': i, 'id': i} for i in frames['personen'].keys() if i != 'id'],
                                            data=pd.DataFrame.from_dict(frames['personen']).to_dict('records')
                                            )
                                        ]
                                    ),
                                html.Div(
                                    style=styling['subdiv'],
                                    children=[
                                        html.H2('Voeg persoon toe'),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Voornaam: ')]
                                                                    ),
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-right': '1px'},
                                                                    children=[
                                                                        dcc.Input(
                                                                            placeholder='Voornaam',
                                                                            type='text',
                                                                            id='voornaam'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Tussenvoegsel(s): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Tussenvoegsel(s)',
                                                                            type='text',
                                                                            id='tussenvoegsel'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Achternaam: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Achternaam',
                                                                            type='text',
                                                                            id='achternaam'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Email adres: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Email adres',
                                                                            type='email',
                                                                            id='email'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )                                                    
                                                ]
                                            ),
                                            html.Button('Voeg gegevens toe', id='addPersonBtn',n_clicks=0)
                                        ]
                                    ),
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Persoon verwijderen'),
                                        dcc.Dropdown(
                                            id='personenDropdown',
                                            options=[{'label': i['Voornaam'] + ' ' + i['Tussenvoegsel']+ ' ' + i['Achternaam'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['personen']).to_dict('records')]
                                            ),
                                        html.Button('Persoon logisch verwijderen', id='delPersBtn',n_clicks=0)
                                        
                                        ]
                                    
                                    
                                    )                                
                            
                                ]
                           
                        ),
                        dcc.Tab(
                            label = 'Werkgevers',
                            style = styling['tabs'],
                            
                            children=[
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Geregistreerde werkgevers'),
                                        dash_table.DataTable(
                                            id='werkgeversTable',
                                            columns = [{'name': i, 'id': i} for i in frames['werkgevers'].keys() if i not in ['id']],
                                            data=pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records')
                                            )
                                        ]
                                    ),
                                html.Div(
                                    style=styling['subdiv'],
                                    children=[
                                        html.H2('Voeg werkgever toe'),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Naam werkgever: ')]
                                                                    ),
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-right': '1px'},
                                                                    children=[
                                                                        dcc.Input(
                                                                            placeholder='Naam werkgever',
                                                                            type='text',
                                                                            id='wgNaam'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('CAO: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='CAO',
                                                                            type='text',
                                                                            id='cao'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Begindatum CAO (JJJJ-MM-DD): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Begindatum CAO (JJJJ-MM-DD)',
                                                                            type='text',
                                                                            id='dd_begin_cao'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Einddatum CAO (JJJJ-MM-DD): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Einddatum CAO (JJJJ-MM-DD)',
                                                                            type='text',
                                                                            id='dd_eind_cao'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Aantal uren per week fulltime: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Aantal uren per week fulltime',
                                                                            type='number',
                                                                            id='urenfulltime'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                
                                                
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Vrij bij feestdagen (T/F): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Vrij bij feestdagen (T/F)',
                                                                            type='text',
                                                                            id='ind_vakantiedagen_vry'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                
                                                                                
                                                
                                                
                                                
                                                
                                                ]
                                            ),
                                            html.Button('Voeg gegevens toe', id='addWgBtn',n_clicks=0)
                                        ]
                                    ),
                                
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Werkgever verwijderen'),
                                        dcc.Dropdown(
                                            id='werkgeverDropdown',
                                            options=[{'label': i['Naam werkgever'] + ' (CAO ' + i['CAO']+')', 'value': i['id']} for i in pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records')]
                                            ),
                                        html.Button('Werkgever logisch verwijderen', id='delWgBtn',n_clicks=0)
                                        
                                        ]
                                    
                                    
                                    )
                                
                                
                                
                                
                                ]
                            ),
                        dcc.Tab(
                            label = 'Contracten',
                            style = styling['tabs'],
                            children=[
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Geregistreerde contracten'),
                                        dash_table.DataTable(
                                            id='contractenTable',
                                            columns = [{'name': i, 'id': i} for i in frames['contracten'].keys() if i not in ['id']],
                                            data=pd.DataFrame.from_dict(frames['contracten']).to_dict('records')
                                            )
                                        ]
                                    ),
                                html.Div(
                                    style=styling['subdiv'],
                                    children=[
                                        html.H2('Voeg contract toe'),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Begindatum contract (JJJJ-MM-DD): ')]
                                                                    ),
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-right': '1px'},
                                                                    children=[
                                                                        dcc.Input(
                                                                            placeholder='Begindatum contract (JJJJ-MM-DD)',
                                                                            type='text',
                                                                            id='dd_begin_contract'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Einddatum contract (JJJJ-MM-DD): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Einddatum contract (JJJJ-MM-DD)',
                                                                            type='text',
                                                                            id='dd_eind_contract'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Percentage deeltijd (*100): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Percentage deeltijd (*100)',
                                                                            type='number',
                                                                            id='percentage'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Uurloon (in eurocenten): ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Uurloon (in eurocenten): ',
                                                                            type='number',
                                                                            id='uurloon'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Verlofuren per jaar: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Verlofuren per jaar',
                                                                            type='number',
                                                                            id='verlofuren'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                
                                                
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Bijzonder verlofuren: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px'},
                                                                children=[
                                                                    dcc.Input(
                                                                            placeholder='Bijzonder verlofuren',
                                                                            type='text',
                                                                            id='bijzverlofuren'
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Persoon: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px', 'width': '300px'},
                                                                children=[
                                                                    dcc.Dropdown(
                                                                        id='persoonContractDropdown',
                                                                        options=[{'label': i['Voornaam'] + ' ' + i['Tussenvoegsel']+ ' ' + i['Achternaam'], 'value': i['E-mail']} for i in pd.DataFrame.from_dict(frames['personen']).to_dict('records')],
                                                                        placeholder='Persoon'
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                                                      
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    style={'display': 'inline-block', 'margin-left': '1px'},
                                                                    children=[
                                                                    dcc.Markdown('Werkgever: ')]
                                                                    ),
                                                            html.Div(
                                                                style={'display': 'inline-block', 'margin-right': '1px', 'width': '300px'},
                                                                children=[
                                                                    dcc.Dropdown(
                                                                        id='werkgeverContractDropdown',
                                                                        options=[{'label': i['Naam werkgever'], 'value': i['Naam werkgever']} for i in pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records')],
                                                                        placeholder='Werkgever'
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),                                                      
                                                
                                                
                                                
                                                ]
                                            ),
                                            html.Button('Voeg gegevens toe', id='addContractBtn',n_clicks=0)
                                        ]
                                    ),
                                
                                html.Div(
                                    style=styling['subdiv'],
                                    children = [
                                        html.H2('Contract verwijderen'),
                                        dcc.Dropdown(
                                            id='contractenDropdown',
                                            options=[{'label': 'Van '+i['Begindatum'] + ' t/m ' + i['Einddatum']+', ' + i['Persoon']+ ', '+ i['Werkgever'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['contracten']).to_dict('records')]
                                            ),
                                        html.Button('Contract logisch verwijderen', id='delContractBtn',n_clicks=0)
                                        
                                        ]
                                    
                                    
                                    )
                                
                                
                                
                                
                                ]                            
                            )
                        ]
                    )
                ]
            )
        ]
    )


