import requests
from gettext import find
import bs4
import telebot
from telebot import types



def dz1(bot, chat_id):
    name = "Привет! Тебя зовут"
    bot.send_message(chat_id, text = name)
def dz2(bot, chat_id):
    name = "..."
    age = 18
    bot.send_message(chat_id, text = f"Здравствуйте! Меня зовут {name}, мне {age} лет.")
def dz3(bot, chat_id):
    name = "..."
    bot.send_message(chat_id, text = name + name + name )
    bot.send_message(chat_id, text = name * 5)
def dz45(bot, chat_id):
    sent = bot.send_message(chat_id, text="Введите имя: ")
    bot.register_next_step_handler(sent, f4, bot, chat_id)
def f4(sent, bot, chat_id):
    sent2 = bot.send_message(chat_id, text="Введите возраст: ")
    bot.register_next_step_handler(sent2, f42, bot, chat_id, sent)
def f42(sent2, bot, chat_id, sent):
    age = int(sent2.text)
    if age < 5:
        bot.send_message(chat_id, text=f"Приветик, {sent.text}! {sent2.text} лет. Ха-ха. Маловато.")
    elif age < 40:
        bot.send_message(chat_id, text=f"Привет, {sent.text}! Ну ничего себе, тебе уже {sent2.text}. Ха-ха)")
    elif age >= 40:
        bot.send_message(chat_id, text=f"Здравствуйте, {sent.text}! Вам, {sent2.text}! Бывает же такое.")
    #bot.send_message(chat_id, text=sent2.text)

def dz6(bot, chat_id):
    sent = bot.send_message(chat_id, text="Введите имя: ")
    bot.register_next_step_handler(sent, f6, bot, chat_id)
def f6(sent, bot, chat_id):

    name = sent.text
    name2 = name[::-1]
    name3 = name[2:6]
    bot.send_message(chat_id, text=name)
    bot.send_message(chat_id, text=name2)
    bot.send_message(chat_id, text=name3)


