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
        return pd.DataFrame.from_dict(frames['personen']).to_dict('records'), 0, 0, persDropd
 

    @app.callback([Output('werkgeversTable', 'data'),
                   Output('addWgBtn', 'n_clicks'),
                   Output('delWgBtn', 'n_clicks'),
                   Output('werkgeverDropdown', 'options'),
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
        return pd.DataFrame.from_dict(frames['werkgevers']).to_dict('records'), 0, 0, wgdropd

    