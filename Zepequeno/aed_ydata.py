from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from ydata_profiling import ProfileReport
caminho_banco = Path("/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite")
if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")
conexao = sqlite3.connect(caminho_banco)
df = pd.read_sql_query("SELECT * FROM vw_vendas_completas", conexao)
profile = ProfileReport(
    df,
    title='Relatório AED - View Vendas Completas',
    explorative=True
)
profile.to_file('relatorio_aed.html')