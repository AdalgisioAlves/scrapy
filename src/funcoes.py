# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import datetime
import csv
import urllib.parse


def readFile(path):
    # VERIFICA SE O ARQUIVO EXISTE
    try:
        with open(path, encoding='utf-8') as f:
            lista_cnae = f.readlines()
            f.close()
        return lista_cnae
    except FileNotFoundError as e:
        return "Arquivo cnae.txt Não fon encontrado"
    except IOError as e:
        return "Não Foi possivel carregar o arquivo"


def dados_cnae(cnae):

    # url = "http://www.fieb.org.br/guia/Resultado_Consulta?CodCnae=C&NomeAtividade=IND%c3%9aSTRIAS%20DE%20TRANSFORMA%c3%87%c3%83O.&operProduto=and&localizacao=&ordenacao=ind_razao_social&page=0&consulta=Consultas%20Especiais"

    p = urllib.parse.urlencode({
        'CodCnae': cnae[0],
        'NomeAtividade': cnae[1],
        'operProduto': 'and',
        'localizacao': '',
        'ordenacao': 'ind_razao_social',
        'page': 0,
        'consulta': 'Consultas Especiais'

    })
    p.encode('ascii')
    url = "http://www.fieb.org.br/guia/Resultado_Consulta.aspx?%s" % p
    urlemp = []
    csv = []
    pagina = requests.get(url)
    html = BeautifulSoup(pagina.content, 'lxml')   
    
    # PEGAR QUANTIDADE DE PAGINAS NO RESULTADO DA CONSULTA
    pagLink = html.find(id="label-consulta-8")
    total_emp = html.find_all(id="label-consulta-3")
    
    for alink in total_emp:
        urlemp.append(alink.a.get('href'))

    for lnk in urlemp:
        url = "http://www.fieb.org.br/guia/" + lnk
        pagina = requests.get(url)
        html = BeautifulSoup(pagina.content, 'lxml')
        dados_emp = list(html.find(id="divDadosIndustria"))
        
        print('Obtendo Links das paginas')
        if parse_csv(dados_emp) != None:
            csv.append(parse_csv(dados_emp))
        
    if len(pagLink.find_all('a')) > 1:
        plinks = pagLink.find_all('a')
        plinks.pop(0)
        urlemp.clear()
        for link in plinks:
            # EXECUTA PAGINAÇÃO

            url = "http://www.fieb.org.br/guia/" + link.get('href')

            pagina = requests.get(url)
            html = BeautifulSoup(pagina.content, 'lxml')
            total_emp = html.find_all(id="label-consulta-3")
            for alink in total_emp:
                urlemp.append(alink.a.get('href'))
            c = 1
            for lnk in urlemp:
                url = "http://www.fieb.org.br/guia/" + lnk
                pagina = requests.get(url)
                html = BeautifulSoup(pagina.content, 'lxml')
                dados_emp = list(html.find(id="divDadosIndustria"))
                if parse_csv(dados_emp) != None:
                    csv.append(parse_csv(dados_emp))
                c += 1  
                print('Tratando Dados html ',c )
            # PEGA OS LINKS DAS EMPRESAS DA PAGINA
    print('Gerando Arquivo CSV QUANDTIDADE DE REGISTROS OBTIDOS ',len(csv))
    export_csv(csv,cnae[0])
  

