# Gabarito: Mini-Projeto Avaliativo da base Varejo

**Disciplina:** Visualização de Dados e Business Intelligence [T4], Módulo 1, Semana 07

Esta é a versão de referência do mini-projeto. Use-a para comparar com o que você entregou: a estrutura das etapas, as decisões de limpeza e, principalmente, **por que** cada decisão foi tomada. Não existe uma única resposta certa para todas as escolhas. Quando houver mais de um caminho aceitável, isso está indicado.

## Arquivos

| Arquivo | O que é |
|---|---|
| `miniprojeto_varejo_gabarito.py` | Script completo e comentado, dividido nas sprints do enunciado |
| `README_Gabarito_T4.md` | Instruções de execução |
| `COMPARE_COM_O_SEU.md` | Os desvios mais comuns nas entregas da turma, para você conferir no seu trabalho |
| `saidas/saida_execucao.txt` | Tudo o que o script imprime no terminal |
| `saidas/df_limpo.csv` | Base tratada (separador `;`) |
| `saidas/registros_invalidos.csv` | Registros separados pela regra do `CO_ID` (vazio nesta base) |

A base original não está na pasta. Baixe `Base Varejo.csv` no [Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data).

## O que o script faz, critério por critério

| Critério da rubrica | Onde está no script |
|---|---|
| 3. Manipulação de CSV | Sprint 1: leitura nativa com `csv.DictReader` e leitura com `pd.read_csv` |
| 4. Nulos e condicionais | Sprint 3: funções com `if/else` para "Sem Categoria" e para o nome do produto; regra para os atributos do cliente |
| 5. Regras de negócio e datas | Sprint 2: função `converter_data` com `datetime.strptime`; Sprint 3: validação do `CO_ID` com separação dos registros inválidos |
| 6. Agrupamentos | Sprint 5: seis agrupamentos com `groupby` e `pivot_table` |
| 7. Estatísticas | Sprint 4: os 7 parâmetros de `CL_FHL`, por cliente e por linha |
| 1 e 2. Versionamento e documentação | Este README e o de instruções |

## Decisões de tratamento

1. **Colunas vazias.** Cada linha do arquivo termina com `;;;;`, o que cria 4 colunas `Unnamed` 100% vazias. Elas são removidas.
2. **Nulos disfarçados.** O pandas diz que não há nulos nas colunas úteis, mas 3.650 linhas têm o texto `#N/D` em categoria e nome, todas do produto `PR_ID 107`. O `fillna()` não pega esse caso, porque `#N/D` é um texto e não um nulo. O script primeiro transforma `#N/D` em nulo de verdade e depois preenche com "Sem Categoria" e "Produto não identificado". As linhas **não** são apagadas, porque são vendas reais de um produto sem cadastro.
3. **Dimensões físicas.** A base não tem peso, altura nem outra medida física. O equivalente são os atributos do cliente (gênero, estado civil, filhos e segmento), que não têm nulos. A regra adotada para o caso de faltar algum: recuperar o valor de outra linha do mesmo cliente e **nunca** preencher filhos com 0, porque 0 é um valor real.
4. **Duplicatas.** São 96.553 linhas idênticas (11,6% da base). Elas foram removidas, porque sem uma coluna de quantidade não dá para provar que são unidades a mais. **Alternativa igualmente válida:** guardar o número de repetições numa coluna `QTD` antes de remover.
5. **Regra do `CO_ID`.** O `CO_ID` é o número da nota fiscal. Ele se repete porque uma compra tem vários itens, então **não** é uma chave única por linha. A regra validada é: cada nota tem um único cliente e uma única data, e o número da nota cresce com o tempo. Registros que quebram a regra vão para `registros_invalidos.csv`. Nesta base, nenhum quebrou.
6. **Datas.** Veja a seção seguinte.

## A armadilha das datas

A coluna `DATA` **mistura dois formatos**:

- quando o 1º número é **maior que 12**, a data está em dia/mês/ano (`23/01/2019`);
- quando o 1º número é **até 12**, a data está em mês/dia/ano, no padrão americano (`01/02/2019` é 2 de janeiro).

