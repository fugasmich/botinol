import psycopg2





def open_connect():
    '''Connect to an existing database'''

    con = psycopg2.connect(database="melbet",
                           user="dimsan",
                           password="domi21092012nika",
                           host="localhost",
                           port="5432")
    return con

def create_line_table():
    """create line table"""
    con = open_connect()
    cur = con.cursor()
    cur.execute('''CREATE TABLE if not exists line_games
  (ID VARCHAR unique,
  TEAMS VARCHAR,
  SCORE VARCHAR,
  TIMER VARCHAR,
  WF_COEF VARCHAR,
  DRW_COEF VARCHAR,
  WSEC_COEF VARCHAR,
  WF_BY_TIME VARCHAR,
  WS_BY_TIME VARCHAR,
  WF_CHANGE VARCHAR,
  WS_CHANGE VARCHAR,
  SUMM_SCORE varchar    
  )''')
    print("Table created successfully")
    con.commit()
    con.close()


def select_by_waiting():

        '''find and put the values which timescore is none, it  means
        game is waiting for begining - first method'''
        print('add data')
        set_data = "insert into line_games (id, teams,score, wf_coef, drw_coef, wsec_coef) VALUES (%s, %s, %s, %s, %s, %s)"
        con = open_connect()
        cur = con.cursor()

        cur.execute(set_data, ('1', '2', '3', '4', '5', '6'))

        con.commit()
        con.close()
        print('all data was added')
