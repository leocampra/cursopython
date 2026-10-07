'''
def por_canal(df, canal):
    return df[df["Canal"]==canal]
'''

def funcao_publica1():
    return "Função pública 1"

def funcao_publica2():
    return "Função pública 2"

def funcao_interna():
    return "Função interna"

# Apenas estas duas funções serão exportadas com import *
__all__ = ["funcao_publica1", "funcao_publica2"]