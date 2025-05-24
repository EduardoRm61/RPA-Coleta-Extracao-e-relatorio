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
        dispoibilidade = livro.find('p', class_='instock availability').text

        estrela_tag = livro.find('p', class_='star-rating')
        estrela_text = estrela_tag.get('class')[1]

        mapa_estrela = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'FIve': 5
        }
        estrelas = mapa_estrela.get(estrela_text, 0)

        dados.append({
            'Título': titulo,
            'Preço': preco,
            'Disponibilidade': dispoibilidade,
            'Estrelas': estrelas
        })

        return dados