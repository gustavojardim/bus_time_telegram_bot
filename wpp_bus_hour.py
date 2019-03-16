from bs4  				import BeautifulSoup
from lxml 				import html

import os
import re 		as regex
import urllib3  as url3
import datetime as date
import telegram
	
REGEX_HOUR_MINUTE = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'	
				
TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

URL = 'http://www.realrodovias.com.br/?pagina=itinerariosPesquisa&detalhe=&linha=COMUNIDADE+02&tabela=horario&enviaConsulta=Consultar'

def get_current_time():
	current_time   = date.datetime.now()
	current_hour   = current_time.hour
	current_minute = current_time.minute
	return str(current_hour) + ":" + str(current_minute)
	
def get_all_leave_times():
	http 	 = url3.PoolManager()
	response = http.request('GET', URL)
	soup 	 = BeautifulSoup(response.data, features = "lxml")
	return soup(text=regex.compile(REGEX_HOUR_MINUTE))

def find_next_leave_time(all_leave_times):
	for hour in all_leave_times:
		if hour > get_current_time():
			print (hour)
			return hour

def send(msg, chat_id, token):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
	
def main():
	all_leave_times = get_all_leave_times()
	
	next_leave_time = find_next_leave_time(all_leave_times)
	
	send(next_leave_time, CHAT_ID, TOKEN) 
	
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()