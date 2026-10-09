import numpy as np
import pandas as pd 
#1
df = pd.read_excel("tabela_vendas_ZePequeno_corrigido.xlsx")
'''
# A partir de uma lista Python
valores_venda = np.array([120.50, 340.00, 89.90, 520.75, 210.00])
print(f"Total vendas: {valores_venda.sum():,.2f}")
'''
'''
print(valores_venda.shape)   
print(valores_venda.dtype)   


# Array de zeros e uns (útil para máscaras)
mascara = np.ones(5, dtype=bool)
print(mascara)


# Intervalo de valores (ex: dias do mês)
dias = np.arange(1, 32)
print(dias)

# Valores igualmente espaçados
faixas = np.linspace(0, 1000, 10)  # 10 faixas de R$0 a R$1000
print(faixas)

valor_venda = np.random.uniform(50, 5000, 500)
print(valor_venda)

comissao = valores_venda * 0.05
print(comissao)
'''
'''
precos = np.array([
    [100, 200, 300, 400],  # Região Norte
    [150, 250, 350, 450],   # Região Sul
    [120, 220, 320, 420]
    ])  # Região Leste
desconto = np.array([0.10, 0.05, 0.15, 0.08])
precos_com_desconto = precos * (1 - desconto)
print(precos_com_desconto)

print(precos_com_desconto.shape)

vendas = np.array([[1200, 3400, 890],
                   [2100, 1500, 430],
                   [980,  4200, 670],
                   [3300, 2800, 990]])
meta_canal = np.array([2000, 3000, 800])
diferenca = vendas - meta_canal
print(diferenca.shape)


media_canal = vendas.mean(axis=0)   # shape (3,)
std_canal   = vendas.std(axis=0)    # shape (3,)
z_score     = (vendas - media_canal) / std_canal  # shape (4,3)

print("Diferença da meta:\n", diferenca)
print("\nZ-score por canal:\n", np.round(z_score, 2))
'''
'''
#1
v = np.array([50, 150, 300, 450, 600])
resultado = v[[1,3]]
print(resultado)
#2
valores = np.array([89.90, 210.00, 520.75])
print(valores.dtype)
print(valores.shape)
#3
vendas_regioes = np.random.randint(50, 1000, (4, 3))
print(vendas_regioes)
acima_500 = vendas_regioes[vendas_regioes > 500]
print(acima_500)
#4
m = np.random.randint(50, 1000, (4, 3))
canal_online = m[:, 1]
media_geral = m.mean()
resultado = canal_online[canal_online > media_geral]
print("Média geral:", media_geral)
print("Vendas Online acima da média:", resultado)
'''
#1
vendas = np.array ([100, 250, 400, 750, 1200])
vendas_com_iva = vendas * 1.12
print(vendas_com_iva)

#2
n = np.array([89.9, 210.0, 520.75, 340.0, 670.3])
print('Média: ', n.mean(), '| Desvio padrão: ', round(n.std(), 2))

#3
v = np.array([240, 300, 570, 900, 1200, 2500, 3200])
classificacao = np.where(v >= 2000, "Alta", np.where(v >= 500, "Média", "Baixa"))
print("Vendas:", v)
print("Classificação:", classificacao)
#4
v = np.random.randint(50, 5000, 10)
p90 = np.percentile(v, 90)
v[v > p90] = np.median(v)
print(p90)
print(v)
