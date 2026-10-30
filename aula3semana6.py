#pip install scikit-learn
'''
MinMaxScaler
Transforma os dados para um intervalo fixo (por padrão, entre 0 e 1).
Exemplo: se você tem notas de 0 a 100, ele converte para valores entre 0 e 1.
Útil quando queremos comparar variáveis em escalas diferentes.
'''
from sklearn.preprocessing import MinMaxScaler
'''
RobustScaler
Similar ao StandardScaler, mas usa mediana e intervalo interquartil em vez de média e desvio padrão.
É resistente a outliers (valores muito extremos).
Exemplo: se temos salários com alguns valores absurdamente altos, ele evita que esses outliers 
distorçam a escala.
'''
from sklearn.preprocessing import RobustScaler
'''
Pipeline
Cria uma sequência de etapas de pré-processamento e modelagem.
Exemplo: primeiro imputar valores ausentes, depois escalar os dados, e por fim aplicar um modelo 
de regressão.
Vantagem: garante que todas as etapas sejam aplicadas de forma consistente, inclusive em novos dados.
'''
from sklearn.pipeline import Pipeline
'''
SimpleImputer
Preenche valores faltantes (NaN).
Estratégias comuns: média, mediana, moda ou um valor fixo.
Exemplo: se uma coluna de idade tem valores ausentes, podemos substituir pela média da idade.
'''
from sklearn.impute import SimpleImputer
'''
StandardScaler
Padroniza os dados para terem média = 0 e desvio padrão = 1.
Exemplo: transforma alturas (em cm) para uma escala normalizada, facilitando algoritmos que 
assumem distribuição normal.

FunctionTransformer
Permite aplicar funções próprias de transformação nos dados.
Exemplo: aplicar logaritmo em uma variável para reduzir assimetria, ou criar uma nova 
feature a partir de cálculos específicos.
'''
from sklearn.preprocessing import StandardScaler, FunctionTransformer

import pandas as pd
import numpy as np

df = pd.read_excel("tabela_vendas_ZePequeno_corrigido.xlsx")

# Inicializando o scaler
scaler = MinMaxScaler()

# Aplicando a transformação (fit calcula min/max, transform aplica a fórmula)
df["Valor_Venda_MinMax"] = scaler.fit_transform(df[["Valor_Venda"]])

# Verificação de integridade
v_min = df["Valor_Venda_MinMax"].min()
v_max = df["Valor_Venda_MinMax"].max()

print(f"Mínimo: {v_min} | Máximo: {v_max}")
# Resultado esperado: Mínimo: 0.0 | Máximo: 1.0

# Aplicação de ambos para comparação
df["MinMax"] = MinMaxScaler().fit_transform(df[["Valor_Venda"]])
df["Robust"] = RobustScaler().fit_transform(df[["Valor_Venda"]])

# Filtrando os 10 maiores para observação
outliers_comp = df.nlargest(10, "Valor_Venda")[["MinMax", "Robust"]]
print(outliers_comp)

# 1. Função para remover outliers via IQR
def remove_outliers_iqr(X):
    X = pd.DataFrame(X)
    Q1 = X.quantile(0.25)
    Q3 = X.quantile(0.75)
    IQR = Q3 - Q1
    # Filtra os dados dentro do limite (opcional: em pipelines, 
    # as vezes apenas clipamos os valores para não quebrar o shape)
    return X.clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR, axis=1)

# 2. Construção do Pipeline
pipeline_processamento = Pipeline([
    # Etapa 1: Imputação pela mediana
    ("imputer", SimpleImputer(strategy="median")),
    
    # Etapa 2: Tratamento de outliers (usando FunctionTransformer)
    ("outlier_remover", FunctionTransformer(remove_outliers_iqr)),
    
    # Etapa 3: Padronização (Z-score)
    ("scaler", StandardScaler())
])

# Execução
dados_processados = pipeline_processamento.fit_transform(df[["Valor_Venda"]])
print(dados_processados)
