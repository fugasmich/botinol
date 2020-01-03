import psycopg2





def open_connect():
    '''Connect to an existing database'''

    con = psycopg2.connect(database="melbet",
                           user="dimsan",
                           password="domi21092012nika",
                           host="127.0.0.1/32",
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