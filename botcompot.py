#!/usr/bin/env python3


from telegram import Update, Bot
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.utils.request import Request

# from live_data import LiveData
from live_data import LiveData
from tst import LiveTST

button_tasher ='Кэф просел'
button_goals_summ = 'максимум забитых голов'
button_update = 'обновить данные'

print('BOT STARTED')
def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise
    return inner


def button_updatedata_handler(update: Update, context: CallbackContext):
    
    update.message.reply_text(
        text='данные обновлены',
        reply_markup=ReplyKeyboardRemove()

    )


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
    if text == button_update:
        return button_updatedata_handler(update=update, context=context)
    if text == button_tasher:
       return button_tasher_handler(update=update, context=context)
    if text == button_goals_summ:
        return button_maxgoals_handler(update=update, context=context)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text=button_update),
                ],

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


def main():
    print('Start')

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

