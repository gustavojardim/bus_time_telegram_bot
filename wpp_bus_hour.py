from lxml import html
from bs4  import BeautifulSoup

import re
import urllib2  as url2
import datetime as date

current_time   = date.datetime.now()
current_hour   = current_time.hour
current_minute = current_time.minute
current_hh_mm  = str(current_hour) + ":" + str(current_minute)

url = 'http://www.realrodovias.com.br/?pagina=itinerariosPesquisa&detalhe=&linha=COMUNIDADE+02&tabela=horario&enviaConsulta=Consultar'

regexHourMinute = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'

html = url2.urlopen(url).read()

soup = BeautifulSoup(html, features = "lxml")

test = soup.find_all(":")

for hour in soup(text=re.compile(regexHourMinute)):
    if hour >= current_hh_mm:
		print hour
		break