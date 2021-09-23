import telebot

from config import token

bot = telebot.TeleBot(token)

# @bot.message_handler(content_types=['photo'])
# def handle_photos(message):
#     # print(message.photo)
#     print(message.photo[-1])
#
#     bot.send_photo(message.from_user.id, message.photo[-1].file_id, caption="Your photo!")
#
#     # bot.send_sticker(..., message.sticker.file_id)
#
#
# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     print(message.text)
#     print(message.entities[0])
#     entity = message.entities[0]
#     value_in_text = message.text[entity.offset: entity.offset + entity.length]
#     print('value from telegram', value_in_text)

from telebot import types


@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=4)
    # btn1 = types.KeyboardButton('a')
    # btn2 = types.KeyboardButton('b')
    # btn3 = types.KeyboardButton('c')
    # btn4 = types.KeyboardButton('d')
    #
    # # keyboard.add(btn1, btn2, btn3)
    # keyboard.row(btn1, btn2, btn3)
    # keyboard.add(btn4)

    # array = ['A', 'B', 'C', 'D']

    # for item in array:
    #     keyboard.add(item)
    keyboard.add(types.KeyboardButton('A'), types.KeyboardButton('B'), types.KeyboardButton('C'),
                 types.KeyboardButton('D'))

    bot.send_message(message.from_user.id, 'Hello! buttons below', reply_markup=keyboard)
    # bot.send_message(message.chat.id, 'Hello! buttons below', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == 'A')
def handle_A(message):
    bot.send_message(message.from_user.id, 'Вы сказали "А"')

@bot.message_handler(func=lambda message: message.text == 'B')
def handle_B(message):
    bot.send_message(message.from_user.id, 'Вы сказали "В"')

@bot.message_handler(func=lambda message: message.text == 'C')
def handle_C(message):
    bot.send_message(message.from_user.id, 'Вы сказали "C"')

@bot.message_handler(func=lambda message: message.text == 'D')
def handle_D(message):
    bot.send_message(message.from_user.id, 'Вы сказали "D"')

bot.polling()
