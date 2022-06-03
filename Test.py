import requests
from gettext import find
import bs4
import telebot
from telebot import types

import requests
from gettext import find
import bs4




def get_word():
    url = "https://calculator888.ru/random-generator/sluchaynoye-slovo"
    req_word = requests.get(url)
    soup = bs4.BeautifulSoup(req_word.text, "html.parser")
    word = soup.find('div', class_="blok_otvet").text

    return word.upper()

print(type(get_word()))