Ler tudo como `dd/mm/aaaa` **não dá nenhum erro**, e é por isso que a armadilha passa despercebida. Mas a evidência aparece quando se compara a data com o número da nota, que cresce com o tempo:

| Leitura | Datas inválidas | Compras fora de ordem | Período |
|---|---|---|---|
| Tudo como dd/mm/aaaa | 0 | 70 | 04/01/2019 a 08/12/2022 |
| Regra mista | 0 | 0 | 02/01/2019 a 19/08/2022 |

Com a regra mista, o arquivo inteiro fica em ordem cronológica. Lendo tudo como dd/mm, 309.229 registros ficam com o mês trocado. Isso explica "meses estranhos" que apareceram em várias análises, como setembro e outubro de 2022 quase vazios: esses meses simplesmente não existem na base, que termina em agosto de 2022.

Na correção, a leitura como dd/mm foi aceita como conversão correta. Esta seção existe para você entender o que estava acontecendo.

## Principais insights

1. **Alimentos concentra 52,4% dos itens**, seguida por Higiene (18,8%) e Limpeza (17,5%). As três somam 88,7%. Não há preço na base, então isso é volume de itens e não faturamento.
2. **O gênero feminino faz mais compras (9.615 contra 8.856), mas porque tem mais clientes (519 contra 481).** Por cliente, os dois compram igual (18,5 e 18,4 compras), e o mix de categorias é praticamente idêntico (Alimentos é 52,4% nos dois).
3. **52,7% dos clientes não têm filhos.** Mediana e moda são 0, a média é 1,14 e o máximo é 4. A média fica acima da mediana porque uma parte dos clientes tem 3 ou 4 filhos. O número de filhos também não muda o mix do carrinho: Alimentos fica entre 52,3% e 52,6% em todos os grupos.
4. **Cada compra tem em média 39,7 itens**, com mínimo de 1 e máximo de 81. O tamanho da compra é o mesmo nos três segmentos (39,6 a 40,0 itens). O segmento B reúne 64,5% dos clientes.
5. **As vendas cresceram de 2019 a 2021** (4.483, 4.794 e 5.505 compras). 2022 tem só 8 meses na base, de janeiro a agosto. O mês com mais compras foi outubro de 2021 (686) e o com menos, novembro de 2019 (188).
6. **Problemas que permanecem na base:** não há preço nem quantidade, o produto 107 não tem cadastro, 109 nomes de produto aparecem com mais de um código (o `PRESUNTO COZIDO` tem 4) e o formato das datas é misturado na origem.

## Reflexão teórica: ETL e qualidade de dados

**ETL** significa Extrair, Transformar e Carregar. Neste projeto, a **extração** é a leitura do CSV do Kaggle. A **transformação** é todo o trabalho de limpeza: ajustar tipos, revelar nulos disfarçados, remover duplicatas, validar regras de negócio e converter datas. A **carga** é a gravação do `df_limpo.csv`, pronto para uma ferramenta de BI.

A principal lição desta base é que **qualidade de dados não é ausência de erro na tela**. O pandas informa zero nulos, mas existem 3.650 `#N/D`. A conversão de data não dá nenhum erro, mas troca o mês de mais de 300 mil registros. As duplicatas não aparecem a olho nu, mas inflariam qualquer contagem em 13%. Nenhum desses problemas avisa que existe. Eles só aparecem quando a gente desconfia e confere.

Por isso a transformação exige entender **o que cada coluna significa**. Saber que o `CO_ID` é o número da nota permite validar a regra da compra e, de quebra, descobrir o problema das datas. Saber que o número de filhos é um dado do cliente, e não do item, muda o jeito certo de calcular a média. E saber que a base não tem preço impede de chamar contagem de itens de "faturamento".

Por fim, cada decisão de limpeza muda o resultado. Apagar ou preencher, remover duplicatas ou guardar a quantidade: as duas opções podem ser defensáveis, desde que a escolha esteja **escrita e justificada**. Uma análise confiável é uma análise que outra pessoa consegue refazer e entender.
