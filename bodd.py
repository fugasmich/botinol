
import datetime
import logging

import psycopg2
from enum import Enum


class ENUMS(Enum):
    DATABASE_NAME = 'postgres'
    HOST = 'localhost'
    USER = 'dimsan'
    PASSWORD = 'domi21092012nika'
    PORT = '5432'
    VS = "~vSv~ "
    URL_MAIN = "https://melbet.com/ru/live/football/"
    URL_JsON = 'https://melbet.com/LiveFeed/Get1x2_VZip?sports=1&count=50&mode=4&cyberFlag=2&partner=8'
    FIRST_W = '(W_F)'
    DRAW = '(DW)'
    SECOND_W = '(S_W)'
    DOUBLE_CHANCE_FRST = '(1_X)'
    DOUBLE_CHANCE_DRAW = '(1_2)'
    DOUBLE_CHANCE_SECD = '(2_X)'
    HANDICAP_L = 'HL'
    HANDICAP_H = 'HH'
    TOTAL_H = 'TH'
    TOTAL_L = 'TL'
    HIGHER = '(B)'
    LOWER = '(L)'


class BetODD():
    waiting_for = []
    downcoefList = []
    downcoefList_second = []
    game_best_score=[]
    # //logging.basicConfig(filename="mb.log", level=logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s', filename='scrapper.log'
    )

    def open_connect(self):
        '''Connect to an existing database'''
        logging.info('connection start')
        con = psycopg2.connect(database=ENUMS.DATABASE_NAME.value,
                               user=ENUMS.USER.value,
                               password=ENUMS.PASSWORD.value,
                               host=ENUMS.HOST.value,
                               port=ENUMS.PORT.value)

        logging.info('connection success')
        return con

    def select_by_waiting(self):
        count = 0
        logging.info('searching waiting matches')
        '''find and put the values which timescore is none, it  means
        game is waiting for begining - first method'''
        get_data = "SELECT * from live_games "
        set_data = "insert into line_games (id, teams,score,timer, wf_coef, drw_coef, wsec_coef) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(get_data)
        rows = cur.fetchall()
        for row in rows:
            if row[3] == '\xa0':
                try:
                    cur.execute(set_data, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    count += 1
                except:
                    print('дубликат')

        con.commit()
        logging.info('matches was found')
        con.close()

    def clear_dublicate_line(self):

        '''remove all dublicates from line_table'''
        logging.info("clear data, remove all duplicates")
        sql = """DELETE FROM line_games WHERE ctid NOT IN
    (SELECT max(ctid) FROM line_games GROUP BY line_games.*);"""
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        logging.info("all duplicates removed")
        con.close()


    def get_data_by_time(self):
        '''
        find the games, which timescore between 05  and 17 minutes
        when needed timescore value is found,
          check for goals that must be null
        '''
        logging.info('collecting data by time intervals')
        date_time_max = datetime.datetime.strptime('15:00', '%M:%S')
        date_time_min = datetime.datetime.strptime('01:00', '%M:%S')
        sql = "Select * from live_games"
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[3] == '\xa0' or int(row[3][:2]) > 59 or len(row[3]) > 5:
                continue
            else:
                date_time_ob = datetime.datetime.strptime(row[3], '%M:%S')
                if date_time_ob < date_time_max and date_time_ob > date_time_min:
                    print("watch for matches")
                    ''' insert data from live table'''

                    if str(row[14]) == '0':
                        print('zero')
                        self.update_data_from_live(row[0])


        logging.info('data by time intervals collected')
        con.commit()
        con.close()
    def clear_data_by_time(self):
        '''
               clear the data which time score is more than 17 minutes
               '''
        date_time_ob = '0'
        logging.info('clear the data which time score is more than 17 minutes ')
        date_time_max = datetime.datetime.strptime('15:00', '%M:%S')
        sql = "Select * from line_games"
        sql_winf = '''Update line_games set wf_change =%s where id=%s '''
        sql_winsec = '''Update line_games set ws_change =%s where id=%s '''
        sql_timer_set = '''Update line_games set timer =%s where id=%s '''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[3] == '\xa0':
                continue
            try:
                date_time_ob = datetime.datetime.strptime(row[3], '%M:%S')
            except:
                date_time_ob = datetime.datetime.strptime('00:00', '%M:%S')
                cur.execute(sql_timer_set, ('00:00', row[0],))
            if date_time_ob > date_time_max or row[11] != '0' or date_time_ob == '00:00':
                    cur.execute(sql_winf, ('0', row[0],))
                    cur.execute(sql_winsec, ('0', row[0],))




        con.commit()
        con.close()



    def create_line_table(self):
        logging.info("create line table")

        con = self.open_connect()
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
      SUMM_SCORE VARCHAR    
      )''')
        logging.info("line Table created successfully")
        con.commit()
        con.close()

    def put_the_changes(self):
        coef_result_f = 0
        coef_result_sec = 0
        print('checking for changes')
        ''' check for coefficients which fallen! It mean the team '''


        self.downcoefList_second.clear()
        sql = '''SELECT * FROM line_games'''
        sql_winf = '''Update line_games set wf_change =%s where id=%s '''
        sql_winsec = '''Update line_games set ws_change =%s where id=%s '''

        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            try:
                coef_result_f = "%.2f" % (100 - ((float(row[7]) / float(row[4]))*100))

            except:
                logging.error('nullable in check_for_changes res_1')
                coef_result_f = 0

            try:
                coef_result_sec = "%.2f" % (100 - ((float(row[8]) / float(row[6]))*100))
            except:
                logging.error('nullable in check_for_changes res_2 ')
                coef_result_sec = 0

            print(coef_result_f, coef_result_sec, 'here')
            cur.execute(sql_winf, (float(coef_result_f), row[0],))
            cur.execute(sql_winsec, (float(coef_result_sec), row[0],))



        con.commit()
        con.close()


    def check_for_best_coef(self):
        self.downcoefList.clear()
        self.waiting_for.clear()
        con = self.open_connect()
        cur = con.cursor()

        sql_best_result = '''Select * from line_games'''
        cur.execute(sql_best_result)
        rows_res = cur.fetchall()
        cef = 0
        second = 0

        for r in rows_res:
            if r[4] < r[6]:
                cef = 100 - (float(r[4]) / float(r[6]) * 100)
            elif r[6] < r[4]:
                cef = 100 - (float(r[6]) / float(r[4]) * 100)
            else:
                if r[10] == r[9]:
                    cef = 0

            if float(r[9]) > 0 and float(r[9]):
                self.downcoefList.append((str(r[1])+' - кэф первого просел на: '+str(r[9])+'%, '+' D:' + str(cef)))
            if float(r[10]) > 0 and float(r[10]):
                self.downcoefList.append((str(r[1]) + ' - кэф второго просел на: ' + str(r[10]) + '%, '+' D:' + str(cef)))
            elif r[3] == '\xa0':
                self.waiting_for.append((str(r[1]) + 'на подходе'))
        con.commit()
        con.close()

    def clear_table_line(self):
        list_line_id = []
        remove_list = []
        '''
            if game was ended clear
         game info in line table
         '''
        sql_check_for_value = '''select * from line_games'''
        sql_find_val = '''select * from live_games where id = %s'''
        sql_drop_from_line = '''Delete from line_games where id=%s'''
        sql_winf = '''Update line_games set wf_change =%s where id=%s '''
        sql_winsec = '''Update line_games set ws_change =%s where id=%s '''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql_check_for_value)
        rows = cur.fetchall()
        for row in rows:
            if str(row[11]) != '0':
                cur.execute(sql_winf, ('0', row[0],))
                cur.execute(sql_winsec, ('0', row[0],))
            list_line_id.append(row[0])
        for i in list_line_id:
            cur.execute(sql_find_val, (i,))
            if cur.fetchone() is None:
                # print(i)
                remove_list.append(i)
        # print(len(remove_list))
        for i in remove_list:
            cur.execute(sql_drop_from_line, (i,))
        con.commit()
        con.close()

    def update_data_from_live(self, id):
        print('update data from live')
        '''
            check the value by id from line_games table
            get the new coeff value and put it into column by_time
        '''
        sql_line = '''select * from line_games'''
        sql_live = '''select * from live_games where id=%s'''
        sql_line_update_f = '''Update line_games set wf_by_time =%s where id=%s'''
        sql_line_update_sec = '''Update line_games set ws_by_time =%s where id=%s'''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql_live, (id,))
        row_live = cur.fetchone()
        if row_live is not None:
            cur.execute(sql_line_update_f, (row_live[4], row_live[0]))
            cur.execute(sql_line_update_sec, (row_live[6], row_live[0]))
        con.commit()
        con.close()


    def add_summscore_inlinegames(self):

        '''
        update the line games table set the new value
         - sumscore to check it variations

        '''

        sql = '''select * from live_games'''
        sql_isert_score = '''update line_games set summ_score = %s where id =%s'''
        sql_timer_update = '''update line_games set timer = %s where id =%s'''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            id = row[0]
            goals = row[14]
            time = row[3]
            cur.execute(sql_isert_score, (goals, id,))
            cur.execute(sql_timer_update, (time, id,))
        con.commit()
        con.close()



    def check_score_max(self):

        '''
        check for max summ of goals

        '''
        sql = '''select * from live_games'''
        sql_isert_score = '''update live_games set summ_score = %s where id =%s'''
        sql_max = '''select teams from live_games where summ_score = (select max(summ_score) from live_games)'''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            id = row[0]
            parts = row[2].rsplit(' ', 2)
            parts_1 = parts[0].rsplit('-', 2)
            t = (int(parts_1[0]) + int(parts_1[1]))
            cur.execute(sql_isert_score, (t, id,))
        cur.execute(sql_max)
        res = cur.fetchone()
        con.commit()
        con.close()
        return res

    def find_max_score(self):
        self.game_best_score.clear()
        sql = '''SELECT teams, MAX (summ_score) FROM live_games GROUP BY teams HAVING MAX(summ_score) > 2'''

        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
           self.game_best_score.append(row[0]+' накидали '+str(row[1])+' штук(и)')

        if(len(self.game_best_score)) == 0:
            self.game_best_score.append("Вяленько как-то")
        con.commit()
        con.close()



    def check_score_null(self):
        id = str
        '''
        check for score where sum is null

        '''
        print('check for null')
        sql = '''select * from line_games'''
        sql_isert_score = '''update line_games set summ_score = %s where id =%s'''
        sql_max = '''select * from line_games where summ_score = 0'''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            id = str(row[0])
            parts = row[2].rsplit(' ', 2)
            parts_1 = parts[0].rsplit('-', 2)
            t = (int(parts_1[0]) + int(parts_1[1]))
            cur.execute(sql_isert_score, (t, id,))
        # cur.execute(sql_max)
        # res = cur.fetchone()
        con.commit()
        con.close()
        print('checking null score')
        return id

    def init_betodds(self):
        self.clear_table_line()
        self.create_line_table()
        self.select_by_waiting()
        self.check_score_null()
        self.add_summscore_inlinegames()
        self.get_data_by_time()
        self.put_the_changes()
        self.check_score_max()
        self.add_summscore_inlinegames()
        self.clear_data_by_time()








