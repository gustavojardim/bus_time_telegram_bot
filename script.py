from bs4   	  	  import BeautifulSoup
from flask 	      import Flask, Response
from datetime 	  import datetime

import os
import re
import telegram
import requests
				
TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

URL = 'http://www.realrodovias.com.br/?pagina=itinerariosPesquisa&detalhe=&linha=COMUNIDADE+02&tabela=horario&enviaConsulta=Consultar'

app = Flask(__name__)

def get_current_time_formatted() -> str:
	""" Returns a string formatted as 00:00 """
	current_time = datetime.now()
	current_hour = current_time.hour
	current_minute = current_time.minute
	return "{:02d}:{:02d}".format(current_hour, current_minute)
	
def get_all_leave_times() -> list[str]:
	""" Extracts a list of strings that match the 00:00 format from the page HTML """
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, features = "lxml")
	return soup(text=re.compile('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'))

def find_next_leave_time(all_leave_times: list) -> str:
	current_time = get_current_time_formatted()
	print(current_time)
	for hour in all_leave_times:
		if hour > current_time:
			return hour
	return all_leave_times[0]

def send_message(msg: str, chat_id: str, token: str):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)

@app.route('/')
def get_next_leave_time():
	all_leave_times = get_all_leave_times()
	
	next_leave_time = find_next_leave_time(all_leave_times)
	
	send_message(next_leave_time, CHAT_ID, TOKEN)
	
	return Response(
		response = 'Next leave time sent to chat id {}'.format(CHAT_ID),
		status = 200
	)
	
if __name__ == '__main__':
	app.run(debug=True)