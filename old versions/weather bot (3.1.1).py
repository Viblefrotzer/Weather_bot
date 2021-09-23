import telebot
from datetime import date, timedelta
token = '1862518364:AAGU26jKgk75lj_IMlFpWZP9r4g0IMtZ0dM'
bot = telebot.TeleBot(token)
states = {}

MAIN_STATE = 'main'
WEATHER_DATE_STATE = 'weather_date_handler'
WEATHER_DATA = {
    'июль': {
        7: 27,
        8: 32,
        9: 45
    }

}
MONTHS = {
    7: 'июль'
}
# CALLS = {
#
# }


# @bot.message_handler(func=lambda message: True)
# def dispatcher(message):
#     print(states)
#     user_id = message.from_user.id
#     state = states.get(user_id, MAIN_STATE)
#     print('current state', user_id, state)
#     if state == MAIN_STATE:
#         main_handler(message)
#     elif state == WEATHER_DATE_STATE:
#         weather_date(message)
#

@bot.message_handler(func=lambda message: True)
def main_handler(message):
    # file_id = (message.photo[1].file_id)
    # bot.send_chat_action(message.from_user.id, 'typing')
    # import time
    # time.sleep(5)
    # bot.send_photo(message.from_user.id, 'https://photoshop-kopona.com/uploads/posts/2018-10/1538636938_1.jpg')
    if 'погода' in message.text.lower():
        # states[message.from_user.id] = WEATHER_DATE_STATE
        bot.send_message(message.from_user.id, 'А какая дата? Введи в формате "Месяц, число"')
        bot.register_next_step_handler(message, weather_date)
    else:
        bot.reply_to(message, 'Я тебя не понял')


@bot.message_handler(func=lambda message: True)  # states.get(message.from_user.id, MAIN_STATE) == WEATHER_DATE_STATE)
def weather_date(message):
    # user_id = message.from_user.id
    # if user_id not in CALLS:
    #     CALLS[user_id] = 0
    # CALLS[user_id] += 1

    if 'сегодня' in message.text.lower():
        today = date.today()
        month_name = MONTHS[today.month]  # например, июнь
        current_day = today.day
        current_weather = WEATHER_DATA[month_name][current_day]
        bot.send_message(message.from_user.id, 'Градусы: {0}'.format(current_weather))
        # states[message.from_user.id] = MAIN_STATE
        bot.register_next_step_handler(message, main_handler)
    elif 'завтра' in message.text.lower():
        today = date.today() + timedelta(days=1)
        month_name = MONTHS[today.month]  # например, июнь
        current_day = today.day
        current_weather = WEATHER_DATA[month_name][current_day]
        bot.send_message(message.from_user.id, 'Градусы: {0}'.format(current_weather))
        # states[message.from_user.id] = MAIN_STATE
        bot.register_next_step_handler(message, main_handler)
    # elif 'вызовы' in message.text.lower():
    #     bot.send_message(message.from_user.id, str(CALLS[message.from_user.id]))
    else:
        # Июнь, 6
        month, day = message.text.split(',')
        day = int(day.strip())
        month = month.lower()
        bot.send_message(message.from_user.id, WEATHER_DATA[month][day])


bot.polling()
