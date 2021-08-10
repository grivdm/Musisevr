from DB import db_table_val, db_table_upd, db_select
from boo import get_output
import telebot
import cred

bot = telebot.TeleBot(TELEGRAM BOT TOKEN)


@bot.message_handler(commands=['start'])
def welcome_start(message):
    us_id = message.from_user.id
    try:
        if db_select(us_id) == 1:
            bot.send_message(message.from_user.id, f'Приветствую тебя, {message.from_user.first_name}. \n'
                                                   '\nТут всё просто, напиши в чате:'
                                                   '\nИмя исполнителя - Название песни '
                                                   '\nили \nИмя исполнителя.'
                                                   '\nМожешь скинуть ссылку на исполнителя или песню.'
                                                   '\nРаботаю с сервисами  Spotify и YaMusic. '
                                                   '\nВперед!')

        if db_select(us_id) == 2:
            bot.send_message(message.from_user.id, f'Вітаю тебе, {message.from_user.first_name}. \n'
                                                   '\nТут все легко, напиши в чаті:'
                                                   '\nІм\'я виконавця - Назва пісні '
                                                   '\nабо \nІм\'я виконавця.'
                                                   '\nМожеш переслати лінк на виконавця або пісню.'
                                                   '\nПрацюю з сервісами Spotify та YaMusic.')

        if db_select(us_id) == 3:
            bot.send_message(message.from_user.id, f'Hi, {message.from_user.first_name}. \n'
                                                   '\nType to the chat:'
                                                   '\n Artist\'s name - Name of song '
                                                   '\nor \nArtist\'s name'
                                                   '\nYou can also send any song or artist link (Spotify or Yandex.Music)')
    except IndexError:
        bot.send_message(message.from_user.id, f'Приветствую тебя, {message.from_user.first_name}. \n'
                                               '\nТут всё просто, напиши в чате:'
                                               '\nИмя исполнителя - Название песни '
                                               '\nили \nИмя исполнителя.'
                                               '\nМожешь скинуть ссылку на исполнителя или песню.'
                                               '\nРаботаю с сервисами  Spotify и YaMusic. '
                                               '\nВперед!')
        db_table_val(user_id=us_id, user_lng=1)


@bot.message_handler(commands=['language'])
def lng(message):
    us_id = message.from_user.id
    key = telebot.types.InlineKeyboardMarkup()
    lng_ru_button = telebot.types.InlineKeyboardButton(text='Русский 🇷🇺', callback_data="Ru")
    lng_ua_button = telebot.types.InlineKeyboardButton(text='Українська 🇺🇦', callback_data="Ua")
    lng_en_button = telebot.types.InlineKeyboardButton(text='English 🇬🇧', callback_data="En")
    key.add(lng_ru_button, lng_ua_button, lng_en_button)
    if db_select(us_id) == 1:
        bot.send_message(message.chat.id, 'Выбери язык:', reply_markup=key)
    if db_select(us_id) == 2:
        bot.send_message(message.chat.id, 'Вибери мову:', reply_markup=key)
    if db_select(us_id) == 3:
        bot.send_message(message.chat.id, 'Choose your language:', reply_markup=key)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'Ru':
        lng_num = int(1)
        bot.send_message(c.message.chat.id, 'Вы выбрали русский')
    if c.data == 'Ua':
        lng_num = int(2)
        bot.send_message(c.message.chat.id, 'Ви обрали українську мову')
    if c.data == 'En':
        lng_num = int(3)
        bot.send_message(c.message.chat.id, 'You have chosen english')
    us_id = c.message.chat.id
    db_table_upd(user_id=us_id, user_lng=lng_num)


@bot.message_handler(content_types=["text"])
def get_msg(message):
    us_id = message.from_user.id
    spotyRep, yandRep, ytmRep = get_output(message.text)
    markup = telebot.types.InlineKeyboardMarkup()
    try:
        if spotyRep is not None:
            markup.add(telebot.types.InlineKeyboardButton(text='spotify', url=spotyRep['urls']['spotify']))
        if yandRep is not None:
            markup.add(telebot.types.InlineKeyboardButton(text='yandex', url=yandRep))
        if db_select(us_id) == 1:
            bot.send_message(message.chat.id, 'Смотри, что удалось найти: \n' + ytmRep, reply_markup=markup)
        if db_select(us_id) == 2:
            bot.send_message(message.chat.id, 'Дивись, що вдалося знайти: \n' + ytmRep, reply_markup=markup)
        if db_select(us_id) == 3:
            bot.send_message(message.chat.id, 'Here is what i found: \n' + ytmRep, reply_markup=markup)
    except:
        if db_select(us_id) == 1:
            bot.send_message(message.chat.id, 'К сожалению, ничего не найдено..'
                                              '\nПопробуй ещё раз или почитай /start')
        if db_select(us_id) == 2:
            bot.send_message(message.chat.id, 'На жаль, нічого не знайдено..'
                                              '\nCпробуй ще раз або почитай /start')
        if db_select(us_id) == 3:
            bot.send_message(message.chat.id, 'Unfortunately, nothing is found..'
                                              '\nTry again or read /start')


if __name__ == '__main__':
    bot.infinity_polling()
