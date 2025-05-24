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
                   preco TEXT,
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
        preco = livro.find('p', class_='price_color').text
        disponibilidade = livro.find('p', class_='instock availability').text.strip()

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


    
extrairDados(url)

visualizar = sqlite3.connect('livraria.db')
cursor = visualizar.cursor()

print("Visualizando tabelas existentes: ")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

print("Visualizar dados da tabela: ")
cursor.execute("SELECT * FROM livros")
for linha in cursor.fetchall():
    print(linha)

visualizar.close()