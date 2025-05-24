import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
from openpyxl import load_workbook
from datetime import datetime


url = 'https://books.toscrape.com/'
dados = []

def gerarRelatorioLivros(titulo, preco, disponibilidade, estrela):
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

    dados.append({
        'Título':titulo,
        'Preço': preco,
        'Disponibilidade': disponibilidade,
        'Estrelas': estrela
    })


    df_livros = pd.DataFrame(dados)

    #%Y = ano com 4 dígitos. %m = mês com dois dígitos...
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    df_info = pd.DataFrame([["Este relatório foi gerado ", agora]], columns=["Informação", "Data"])

    df_final = pd.concat([df_info, pd.DataFrame([[]]), df_livros], ignore_index=True)

    # Junção
    df_final.to_excel('livros.xlsx', index=False, engine='openpyxl')

def extrairDados(url_base):
    resposta = requests.get(url_base)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    livros = soup.find_all('article', class_='product_pod')
    
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

        gerarRelatorioLivros(titulo, preco, disponibilidade, estrelas)



    
# extrairDados(url)
