from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

def telegram_bot_sendtext(bot_message):
    bot_token = '1250501014:AAHuPe2lgjcTIFm9Z53V5ver5X2oRuImH8g'
    bot_chatID = '589954195'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

session = requests.session()
url = 'https://service.berlin.de/dienstleistung/324873/standort/123613/'
data = urlopen(url)

soup = BeautifulSoup(data, 'html.parser')
products = soup.findAll('div', {'class': 'content-marginal-termin'})
for p in products:
    link = p.find('a')['href']

r = session.get(link)
parseData = BeautifulSoup(r.content,'html.parser')
findDates = parseData.findAll('td',{'class':'buchbar'})
findmonth = parseData.findAll('th',{'class':'month'})

for m in findmonth:
    month = m.text.strip()

for t in findDates:
    time = t.find('a')['href']
    date = t.text.strip()
    bot_msg = 'Available date for:\n Kita-Gutschein am Standort Jugendamt Treptow-Köpenick - Kitagutscheinverfahren und Hort\n'+date+month+'\nfor booking:\n'+url
    telegram_bot_sendtext(bot_msg)
   # print(date+month)


base_url = 'https://service.berlin.de'
completeUrl = base_url+time
chooseTime = session.get(completeUrl)
parseTime = BeautifulSoup(chooseTime.content,'html.parser')
showTime = parseTime.findAll('h1',{'class': 'title'})
session.close()


