id	vendedor	produto	    valor
1	Ana	        Notebook	3000
2	João	    Mouse	    100
3	Ana	        Teclado	    200
4	Maria	    Monitor	    1500
5	João	    Notebook	3000
6	Ana	        Mouse	    100


# ROW_NUMBER() - Queremos numerar as vendas da maior para a menor
SELECT
    id,
    vendedor,
    valor,
    ROW_NUMBER() OVER(
        ORDER BY valor DESC, id ASC
    ) AS numero_linha
FROM vendas;

id	vendedor	valor	numero_linha
1	Ana	        3000	1
5	João	    3000	2
4	Maria	    1500	3
3	Ana	        200	    4
2	João	    100	    5
6	Ana	        100	    6

# RANK() - Queremos classificar os vendedores de acordo com o valor de suas 
# vendas individuais
SELECT
    vendedor,
    valor,
    RANK() OVER(
        ORDER BY valor DESC
    ) AS classificacao
FROM vendas;

vendedor	valor	classificacao
Ana	        3000	1
João	    3000	1
Maria	    1500	3
Ana	        200	    4
João	    100	    5
Ana	        100	    5

#DENSE_RANK() - Queremos classificar os vendedores de acordo com o valor de 
# suas vendas individuais sem pular posições

SELECT
    id,
    vendedor,
    produto,
    valor,
    DENSE_RANK() OVER(
        ORDER BY valor DESC
    ) AS classificacao
FROM vendas;

Valor	RANK()	DENSE_RANK()
3000	1	    1
3000	1	    1
1500	3	    2
200	    4	    3
100	    5	    4
100	    5	    4

#SUM() OVER() - Total de vendas por vendedor

SELECT
    id,
    vendedor,
    produto,
    valor,
    SUM(valor) OVER(
        PARTITION BY vendedor
    ) AS total_vendedor
FROM vendas;

vendedor	produto	   valor	total_vendedor
Ana	        Notebook	3000	3300
João	    Mouse	    100	    3100
Ana	        Teclado	    200	    3300
Maria	    Monitor	    1500	1500
João	    Notebook	3000	3100
Ana	        Mouse	    100	    3300

# Exemplo B: Soma acumulada (Running Total) - Queremos acompanhar como as vendas 
# vão acumulando ao longo dos registros.

SELECT
    id,
    vendedor,
    produto,
    valor,
    SUM(valor) OVER(
        PARTITION BY vendedor
        ORDER BY id
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS venda_acumulada
FROM vendas;

id	vendedor	valor	venda_acumulada
1	Ana	        3000	3000
2	João	    100	    100
3	Ana	        200	    3200
4	Maria	    1500	1500
5	João	    3000	3100
6	Ana	        100	    3300