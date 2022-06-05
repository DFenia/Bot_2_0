import requests
from gettext import find
import bs4
import telebot
from telebot import types

def f(bot, chat_id):
    name = "t"
    bot.send_message(chat_id, text = name)

def i(bot, chat_id):
    name = "i"
    bot.send_message(chat_id, text = name)

def t(bot, chat_id):
    name = "f"
    bot.send_message(chat_id, text = name)