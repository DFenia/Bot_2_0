import json
from gettext import find
from io import BytesIO

import bs4
import telebot
from telebot import types
import requests

import DZ
import menuBot
from menuBot import Menu, Users
import random




bot = telebot.TeleBot('5306102005:AAHUvZCTAXSj3F8TCTmGbR5xFUr_J2Tdr34')


#команды

@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEEkq9iaT_FQTC2XiYqEMXDaZicoSlafQACmxIAAkesoUshgGwRAAF2MPYkBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я ProstoBot! Выберите действие:"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


#получение

@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)


@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)

@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)

@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)

@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)

@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")

@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)

    from Weather import WeatherFromPyOWN
    pyOWN = WeatherFromPyOWN()
    bot.send_message(chat_id, pyOWN.getWeatherAtCoords(location.latitude, location.longitude))
    bot.send_message(chat_id, pyOWN.getWeatherForecastAtCoords(location.latitude, location.longitude))

@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu != None:
        if subMenu.name == "Камень, ножницы, бумага, ящерица, Спок":
            gameRSPLS.info_RSPLS(bot, chat_id)
        elif subMenu.name == "Виселица":
            gameW = botGames.newGame(chat_id, botGames.Word_game(bot, chat_id))
            gameW.word_start()
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        # ======================================= Развлечения
        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")
        elif ms_text == "Прислать котика":
            bot.send_photo(chat_id, photo=get_catURL(), caption="Вот тебе котик!")
        elif ms_text == "Человек и email":
            get_personURL(chat_id)
        elif ms_text == "Прислать анекдот":
            bot.send_message(chat_id, text=get_anekdot())
        elif ms_text == "Создать пароль":
            bot.send_message(chat_id, text=get_password())
        elif ms_text == "Прислать игру":
            send_game(chat_id)



        # ======================================= модуль ДЗ
        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4/5":
            DZ.dz45(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)
        # ======================================= случайный текст
    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")



# ----------------------------------------------------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call): # передать параметры
    pass




# ----------------------------------------------------------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.cur_menu(not Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)
    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return True
    else:
        return False

def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: DFenia")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/DFenia")
    markup.add(btn1)
    img = open('кот1.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

def send_game(chat_id):

    url = "https://store.steampowered.com/explore/random/"
    req_game = requests.get(url)
    soup = bs4.BeautifulSoup(req_game.text, "html.parser")

    prise = ''
    prise = soup.find('div', class_="game_purchase_price price")
    if prise == None:
        prise = ' '
    else:
        prise = soup.find('div', class_="game_purchase_price price").getText().strip()
    developer = soup.find('div', id="developers_list").getText().strip()

    info_list = []
    info = soup.find('div', id="genresAndManufacturer").getText()
    info_list=list(info)

#ссылка
    steam = soup.find('div', class_="share share_dialog").getText()
    steam_url = str(steam)
    steam_url = steam_url[29:]

#вытащить картинку
    picture_list = []
    images = soup.find_all('img')
    for image in images:
        src = image.get("src")
        picture_list.append(src)
    picture=picture_list[6]

#меняем текст
    info_list = info.split()
    i = info_list.index("Title:")
    info_list[i] = "\nНазвание: "
    i = info_list.index("Genre:")
    info_list[i] = "\nЖанр: "
    i = info_list.index("Developer:")
    info_list[i] = "\nРазработчик: "
    i = info_list.index("Publisher:")
    info_list[i] = "\nИздатель: "
    i = info_list.index("Release")
    info_list[i] = "\nДата"
    i = info_list.index("Date:")
    info_list[i] = "выхода:"
    info_list.append("\nЦена: ")
    info_list.append(prise)
#отзывы
    rev = soup.find('div', class_="summary_section").getText()
    rev_list = str(rev)
    rev_list = rev_list[18:]
    rev_list = "\nОтзывы:  " + rev_list

    info_list.append(rev_list)




    info = " ".join(info_list)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Ссылка на игру", url=steam_url)
    markup.add(btn1)
    bot.send_photo(chat_id, photo=picture, caption=info, reply_markup=markup)


def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]


def get_password():
    array_facts = []
    req_fact = requests.get('https://randstuff.ru/password/')
    soup = bs4.BeautifulSoup(req_fact.text, "html.parser")
    result_find = soup.select('.cur')
    for result in result_find:
        array_facts.append(result.getText().strip())
    return array_facts[0]


def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
    return url

def get_catURL():
    url = ""
    req = requests.get("https://api.thecatapi.com/v1/images/search")
    if req.status_code == 200:
        r_json = req.json()
        url = r_json[0]["url"]
    return url

def get_personURL(chat_id):
    """url = ""
    req = requests.get('https://api.thecatapi.com/v1/images/search')
    r_json = json.loads(req.text)

    url = r_json['url']
    return url"""
    url = requests.get("https://jsonplaceholder.typicode.com/users")
    text = url.text

    data = json.loads(text)
    people = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    r_people = random.choice(people)

    user = data[int(r_people)]
    email = user['email']
    user_info = f"{user['name']}\n" + email
    bot.send_message(chat_id, text=user_info)



bot.polling(none_stop=True, interval=0)
print()
