# Compare com o seu trabalho

Estes são os desvios que mais apareceram nas entregas da turma. Use a lista como checklist: para cada item, confira se aconteceu no seu projeto e veja como o gabarito resolve.

## Entrega e documentação

- [ ] **Só o zip, sem GitHub.** O enunciado pede repositório público. O zip sozinho perde o critério de versionamento.
- [ ] **Código num branch que ninguém vê.** Se o código ficou num pull request aberto ou num branch diferente do principal, quem abre o link vê o repositório vazio. Confira o link em uma janela anônima antes de entregar.
- [ ] **README sem insights.** Descrever as etapas ("carreguei, limpei, agrupei") não é insight. Insight é um resultado dos dados, de preferência com número: "Alimentos concentra 52,4% dos itens".
- [ ] **Conclusões só no código.** As conclusões precisam estar no README, que é o que a rubrica avalia.
- [ ] **"Faturamento" sem preço.** A base não tem valor em R$. Contagem de itens é volume, não faturamento.

## Leitura da base

- [ ] **Base incompleta.** Se o upload para o Colab foi interrompido, o pandas lê só parte do arquivo sem dar erro. A base tem **830.000 linhas**. Confira o `len(df)` antes de seguir.
- [ ] **Dados fictícios.** Gerar dados aleatórios "parecidos" no lugar da base real não é análise exploratória da base Varejo.

## Nulos

- [ ] **`fillna()` no `#N/D`.** O `#N/D` é um texto, não um nulo, então o `fillna("Sem Categoria")` não troca nada. Use `replace`, `na_values=["#N/D"]` na leitura ou uma função com `if/else`, como no gabarito. Depois confira: quantas linhas ficaram com "Sem Categoria"? O certo são 3.228 depois de remover as duplicatas.
- [ ] **Apagar as linhas com `#N/D`.** A rubrica pede "Sem Categoria". Apagar tira vendas reais das contagens.
- [ ] **Tratar só a categoria.** O nome do produto também vem como `#N/D` nas mesmas linhas.

## Duplicatas

- [ ] **Percentual sem multiplicar por 100.** `duplicadas / total` dá 0,116. Imprimir isso com `%` mostra "0,12%", quando o certo é 11,6%. Uma decisão tomada em cima desse número fica errada.
- [ ] **"0 duplicatas" no notebook.** Se as células foram executadas fora de ordem, a contagem pode aparecer depois da remoção. Antes de entregar, use **Reiniciar e executar tudo**.

## Identificador de compra (`CO_ID`)

- [ ] **Não validou o `CO_ID`.** Foi o ponto mais perdido da turma. A regra é: cada nota tem um único cliente e uma única data. O gabarito confere isso com `groupby("CO_ID")` e separa os registros que quebram a regra.
- [ ] **Achar que o `CO_ID` é "empresa".** O PDF do Kaggle diz que é o número da nota fiscal.
- [ ] **Tratar o `CO_ID` como chave única.** Ele se repete porque cada compra tem vários itens. Remover linhas por `CO_ID` repetido apaga itens válidos.
- [ ] **Validar só se está vazio.** É um começo, mas não testa a regra de negócio.

## Datas

- [ ] **Converter numa variável solta.** `datas = pd.to_datetime(df["DATA"])` não muda o `df`. A coluna precisa ser substituída: `df["DATA"] = ...`.
- [ ] **Formato errado.** `format="%y/%m/%d"` transforma **todas** as datas em inválidas, porque a base usa ano com 4 dígitos no fim.
- [ ] **Formatos misturados.** A base mistura mês/dia com dia/mês. Veja a seção "A armadilha das datas" no README. Se a sua análise mostrou setembro e outubro de 2022 quase vazios, a causa é essa: a base termina em agosto de 2022.
- [ ] **Script que depende da versão.** `select_dtypes(include=["str"])` só funciona no pandas 3 e quebra no pandas 2, que é o do Colab.

## Estatísticas

- [ ] **`describe()` sozinho.** Ele não mostra a moda. Faltou um dos 7 parâmetros.
- [ ] **Por linha ou por cliente?** O número de filhos é do cliente, mas se repete em cada item comprado. Calcular por linha dá mais peso a quem compra mais. As duas formas foram aceitas, mas a por cliente é a mais correta (média 1,136 contra 1,146).

## Agrupamentos

- [ ] **Média do `CO_ID`.** O número da nota é um código, não uma medida. A média dele não significa nada. Para contar compras, use `nunique()`.
- [ ] **`CO_ID` como coluna de `pivot_table`.** Gera uma tabela com 18 mil colunas, uma por nota, que não mostra padrão nenhum.
- [ ] **Comparar totais de grupos de tamanhos diferentes.** "Mulheres compram mais" é verdade no total, mas elas também são mais clientes. Por cliente, os dois gêneros compram igual.

## Reprodutibilidade

- [ ] **Só roda no Colab.** `from google.colab import files` quebra fora do Colab. Se usar, deixe comentado ou dentro de um `if`.
- [ ] **Pacote que não é usado.** Importar `kagglehub` e depois ler o arquivo local faz o script quebrar para quem não tem o pacote.
- [ ] **Reler o CSV em cada bloco.** Carregue a base uma vez e trabalhe sempre no mesmo `df`.
