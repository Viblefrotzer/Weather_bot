import telebot
from telebot import types
import json
import os
import requests

OWM_API_key = os.environ['OWM_API_key']
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

MAIN_STATE = 'main'
CITY_STATE = 'city'
WEATHER_DATE_STATE = 'weather_date_state'

try:
    data = json.load(open('db/data.json', 'r', encoding='utf-8'))
except FileNotFoundError:
    data = {
        'states': {},
        MAIN_STATE: {

        },
        CITY_STATE: {

        },
        WEATHER_DATE_STATE: {
            # id: city
        },
    }


def change_data(key, user_id, value):
    data[key][user_id] = value
    json.dump(
        data,
        open('db/data.json', 'w', encoding='utf-8'),
        indent=2,
        ensure_ascii=False,
    )


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = data['states'].get(user_id, MAIN_STATE)  # если пользователь в первый раз
    if state == MAIN_STATE:
        main_handler(message)
    elif state == CITY_STATE:
        city_handler(message)
    elif state == WEATHER_DATE_STATE:
        weather_date(message)


def main_handler(message):
    user_id = str(message.from_user.id)
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Погода'))
        bot.send_message(
            user_id,
            'Этот бот умеет показывать погоду',
            reply_markup=markup,
        )
        change_data('states', user_id, MAIN_STATE)
    elif message.text == 'Погода':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['мск', 'спб']]
        )
        bot.send_message(user_id, "А какой город? Москва или Спб?", reply_markup=markup)
        change_data('states', user_id, CITY_STATE)
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id, 'Я тебя не понял', reply_markup=markup)


def city_handler(message):
    user_id = str(message.from_user.id)
    if message.text.lower() in ['мск', 'спб']:
        global city_name
        city_name = ""
        change_data(WEATHER_DATE_STATE, user_id, message.text.lower())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['сегодня', 'завтра']]
        )
        bot.send_message(user_id, 'А какая дата? введи "сегодня" или "завтра"', reply_markup=markup)
        change_data('states', user_id, WEATHER_DATE_STATE)
        if message.text.lower() == 'мск':
            city_name = 'Москва'
        elif message.text.lower() == 'спб':
            city_name = 'Санкт-Петербург'
        return city_name
    else:
        bot.reply_to(message, 'Я тебя не понял')


def weather_date(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Погода'))
    user_id = str(message.from_user.id)
    api_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': OWM_API_key,
        'units': 'metric',
        'lang': 'ru'
    }
    if message.text == 'сегодня':
        result = requests.get(api_url, params=params)
        data = result.json()
        template = 'Сегодня в городе {} температура {}°, {}.'
        pogoda = template.format(city_name, data['list'][0]['main']['temp'], data['list'][0]['weather'][0]['description'])
        bot.send_message(user_id, pogoda)
        change_data('states', user_id, MAIN_STATE)

    elif message.text == 'завтра':
        result = requests.get(api_url, params=params)
        data = result.json()
        template = 'Завтра в городе {} температура {}°, {}.'
        pogoda = template.format(city_name, data['list'][8]['main']['temp'], data['list'][8]['weather'][0]['description'])
        bot.send_message(user_id, pogoda)
        change_data('states', user_id, MAIN_STATE)


    else:
        bot.reply_to(message, "Я тебя не понял")


if __name__ == "__main__":
    bot.polling()
