import telebot
token = '1862518364:AAGU26jKgk75lj_IMlFpWZP9r4g0IMtZ0dM'
bot = telebot.TeleBot(token)
states = {}


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    bot.reply_to(message, message.text)


bot.polling()
