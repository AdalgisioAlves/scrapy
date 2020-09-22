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
    
    url = "http://www.fieb.org.br/guia/Resultado_Consulta.aspx?operProduto=and&localizacao=&ordenacao=ind_razao_social&page=9&consulta=Consultas+Especiais&consulta=Consultas+Especiais"
    #url = "http://www.fieb.org.br/guia/Resultado_Consulta?CodCnae=C&NomeAtividade=IND%c3%9aSTRIAS%20DE%20TRANSFORMA%c3%87%c3%83O.&operProduto=and&localizacao=&ordenacao=ind_razao_social&page=0&consulta=Consultas%20Especiais"
    p = {
        'CodCnae': cnae[0],
       'NomeAtividade': cnae[1]
    }
    #print(urllib.parse.urlencode(p))
    pagina = requests.get(url,params=p)
    html = BeautifulSoup(pagina.text, 'lxml')
    print(html)
    # PEGAR QUANTIDADE DE PAGINAS NO RESULTADO DA CONSULTA
    r = html.find(id="label-consulta-8")
    empresas = parser_html(html)
    if empresas:
        export_csv(empresas, True)

    if len(r.find_all('a')) > 0:
        print('Request OUtras Paginas')
        for link in r.find_all('a'):
            url = "http://www.fieb.org.br/guia/" + link.get('href')
            pagina = requests.get(url)
            html = BeautifulSoup(pagina.text, 'lxml')
            empresas = parser_html(html)
            if empresas:
                export_csv(empresas, False)


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


def export_csv(data_empresa, novo):
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
