from telegram import Update, Bot
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.utils.request import Request

<<<<<<< HEAD
#import time
#from multiprocessing import Process
=======
button_tasher ='Кэф просел'
button_goals_summ = 'максимум забитых голов'
>>>>>>> bf680527300e3743884bb5b332bcd193483286eb


<<<<<<< HEAD
#from BetOddClass import BetODD
#from live_data import LiveData

TOKEN ='1001485513:AAHSRknpCk7m6OwyViqO2K3F8xxVbEAzNlw'
#live_data = LiveData()
bot = telebot.TeleBot(TOKEN)
#bet_odd = BetODD()
=======

def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e
    return inner
>>>>>>> bf680527300e3743884bb5b332bcd193483286eb



def button_tasher_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='здесь отобразятся команды с просевшими коэфициентами',


    )
def button_maxgoals_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='здесь отобразятся игры с максимальным количеством забитых голов',

    )
@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_tasher:
       return button_tasher_handler(update=update, context=context)
    if text == button_goals_summ:
        return button_maxgoals_handler(update=update, context=context)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_tasher), KeyboardButton(text=button_goals_summ),
            ],
        ],
        resize_keyboard=True,
    )

    update.message.reply_text(
        text='выбери действие:',
        reply_markup=reply_markup,
    )

<<<<<<< HEAD
 #   s = bet_odd.t
 #   if len(s)==0:
     msg = bot.send_message(message.chat.id, "there  are not to show ")
  #  else:
   #     for i in range(0, len(s)):
  #          msg = bot.send_message(message.chat.id, s[i])
=======
>>>>>>> bf680527300e3743884bb5b332bcd193483286eb

def main():
    print('Start')

<<<<<<< HEAD
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
=======
    req=Request(
        connect_timeout=0.5,
    )
    bot = Bot(
        request=req,
        token='1035105683:AAHDivtSyIbpS4SyMnxd2Z-Ut2JcS84GBMA',
        base_url='https://telegg.ru/orig/bot',

    )
    updater = Updater(
        bot=bot,
        use_context=True,

    )
    print(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))


    updater.start_polling()
    updater.idle()
    print('Finish')


if __name__ == '__main__':
    main()
>>>>>>> bf680527300e3743884bb5b332bcd193483286eb
