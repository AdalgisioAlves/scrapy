# -*- coding: utf-8 -*-
import src.funcoes as f
    
meus_cnae = f.readFile('input\cnae.txt')
print( 'QUANTIDADE DE CNAES LIDOS ',len(meus_cnae))
for cnae in meus_cnae:
    f.dados_cnae(cnae.rstrip('\n').split("-"))
  
    #ENvia PARA FUNÇÃO REALIZAR SCRAP
    
    
