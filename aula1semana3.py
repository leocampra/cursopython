nome_completo = input("Qual o nome completo ")
idade = int(input("Qual a sua idade "))
desejo = input("Crie a sua lista de desejos separando por vígula ")
produtos = ["geladeira", "tv", "videogame", "celular"]
valor = [8000,2000,5000,700]
separar_nome = nome_completo.split(' ')
print("Olá {} {}".format(separar_nome[0],separar_nome[len(separar_nome)-1]))
lista_desejo = desejo.split(', ')
for item in lista_desejo:
    if item in produtos:
        i=produtos.index(item)
        print("{} custa R${},00".format(produtos[i],valor[i]))
    if idade<=20 and item in produtos:
        print("Voce ganhou {}".format(item))