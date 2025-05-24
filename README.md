Você foi contratado por uma empresa de tecnologia para criar um sistema
automatizado capaz de extrair informações públicas sobre países e produtos de
interesse, armazená-las e apresentar os dados de forma clara e organizada.
Seu projeto deve contemplar duas tarefas complementares:
🔹 Parte 1 – Extração de Dados via API REST
Desenvolva um script que:
1. Solicite ao usuário o nome de 3 países;
2. Utilize a API pública https://restcountries.com/v3.1/name/{pais} para
buscar as seguintes informações:
- Nome comum e oficial
- Capital
- Continente
- Região e sub-região
- População
- Área
- Moeda (nome e símbolo)
- Idioma principal
- Fuso horário
- URL da bandeira
3. Armazene os dados em um banco SQLite chamado paises.db, em uma
tabela chamada 'paises'.
🔹 Parte 2 – Web Scraping com BeautifulSoup
Utilizando a biblioteca requests e BeautifulSoup, acesse o site
https://books.toscrape.com/ e colete os seguintes dados dos 10 primeiros
livros:
- Título
- Preço
- Avaliação (estrelas)
- Disponibilidade
Grave essas informações em uma tabela chamada 'livros' no banco de dados
livraria.db.

📄 Parte 3 – Relatório Final
Gere um relatório em Excel (openpyxl) ou Word (python-docx) contendo:
- Os dados dos países extraídos na Parte 1
- Os dados dos livros extraídos na Parte 2
- Nome do aluno e data de geração do relatório
- Dados organizados em formato de tabela clara
