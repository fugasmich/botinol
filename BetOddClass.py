import datetime

import psycopg2





# itistime_list = []

class BetODD():
    t = []

    def open_connect(self):
        '''Connect to an existing database'''

        con = psycopg2.connect(database="postgres",
                               user="dimsan",
                               password="domi21092012nika",
                               host="127.0.0.1",
                               port="5432")
        return con

    def select_by_waiting(self):

        '''find and put the values which timescore is none, it  means
        game is waiting for begining - first method'''
        get_data = "SELECT * from live_games "
        set_data = "insert into line_games (id, teams,score, wf_coef, drw_coef, wsec_coef) VALUES (%s, %s, %s, %s, %s, %s)"
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(get_data)
        rows = cur.fetchall()
        for row in rows:
            if row[3] == '\xa0':
                try:
                    cur.execute(set_data, (row[0], row[1], row[2], row[4], row[5], row[6]))
                except:
                    print('дубликат')
        con.commit()
        con.close()

    def clear_dublicate_line(self):




        '''remove all dublicates from line_table'''
        sql = """DELETE FROM line_games WHERE ctid NOT IN
    (SELECT max(ctid) FROM line_games GROUP BY line_games.*);"""
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def get_data_by_time(self):
        '''
        find the games, which timescore between 05  and 17 minutes
        when needed timescore value is found,
          check for goals that must be null
        '''

        date_time_max = datetime.datetime.strptime('15:00', '%M:%S')
        date_time_min = datetime.datetime.strptime('05:00', '%M:%S')
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
                    ''' insert data from live table'''
                    if row[11] == '0':
                        print('catch')
                        self.update_data_from_live(row[0])



        con.commit()
        con.close()

    def create_line_table(self):

        """create line table"""
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
      SUMM_SCORE varchar    
      )''')
        print("Table created successfully")
        con.commit()
        con.close()

    def check_for_changes(self):
        self.t.clear()
        ''' check for coefficients which fallen! It mean the team '''

        sql = '''SELECT * FROM line_games'''
        sql_winf = '''Update line_games set wf_change =%s where id=%s '''
        sql_winsec = '''Update line_games set ws_change =%s where id=%s '''
        sql_best_result = '''Select * from line_games'''
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            if row[7] is not None and row[7] != 'LCK':
                res_1 = "%.2f" % (float(row[4]) - float(row[7]))
            else:
                res_1 = 0
            if row[8] is not None and row[8] != 'LCK':
                res_2 = "%.2f" % (float(row[6]) - float(row[8]))
            else:
                res_2 = 0
            cur.execute(sql_winf, (float(res_1), row[0]))
            cur.execute(sql_winsec, (float(res_2), row[0]))
        cur.execute(sql_best_result)
        rows_res = cur.fetchall()
        for r in rows_res:
            if r[9] is not None or r[10] is not None:
                if float(r[9]) > 0:
                    self.t.append(r[1] + " " + 'тащит!!! кэф  первого просел на ' + " " + "%.2f" % (
                                float(r[9])) + " " + '%')

                elif float(r[10]) > 0:
                    self.t.append(r[1] + " " + 'тащит!!! кэф  второго просел на ' + " " + "%.2f" % (
                                 float(r[10])) + " " + '%')

                else:
                    # self.t.append('следим за матчем: ' + r[1])
                    continue
        con.commit()
        con.close()
        return self.t

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
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql_check_for_value)
        rows = cur.fetchall()
        for row in rows:
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

    def check_score_null(self):
        '''
        check for score where sum is null

        '''
        sql = '''select * from line_games'''
        sql_isert_score = '''update line_games set summ_score = %s where id =%s'''
        # sql_max = '''select id from line_games where summ_score = 0'''
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
        # cur.execute(sql_max)
        res = cur.fetchone()
        con.commit()
        con.close()
        return res

    def init_betodds(self):
        self.select_by_waiting()
        self.check_score_null()
        self.check_for_changes()
        self.get_data_by_time()

        self.clear_table_line()





