
#import time
#from multiprocessing import Process

import telebot

#from BetOddClass import BetODD
#from live_data import LiveData

TOKEN ='1001485513:AAHSRknpCk7m6OwyViqO2K3F8xxVbEAzNlw'
#live_data = LiveData()
bot = telebot.TeleBot(TOKEN)
#bet_odd = BetODD()






@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'HELLO')

@bot.message_handler(commands=['run'])
def send_data(message):

 #   s = bet_odd.t
 #   if len(s)==0:
     msg = bot.send_message(message.chat.id, "there  are not to show ")
  #  else:
   #     for i in range(0, len(s)):
  #          msg = bot.send_message(message.chat.id, s[i])


#def  check_send_message():
 #   live_data = LiveData()

  #  while True:
   #     try:
    #        live_data.main()
     #       bet_odd.create_line_table()
      #      bet_odd.select_by_waiting()
            # with open('mb.log', 'w'):
            #     logging.basicConfig(filename="mb.log", level=logging.INFO)
        #    time.sleep(30)
       # except:
         #   print("falsess")

#p1 = Process(target=check_send_message(),args=())
#p1.start()

bot.polling()
