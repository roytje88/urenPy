import sqlite3, os
from sqlite3 import Error

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute('pragma foreign_keys = ON;')
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        

def createDB():
    conn = create_connection('urenPy.db')
    persoonTable = """CREATE TABLE IF NOT EXISTS persoon (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    voornaam text not null,
                    tussenvoegsel text not null,
                    achternaam text not null,
                    email text not null,
                    sts_rec integer
    );"""
    werkgeversTable = """CREATE TABLE IF NOT EXISTS werkgever (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        naam text not null,
                        cao text,
                        dd_begin_cao text,
                        dd_eind_cao text,
                        urenfulltime integer,
                        ind_vakantiedagen_vry text,
                        sts_rec integer
    );"""
    contractenTable = """CREATE TABLE IF NOT EXISTS contracten (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        dd_begin text,
                        dd_eind text,
                        percentage integer,
                        uurloon integer,
                        verlofuren integer,
                        bijzverlofuren integer,
                        id_werkgever,
                        id_persoon,
                        sts_rec integer
    );"""
    soortenUrenTable = """CREATE TABLE IF NOT EXISTS urensoort (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        percentage integer,
                        omschryving text
    );"""
    
    standaardUren = """CREATE TABLE IF NOT EXISTS standaarduren (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        id_persoon integer,
                        maandag integer,
                        dinsdag integer,
                        woensdag integer,
                        donderdag integer,
                        vrijdag integer,
                        zaterdag integer,
                        zondag integer

    );"""

    kalender =  """CREATE TABLE IF NOT EXISTS kalender (
                        datum text PRIMARY KEY,
                        jaartal integer,
                        kwartaal integer,
                        maand integer,
                        eerstedagmaand text,
                        laatstedagmaand text,
                        periodemaand integer,
                        periode4weken integer,
                        eerstedag4weken text,
                        laatstedag4weken text,
                        jaar4weken integer,
                        vierwekennummer integer,
                        isoweek integer,
                        dagoms text,
                        dagjaar integer,
                        dagmaand integer,
                        dagweek integer,
                        eerstedagweek text,
                        laatstedagweek text
    );"""
    
    opgeslagenweken =  """CREATE TABLE IF NOT EXISTS opgeslagenweken (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        id_contract integer,
                        jaar integer,
                        isoweek integer,
                        ind_def integer
    );"""
    
    uren =  """CREATE TABLE IF NOT EXISTS uren (
                datum text,
                id_contract integer,
                id_soort integer,
                uren integer,
                PRIMARY KEY (datum, id_contract, id_soort)
    );"""
    
    create_table(conn, persoonTable)
    create_table(conn, werkgeversTable)
    create_table(conn, contractenTable)
    create_table(conn, soortenUrenTable)
    create_table(conn, standaardUren)
    create_table(conn, kalender)
    create_table(conn, opgeslagenweken)
    create_table(conn, uren)

def addUrensoort(conn, percentage,omschryving):
    sql = "INSERT INTO urensoort (percentage, omschryving) VALUES ('"+\
    percentage+"','"+\
    omschryving+"');"
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

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
    
def addKalenderdata(jaar):
    import pandas as pd
    kalender = pd.read_csv('kalender.csv').values.tolist()
    conn = create_connection('urenPy.db')
    c = conn.cursor()
    for i in kalender:
        if  i[1] == jaar:
            sql = """insert into kalender ('DATUM', 'JAARTAL', 'KWARTAAL', 'MAAND', 'EERSTEDAGMAAND','LAATSTEDAGMAAND', 'PERIODEMAAND', 'PERIODE4WEKEN', 'EERSTEDAG4WEKEN','LAATSTEDAG4WEKEN', 'JAAR4WEKEN', 'VIERWEKENNUMMER', 'ISOWEEK','DAGOMS', 'DAGJAAR', 'DAGMAAND', 'DAGWEEK','EERSTEDAGWEEK','LAATSTEDAGWEEK') values ("""+\
                """'20"""+\
                  i[0][6:8]+'-'+i[0][3:6]+i[0][0:2]+\
                  """','"""+\
                  str(i[1])+\
                  """','"""+\
                  str(i[2])+\
                  """','"""+\
                  str(i[3])+\
                  """','"""+\
                  """20"""+i[4][6:8]+'-'+i[4][3:6]+i[4][0:2]+\
                  """','"""+\
                  """20"""+i[5][6:8]+'-'+i[5][3:6]+i[5][0:2]+\
                  """','"""+\
                  str(i[6])+\
                  """','"""+\
                  str(i[7])+\
                  """','"""+\
                  """20"""+i[8][6:8]+'-'+i[8][3:6]+i[8][0:2]+\
                  """','"""+\
                  """20"""+i[9][6:8]+'-'+i[9][3:6]+i[9][0:2]+\
                  """','"""+\
                  str(i[10])+\
                  """','"""+\
                  str(i[11])+\
                  """','"""+\
                  str(i[12])+\
                  """','"""+\
                  i[13]+\
                  """','"""+\
                  str(i[14])+\
                  """','"""+\
                  str(i[15])+\
                  """','"""+\
                  str(i[16])+\
                  """','"""+\
                  """20"""+i[17][6:8]+'-'+i[17][3:6]+i[17][0:2]+\
                  """','"""+\
                  """20"""+i[18][6:8]+'-'+i[18][3:6]+i[18][0:2]+\
                  """');"""
            try:

                c.execute(sql)

            except Error as e:
                print(e)
    conn.commit()    
