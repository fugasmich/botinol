import json
import os
import re
import unicodedata
from datetime import datetime
from enum import Enum
from urllib import request

import psycopg2
import requests
import requests as requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class ENUMS(Enum):
    VS = "~vSv~ "
    URL_MAIN = "https://melbet.com/ru/live/football/"
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




web_r = requests.get(ENUMS.URL_MAIN.value)
web_soup = BeautifulSoup(web_r.text, 'lxml')

driver = webdriver.Firefox()
driver.get(ENUMS.URL_MAIN.value)
html = driver.execute_script("return document.documentElement.outerHTML")
sel_soup = BeautifulSoup(html, 'lxml')

# get needed time by Id
times_by_Id = []
# the real time id
id_live = []
#teams
teams = []
#times
times =[]
#score
score =[]

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



#get coefficients
coeffficients = []


# получаем матчи продолжительностью до
def get_time():
    time_tmp = []
    for x in sel_soup.find_all(attrs={'class': 'time'}):
        if x.text is not None:
            if x.text == ' ':
                time_tmp.append('*')
            time_tmp.append(re.sub('\ |\(|\.|\)|\/|\;|', '', x.text))

    for i in range(0, len(time_tmp)):
        if i % 2 != 0:
            times.append(time_tmp[i])

    # for i in range(0, len(time_tmp)):
    #     if i % 2 == 0:
    #         times.append(time_tmp[i])
    # return times


# getting id of games
def get_Id():
    for x in sel_soup.find_all('a', attrs={'class': 'nameLink'}):
        id_live.append(x.get('id'))
    return id_live


# get the games coefficients by own id
def get_coefficients(id):
    i = 1;
    for x in sel_soup.find_all("span", attrs={'class': 'num'}):
        if i > 10:
            i = 1
        if x.get('data-gameid') == id:
            if x.get('data-param') != '0':
                coeffficients.append(id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                    'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get(
                    'data-coef') + "(" +
                                                 x.get('data-param') + ")")
            else:
                coeffficients.append(id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                    'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get('data-coef'))
            i += 1


# get the ides and put its for search
def fill_coeff_data_list():
    for i in range(0, len(id_live)):
        get_coefficients(id_live[i])


# get the coefficients value by
# #type key
def coefficient_extractor(key):
    tmp_list = []
    for i in range(0, len(coeffficients)):
        if key in coeffficients[i]:
            tmp_list.append(coeffficients[i][14:])
    return tmp_list


# just combine two string
def list_row_concat(l1, l2, split):
    l3 = []
    for i in range(0, len(l2)):
        l3.append(l1[i] + split + l2[i])
    return l3

# get the teams
# def get_teams_list():
#     temp_ = []
#     l_team1 = []
#     l_team2 = []
#     for x in sel_soup.find_all(attrs={'class': 'team'}):
#         if "Игра" not in x.text or "матч" not in x.text or 'финал' not in x.text:
#             temp_.append(x.text)
#     for i in range(0, len(temp_)):
#             if temp_[i] is not None:
#                 if i % 2 == 0 and temp_[i] is not "":
#                     l_team1.append(temp_[i])
#                 elif i % 2 != 0 and temp_[i] is not "":
#                     l_team2.append(temp_[i])
#     for w in range(0, len(l_team1)):
#
#         teams.append(l_team1[w]+"VS "+l_team2[w])


# get the goal_score
def get_score():
    temp_ = []
    for x in sel_soup.find_all(attrs={'class': 'hideNums'}):
        score.append(x.text)
    # return score

def get_ligue():
    for x in sel_soup.find_all(attrs={'class': 'kofsTableLigaName'}):
        print(x.text, x.get('liga'))


def init_all_coef():
    for w in range(0, len(coefficient_extractor('t1*'))):
        coeff_w_first.append(coefficient_extractor('t1*')[w])

    for w in range(0, len(coefficient_extractor('t2*'))):
        coeff_draw.append(coefficient_extractor('t2*')[w])

    for w in range(0, len(coefficient_extractor('t3*'))):
        coeff_w_second.append(coefficient_extractor('t3*')[w])

    for w in range(0, len(coefficient_extractor('t4*'))):
        coeff_dcw_first.append(coefficient_extractor('t4*')[w])

    for w in range(0, len(coefficient_extractor('t5*'))):
        coeff_dc_draw.append(coefficient_extractor('t5*')[w])

    for w in range(0, len(coefficient_extractor('t6*'))):
        coeff_dcw_second.append(coefficient_extractor('t6*')[w])

    for w in range(0, len(coefficient_extractor('t7*'))):
        coeff_han_f_l.append(coefficient_extractor('t7*')[w])

    for w in range(0, len(coefficient_extractor('t8*'))):
        coeff_han_s_H.append(coefficient_extractor('t8*')[w])

    for w in range(0, len(coefficient_extractor('t9*'))):
        coeff_tH.append(coefficient_extractor('t9*')[w])

    for w in range(0, len(coefficient_extractor('t10*'))):
        coeff_tL.append(coefficient_extractor('t10*')[w])

#create database
def table_create():
    con = psycopg2.connect(
    database="postgres",
    user="dimsan",
    password="domi21092012nika",
    host="127.0.0.1",
    port="5432"
        )

    cur = con.cursor()
    cur.execute('''CREATE TABLE  if not exists live_games (ID VARCHAR,TEAMS VARCHAR,SCORE VARCHAR,TIMER VARCHAR,WF_COEF VARCHAR,DRW_COEF VARCHAR, WSEC_COEF VARCHAR, WF_DCHANCE_COEF VARCHAR,DRW_DCHANCE_COEF VARCHAR,WSEC_DCHANCE_COEF VARCHAR,HANDICF_LOW VARCHAR,HANDICS_HIGH VARCHAR,T_HIGH VARCHAR, T_LOW VARCHAR)''')

    print("Table created successfully")
    con.commit()
    con.close()


#fill data base
def fill_DB_data():
    """ insert a new vendor into the vendors table """
    clear = '''DELETE FROM live_games'''
    sql = """INSERT INTO live_games(id, teams, score, timer, wf_coef, drw_coef,
            wsec_coef, wf_dchance_coef, drw_dchance_coef, wsec_dchance_coef, handicf_low, handics_high, t_high,t_low)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    conn = None

    try:
        # read database configuration

        # connect to the PostgreSQL database
        conn = psycopg2.connect(database="postgres",
        user="dimsan",
        password="domi21092012nika",
        host="127.0.0.1",
        port="5432")
        # create a new cursor
        cur = conn.cursor()
        cur.execute(clear)
        # execute the INSERT statement
        for i in range(0, len(teams)):
            cur.execute(sql, (id_live[i], teams[i], score[i], times[i],
                              coeff_w_first[i], coeff_draw[i], coeff_w_second[i],
                              coeff_dcw_first[i], coeff_dc_draw[i], coeff_dcw_second[i],
                              coeff_han_f_l[i], coeff_han_s_H[i],
                              coeff_tH[i], coeff_tL[i]))



        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# read json to get leagues with teams
def get_teams_list():
    req = requests.get('https://melbet.com/LiveFeed/Get1x2_VZip?sports=1&count=50&mode=4&cyberFlag=2&partner=8')
    list_js = req.json()
    for t in list_js['Value']:
        teams.append(t['L'] + ':' + " " + t['O1'] + ' vs ' + t['O2'])

def main():
    get_Id()
    fill_coeff_data_list()
    get_teams_list()
    get_score()
    get_time()
    init_all_coef()
    table_create()
    fill_DB_data()
    driver.close()
main()
# if __name__ == '__main__':




