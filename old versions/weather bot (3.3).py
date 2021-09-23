import telebot
from datetime import date, timedelta
from config import token

# token = '1862518364:AAGU26jKgk75lj_IMlFpWZP9r4g0IMtZ0dM'
bot = telebot.TeleBot(token)
states = {}

MAIN_STATE = 'main'
WEATHER_DATE_STATE = 'weather_date_handler'
WEATHER_DATA = {
    'июль': {
        7: 27,
        8: 32,
        9: 45,
        10: 10,
        11: 11,
        12: 12,
        13: 13
    }

}
MONTHS = {
    7: 'июль'
}
calls = {

}


@bot.message_handler(func=lambda message: True)
def main_handler(message):
    if 'погода' in message.text.lower():
        bot.send_message(message.from_user.id, 'А какая дата? Введи в формате "Месяц, число"')
        bot.register_next_step_handler(message, weather_date)
    if 'вызовы' in message.text.lower():
        bot.send_message(message.from_user.id, str(calls[message.from_user.id]))
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понял')


def weather_date(message):
    user_id = message.from_user.id
    if user_id not in calls:
        calls[user_id] = 0

    calls[user_id] += 1

    if 'сегодня' in message.text.lower():
        today = date.today()
        month_name = MONTHS[today.month]  # например, июль
        current_day = today.day
        current_weather = WEATHER_DATA[month_name][current_day]
        bot.send_message(message.from_user.id, 'Градусы: {0}'.format(current_weather))
        bot.register_next_step_handler(message, main_handler)

    elif 'завтра' in message.text.lower():
        today = date.today() + timedelta(days=1)
        month_name = MONTHS[today.month]  # например, июль
        current_day = today.day
        current_weather = WEATHER_DATA[month_name][current_day]
        bot.send_message(message.from_user.id, 'Градусы: {0}'.format(current_weather))
        bot.register_next_step_handler(message, main_handler)
    else:
        month, day = message.text.split(',')
        day = int(day.strip())
        month = month.lower()
        bot.reply_to(message, WEATHER_DATA[month][day])
        bot.register_next_step_handler(message, main_handler)


if __name__ == '__main__':
    bot.polling()
