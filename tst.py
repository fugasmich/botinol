import os
import re
import time
from enum import Enum
from multiprocessing import Process


import requests as requests
from bs4 import BeautifulSoup
from selenium import webdriver

from BetOddClass import BetODD


class ENUMS(Enum):
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


class LiveTST():
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

    def run_driver(self):
        # web_r = requests.get(ENUMS.URL_MAIN.value)
        # web_soup = BeautifulSoup(web_r.text, 'lxml')
        #
        # self.driver = webdriver.Firefox()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("/usr/bin/goggle-chrome")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)

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

    # getting id of games
    def get_Id(self):
        for x in self.sel_soup.find_all('a', attrs={'class': 'nameLink'}):
            self.id_live.append(x.get('id'))
        if len(self.id_live) != 0:
            print('Ай-ди собраны')
        else:
            print('Ай-ди не собраны')
        return self.id_live

    # get the games coefficients by own id
    def get_coefficients(self, id):
        i = 1
        for x in self.sel_soup.find_all("span", attrs={'class': 'num'}):
            if i > 10:
                i = 1
            if x.get('data-gameid') == id:
                if x.get('data-param') != '0':
                    self.coeffficients.append(
                        id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                            'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get(
                            'data-coef') + "(" +
                                                         x.get('data-param') + ")")
                else:
                    self.coeffficients.append(
                        id + " " + 't' + str(i) + "*" + " LCK" if x.get('data-block') == '0' or x.get(
                            'data-block') == 'true' else id + " " + 't' + x.get('data-type') + "*" + " " + x.get(
                            'data-coef'))
                i += 1

    # get the ides and put its for search
    def fill_coeff_data_list(self):
        for i in range(0, len(self.id_live)):
            self.get_coefficients(self.id_live[i])
        if len(self.coeffficients) != 0:
            print('данные о коэффициентах собраны')
        else:
            print('данные о коэффициентах собраны')

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
        if len(self.score) != 0:
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
            self.teams.append(
                list_js['Value'][t]['L'] + ':' + " " + list_js['Value'][t]['O1'] + ' vs ' + list_js['Value'][t]['O2'])
            # print( list_js['Value'][t]['O1'] + ' vs ' + list_js['Value'][t]['O2'])



    def main(self):
        self.run_driver()
        self.get_Id()
        self.fill_coeff_data_list()
        self.get_teams_list()
        self.get_score()
        self.get_time()
        self.init_all_coef()
        self.driver.close()


