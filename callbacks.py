from dash.dependencies import Output, Input
from database import readTable, dframes, addPerson, create_connection, addWerkgever
import pandas as pd
from database import readTable,dframes,logischVerwijderen
from dash.exceptions import PreventUpdate
import dash

database = "urenPy.db"
conn = create_connection(database)

def register_callbacks(app):
    @app.callback([Output('personenTable', 'data'),
                   Output('addPersonBtn','n_clicks'),
                   Output('delPersBtn','n_clicks'),
                   Output('personenDropdown', 'options'),
                   Output('persoonContractDropdown','options'),
                  ], 
                  [Input('addPersonBtn', 'n_clicks'),
                   Input('voornaam', 'value'),
                   Input('tussenvoegsel', 'value'),
                   Input('achternaam', 'value'),
                   Input('email', 'value'),
                   Input('delPersBtn', 'n_clicks'),
                   Input('personenDropdown', 'options'),
                  ])
    def addPersonBtn(n_clicks, voornaam, tussenvoegsel, achternaam, email, delPersBtn, personenDropdown):
        ctx = dash.callback_context
        if n_clicks > 0:
            if voornaam == None:
                voornaam = ''
            if tussenvoegsel == None:
                tussenvoegsel = ''
            if achternaam == None:
                achternaam = ''
            if email == None:
                email = ''
            addPerson(conn, voornaam, tussenvoegsel, achternaam, email)
        if delPersBtn > 0 and personenDropdown != None:
            logischVerwijderen('persoon', personenDropdown)
        frames=dframes()
        persDropd = [{'label': i['Voornaam'] + ' ' + i['Tussenvoegsel']+ ' ' + i['Achternaam'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['personen']).to_dict('records')]
        persContractDd = [{'label': i['Voornaam'] + ' ' + i['Tussenvoegsel']+ ' ' + i['Achternaam'], 'value': i['E-mail']} for i in pd.DataFrame.from_dict(frames['personen']).to_dict('records')]
        return pd.DataFrame.from_dict(frames['personen']).to_dict('records'), 0, 0, persDropd, persContractDd
 

    @app.callback([Output('werkgeversTable', 'data'),
                   Output('addWgBtn', 'n_clicks'),
                   Output('delWgBtn', 'n_clicks'),
                   Output('werkgeverDropdown', 'options'),
                   Output('werkgeverContractDropdown','options'),
                  ],
                  [Input('addWgBtn', 'n_clicks'),
                   Input('wgNaam', 'value'),
                   Input('cao', 'value'),
                   Input('dd_begin_cao', 'value'),
                   Input('dd_eind_cao', 'value'),
                   Input('urenfulltime', 'value'),
                   Input('ind_vakantiedagen_vry', 'value'),
                   Input('delWgBtn', 'n_clicks'),
                   Input('werkgeverDropdown', 'value'),
                  ])
    def addWerkgeverBtn(n_clicks, wgNaam, cao, dd_begin_cao, dd_eind_cao, urenfulltime, ind_vakantiedagen_vry, delWgBtn, werkgeverDropdown):
        ctx = dash.callback_context
        if n_clicks > 0:
            if wgNaam == None:
                wgNaam = ''
            if cao == None:
                cao = ''
            if dd_begin_cao == None:
                dd_begin_cao = ''
            if dd_eind_cao == None:
                dd_eind_cao = ''
            if urenfulltime == None:
                urenfulltime = ''
            if ind_vakantiedagen_vry == None:
                ind_vakantiedagen_vry = ''
            addWerkgever(conn, wgNaam, cao, dd_begin_cao, dd_eind_cao, urenfulltime, ind_vakantiedagen_vry)
        if delWgBtn > 0 and werkgeverDropdown !=None :
            logischVerwijderen('werkgever', werkgeverDropdown)
        frames=dframes()       
        wgdropd = [{'label': i['Naam werkgever'] + ' (CAO ' + i['CAO']+')', 'value': i['id']} for i in pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records')]
        wgContractDd = [{'label': i['Naam werkgever'], 'value': i['Naam werkgever']} for i in pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records')]
        return pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records'), 0, 0, wgdropd, wgContractDd
    
    @app.callback([Output('contractenTable', 'data'),
                   Output('addContractBtn','n_clicks'),
                   Output('delContractBtn','n_clicks'),
                   Output('contractenDropdown', 'options'),
                  ], 
                  [Input('addContractBtn', 'n_clicks'),
                   Input('dd_begin_contract', 'value'),
                   Input('dd_eind_contract', 'value'),
                   Input('percentage', 'value'),
                   Input('uurloon', 'value'),
                   Input('verlofuren', 'value'),
                   Input('bijzverlofuren', 'value'),
                   Input('werkgeverContractDropdown','value'),
                   Input('persoonContractDropdown','value'),
                   Input('delContractBtn','n_clicks'),
                   Input('contractenDropdown','value'),
                  ])
    def addContractB(n_clicks, dd_begin_contract, dd_eind_contract, percentage, uurloon, verlofuren, bijzverlofuren, werkgeverContractDropdown, persoonContractDropdown, delContractBtn, contractenDropdown):
        ctx = dash.callback_context
        if n_clicks > 0:
            if dd_begin_contract == None:
                dd_begin_contract = ''
            if dd_eind_contract == None:
                dd_eind_contract = ''
            if percentage == None:
                percentage = ''
            if uurloon == None:
                uurloon = ''
            if verlofuren == None:
                verlofuren = ''
            if bijzverlofuren == None:
                bijzverlofuren = ''
                
            addContract(conn, dd_begin_contract, dd_eind_contract, percentage, uurloon, verlofuren, bijzverlofuren,werkgeverContractDropdown, persoonContractDropdown)
        if delContractBtn > 0 and contractenDropdown != None:
            logischVerwijderen('contracten', contractenDropdown)
        frames=dframes()
        contrDd = [{'label': 'Van '+i['Begindatum'] + ' t/m ' + i['Einddatum']+', ' + i['Persoon']+ ', '+ i['Werkgever'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['contracten']).to_dict('records')]
        return pd.DataFrame.from_dict(frames['contracten']).to_dict('records'), 0, 0, contrDd
    