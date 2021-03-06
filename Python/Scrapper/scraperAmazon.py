import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os






#cria ou atualiza o documento de metadados com os nomes dos produtos sendo observados passados atravez da lista
def metadados(lista):
    meta_json = {}
    if os.path.exists("metadados.dat"):#verifica se existe o arquivo
        #se existir
        with open("metadados.dat","r") as myfile:#abre o arquivo
            meta_json = json.load(myfile)#carrega as informações do arquivo
    else:#caso não exista
        #cria um modelo vazio da estrutura do arquivo(em json)
        meta_json = {
            'nomes': [],
        }

    #agora com as informações carregadas(seja vazio ou com os dados do arquivo)
    for produto in lista:#para todos os produtos passados na lista de produtos
        s = produto["nome"]#pega o nome do produto atual
        name = "".join(x for x in s if x.isalnum())#formata ele para um nome compativel com a formatação para arquivos
        if not(name in meta_json['nomes']):#se o nome já não estiver presente na lista
            meta_json['nomes'].append(name)#adiciona o nome a lista

    with open("metadados.dat","w+") as myfile:#abre o arquivo novamente, agora com a garantia da existencia ou criando se necessário
        json.dump(meta_json,myfile)#insere as informações (atualizadas ou geradas agora)


#recebe os dados de um produto especifico e armazena eles no arquivo dele existente ou gera o arquivo para iniciar o armazenamento
def storeData(produto):
    prod_json = {}#cria o formato vazio do produto
    s = produto["nome"]#recebe o nome do produto
    path = "".join(x for x in s if x.isalnum())#formata o nome para a formatação de nome de arquivo
    date = datetime.today().strftime('%Y-%m-%d')#recebe a data atual do momento da medição de preço
    price =  produto["preco"]#recebe o preço atual
    #print(path)
    
    
    if os.path.exists("produtos\\"+path):#caso o arquivo já exista
        with open("produtos\\"+path,"r") as myfile:#abre o arquivo do produto
            prod_json = json.load(myfile)#carrega as informações passadas
            
    else:#caso contrário
        prod_json = {#cria o produto com apenas as informações atuais
            'nome': s,#nome base
            'safe_file_name':path,#nome editado para arquivo
            'preco_data': [],#vetor com duplas de preço e data
            'tracking': False#bandeira de caso tenha interesse em exibir em grafico
            }

    temp_arr = [price,date]#recebe o proeço e a data da medição atual
    prod_json['preco_data'].append(temp_arr)#adiciona as informações antigas(caso tenha)

    with open("produtos\\"+path,"w+") as myfile:#abre ou cria o arquivo
            json.dump(prod_json,myfile)#insere as informações atualizadas


def getInfoFromAmazonProd(url):
    req = requests.get(url,headers={"User-Agent":"Defined"})  #faz a requisição(ou seja, acessa) do site

    if req.status_code == 200: #caso consiga acessar o site
        print('Requisição bem sucedida!')
        conteudo = req.content#atribui o html a uma variável
    

    soup = BeautifulSoup(conteudo, 'html.parser') #informa o html para o interpretador

    tag = soup.find(id="priceblock_ourprice").get_text()#encontra na pagina o preço
    name = soup.find(id="productTitle").get_text()#encontra na pagina o nome do produto
    nome = name.replace('\n','')#retira caracteres inuteis
    nomes = [nome]#armazena o nome na lista

    price = tag.split('$')[1]#remove o simbolo de dinheiro do preço
    produto = {"nome":nome, "preco":price.replace(',','.')}#cria um objeto de produto basico para mandar para as funções
    metadados([produto])#passa uma lista com o produto recebido
    
    storeData(produto)#armazena as informações do produto recebido
    #print(type(nome))



#requisita os preços desses produtos
getInfoFromAmazonProd("https://www.amazon.com.br/dp/B07FQK1TS9")
getInfoFromAmazonProd("https://www.amazon.com.br/gp/product/B0773XBMB6/ref=s9_acss_bw_cg_11einkpg_3b1_w?pf_rd_m=A3RN7G7QC5MWSZ&pf_rd_s=merchandised-search-4&pf_rd_r=TGGXJTS4BT0HGD9CZE3M&pf_rd_t=101&pf_rd_p=6e37f045-f0a4-4086-979f-b28dd60932d9&pf_rd_i=5475881011")
