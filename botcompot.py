#!/usr/bin/env python3


from telegram import Update, Bot
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.utils.request import Request

from BetOddClass import BetODD

button_tasher ='Чё там с кэфами?'
button_goals_summ = 'максимум забитых голов'
button_update = 'обновить данные'

print('BOT STARTED')
betOdd = BetODD()
def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise
    return inner




def button_tasher_handler(update: Update, context: CallbackContext):
    betOdd.init_betodds()
    if len(betOdd.downcoefList_first) > 0:
        for j in betOdd.downcoefList_first:
            update.message.reply_text(
                text=j,
            )
    elif len(betOdd.downcoefList_second) > 0:
        for i in betOdd.downcoefList_second:
            update.message.reply_text(
                text=i,
            )
    elif len(betOdd.t) > 0:
        for k in betOdd.t:
            update.message.reply_text(
                text=k,
            )
    else:
        update.message.reply_text(
            text='пока тишина....',
        )

def button_maxgoals_handler(update: Update, context: CallbackContext):
        betOdd.init_betodds()

        for j in betOdd.game_best_score:
            update.message.reply_text(
                text=j,
            )
        if len(betOdd.game_best_score) == 0:
            update.message.reply_text(
                text='как-то вяленько...',
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




def main():
    print('Start')

    req = Request(
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



    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()
    print('Finish')


if __name__ == '__main__':
    main()


