import requests
dados_api = []

def requisicao(pais):
    url = "https://restcountries.com/v3.1/name/{pais}"
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