# Instruções de execução: gabarito do Mini-Projeto Varejo (T4)

## VS Code ou terminal

1. Instale o Python 3.10 ou mais novo.
2. Instale o pandas: `pip install pandas`
3. Baixe `Base Varejo.csv` no [Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data) e coloque na mesma pasta do script.
4. Rode:

```bash
python miniprojeto_varejo_gabarito.py
```

Se a base estiver em outra pasta, passe o caminho:

```bash
python miniprojeto_varejo_gabarito.py "C:/Downloads/Base Varejo.csv"
```

## Google Colab

1. Envie `miniprojeto_varejo_gabarito.py` e `Base Varejo.csv` para os arquivos da sessão.
2. Numa célula, rode:

```python
%run miniprojeto_varejo_gabarito.py "Base Varejo.csv"
```

## O que esperar

A execução leva menos de 30 segundos. O relatório aparece no terminal, separado por sprint, e os arquivos `df_limpo.csv` e `registros_invalidos.csv` são gravados na pasta `saidas/`. A saída completa de uma execução está em `saidas/saida_execucao.txt`, para você comparar com a sua.

O script funciona com o pandas 2 e com o pandas 3.
