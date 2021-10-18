import pandas as pd
import sqlite3
from sqlite3 import Error

database = "urenPy.db"
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def addWerkgever(conn, naam, cao, dd_begin_cao, dd_eind_cao, urenfulltime, ind_vakantiedagen_vry):        
    sql = "INSERT INTO werkgever (naam, cao, dd_begin_cao, dd_eind_cao, urenfulltime, ind_vakantiedagen_vry,sts_rec) VALUES ('"+\
        naam+"','"+\
        cao+"','"+\
        dd_begin_cao+"','"+\
        dd_eind_cao+"','"+\
        str(urenfulltime)+"','"+\
        ind_vakantiedagen_vry+"','1');"
    try:
        conn = create_connection(database)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

def addPerson(conn, voornaam, tussenvoegsel, achternaam, email):
    try:
        conn = create_connection(database)
        c = conn.cursor()
        c.execute('select email from persoon;')
        emails = [i[0] for i in c.fetchall()]
        if email in emails:
         
            print('Emailadres '+email+ ' bestaat al!')
        else:
            sql = "INSERT INTO persoon (voornaam,tussenvoegsel,achternaam,email,sts_rec) VALUES ('"+\
                voornaam+"','"+\
                tussenvoegsel+"','"+\
                achternaam+"','"+\
                email+"','1');"
            try:
                c = conn.cursor()
                c.execute('pragma foreign_keys = ON;')
                c.execute(sql)
                conn.commit()
            except Error as e:
                print(e)
    except:
        pass

def urenDef(conn, jaar, week, contract, definitief):
    sql = "select * from opgeslagenweken where jaar = '"+str(jaar)+"' and isoweek = '"+ str(week) + "' and id_contract = '"+str(contract)+"';"
    try:
        conn = create_connection(database)
        c = conn.cursor()
        if c.execute(sql).fetchall() == []:
            newsql = "insert into opgeslagenweken (id_contract,jaar, isoweek, ind_def) values ('" + str(contract) + "','" +str(jaar)+"','"+str(week)+"','"+str(definitief) + "');"
        else:
            newsql = "update opgeslagenweken set ind_def= "+str(definitief) + " where isoweek = '" + str(week) + "' and jaar = '" + str(jaar) +"' and id_contract = '" +str(contract)+"';"
        try:
            conn = create_connection(database)
            c = conn.cursor()
            c.execute(newsql)
            conn.commit()
        except Error as e:
            print(e)
            
    except:
        pass
    
def addContract(conn, dd_begin, dd_eind, percentage, uurloon, verlofuren, bijzverlofuren, werkgever, email):        
    conn = create_connection(database)
    c = conn.cursor()
    c.execute("select id from werkgever where naam = '"+werkgever+"';")
    id_werkgever = str(c.fetchall()[0][0])

    conn = create_connection(database)
    c = conn.cursor()
    c.execute("select id from persoon where email = '"+email+"';")
    id_persoon = str(c.fetchall()[0][0])
    
    sql = "INSERT INTO contracten (dd_begin, dd_eind, percentage, uurloon, verlofuren, bijzverlofuren, id_werkgever, id_persoon, sts_rec) VALUES ('"+\
        dd_begin+"','"+\
        dd_eind+"','"+\
        percentage+"','"+\
        uurloon+"','"+\
        verlofuren+"','"+\
        bijzverlofuren+"','"+\
        id_werkgever+"','"+\
        id_persoon+"','1');"
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
def addUrensoort(conn, percentage,omschryving):
    sql = "INSERT INTO urensoort (percentage, omschryving) VALUES ('"+\
    percentage+"','"+\
    omschryving+"');"
    try:
        conn = create_connection(database)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
def stdUrenwijzigen(persoon_id, mon, tue, wed, thu, fri, sat, sun):
    sql = "DELETE FROM standaarduren WHERE id_persoon = '" + persoon_id + "';"
    conn = create_connection(database)
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)
    addStandaarduren(conn, persoon_id, mon, tue, wed, thu, fri, sat, sun)
        
        
def addStandaarduren(conn, id_persoon, mon, tue, wed, thu, fri, sat, sun):
    sql = "INSERT INTO standaarduren (id_persoon, maandag, dinsdag, woensdag, donderdag, vrijdag, zaterdag, zondag) VALUES ('"+\
    str(id_persoon)+"','"+\
    str(mon)+"','"+\
    str(tue)+"','"+\
    str(wed)+"','"+\
    str(thu)+"','"+\
    str(fri)+"','"+\
    str(sat)+"','"+\
    str(sun)+"');"
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)        

def readTable(table,inclusieflogischverwijderd=True):
    import pandas as pd
    con = sqlite3.connect("urenPy.db")
    if inclusieflogischverwijderd:
        df = pd.read_sql_query("SELECT * from "+table, con)
    else:
        df = pd.read_sql_query("SELECT * from "+table+" where sts_rec=1", con)
    con.close()
    return df
    
    
