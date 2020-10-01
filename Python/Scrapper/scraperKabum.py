import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Cria ou atualiza o documento de metadados com os nomes dos produtos sendo observados passados atravez da lista
def metadados(lista):
    meta_json = {}
    # Verifica se existe o arquivo
    if os.path.exists("metadados.dat"):
        # Se existir, abre e carrega as informações
        with open("metadados.dat","r") as myfile:
            meta_json = json.load(myfile)
    else:
        # Caso não exista, cria um modelo vazio da estrutura do arquivo (em json)
        meta_json = {
            'nomes': [],
        }

    # Agora com as informações carregadas(seja vazio ou com os dados do arquivo)
    # Para todos os produtos passados na lista de produtos
    for produto in lista:
        s = produto["nome"]
        # Formata ele para um nome compativel com a formatação para arquivos
        name = "".join(x for x in s if x.isalnum())
        # Se o nome já não estiver presente na lista, adiciona o nome a lista
        if not(name in meta_json['nomes']):
            meta_json['nomes'].append(name)

    # Abre o arquivo novamente, agora com a garantia da existencia ou criando se
    # necessário,  e insere as informações (atualizadas ou geradas agora)
    with open("metadados.dat","w+") as myfile:
        json.dump(meta_json,myfile)


# Recebe os dados de um produto especifico e armazena eles no arquivo dele 
# existente ou gera o arquivo para iniciar o armazenamento
def storeData(produto):
    prod_json = {}
    s = produto["nome"]
    # Formata o nome para a formatação de nome de arquivo
    path = "".join(x for x in s if x.isalnum())
    # Recebe a data atual do momento da medição de preço
    date = datetime.today().strftime('%Y-%m-%d')
    price =  produto["preco"]
    
    # Caso o arquivo já exista, abre e carrega as informações passadas
    if os.path.exists("produtos\\"+path):
        with open("produtos\\"+path,"r") as myfile:
            prod_json = json.load(myfile)
    # Se não existir, cria o produto com apenas as informações atuais
    else:
        prod_json = {
            'nome': s,
            'safe_file_name':path,
            'preco_data': [],
            'tracking': False # flag para caso tenha interesse em exibir em grafico
            }

    # Recebe o preço e a data da medição atual e adiciona as informações antigas, caso tenha
    temp_arr = [price,date]
    prod_json['preco_data'].append(temp_arr)

    with open("produtos\\"+path,"w+") as myfile:
            json.dump(prod_json,myfile)



# Tendo um url de uma pagina de *´PESQUISA DE PRODUTO* da Kabum, recebe as
# informações de todos os resultados da pesquisa
def getInfoFromKabum(url):
    # Faz a requisição do site
    req = requests.get(url)

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        conteudo = req.content

    # Informa o html para o interpretador
    soup = BeautifulSoup(conteudo, 'html.parser')

    # Procura no html a tag=script
    scripts = soup.find_all(type="text/javascript")

    # Procura em todas as todos os scripts a string "listagemDados"
    data = re.findall(r'\bconst\s+listagemDados\s*=\s*(\[[^\]]*\])', scripts[9].string, re.DOTALL)

    # Carrega o json da variável
    lista = json.loads(data[0])
    print("inserindo no arquivo metadados a lista de produtos")
    metadados(lista)
    print("armazenando as informações dos produtos")
    for produto in lista:
        storeData(produto)


#getInfoFromKabum('https://www.kabum.com.br/hardware/ssd-2-5?pagina=1&ordem=5&limite=30&prime=false&marcas=[]&tipo_produto=[]&filtro=[]')
getInfoFromKabum('https://www.kabum.com.br/hardware/ssd-2-5?pagina=1&ordem=5&limite=100&prime=false&marcas=[%2282%22,%2212%22,%2250%22,%226%22,%221%22,%2236%22]&tipo_produto=[]&filtro=[[%221660%22]]')
getInfoFromKabum('https://www.kabum.com.br/hardware/memoria-ram?pagina=1&ordem=5&limite=30&prime=false&marcas=[]&tipo_produto=[]&filtro=[[%221534%22],[%221544%22]]')