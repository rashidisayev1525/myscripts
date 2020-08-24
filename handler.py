import sys
import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintoshf  Mac OS X 10_12_6) AppeWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}
bot = telebot.TeleBot('')
chat_id = ''
keyboard1 = types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Anmeldung', 'KitaGutschein')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Welcome to terminator!Please choose service in Burgeramt:)',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'anmeldung':
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
            findmonth = parseData.findAll('th', {'class': 'month'})
        if len(findDates) == 0:
            bot.send_message(chat_id, "No available dates or smth. wrong with website!")
            sys.exit()

        for m in findmonth:
            month = m.text.strip()

        for t in findDates:
            timeLink = t.find('a')['href']
            getTime = 'https://service.berlin.de' + timeLink
            params = {
                'termin': 1,  # Not sure if necessary
                'dienstleisterlist': ',', '123613'
                                          'anliegen[]': '324873',
        }
            timeList = requests.get(getTime, params=params, headers=headers)
            semiFinalTime = BeautifulSoup(timeList.text, 'html.parser')
            finalTime = semiFinalTime.findAll('th', {'class': 'buchbar'})
            date = t.text.strip()
            msgToBeSend = date+month+url+finalTime
            bot.send_message(chat_id,msgToBeSend)

    elif message.text.lower() == 'kitagutschein':
        bot.send_message(message.chat.id, 'Wait please searching...')
    else:
        bot.send_message(message.chat.id, "Alinmadi")


bot.polling()

# ALL_BUERGERAMTS = (
#     122210, 122217, 327316, 122219, 327312, 122227, 122231, 327346, 122243, 327348, 122252, 329742, 122260, 329745,
#     122262, 329748, 122254, 329751, 122271, 327278, 122273, 122277, 327276, 122280, 327294, 122282, 122284, 122291,
#     327270, 122285, 327266, 122286, 327264, 122296, 327268, 150230, 122301, 122297, 122294, 122312, 329763, 122304,
#     327330, 122311, 327334, 122309, 327332, 122281, 122279, 122276, 122274, 122267, 122246, 327318, 122251, 327320,
#     122257, 122208, 122226
# )

# session = requests.session()
#
# # url = 'https://service.berlin.de/dienstleistung/324873/standort/123613/'
# # data = urlopen(url)
# url = 'https://service.berlin.de/dienstleistung/120686/'
# data = requests.get(url, headers)
# soup = BeautifulSoup(data.text, 'html.parser')
# products = soup.findAll('div', {'class': 'zmstermin-multi inner'})
#
# for p in products:
#     link = p.find('a')['href']
#
#     r = session.get(link)
#
#
# parseData = BeautifulSoup(r.text, 'html.parser')
# findDates = parseData.findAll('td', {'class': 'buchbar'})
# findmonth = parseData.findAll('th', {'class': 'month'})
#
#
#
# # if len(findDates) == 0:
# #     # telegram_bot_sendtext('No available dates')
# #     bot.send_message(chat_id, "No available dates!")
# #     sys.exit()
# #
# for m in findmonth:
#      month = m.text.strip()
# print(month)
# #
# for t in findDates:
#      dates = t.text.strip()
#      print(dates)


    # print(timeLink)
#     getTime = 'https://service.berlin.de' + timeLink
#     params = {
#         'termin': 1,  # Not sure if necessary
#         'dienstleisterlist': ',', '123613'
#                                  'anliegen[]': '324873',
#    }
#     timeList = requests.get(getTime, params=params, headers=headers)
#     semiFinalTime = BeautifulSoup(timeList.text, 'html.parser')
#     finalTime = semiFinalTime.findAll('th', {'class': 'buchbar'})
#     date = t.text.stip()