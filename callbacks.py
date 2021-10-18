from dash.dependencies import Output, Input
from database import readTable, dframes, addPerson, create_connection, addWerkgever, addContract, stdUrenwijzigen, urenDef, urenInvullen
import pandas as pd
from database import readTable,dframes,logischVerwijderen
from dash.exceptions import PreventUpdate
import dash
import dash_core_components as dcc
import plotly.express as px

database = "urenPy.db"
conn = create_connection(database)

def register_callbacks(app):
    @app.callback([Output('personenTable', 'data'),
                   Output('addPersonBtn','n_clicks'),
                   Output('delPersBtn','n_clicks'),
                   Output('personenDropdown', 'options'),
                   Output('persoonContractDropdown','options'),
                   Output('persoonUrenDropdown','options'),
                   Output('persoonStandaarduren','options'),
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
        return pd.DataFrame.from_dict(frames['personen']).to_dict('records'), 0, 0, persDropd, persContractDd, persDropd, persDropd
 

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
                
            addContract(conn, dd_begin_contract, dd_eind_contract, str(percentage), str(uurloon), str(verlofuren), str(bijzverlofuren), werkgeverContractDropdown, persoonContractDropdown)
        if delContractBtn > 0 and contractenDropdown != None:
            logischVerwijderen('contracten', contractenDropdown)
        frames=dframes()
        contrDd = [{'label': 'Van '+i['Begindatum'] + ' t/m ' + i['Einddatum']+', ' + i['Persoon']+ ', '+ i['Werkgever'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['contracten']).to_dict('records')]
        return pd.DataFrame.from_dict(frames['contracten']).to_dict('records'), 0, 0, contrDd
    

    @app.callback(Output('contractUrenDropdown','options'),
                      Input('persoonUrenDropdown','value'))
    def contractVullen(persoon):
        frames = dframes()
        if persoon != None:
            dropdown = [{'label': i['Begindatum'] + ', ' + i['Persoon']+ ', '+ i['Werkgever'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['contracten']).to_dict('records') if i['id_persoon'] == persoon]
            return dropdown
        else:
            dropdown = [{'label': i['Begindatum'] + ', ' + i['Persoon']+ ', '+ i['Werkgever'], 'value': i['id']} for i in pd.DataFrame.from_dict(frames['contracten']).to_dict('records')]
            return dropdown
        

        
        
    @app.callback([Output('MonHourStd','value'),
                   Output('MonMinStd','value'),
                   Output('TueHourStd','value'),
                   Output('TueMinStd','value'),
                   Output('WedHourStd','value'),
                   Output('WedMinStd','value'),
                   Output('ThuHourStd','value'),
                   Output('ThuMinStd','value'),
                   Output('FriHourStd','value'),
                   Output('FriMinStd','value'),
                   Output('SatHourStd','value'),
                   Output('SatMinStd','value'),
                   Output('SunHourStd','value'),
                   Output('SunMinStd','value'),
                  ],
                  [Input('persoonStandaarduren','value'),
                   Input('changeStdUren' ,'n_clicks'),
                   Input('MonHourStd','value'),
                   Input('MonMinStd','value'),
                   Input('TueHourStd','value'),
                   Input('TueMinStd','value'),
                   Input('WedHourStd','value'),
                   Input('WedMinStd','value'),
                   Input('ThuHourStd','value'),
                   Input('ThuMinStd','value'),
                   Input('FriHourStd','value'),
                   Input('FriMinStd','value'),
                   Input('SatHourStd','value'),
                   Input('SatMinStd','value'),
                   Input('SunHourStd','value'),
                   Input('SunMinStd','value'),
                  ])
    def showStandaardUren(value, n_clicks, monhour, monmin, tuehour, tuemin, wedhour, wedmin, thuhour, thumin, frihour, frimin, sathour, satmin, sunhour, sunmin):
        frames = dframes()
        ctx = dash.callback_context
        if value == None or value == 0:
            uren = [0,0,0,0,0,0,0]
            minuten = [0,0,0,0,0,0,0]

        else:
            
            frame = pd.DataFrame(frames['standaarduren'])
            lijst = frame[frame['ID persoon'] == value].values.tolist()[0][-7:]
            uren = []
            minuten = []
            for i in lijst:
                minuten.append((i % 1)*60)
                uren.append(i-(i % 1))
        
        if n_clicks >0 and value  != None:
                stdUrenwijzigen(conn, monhour + monmin/60, tuehour + tuemin/60, wedhour + wedmin/60, thuhour + thumin/60, frihour + frimin/60, sathour + satmin/60, sunhour + sunmin/60)
                
        
        return uren[0], minuten[0], uren[1], minuten[1], uren[2], minuten[2], uren[3], minuten[3], uren[4], minuten[4], uren[5], minuten[5], uren[6], minuten[6]

    

    
    @app.callback([Output('defofniet','children'),
                   Output('MonDate','children'),
                   Output('TueDate','children'),
                   Output('WedDate','children'),
                   Output('ThuDate','children'),
                   Output('FriDate','children'),
                   Output('SatDate','children'),
                   Output('SunDate','children'),
                   Output('MonHour','value'),
                   Output('MonMin','value'),
                   Output('TueHour','value'),
                   Output('TueMin','value'),
                   Output('WedHour','value'),
                   Output('WedMin','value'),
                   Output('ThuHour','value'),
                   Output('ThuMin','value'),
                   Output('FriHour','value'),
                   Output('FriMin','value'),
                   Output('SatHour','value'),
                   Output('SatMin','value'),
                   Output('SunHour','value'),
                   Output('SunMin','value'),
                   Output('toggleDef','n_clicks'),
                  ],
                  [Input('jaar','value'),
                   Input('isoweek','value'),
                   Input('contractUrenDropdown','value'),
                   Input('toggleDef','n_clicks'),
                  ])
    def vulUrentabblad(jaar,week,contract, n_clicks):
        print(contract)
        ctx = dash.callback_context

        
        toreturn = 'Niet definitief'
        try: 
            df = pd.DataFrame(readTable('opgeslagenweken').to_dict())
            df = df[df['jaar'] == jaar][df['isoweek'] == week][df['id_contract'] == contract]
            if df.iat[0,4] == 1:
                toreturn = 'Definitief'
        except:
            pass
        if n_clicks > 0:
            if toreturn == 'Niet definitief':
                print(contract)
                urenDef(conn, jaar, week, contract, 1)
            elif toreturn == 'Definitief':
                urenDef(conn, jaar, week, contract, 0)
            toreturn = 'Niet definitief'
            try: 
                df = pd.DataFrame(readTable('opgeslagenweken').to_dict())
                df = df[df['jaar'] == jaar][df['isoweek'] == week][df['id_contract'] == contract]
                if df.iat[0,4] == 1:
                    toreturn = 'Definitief'
            except:
                pass            
            
        cal = readTable('kalender')
        cal = cal[cal['jaartal'] == jaar][cal['isoweek'] == week]
        cal = cal.sort_values('dagweek')
        
        lijst = []
        for i in range(0,7):
            lijst.append(str(cal.iat[i,13])+' '+str(cal.iat[i,15])+'-' + str(cal.iat[i,3]) + '-' + str(cal.iat[i,1]) )
        
        frames = dframes()
        
        def welkeuren(datum,idPersoon):
            df = pd.DataFrame(frames['uren'])
            dag = cal[cal['datum'] == datum].iat[0,16] + 2
            dfStd = pd.DataFrame(frames['standaarduren'])
            toreturn = dfStd[dfStd['ID persoon'] == idPersoon].iat[0,dag]    
            try: 
                toreturn = df[df['datum'] == datum].iat[0,3]
            except:
                pass
            return toreturn
        
        if contract != None:
            contr = pd.DataFrame(frames['contracten'])
            persoon = 0
            try:
                persoon = contr[contr['id']== contract].iat[0,9]
            except:
                pass
            def urenenminuten(volledigeuren):
                return [volledigeuren - (volledigeuren % 1), (volledigeuren % 1)*60]

            lijsturen = []
            lijstminuten = []
            
            for i in range(0,7):
                volledigeuren=welkeuren(cal.iat[i,0],persoon)
                lijsturen.append(urenenminuten(volledigeuren)[0])
                lijstminuten.append(urenenminuten(volledigeuren)[1])
                
        else:
            lijsturen = [0,0,0,0,0,0,0]
            lijstminuten = [0,0,0,0,0,0,0]
        

        return toreturn,lijst[0],lijst[1],lijst[2],lijst[3],lijst[4],lijst[5],lijst[6],lijsturen[0],lijstminuten[0],lijsturen[1],lijstminuten[1],lijsturen[2],lijstminuten[2],lijsturen[3],lijstminuten[3],lijsturen[4],lijstminuten[4],lijsturen[5],lijstminuten[5],lijsturen[6],lijstminuten[6],0
        
        
            
    @app.callback([Output('savedMon','children'),
                   Output('monSave','n_clicks'),
                  ],
                  [Input('MonDate','children'),
                   Input('monSave','n_clicks'),
                   Input('MonHour','value'),
                   Input('MonMin','value'),
                   Input('MonType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedTue','children'),
                   Output('tueSave','n_clicks'),
                  ],
                  [Input('TueDate','children'),
                   Input('tueSave','n_clicks'),
                   Input('TueHour','value'),
                   Input('TueMin','value'),
                   Input('TueType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedWed','children'),
                   Output('wedSave','n_clicks'),
                  ],
                  [Input('WedDate','children'),
                   Input('wedSave','n_clicks'),
                   Input('WedHour','value'),
                   Input('WedMin','value'),
                   Input('WedType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedThu','children'),
                   Output('thuSave','n_clicks'),
                  ],
                  [Input('ThuDate','children'),
                   Input('thuSave','n_clicks'),
                   Input('ThuHour','value'),
                   Input('ThuMin','value'),
                   Input('ThuType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedFri','children'),
                   Output('friSave','n_clicks'),
                  ],
                  [Input('FriDate','children'),
                   Input('friSave','n_clicks'),
                   Input('FriHour','value'),
                   Input('FriMin','value'),
                   Input('FriType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedSat','children'),
                   Output('satSave','n_clicks'),
                  ],
                  [Input('SatDate','children'),
                   Input('satSave','n_clicks'),
                   Input('SatHour','value'),
                   Input('SatMin','value'),
                   Input('SatType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0
            
    @app.callback([Output('savedSun','children'),
                   Output('sunSave','n_clicks'),
                  ],
                  [Input('SunDate','children'),
                   Input('sunSave','n_clicks'),
                   Input('SunHour','value'),
                   Input('SunMin','value'),
                   Input('SunType','value'),
                   Input('contractUrenDropdown','value'),
                  ])
    def maandagOpslaan(datum, n_clicks, uren, minuten, soort, contract):
        ctx = dash.callback_context
        if n_clicks >0:
            date = datum[-4:]+'-'+datum[-7:-5]+'-'+datum[-10:-8]
            if contract != None:
                urenInvullen(date, contract, uren, minuten, soort)
                return 'Opgeslagen', 0
            else:
                return 'Eerst een contract kiezen!', 0
        else:
            return '',0

    
    
    
    
    
    
    
    
    # @app.callback(Output('urenGraph','figure'),
    #               Input('contractUrenDropdown','value'))
    # def createGraph(value):
    #     if value != None:
    #         frames = dframes()
    #         df = pd.DataFrame(frames['uren'])
    #         return px.pie(df, values='uren',names='id_soort')
    #     else:
    #         return ' '