import telebot
from BetOddClass import BetODD

TOKEN ='1001485513:AAHSRknpCk7m6OwyViqO2K3F8xxVbEAzNlw'

bot = telebot.TeleBot(TOKEN)
bet_odd = BetODD()






@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Привет! Я codex_bot!')

@bot.message_handler(commands=['run'])
def send_data(message):
    bet_odd.init_betodds()
    s = bet_odd.t
    if len(s)==0:
        msg = bot.send_message(message.chat.id, "пока нехуй ловить")
    else:
        for i in range(0, len(s)):
            msg = bot.send_message(message.chat.id, s[i])



bot.polling()


