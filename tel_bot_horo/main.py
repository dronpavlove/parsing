"""
Основной модуль программы телеграмм-бота.
Содержит функции, отвечающие за взаимодействие бота с пользователем:
обработка команд;
обработка любых сообщений;
обработка нажатия кнопки.
"""

import telebot
from user_class_new import User
from typing import Any
from settings import TOKEN, horo_data, day_data
import time


users = dict()
bot = telebot.TeleBot(TOKEN)
command = ['help', 'Help', 'Horo', 'horo']
command_text = '\n/help — <i>помощь</i>'\
               '\n/horo - <i>гороскоп</i>'


@bot.message_handler(commands=command)
def handle_command(message):
    """
    Обрабатывает команды типа '/text'
    """
    users[f"{message.chat.id}"] = [message.from_user.first_name, message.from_user.last_name]
    if message.text == '/help' or message.text == '/Help' or message.text == '/start' or message.text == '/Start':
        bot.send_message(message.chat.id, 'Выбирайте, что будем искать.\n'
                                          'Вот перечень моих команд:\n(Here is a list of my commands:)\n'
                         + command_text, parse_mode='HTML')

    elif message.text == '/Horo' or message.text == '/horo':
        User(message.chat.id, bot, command_text).horo_list()


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    """
    Отвечает на текстовые сообщения, которые не предусмотрены в работе бота
    """
    text = 'Что-то пошло не так...' \
           '\nДавайте попробуем ещё раз.' \
           '\nВот перечень моих команд:'
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, command_text, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle(call) -> Any:
    """
    Обработка кнопок.
    """
    # print(call.data.split(',')[1])
    if call.data in horo_data.values():
        horo_name = call.data
        User(call.message.chat.id, bot, command_text).horo_detail(horo_name=horo_name)
    elif call.data == 'all_horo':
        User(call.message.chat.id, bot, command_text).horo_list()
    elif call.data.split(',')[0] in day_data.values():
        horo_name = call.data.split(',')[1]
        day = call.data.split(',')[0]
        User(call.message.chat.id, bot, command_text).horo_detail(horo_name=horo_name, day=day)


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
