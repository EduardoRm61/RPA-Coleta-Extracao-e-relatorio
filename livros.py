import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3

url = 'https://books.toscrape.com/'

def registrarDados(titulo, preco, disponibilidade, estrela):
    conexao = sqlite3.connect('livraria.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT,
                   preco REAL,
                   disponibilidade TEXT,
                   estrela INTEGER
                   )
            ''')
    cursor.execute('''
        INSERT INTO livros(
                   titulo, preco,
                   disponibilidade, estrela
                   ) VALUES (?,?,?,?)
                   ''',(
                       titulo, preco, disponibilidade, estrela
                   ))
    conexao.commit()
    conexao.close()

def extrairDados(url_base):
    resposta = requests.get(url_base)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    livros = soup.find_all('article', class_='product_pod')
    dados = []
    for livro in livros[:10]:
        titulo = livro.h3.a['title']
        preco = float(livro.find('p', class_='price_color').text.strip()[1:])
        disponibilidade = livro.find('p', class_='instock availability').text

        estrela_tag = livro.find('p', class_='star-rating')
        estrela_text = estrela_tag.get('class')[1]

        mapa_estrela = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        estrelas = mapa_estrela.get(estrela_text, 0)

        registrarDados(titulo, preco, disponibilidade, estrelas)
        print(f'Dados de livros inseridos com êxito!')

    
extrairDados(url)