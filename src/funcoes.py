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


def dados_cnae(cnae, cont):

    #url = "http://www.fieb.org.br/guia/Resultado_Consulta?CodCnae=C&NomeAtividade=IND%c3%9aSTRIAS%20DE%20TRANSFORMA%c3%87%c3%83O.&operProduto=and&localizacao=&ordenacao=ind_razao_social&page=0&consulta=Consultas%20Especiais"

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
    urlemp  = []
    csv     = []
    pagina = requests.get(url)
    html = BeautifulSoup(pagina.text, 'lxml')
    # PEGAR QUANTIDADE DE PAGINAS NO RESULTADO DA CONSULTA
    paginacao = html.find(id="label-consulta-8")
    total_emp = html.find_all(id="label-consulta-3")
    for alink in total_emp:
        urlemp.append(alink.a.get('href'))
        
    for lnk in urlemp:
        url = "http://www.fieb.org.br/guia/" + lnk
        pagina = requests.get(url)
        html = BeautifulSoup(pagina.content, 'lxml')       
        dados_emp = list(html.find(id="divDadosIndustria"))
        
        if len(dados_emp) == 99:
            print('Gerando Dados CSV 1')
            csv.append(parse_csv(dados_emp))

    if len(paginacao.find_all('a')) > 0:
      
        urlemp.clear()
        for link in paginacao.find_all('a'):
            #EXECUTA PAGINAÇÃO
            
            url = "http://www.fieb.org.br/guia/" + link.get('href')
            
            pagina = requests.get(url)
            html = BeautifulSoup(pagina.content, 'lxml')
            total_emp = html.find_all(id="label-consulta-3")
            for alink in total_emp:
                urlemp.append(alink.a.get('href'))
                
            for lnk in urlemp:
                url = "http://www.fieb.org.br/guia/" + lnk
                pagina = requests.get(url)
                html = BeautifulSoup(pagina.content, 'lxml')       
                dados_emp = list(html.find(id="divDadosIndustria"))
                
                if len(dados_emp) == 99:
                    print('Gerando Dados CSV 1')
                    csv.append(parse_csv(dados_emp))
            #PEGA OS LINKS DAS EMPRESAS DA PAGINA
        
    export_csv(csv)
    exit()

def parser_html(html):
    empresas = {
        'razao_soc': '',
        'nome_fantazia': '',
        'telefone': '',
        'atv_economica': '',
        'municipio': '',
        'produtos': ''
    }
    rz_soc = []
    nome_fantazia = []
    telefone = []
    atv_economica = []
    municipio = []
    produtos = []

    body = html.find(id="ContentPlaceHolder1_generalContent_divResultado")
    if body == None:
        return False

    tb_resultado = body.findAll('table')[0]
    # RAZÃO SOCIAL DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-3"):
        rz_soc.append(rz.find('div').find('span').a.text)
    # NOMES DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-4"):
        nome_fantazia.append(rz.find('span').nextSibling.nextSibling.text)
    # TELEFONE DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-10"):
        telefone.append(rz.find('span').nextSibling.nextSibling.text)
    # ECONOMICA DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-5"):
        atv_economica.append(rz.find('span').nextSibling.nextSibling.text)
     # ECONOMICA DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-6"):
        municipio.append(rz.find('span').nextSibling.nextSibling.text)
      # ECONOMICA DAS EMPRESAS
    for rz in tb_resultado.find_all(id="label-consulta-7"):
        produtos.append(rz.find('span').nextSibling.nextSibling.text)
    empresas['razao_soc'] = rz_soc
    empresas['nome_fantazia'] = nome_fantazia
    empresas['telefone'] = telefone
    empresas['atv_economica'] = atv_economica
    empresas['municipio'] = municipio
    empresas['produtos'] = produtos
    return empresas


def export_csv(dados_emp):
    try:
        h = 'Nome da Empresa;Origem;Sub-Origem;Mercado;Produto;Site;País;Estado;Cidade;Logradouro;Numero;Bairro;Complemento;CEP;Telefone;Telefone 2;Observação;Nome Contato;E-mail Contato;Cargo Contato;Tel. Contato;Tel. 2 Contato;LinkedIn Contato;Tipo do Serv. Comunicação;ID do Serv. Comunicação;CpfCnpj;Duplicado'
        x = datetime.datetime.now()
        file = x.strftime('%d-%m-%Y')
        path = os.getcwd()+'\\output\\cnae_'+file+".csv"
        l = 0
        if novo == True:

            with open(path, 'w') as f:
                f.write(h+'\n')
                while len(data_empresa['razao_soc']) > l:
                    linha = data_empresa['razao_soc'][l] + ';;;;' + data_empresa['produtos'][l].replace(';', ' ') + ';SITE;BRASIL;BAHIA;' + data_empresa['municipio'][l] + ';' + \
                        'LOGRADOURO;NUMERO;BAIRRO;COMPLEMENTO;CEP;' + \
                        data_empresa['telefone'][l] + \
                        ';OBservação;Nome Contato;E-mail Contato;Cargo Contato;Tel. Contato;Tel. 2 Contato'
                    f.write(linha+'\n')
                    l += 1
            f.close()
        else:
            with open(path, 'a') as f:
                while len(data_empresa['razao_soc']) > l:
                    linha = data_empresa['razao_soc'][l] + ';;;;' + data_empresa['produtos'][l].replace(';', ' ') + ';SITE;BRASIL;BAHIA;' + data_empresa['municipio'][l] + ';' + \
                        'LOGRADOURO;NUMERO;BAIRRO;COMPLEMENTO;CEP;' + \
                        data_empresa['telefone'][l] + \
                        ';OBservação;Nome Contato;E-mail Contato;Cargo Contato;Tel. Contato;Tel. 2 Contato'
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
        'Municipio': [],
        'Produtos': [],
        'Site':[],
        'Pais':[],
        'Estado':[],
        'Cidade':[],
        'Logradouro':[],
        'Numero':[],
        'Bairro':[],
        'Complemento':[],
        'CEP':[],
        'Telefone2':[],
        'CpfCnpj':[]

    }
    if(dados_emp):
        #exit()
        empresas['NomeEmpresa'].append(dados_emp[1].text)
        empresas['Telefone'].append(dados_emp[87].text)
        empresas['Mercado'].append(dados_emp[28].text)
        empresas['Produtos'].append(dados_emp[32].text)
        empresas['Site'].append(dados_emp[97].text)
        empresas['Pais'].append('Brasil')
        empresas['Estado'].append('BA')
        empresas['Cidade'].append(dados_emp[72].text)
        empresas['Logradouro'].append(dados_emp[57].text) 
        empresas['Numero'].append( 'S/N')
        empresas['Bairro'].append(dados_emp[67].text)
        empresas['CEP'].append(dados_emp[82].text)
        empresas['Telefone2'].append(dados_emp[87].text)
        empresas['CpfCnpj'].append(dados_emp[4])
        return empresas
    else:
        return False     
    