def dframes():
    frames = {}
    personen = readTable('persoon',inclusieflogischverwijderd=False).rename(columns={'voornaam': 'Voornaam', 
                                                                                     'tussenvoegsel': 'Tussenvoegsel',
                                                                                     'achternaam': 'Achternaam',
                                                                                     'email': 'E-mail',
                                                                                     'sts_rec': 'Logisch verwijderd'})
    frames['personen'] = personen.to_dict()
    
    werkgevers = readTable('werkgever',inclusieflogischverwijderd=False).rename(columns={'naam': 'Naam werkgever',
                                                                                         'urenfulltime': 'Aantal uren per week fulltime',
                                                                                         'ind_vakantiedagen_vry': 'Vrij bij feestdagen',
                                                                                         'cao': 'CAO','dd_begin_cao': 'Begindatum CAO',
                                                                                         'dd_eind_cao': 'Einddatum CAO',
                                                                                         'sts_rec': 'Logisch verwijderd'})
    
    frames['werkgevers'] = werkgevers.to_dict()
    
    contracten = readTable('contracten',inclusieflogischverwijderd=False)
    contracten['id_persoon'] = contracten['id_persoon'].astype(int)
    contracten['id_werkgever'] = contracten['id_werkgever'].astype(int)
    merged = contracten.merge(readTable('persoon'), left_on='id_persoon',right_on='id', how='left').merge(readTable('werkgever'), left_on='id_werkgever', right_on='id', how='left')
    merged['persoon'] = merged[['voornaam','tussenvoegsel','achternaam']].agg(' '.join, axis=1)
    merged = merged[['id_x','dd_begin','dd_eind','percentage','uurloon','verlofuren','bijzverlofuren','persoon','naam','id_persoon']]
    merged.set_index('id_x')
    contracten2 = merged.rename(columns={'id_x': 'id',
                                        'dd_begin': 'Begindatum',
                                        'dd_eind': 'Einddatum',
                                        'percentage': 'Percentage deeltijd',
                                        'uurloon': 'Uurloon',
                                        'verlofuren': 'Wettelijke verlofuren',
                                        'bijzverlofuren': 'Bijzonder verlofuren',
                                        'persoon': 'Persoon',
                                        'naam': 'Werkgever'
                                                                                         })
    
    frames['contracten'] = contracten2.to_dict()

    merged = readTable('standaarduren').merge(readTable('persoon'), left_on='id_persoon',right_on='id', how='left')
    merged['persoon'] = merged[['voornaam','tussenvoegsel','achternaam']].agg(' '.join, axis=1)
    merged = merged[['id_x','id_persoon','persoon','maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']]
    standaarduren = merged.rename(columns={'id_x': 'id',
                                          'id_persoon': 'ID persoon',
                                          'persoon': 'Persoon',
                                          'maandag': 'Maandag',
                                          'dinsdag': 'Dinsdag',
                                          'woensdag': 'Woensdag',
                                          'donderdag': 'Donderdag',
                                          'vrijdag': 'Vrijdag',
                                          'zaterdag': 'Zaterdag',
                                          'zondag': 'Zondag'
                                         })
    frames['standaarduren'] = standaarduren.to_dict()
    
    frames['opgeslagenweken'] = readTable('opgeslagenweken').to_dict()
    
    frames['urensoort'] = readTable('urensoort').to_dict()
    
    frames['uren'] = readTable('uren').to_dict()
    
    return frames
    


def logischVerwijderen(table,id):
    
    con = sqlite3.connect('urenPy.db')
    try:
        sql = 'update ' + table + ' set sts_rec=9 where id = ' + str(id)
        c = con.cursor()
        c.execute(sql)
        con.commit()
        con.close()
    except Error as e:
        print(e)

        
        
def urenInvullen(datum, contract, uren, minuten, soort):
    sql = "select * from uren where datum = '" + datum + "' and id_contract = '" + str(contract) + "' and id_soort = '" + str(soort) + "';"
    hours = int(uren) + int(minuten) / 60
    try:
        conn = create_connection(database)
        c = conn.cursor()
        if c.execute(sql).fetchall() == []:
            
            newsql = "insert into uren (datum, id_contract, id_soort, uren) values ('"+datum+"','"+str(contract)+"','"+str(soort)+"','"+str(hours)+"');"
        else:
            newsql = "update uren set uren = '"+str(hours)+"' where datum = '"+datum+"' and id_contract = '"+str(contract)+"' and id_soort = '"+str(soort)+"';"
        print(newsql)
        try:
            conn = create_connection(database)
            c = conn.cursor()
            c.execute(newsql)
            conn.commit()
        except Error as e:
            print(e)
    except:
        pass
    
    
    
    