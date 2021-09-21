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
