"""Модуль содержит класс User"""

from telebot import types
import requests
from bs4 import BeautifulSoup as Soup
from settings import horo_data, day_data


class User:
    """
    Класс, отвечающий за взаимодействие с отдельным пользователем.
    Пинимает id-пользователя, сгенерированного бота и текстовую конструкцию для ответов.
    """
    def __init__(self, chat_id, bot, command_text):
        self.chat_id = chat_id
        self.bot = bot
        self.command_text = command_text

    def horo_list(self):
        text = "Веду поиск, надо подождать..."
        markup = types.InlineKeyboardMarkup()
        for key, value in horo_data.items():
            button = types.InlineKeyboardButton(key, callback_data=value)
            markup.row(button)
        self.bot.send_message(self.chat_id, text, reply_markup=markup)

    def horo_detail(self, horo_name, day='today'):
        markup = types.InlineKeyboardMarkup()
        for key, value in day_data.items():
            button = types.InlineKeyboardButton(key, callback_data=value + f',{horo_name}')
            markup.row(button)
        text = "Веду поиск, надо подождать..."
        self.bot.send_message(self.chat_id, text)
        url = f"https://horo.mail.ru/prediction/{horo_name}/{day}/"
        response = requests.get(url)
        res = response.text
        for key, value in day_data.items():
            if value == day:
                text = f'<b>{key}\n</b>'
        for i in Soup(res, 'html.parser').find_all('p'):
            text += f'<i>{str(i)[3:-4:]}</i>'
        self.bot.send_message(self.chat_id, text, parse_mode='HTML', reply_markup=markup)