def export_csv(data_empresa,cnae):
    try:
        h = 'Nome da Empresa;Origem;Sub-Origem;Mercado;Produto;Site;País;Estado;Cidade;Logradouro;Numero;Bairro;Complemento;CEP;Telefone;Telefone 2;Observação;\
            Nome Contato;E-mail Contato;Cargo Contato;Tel. Contato;Tel. 2 Contato;LinkedIn Contato;Tipo do Serv. Comunicação;ID do Serv. Comunicação;CpfCnpj;Duplicado'
        x = datetime.datetime.now()
        file = x.strftime('%d-%m-%Y')
        path = os.getcwd()+'\\output\\cnae_'+cnae+ "_" + file+".csv"
        l = 0
       
        with open(path, 'w') as f:
            print('Arquivo Gerado com Suceso' + file)
            f.write(h+'\n')
            for e in data_empresa:
                
                linha = e['NomeEmpresa'][0] + ';;;;' +e['Mercado'][0] + e['Produtos'][0].replace(';', ' ') + ';' + e['Site'][0] + ';BRASIL;BAHIA;' + e['Cidade'][0] + ';' + \
                e['Logradouro'][0] + ';S/N;' + e['Bairro'][0] + ';COMPLEMENTO;' + e['CEP'][0] + ';' + e['Telefone'][0] + ';;OBservação;Nome Contato;' + \
                e['Email'][0] + ';Cargo Contato;Tel. Contato;Tel. 2 Contato;LinkedIn Contato;Tipo do Serv. Comunicação;ID do Serv. Comunicação;'+e['CpfCnpj'][0] +';Duplicado'
                f.write(linha+'\n')
                l += 1
        f.close()

    except FileNotFoundError as e:
        print("Arquivo cnae.txt Não fon encontrado", e)
        exit()
    except IOError as e:
        print("Não Foi possivel carregar o arquivo", e)
        exit()
    print('Arquivo gerado com sucesso :'+file)


def parse_csv(dados_emp):

    empresas = {
        'NomeEmpresa': [],
        'Telefone': [],
        'Mercado': [],
        'Produtos': [],
        'Site': [],
        'Pais': [],
        'Estado': [],
        'Cidade': [],
        'Logradouro': [],
        'Numero': [],
        'Bairro': [],
        'Complemento': [],
        'CEP': [],
        'Telefone2': [],
        'Email': [],
        'CpfCnpj': []

    }

    if len(dados_emp) == 99:
       
        empresas['NomeEmpresa'].append(dados_emp[1].text)
        empresas['Telefone'].append(dados_emp[87].text)
        empresas['Mercado'].append(dados_emp[28].text)
        empresas['Produtos'].append(dados_emp[32].text)
        empresas['Site'].append(dados_emp[97].text)
        empresas['Pais'].append('Brasil')
        empresas['Estado'].append('BA')
        empresas['Cidade'].append(dados_emp[72].text)
        empresas['Logradouro'].append(dados_emp[57].text)
        empresas['Numero'].append('S/N')
        empresas['Bairro'].append(dados_emp[67].text)
        empresas['CEP'].append(dados_emp[82].text)
        empresas['Telefone2'].append(dados_emp[87].text)
        empresas['CpfCnpj'].append(dados_emp[4])
        empresas['Email'].append(dados_emp[92].text)
        return empresas
    if len(dados_emp) == 102:
       
        empresas['NomeEmpresa'].append(dados_emp[1].text)
        empresas['Telefone'].append(dados_emp[90].text)
        empresas['Mercado'].append(dados_emp[28].text)
        empresas['Produtos'].append(dados_emp[32].text)
        empresas['Site'].append(dados_emp[100].text)
        empresas['Pais'].append('Brasil')
        empresas['Estado'].append('BA')
        empresas['Cidade'].append(dados_emp[75].text)
        empresas['Logradouro'].append(dados_emp[60].text)
        empresas['Numero'].append('S/N')
        empresas['Bairro'].append(dados_emp[70].text)
        empresas['CEP'].append(dados_emp[85].text)
        empresas['Telefone2'].append(dados_emp[90].text)
        empresas['CpfCnpj'].append(dados_emp[4])
        empresas['Email'].append(dados_emp[95].text)

        return empresas
    if len(dados_emp) == 103:
       
        empresas['NomeEmpresa'].append(dados_emp[1].text)
        empresas['Telefone'].append(dados_emp[91].text)
        empresas['Mercado'].append(dados_emp[28].text)
        empresas['Produtos'].append(dados_emp[32].text)
        empresas['Site'].append(dados_emp[101].text)
        empresas['Pais'].append('Brasil')
        empresas['Estado'].append('BA')
        empresas['Cidade'].append(dados_emp[76].text)
        empresas['Logradouro'].append(dados_emp[61].text)
        empresas['Numero'].append('S/N')
        empresas['Bairro'].append(dados_emp[71].text)
        empresas['CEP'].append(dados_emp[82].text)
        empresas['Telefone2'].append(dados_emp[87].text)
        empresas['CpfCnpj'].append(dados_emp[4])
        empresas['Email'].append(dados_emp[96].text)
        return empresas
        
