# -*- coding: utf-8 -*-
import src.funcoes as f
    
meus_cnae = f.readFile('input\cnae.txt')
cont = 0
for cnae in meus_cnae:
    f.dados_cnae(cnae.split("-"),cont)
    cont =+ 1
    exit()
    #ENvia PARA FUNÇÃO REALIZAR SCRAP
    
    
