import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintoshf  Mac OS X 10_12_6) AppeWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Connection': 'keep-alive'
}
bot = telebot.TeleBot('1132128114:AAHv1AWnTqtX4SHiUtcVKIIw3xc22-KVvks')
keyboard1 = types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Get info')


@bot.message_handler(commands=['start'])
def start_message(message):
    welcome = 'Welcome to COVID19 travel restrictions ' + message.from_user.first_name + '!\nThis bot will give you info abot red zones where travel is not allowed. \n Source: https://www.rki.de/'
    bot.send_message(message.chat.id, welcome,
                     reply_markup=keyboard1)

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        global msgToBeSend, stand
        if message.text.lower() == 'get info':
            bot.send_message(message.chat.id, 'Wait please ...')
            url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html'

            data = requests.get(url, headers)
            soup = BeautifulSoup(data.text, 'html.parser')
            findDates = soup.findAll('div', {'class': 'subheadline'})
        for i in findDates:
            stand = i.text.strip()

        for a in soup.find_all('a', class_="InternalLink download"):
            msgToBeSend = 'https://www.rki.de/' + a['href']
        text = 'Your link is ready please download pdf and find your info!(Last update)' + stand
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Download PDF!", url=msgToBeSend)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, text,
                         reply_markup=keyboard)


bot.infinity_polling()
