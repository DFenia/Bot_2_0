from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from test_dbase import DBase
API_TELEGRAM = '5306102005:AAHUvZCTAXSj3F8TCTmGbR5xFUr_J2Tdr34'
updater = Updater(API_TELEGRAM)
dispatcher = updater.dispatcher

dbase = DBase()

def about():
    return "Команды поддерживаемые ботом: \n" \
           "/table <название таблицы>"


# функция обработки команды '/start'
def func_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Какую таблицу вывести? По шаблону /table (таблица)")


# функция обработки текстовых сообщений
def func_text(update, context):
    text_out = 'Информация: \n' + about()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)


# функция обработки команды '/table'
def func_table(update, context):
    if context.args:
        text_reply = dbase.get_navigator_data(context.args[0])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_reply)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Таблица не указана!')


# функция обработки не распознанных команд
def func_unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Такой команды нет!")


# обработчик команды '/start'
start_handler = CommandHandler('start', func_start)
dispatcher.add_handler(start_handler)

# обработчик текстовых сообщений
text_handler = MessageHandler(Filters.text & (~Filters.command), func_text)
dispatcher.add_handler(text_handler)

# обработчик команды '/table'
navigators_handler = CommandHandler('table', func_table)
dispatcher.add_handler(navigators_handler)

# обработчик не распознанных команд
unknown_handler = MessageHandler(Filters.command, func_unknown)
dispatcher.add_handler(unknown_handler)

# запуск прослушивания сообщений
updater.start_polling()
# обработчик нажатия Ctrl+C
updater.idle()
