from lxml import html
from bs4  import BeautifulSoup

import re 		as regex
import urllib2  as url2
import datetime as date
import telegram

def find_next_leave_time(all_leave_times):
	for hour in all_leave_times:
		if hour >= current_hh_mm:
			print hour
			return hour

def send(msg, chat_id, token):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
			
my_token   = 'telegram bot token'
my_chat_id = 'telegram chat id'

result = None

regexHourMinute = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'

url = 'http://www.realrodovias.com.br/?pagina=itinerariosPesquisa&detalhe=&linha=COMUNIDADE+02&tabela=horario&enviaConsulta=Consultar'

current_time   = date.datetime.now()
current_hour   = current_time.hour
current_minute = current_time.minute
current_hh_mm  = str(current_hour) + ":" + str(current_minute)

html = url2.urlopen(url).read()

soup = BeautifulSoup(html, features = "lxml")

all_leave_times = soup(text=regex.compile(regexHourMinute))

next_leave_time = find_next_leave_time(all_leave_times)

send(next_leave_time, my_chat_id, my_token) 