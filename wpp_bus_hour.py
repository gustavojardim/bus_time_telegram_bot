from lxml import html
import requests as req

url = 'http://www.realrodovias.com.br/?pagina=itinerariosPesquisa&detalhe=&linha=COMUNIDADE+02&tabela=horario&enviaConsulta=Consultar'

page = req.get(url)

html_tree = html.fromstring(page.content)

hours = html_tree.xpath('//div[@id="horariosInt"]/text()')

print hours


' Pseudo code
def getAllHours(html):
	loop html as str:
		if str[2] == ':':
			add in hours
	return hours