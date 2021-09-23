import telebot

# from pprint import pprint

token = '1862518364:AAGU26jKgk75lj_IMlFpWZP9r4g0IMtZ0dM'

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def weather(message):
    print(message)
    if message.text == '/start':
        # bot.reply_to(message, 'Хрю-хрю-хрю')
        bot.reply_to(message, 'Это свинский бот, он умеет показывать погоду на сегодня и завтра. ')
    elif message.text == 'Привет':
        bot.reply_to(message, 'Хрювет, ' + message.from_user.first_name + '!')
    elif message.text == 'погода на сегодня':
        bot.reply_to(message, '34 градуса, Хрю')
    elif message.text == 'погода на завтра':
        bot.reply_to(message, '35 градусов, Хрю-хрю')
    else:
        # bot.reply_to(message, 'Я свинья тупая!')

        bot.send_message(
            message.chat.id,
            'Трололо!',
            # reply_to_message_id=message.message.id,
        )

    # bot.reply_to(message, message.text)
    # bot.reply_to(message, '')


bot.polling()
