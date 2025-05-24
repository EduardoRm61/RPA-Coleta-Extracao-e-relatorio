import requests
import sqlite3
import pandas as pd
dados_api = []



def relatorioDados(nome, nome_ofc, capital, continente, regiao, sub_reg, populacao, area, idioma, moeda_nome, moeda_simb, fuso, url_bandeira):
    conexao = sqlite3.connect("paises.db") #Abrimos ou criamos um arquivo com extensão ao BD chamado paises. Também criamos um obj chamado extensão
    cursor = conexao.cursor() # Criamos um cursor, um objeto intermediario para executar comandos SQL dentro do BD. Com ele podemos fazer CREAT TABLE, INSERT INT, SELECT

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paises(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                nome_oficial TEXT,
                capital TEXT,
                continente TEXT,
                regiao TEXT,
                sub_regiao TEXT,
                populacao INTEGER,
                area REAL,
                idioma TEXT,
                moeda_nome TEXT,
                moeda_simbolo TEXT,
                fuso TEXT,
                url_bandeira TEXT
            )
        ''')
    
    cursor.execute('''
        INSERT INTO paises(
                   nome, nome_oficial, capital, continente, regiao, sub_regiao,
                   populacao, area, idioma, moeda_nome, moeda_simbolo,fuso, url_bandeira
                   ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    nome, nome_ofc, capital, continente, regiao, sub_reg,
                    populacao, area, idioma, moeda_nome, moeda_simb, fuso, url_bandeira
                ))
    conexao.commit() #Estamos deixando registrado nossa ação no banco de dados
    conexao.close()

    print(f"Dados do país {nome} armazenados.")

def solicitaDados(pais):
    url = f"https://restcountries.com/v3.1/name/{pais}"
    resposta = requests.get(url)

    if resposta.status_code!=200:
        print({"requisição inválida":"Erro ao buscar os dados"})
        return
    
    dados = resposta.json()
    if not dados:
        print({f"Requisição inválida":"Erro ao buscar nome do país{pais}"})
        return
    
    pais = dados[0]

    try:
        nome = pais['name']['common'] # esta contido dentro de um dicionário, sendo assim acessamos pela chave que retorna o valor
        nome_ofc = pais['name']['official']
        capital = pais.get('capital', ['Sem capital'])[0] # Só necessário caso o campo esteja vazio. E capital nos retorna uma lista, por essa razão o zero
        # "capital": ["Brasília"]
        continente = pais.get('continents',['Desconhecido'])[0]
        regiao =  pais['region']
        sub_reg = pais['subregion']
        populacao = pais['population'] 
        area = pais['area']
        lingua = pais.get('languages',{}) # Pegamos o dicionário ou lista completa com a chave languages
        #Aqui está tranformando em lista o valor de languages e pegando exatamente o índice 0 que representa o idioma principal,
        #depois checa se a variável está vazia, se sim ela passa a valer sem idioma
        idioma = list(lingua.values())[0] if lingua else 'Sem idioma' 
        fuso = pais['timezones'][0]
        url_bandeira = pais.get('flags',{}).get('png','Sem URL') # Entramos no dicionário com nome flag me pais, caso não exista devolvemos {}. depois acessamos a chave png

        currencies = pais.get('currencies',{}) # Estamos pegando o dicionário completo de currencies, caso não exista o deixamos vazio.
        if currencies:
            moeda_info = list(currencies.values())[0] # Estamos acessando as informações de moesda, tranformando em lista por assim será fácil pegar o indice 0 que representa a moeda principa
            moeda_nome = moeda_info.get('name', 'Desconhecido') # Dentro de moeda_info pegamos o nome dela
            moeda_simb = moeda_info.get('symbol', 'N/A')

        

        relatorioDados(nome, nome_ofc, capital, continente, regiao,
                        sub_reg, populacao, area, idioma, moeda_nome,
                        moeda_simb, fuso, url_bandeira)
    except Exception as e:
        print({"Erro ao processar os dados":str(e)})




pais = input("Digite o nome do País em Inglês: ")
solicitaDados(pais)

for i in range(2):
    pais = input("Digite o nome de outro País, também em Inglês: ")
    solicitaDados(pais)

visualizar = sqlite3.connect('paises.db')
cursor = visualizar.cursor()

print("Tabelas existentes: ")
cursor.execute('SELECT * FROM  paises')
for linha in cursor.fetchall():
    print(linha)


print("Dados existentes nas tabelas: ")
cursor.execute("SELECT name FROM sqlite_master WHERE type ='table';")
print(cursor.fetchall())

visualizar.close()