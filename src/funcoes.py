# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import datetime
import csv
import urllib.parse
import src.util as u

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
    NUM_PAGINA = html.find(id="ContentPlaceHolder1_generalContent_rpt_lblLastPage").text
    URL_EMPRESA = html.find_all(id="label-consulta-3")  #LINKS DO PERFIL DA EMPRESA PAGINA 1
    for alink in URL_EMPRESA:
                urlemp.append(alink.a.get('href'))
    for lnk in urlemp:
        url = "http://www.fieb.org.br/guia/" + lnk
        pagina = requests.get(url)
        html = BeautifulSoup(pagina.content, 'lxml')
        dados_emp = limpa_dados(list(html.find(id="divDadosIndustria")))
        
        #print('Obtendo Links das paginas')
        if dados_emp != None and dados_emp != False:
            csv.append(u.parse_csv(dados_emp))
        
    if  int(NUM_PAGINA)  > 1:
        urlemp.clear()
        i = 1 
        while int(NUM_PAGINA) > i:       # EXECUTA PAGINAÇÃO
            print('INTERAÇÃO HTML %',i)
            p = urllib.parse.urlencode({
                'CodCnae': cnae,
                'NomeAtividade': cnae[1],
                'operProduto': 'and',
                'localizacao': '',
                'ordenacao': 'ind_razao_social',
                'page': i,
                'consulta': 'Consultas Especiais'
            })
            p.encode('ascii')
            url = "http://www.fieb.org.br/guia/Resultado_Consulta.aspx?%s" % p
            

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
                dados_emp = limpa_dados(list(html.find(id="divDadosIndustria")))
                
                if dados_emp == False:
                    print(url)
                    print(html)
                    exit()
                #if parse_csv(dados_emp) != None:
                csv.append(u.parse_csv(dados_emp))
                c += 1  
            urlemp.clear()
            i += 1        
         # PEGA OS LINKS DAS EMPRESAS DA PAGINA
    
    export_csv(csv,cnae)
    csv.clear()
  
def limpa_dados(dados):
    ret = []
    for d in dados:
        if d != '\n' and d != ' ' and d.name != 'br': 
            ret.append(d)
        
    return ret

def export_csv(data_empresa,cnae):
    try:
        h = 'Nome da Empresa;Origem;Sub-Origem;Mercado;Produto;Site;País;Estado;Cidade;Logradouro;Numero;Bairro;Complemento;CEP;Telefone;Telefone 2;Observação;\
            Nome Contato;E-mail Contato;Cargo Contato;Tel. Contato;Tel. 2 Contato;LinkedIn Contato;Tipo do Serv. Comunicação;ID do Serv. Comunicação;CpfCnpj;Duplicado'
        x = datetime.datetime.now()
        file = x.strftime('%d-%m-%Y')
        path = os.getcwd()+'\\output\\cnae_'+cnae[0]+ "_" + file+".csv"
        l = 0
       
        with open(path, 'w') as f:
            print('Arquivo Gerado com Suceso ' + file)
            f.write(h+'\n')
            for e in data_empresa:
                if e != None and e != False:
                    telefone = e['Telefone'].split('/')
                    if len(telefone )> 2:
                         t1 = telefone[0]                         
                         t2 = telefone[1]
                         t3 = telefone[2]
                    else: 
                        t1 = telefone[0]
                        t2 = ""
                        t3 = ""                    
                    linha = e['NomeEmpresa'] + ';;;' +cnae[1].rstrip('\n') +';' +e['Mercado'] + e['Produtos'].replace(';', ' ') + ';' + e['Site'] + ';BRASIL;BAHIA;' + e['Cidade'] + ';' + \
                    e['Logradouro'] + ';S/N;' + e['Bairro'] + ';;' + e['CEP'] + ';' + t1 +';'+t2+';; ;' + \
                    e['Email'] + '; ;'+ t3 +';;;;;'+ str(e['CpfCnpj']) +';'
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

