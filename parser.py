import json
import lxml
import requests
from bs4 import BeautifulSoup
import time
from telebot import TeleBot
from telebot import types
import emoji

bot = TeleBot('Token')

# Функция для возврата в главное меню
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width = 1)
    item_1 = types.InlineKeyboardButton('◀Фондовый и срочный рынок', callback_data = 'stock_market')
    item_2 = types.InlineKeyboardButton('◀Выставить сигналы', callback_data = 'signal')
    item_3 = types.InlineKeyboardButton('◀О нас', callback_data = 'about')
    markup.add(item_1, item_2, item_3)
    return markup

# Запускаем бота по кнопке "satrt" и создаем главное меню
@bot.message_handler(commands = ['start'])
def start(message):

    markup = types.InlineKeyboardMarkup(row_width = 1)
    item_1 = types.InlineKeyboardButton('◀Фондовый и срочный рынок', callback_data = 'stock_market')
    item_2 = types.InlineKeyboardButton('◀Выставить сигналы', callback_data = 'signal')
    item_3 = types.InlineKeyboardButton('◀О нас', callback_data = 'about')
    markup.add(item_1, item_2, item_3)

    bot.send_message(message.chat.id, '<b>Главное меню</b>', parse_mode='HTML', reply_markup=markup)

# Подключаем команды к кнопкам
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'stock_market':
            bot.send_message(call.message.chat.id, 'Фондовый и срочный рынок\n\n'
                                                   'Настроенные инструменты:\n'
                                                   '⚫Акции Московской биржи;\n'
                                                   '⚫Фьючерсы Московской биржи;\n\n'
                                                   'Подключенные биржи:\n'
                                                   '🇷🇺Московская биржа\n\n'
                                                   '<s>🇺🇸Американские биржи</s>\n\n' +
                             '<i>По техническим причинам\nинструменты Американского рынка временно недоступны.</i>',
                             parse_mode='HTML')

            markup_price = types.InlineKeyboardMarkup(row_width=1)
            item_1 = types.InlineKeyboardButton('◀Стоимость акций', callback_data='share_price')
            item_2 = types.InlineKeyboardButton('◀Главное меню', callback_data='main_menu')
            markup_price.add(item_1, item_2)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup_price)

        elif call.data == 'signal':
            bot.send_message(call.message.chat.id, 'loading')
        elif call.data == 'about':
            bot.send_message(call.message.chat.id, '    Мы являемся растущим проектом, который создает вспомогательный инструмент'\
                                                   ' для инвестора и трейдера, позволяющий производить анализ и выбор инвестиций')
        elif call.data == 'main_menu':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Главное меню', reply_markup=main_menu())
        elif call.data == 'share_price':
            tiker = bot.send_message(call.message.chat.id, 'Введите тикер')

            def search_tiker(message):
                bot.register_next_step_handler(tiker, search)

# Делаем активным строчку ввода
@bot.message_handler(content_types=['text'])
def search(message):
    bot.send_message(message.chat.id, 'Анализируем стоимость')
    url = f'https://www.tinkoff.ru/invest/recommendations/?query=' + message.text
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    full_page = requests.get(url, headers=headers)
    soup = (BeautifulSoup(full_page.text, 'lxml'))
    data = soup.findAll('span', {'class': 'Money-module__money_p_VHJ'})
    data = data[0].text[:6].replace('Â', '').replace(' ', '').replace(',', '.')
    currency = f'Стоимость акции: {float(data)}₽'
    bot.send_message(message.chat.id, currency)

bot.polling(none_stop=True)


