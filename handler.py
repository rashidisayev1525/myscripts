import ssl
import sys

import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintoshf  Mac OS X 10_12_6) AppeWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Connection': 'keep-alive'
}
bot = telebot.TeleBot('')
keyboard1 = types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Anmeldung einer Wohnung', 'Ausländerbehörde')


def return_month(hereFindMonth):
    for m in hereFindMonth:
        monthNew = m.text.strip()
        return monthNew


@bot.message_handler(commands=['start'])
def start_message(message):
    welcome = 'Welcome to terminator ' + message.from_user.first_name + '!\nPlease choose service in Burgeramt:'
    bot.send_message(message.chat.id, welcome,
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global month, findDates, findMonth
    if message.text.lower() == 'anmeldung einer wohnung':
        bot.send_message(message.chat.id, 'Wait please searching...')
        session = requests.session()
        url = 'https://service.berlin.de/dienstleistung/120686/'

        data = requests.get(url, headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        products = soup.findAll('div', {'class': 'zmstermin-multi inner'})
        for p in products:
            link = p.find('a')['href']
            r = session.get(link)
        parseData = BeautifulSoup(r.text, 'html.parser')
        findDates = parseData.findAll('td', {'class': 'buchbar'})
        # findMonth = parseData.findAll('th', {'class': 'month'})
        if len(findDates) == 0:
            sorryMsg = 'Sorry  ' + message.from_user.first_name + '!\n But there are no available dates.\n It is also happens sometimes when something wrong with web page'
            bot.send_message(message.chat.id, sorryMsg)
            sys.exit()
        for m in parseData.findAll('th', {'class': 'month'}):
            month = m.text.strip()
            break
        # fuckingMonth = return_month(findMonth)
        for t in findDates:
            date = t.text.strip()
            msgToBeSend = date + " " + month + "\n"
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Book now!", url=url)
            keyboard.add(url_button)
            bot.send_message(message.chat.id, msgToBeSend, reply_markup=keyboard)
        #  print(fuckingMonth)


    elif message.text.lower() == 'ausländerbehörde':
        bot.send_message(message.chat.id, 'Under construction...')

    else:
        bot.send_message(message.chat.id, "Ops..Contact rashidisayev@gmail.com")


bot.polling(True, timeout=300)
bot.infinity_polling()