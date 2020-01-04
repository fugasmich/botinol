#!/usr/local/bin/python
# coding=utf-8
import os

from selenium import webdriver
import logging
import os

import re
import time

from multiprocessing import Process

import psycopg2
import requests as requests
from bs4 import BeautifulSoup
from enum import Enum
from selenium import webdriver


from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class ENUMS(Enum):
    DATABASE_NAME = 'melbet'
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


class LiveData():
    # //logging.basicConfig(filename="mb.log", level=logging.INFO)



    # get needed time by Id
    times_by_Id = []
    # the real time id
    id_live = []
    # teams
    teams = []
    # times
    times = []
    # score
    score = []
    # get coefficients
    coeffficients = []
    coeff_w_first = []
    coeff_draw = []
    coeff_w_second = []
    coeff_dcw_first = []
    coeff_dc_draw = []
    coeff_dcw_second = []
    coeff_han_f_l = []
    coeff_han_s_H = []
    coeff_tH = []
    coeff_tL = []
    html = ''
    sel_soup = BeautifulSoup(html, 'lxml')

    def open_connect(self):
        '''Connect to an existing database'''
        con = psycopg2.connect()
        try:
            con = psycopg2.connect(database=ENUMS.DATABASE_NAME.value,
                                   user=ENUMS.USER.value,
                                   password=ENUMS.PASSWORD.value,
                                   host=ENUMS.HOST.value,
                                   port=ENUMS.PORT.value)
            logging.info('connection is is success')
        except ConnectionError as ex:
            logging.error(ex)
        return con




    def run_driver(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("/usr/bin/goggle-chrome")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome()


        web_r = requests.get(ENUMS.URL_MAIN.value)
        web_soup = BeautifulSoup(web_r.text, 'lxml')

        # self.driver = webdriver.Firefox(firefox_binary=binary,
        #                        capabilities=caps,
        #                        executable_path=r'/usr/local/bin/geckodriver')
        # self.driver = webdriver.Firefox()
        self.driver.get(ENUMS.URL_MAIN.value)
        self.html = self.driver.execute_script("return document.documentElement.outerHTML")
        self.sel_soup = BeautifulSoup(self.html, 'lxml')



    # получаем матчи продолжительностью до
    def get_time(self):
        time_tmp = []
        for x in self.sel_soup.find_all(attrs={'class': 'time'}):
            if x.text is not None:
                if x.text == ' ':
                    time_tmp.append('*')
                time_tmp.append(re.sub('\ |\(|\.|\)|\/|\;|', '', x.text))

        for i in range(0, len(time_tmp)):
            if i % 2 != 0:
                self.times.append(time_tmp[i])
        if len(self.times) != 0:
            logging.info('timers list was appended')
        else:
            logging.error('timers list has no appended')
        return self.times


    # getting id of games
    def get_Id(self):
        for x in self.sel_soup.find_all('a', attrs={'class': 'nameLink'}):
            self.id_live.append(x.get('id'))
        if len(self.id_live) != 0 :
            logging.info('ides list was appended')
        else:
            logging.error('ides list has no append')
        return self.id_live

    # get the games coefficients by own id
    def get_coefficients(self, id):

        try:
            i = 1
            for x in self.sel_soup.find_all("span", attrs={'class': 'num'}):
                if i > 10:
                    i = 1
                if x.get('data-gameid') == id:
                    if x.get('data-param') != '0':
                        self.coeffficients.append(id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                            'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get(
                            'data-coef') + "(" +
                                                         x.get('data-param') + ")")
                    else:
                        self.coeffficients.append(id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                            'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get(
                            'data-coef'))
                    i += 1
            logging.info('all coefficients was appended in the list')
        except Exception as ex:
            logging.error(ex)


    # get the ides and put its for search
    def fill_coeff_data_list(self):
        for i in range(0, len(self.id_live)):
            self.get_coefficients(self.id_live[i])
        if len(self.coeffficients) != 0:
            logging.info('данные о коэффициентах собраны')
        else:
            logging.error('данные о коэффициентах собраны')
    # get the coefficients value by
    # #type key
    def coefficient_extractor(self, key):
        tmp_list = []
        for i in range(0, len(self.coeffficients)):
            if key in self.coeffficients[i]:
                tmp_list.append(self.coeffficients[i][14:])
        return tmp_list



    # get the goal_score
    def get_score(self):
        temp_ = []
        for x in self.sel_soup.find_all(attrs={'class': 'hideNums'}):
            self.score.append(x.text)
        # return score
        if  len(self.score) !=0:
            print("информация о счете собрана")

        else:
            print("информация о счете не собрана")



    def init_all_coef(self):

        try:
            for w in range(0, len(self.coefficient_extractor('t1*'))):
                self.coeff_w_first.append(self.coefficient_extractor('t1*')[w])

            for w in range(0, len(self.coefficient_extractor('t2*'))):
                self.coeff_draw.append(self.coefficient_extractor('t2*')[w])

            for w in range(0, len(self.coefficient_extractor('t3*'))):
                self.coeff_w_second.append(self.coefficient_extractor('t3*')[w])

            for w in range(0, len(self.coefficient_extractor('t4*'))):
                self.coeff_dcw_first.append(self.coefficient_extractor('t4*')[w])

            for w in range(0, len(self.coefficient_extractor('t5*'))):
                self.coeff_dc_draw.append(self.coefficient_extractor('t5*')[w])

            for w in range(0, len(self.coefficient_extractor('t6*'))):
                self.coeff_dcw_second.append(self.coefficient_extractor('t6*')[w])

            for w in range(0, len(self.coefficient_extractor('t7*'))):
                self.coeff_han_f_l.append(self.coefficient_extractor('t7*')[w])

            for w in range(0, len(self.coefficient_extractor('t8*'))):
                self.coeff_han_s_H.append(self.coefficient_extractor('t8*')[w])

            for w in range(0, len(self.coefficient_extractor('t9*'))):
                self.coeff_tH.append(self.coefficient_extractor('t9*')[w])

            for w in range(0, len(self.coefficient_extractor('t10*'))):
                self.coeff_tL.append(self.coefficient_extractor('t10*')[w])
            print('все коэффициенты распределены')
        except:
            print('коэффициенты не распределены')


    # read json to get leagues with teams
    def get_teams_list(self):
        req = requests.get(ENUMS.URL_JsON.value)
        list_js = req.json()
        for t in range(0, len(list_js['Value'])):
            self.teams.append(list_js['Value'][t]['L'] + ':' + " " + list_js['Value'][t]['O1'] + ' vs ' + list_js['Value'][t]['O2'])
            # print( list_js['Value'][t]['O1'] + ' vs ' + list_js['Value'][t]['O2'])
            print(self.teams[0])
    # create database
    def table_create(self):
        # con = psycopg2.connect(
        #     database="postgres",
        #     user="dimsan",
        #     password="domi21092012nika",
        #     host="127.0.0.1",
        #     port="5432"
        # )
        con = self.open_connect()
        cur = con.cursor()
        cur.execute('''CREATE TABLE  if not exists live_games  
         (ID VARCHAR,
         TEAMS VARCHAR,
         SCORE VARCHAR,
         TIMER VARCHAR,
         WF_COEF VARCHAR,
         DRW_COEF VARCHAR,
         WSEC_COEF VARCHAR,
         WF_DCHANCE_COEF VARCHAR ,
         DRW_DCHANCE_COEF VARCHAR,
         WSEC_DCHANCE_COEF VARCHAR,
         HANDICF_LOW VARCHAR, 
         HANDICS_HIGH VARCHAR,     
         T_HIGH VARCHAR,
         T_LOW VARCHAR
        
        )''')

        print("таблица live_games создана")
        con.commit()
        con.close()

    # fill data base
    def fill_DB_data(self):
        """ insert a new vendor into the vendors table """
        clear = '''DELETE FROM live_games'''
        sql = """INSERT INTO live_games(id, teams, score, timer, wf_coef, drw_coef,
                wsec_coef, wf_dchance_coef, drw_dchance_coef, wsec_dchance_coef, handicf_low, handics_high, t_high,t_low)
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        conn = None

            # try:
            # read database configuration

        # connect to the PostgreSQL database
        # conn = psycopg2.connect(database="postgres",
        #                         user="dimsan",
        #                         password="domi21092012nika",
        #                         host="127.0.0.1",
        #                         port="5432")
        conn = self.open_connect()
        # create a new cursor
        cur = conn.cursor()
        cur.execute(clear)
        # print(len(self.id_live))
        # print(len(self.teams))
        # print(len(self.score))
        # print(len(self.times))
        # execute the INSERT statement
        for i in range(0, len(self.id_live)):
            cur.execute(sql, (self.id_live[i], self.teams[i], self.score[i], self.times[i],
                              self.coeff_w_first[i], self.coeff_draw[i], self.coeff_w_second[i],
                              self.coeff_dcw_first[i], self.coeff_dc_draw[i], self.coeff_dcw_second[i],
                              self.coeff_han_f_l[i], self.coeff_han_s_H[i],
                              self.coeff_tH[i], self.coeff_tL[i]))

        self.id_live.clear()
        self.score.clear()
        self.times.clear()
        self.teams.clear()
        self.coeffficients.clear()
        self.coeff_w_first.clear()
        self.coeff_draw.clear()
        self.coeff_w_second.clear()
        self.coeff_dcw_first.clear()
        self.coeff_dc_draw.clear()
        self.coeff_dcw_second.clear()
        self.coeff_han_f_l.clear()
        self.coeff_han_s_H.clear()
        self.coeff_tH.clear()
        self.coeff_tL.clear()
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print('таблица live_games Заполнена данными')
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print('ошибка при добавлени данных в таблицу live-games')
        #     print(error)
        # finally:
        if conn is not None:
            conn.close()

    #
    # def clear_data(self):
    #     clear = '''DELETE FROM live_games'''
    #
    #     conn = psycopg2.connect(database="postgres",
    #                         user="dimsan",
    #                         password="domi21092012nika",
    #                         host="127.0.0.1",
    #                         port="5432")
    #     # create a new cursor
    #     cur = conn.cursor()
    #
    #     cur.execute(clear)
    #     conn.commit()
    #     conn.close()


    def clear_dublicate_live(self):
        '''remove all dublicates from line_table'''
        sql = """DELETE FROM live_games WHERE ctid NOT IN
    (SELECT max(ctid) FROM live_games GROUP BY live_games.*);"""
        # con = psycopg2.connect(
        #     database="postgres",
        #     user="dimsan",
        #     password="domi21092012nika",
        #     host="127.0.0.1",
        #     port="5432"
        # )
        con = self.open_connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def main(self):

        # self.clear_data()
        self.run_driver()
        # self.get_Id()
        # self.fill_coeff_data_list()
        # self.get_teams_list()
        # self.get_score()
        # self.get_time()
        # self.init_all_coef()
        # self.table_create()
        # self.fill_DB_data()
        # self.driver.close()



