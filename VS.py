import requests
from gettext import find
import bs4
import telebot
from telebot import types

def f(bot, chat_id):
    name = "teorema"
    bot.send_message(chat_id, text = name)

def integral(bot, chat_id):
    name = "integral"
    bot.send_message(chat_id, text=name)

def t(bot, chat_id):
    name = "function"
    bot.send_message(chat_id, text = name)