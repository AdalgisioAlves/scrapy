# -*- coding: utf-8 -*-
import src.funcoes as f
    
meus_cnae = f.readFile('input\cnae.txt')

for cnae in meus_cnae:
    f.dados_cnae(cnae.split("-"))
    #ENvia PARA FUNÇÃO REALIZAR SCRAP
    
    
