import random
import telebot
from telebot import types
from io import BytesIO

import bs4
import telebot
from telebot import types
import requests
import menuBot
from menuBot import Menu, Users

import random

def info_RSPLS(bot, chat_id):
    text_RSPLS = "Победитель определяется по следующим правилам:\n\n" \
                 "1. Камень побеждает ножницы и ящерицу\n" \
                 "2. Бумага побеждает камень и Спока\n" \
                 "3. Ножницы побеждают бумагу и ящерицу\n"\
                 "4. Ящерица побеждает Спока и бумагу\n" \
                 "5. Спок побеждает камень и ножницы\n" \

    img_RSPLS = open('игра.png', 'rb')
    bot.send_photo(chat_id, caption=text_RSPLS, photo=img_RSPLS)

def game_RSPLS(bot, chat_id, message):
    winner = None
    actions = ["Камень", "Ножницы", "Бумага", "Ящерица", "Спок"]
    computer_action = random.choice(actions)
    playerChoice = message.text
    code = playerChoice[0] + computer_action[0]
    choices = "Игрок выбрал - " + playerChoice + "\n" + "Бот выбрал - " + computer_action + "\n\n"
    if playerChoice == computer_action:
        winner = choices + "Ничья!"
    elif code == "КН" or code == "БК" or code == "БС" or code == "КЯ" or code == "КН" or code == "ЯС" or code == "ЯБ" \
            or code == "СН" or code == "СК" or code == "НБ" or code == "НЯ":
        winner = choices + "Игрок выиграл!"

    else:
        winner = choices + "Бот выиграл!"

    bot.send_message(chat_id, text=winner)