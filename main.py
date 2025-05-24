# Aqui será rodado todo o projeto
import sqlite3
from livros import gerarRelatorioLivros
from paises import gerarRelatoriPaises

def main():
    gerarRelatoriPaises()
    gerarRelatorioLivros()

    visualizar = sqlite3.connect('livraria.db')
    cursor = visualizar.cursor()

    print("Visualizando tabelas de Livros: ")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    print("Visualizar dados da tabela Livros: ")
    cursor.execute("SELECT * FROM livros")
    for linha in cursor.fetchall():
        print(linha)

    visualizar.close()

    






    print("Relatório de países e livros gerados com êxito")