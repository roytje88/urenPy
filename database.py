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
    merged = merged[['id_x','dd_begin','dd_eind','percentage','uurloon','verlofuren','bijzverlofuren','persoon','naam']]
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
    print(contracten.to_dict())
    print([{'name': i, 'id': i} for i in frames['contracten'].keys() if i not in ['id']])
    print(pd.DataFrame.from_dict(frames['contracten']).to_dict('records'))
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
