from bs4   	  	  import BeautifulSoup
from datetime 	  import datetime

import os
import re
import pickle
import telebot
import requests
				
TOKEN   = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(__name__)

def get_current_time_formatted() -> str:
	""" Returns a string formatted as 00:00 """
	current_time = datetime.now()
	current_hour = current_time.hour
	current_minute = current_time.minute
	return "{:02d}:{:02d}".format(current_hour, current_minute)
	
def get_all_departure_times(bus_line_url: str) -> list[str]:
	""" Extracts a list of strings that match the 00:00 format from the page HTML """
	page = requests.get(bus_line_url)
	soup = BeautifulSoup(page.content, features = "lxml")
	return soup(text=re.compile('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'))

def find_next_departure_time(all_departure_times: list) -> str:
	current_time = get_current_time_formatted()
	for hour in all_departure_times:
		if hour > current_time:
			return hour
	return all_departure_times[0]

def save_bus_lines(bus_lines: dict, chat_id: str):
    with open('data/{}_bus_lines.pkl'.format(chat_id), 'wb') as f:
        pickle.dump(bus_lines, f, pickle.HIGHEST_PROTOCOL)

def load_bus_lines(chat_id: str):
    with open('data/{}_bus_lines.pkl'.format(chat_id), 'rb') as f:
        return pickle.load(f)

@bot.route('/set_line ?(.*)')
def set_line(message: dict, input: str):
	chat_id = message.get('from').get('id')

	input_list = input.split()
	bus_line = input_list[1]
	url = input_list[0]

	try:
		user_bus_lines = load_bus_lines(chat_id=chat_id)
		user_bus_lines[bus_line] = url
		save_bus_lines(
			bus_lines=user_bus_lines,
			chat_id=chat_id
		)
	except Exception as e:
		save_bus_lines(
			bus_lines = {bus_line : url},
			chat_id = chat_id
		)

	message = "{} bus line saved".format(bus_line)

	bot.send_message(chat_id=chat_id, text=message)

@bot.route('/get ?(.*)')
def get(message: dict, bus_line: str):
	chat_id = message.get('from').get('id')

	try:
		user_bus_lines = load_bus_lines(chat_id=chat_id)
		selected_bus_line = user_bus_lines.get(bus_line)
		all_departure_times = get_all_departure_times(bus_line_url=selected_bus_line)
		next_departure_time = find_next_departure_time(all_departure_times)
		message = 'Your bus next departure time is {}'.format(next_departure_time)
	except FileNotFoundError:
		message = 'You have no lines registered'
	except requests.exceptions.MissingSchema:
		message = 'You have not set a bus line for the name {}'.format(bus_line)
	except Exception as e:
		message = 'Sorry, something unexpected happened in my program'

	bot.send_message(chat_id=chat_id, text=message)
	
if __name__ == '__main__':
	bot.config['api_key'] = TOKEN
	bot.poll(debug=True)