import matplotlib.pyplot as plt
import matplotlib.dates as pltd
import datetime
import os
import json

#Le o arquivo de metadados com os nomes dos produtos sendo observados
def read_from_meta():
    nomes = []#vetor com os nomes
    if os.path.exists("metadados.dat"):
        with open("metadados.dat","r") as myfile:
            meta_json = json.load(myfile)
            nomes = meta_json['nomes']
    

    return nomes

#recebendo o nome do produto(formatado para nome de arquivo) lé tal arquivo e obtem as informações necessárias
def read_from_prod(nome):
    precos = []#vetor com os preços
    datas = []#vetor com as datas
    nomes_prods = '' #nome do produto em questão
    tracking = False 
    if os.path.exists("produtos\\"+nome):
        with open("produtos\\"+nome,"r") as myfile:
            prod_json = json.load(myfile)
            for info in prod_json["preco_data"]:
                precos.append(float(info[0]))
                date_obj = datetime.datetime.strptime(info[1],'%Y-%m-%d')
                datas.append(date_obj)
            nomes_prods = prod_json['nome']
            tracking = prod_json['tracking']
            
    
    return precos,datas,nomes_prods,tracking


#def plot_from_precos(precos):
    #plt.plot(precos)
    #plt.show()


#print(read_from_meta())
#produtos = read_from_meta()
#print(produtos[0])
#print(read_from_prod(produtos[0]))