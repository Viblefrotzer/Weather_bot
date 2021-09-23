import telebot
from telebot import types
from config import token

bot = telebot.TeleBot(token)

states = {}

MAIN_STATE = 'main'
CITY_STATE = 'city'
WEATHER_DATE_STATE = 'weather_date_state'


@bot.message_handler(func=lambda message: True)
def dispatcher(message):
    user_id = message.from_user.id
    state = states.get(user_id, MAIN_STATE)  # если пользователь в первый раз
    if state == MAIN_STATE:
        main_handler(message)
    elif state == CITY_STATE:
        city_handler(message)
    elif state == WEATHER_DATE_STATE:
        weather_date(message)


def main_handler(message):
    user_id = message.from_user.id

    if message.text == '/start':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Погода'))

        bot.send_message(
            user_id,
            'Этот бот умеет показывать погоду',
            reply_markup=markup,
        )
        states[user_id] = MAIN_STATE

    elif message.text == 'Погода':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['мск', 'спб']]
        )
        bot.send_message(user_id, "А какой город? Москва или Спб?", reply_markup=markup)
        states[user_id] = CITY_STATE

    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id, 'Я тебя не понял', reply_markup=markup)


data = {
    MAIN_STATE: {

    },
    CITY_STATE: {

    },
    WEATHER_DATE_STATE: {
        # id: city
    },
}


def city_handler(message):
    user_id = message.from_user.id
    if message.text.lower() in ['мск', 'спб']:
        data[WEATHER_DATE_STATE][user_id] = message.text.lower()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(
            *[types.KeyboardButton(button) for button in ['сегодня', 'завтра']]
        )
        bot.send_message(user_id, 'А какая дата? введи "сегодня" или "завтра"', reply_markup=markup)
        states[user_id] = WEATHER_DATE_STATE
    else:
        bot.reply_to(message, 'хрю')


WEATHER = {
    'спб': {
        'сегодня': '27',
        'завтра': '32',
    },
    'мск': {
        'сегодня': '10',
        'завтра': '6',
    },
}


def weather_date(message):
    user_id = message.from_user.id
    city = data[WEATHER_DATE_STATE][user_id]

    if message.text == 'сегодня':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        states[user_id] = MAIN_STATE

    elif message.text == 'завтра':
        bot.send_message(user_id, WEATHER[city][message.text.lower()])
        states[user_id] = MAIN_STATE

    elif message.text.lower() == 'Назад':
        bot.send_message(user_id, 'Вернулся назад')
        states[user_id] = MAIN_STATE

    else:
        bot.reply_to(message, "Я тебя не понял")


if __name__ == "__main__":
    bot.polling()
