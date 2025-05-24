import requests
import pandas as pd
from bs4 import BeautifulSoup

# - Título
# - Preço
# - Avaliação (estrelas)
# - Disponibilidade

url = 'https://books.toscrape.com/'
resposta = requests.get(url)
# htmm = teste.text
# print(htmm)

def extrairDados(url_base, url_pag):
    resposta = requests.get(url_base,url_pag)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    livros = soup.find_all('article', class_='product_pod')
    dados = []
    for livro in livros:
        titulo = livro.h3.a['title']
        preco = livro.find('p', class_='price_color').text
        