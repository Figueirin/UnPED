from models.produto import Produto
from services.persistencia import salvar_cardapio
from services.persistencia import salvar_pedidos
def exibir_menu():
    # Desenha o menu do bar no console e captura a escolha
    print("\n UnPED - Comandas")
    print("1- Abrir Comanda")
    print("2- Adicionar item a Comanda")
    print("3- Ver extrato")
    print("4- Fechar Comanda")
    print("5- Mostrar Cardapio")
    print("6- Cadastrar Produto")
    print("7- Listar comandas abertas")
    print("0- Sair")

    opcao = input("Escolha uma Opcao ")
    return opcao

def obter_inteiro(mensagem):
    # Tratamento de erro: repete a pergunta se o usuário digitar algo que não seja um número inteiro
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
        
def obter_float(mensagem):
    # Tratamento de erro: garante a digitação correta de preços decimais (float)
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: Digite um preço/número decimal válido!")

def lancar_item(pedido, cardapio):
    # Loop interativo para lançar vários itens à comanda de uma única vez sem voltar ao menu
    while True:
        print("\n=== Cardapio ===")
        cardapio.listar_produtos()
        nome_prod = input("Digite o nome do produto que deseja: ")
        produto = cardapio.buscar_produto(nome_prod)

        if produto:
            qtd = obter_inteiro(f"Quantidade de {produto.nome}: ")
            
            if qtd <= 0:
                print("Erro: A quantidade deve ser maior que zero!")

            else:
                pedido.adicionar_item(produto, qtd)
                print(f"{qtd}x {produto.nome} adicionado(s) com sucesso!")

        else:
            print("Produto não encontrado no cardápio!")

        # Pergunta se quer continuar na mesma rotina de lançamento
        mais_itens = input("Deseja adicionar mais um item? s/n: ").strip().lower()

        if mais_itens != 's':
            break

def fluxo_abrir_comanda(service, cardapio):
    num = obter_inteiro("Numero da comanda: ")
    nome = input("Nome do cliente: ")

    if not nome.strip():
        print("O nome nao pode ser vazio")

    else:
        sucesso = service.abrir_comanda(num, nome)

        if sucesso:
            salvar_pedidos(service.pedidos_ativos)
            deseja_pedido = input("Deseja fazer mais algum pedido? s/n: ").strip().lower()

            if deseja_pedido == 's':
                pedido = service.buscar_comandas(num)
                lancar_item(pedido, cardapio)
                salvar_pedidos(service.pedidos_ativos)

def fluxo_adicionar_item(service, cardapio):
    num = obter_inteiro("Numero da Comanda: ")
    pedido = service.buscar_comandas(num)

    if pedido:
        lancar_item(pedido, cardapio)
        salvar_pedidos(service.pedidos_ativos)

    else:
        print("Comanda nao encontrada")

def fluxo_ver_extrato(service, cardapio):
    num = obter_inteiro("Numero da comanda: ")
    pedido = service.buscar_comandas(num)

    if pedido:
        print("\n" + str(pedido))

    else:
        print("Comanda nao encontrada")

def fluxo_fechar_comanda(service, cardapio):
    num = obter_inteiro("Numero da comanda para fechamento: ")
    pedido = service.fechar_comanda(num)

    if pedido:
        print("\n === Comanda Fechada com Sucesso ===")
        print(pedido)
        salvar_pedidos(service.pedidos_ativos)

    else:
        print("Comanda nao encontrada!")

def fluxo_listar_cardapio(service, cardapio):
    print("\n === Cardapio ===")
    cardapio.listar_produtos()

def fluxo_cadastrar_produto(service, cardapio):
    nome = input("Nome do produto a ser adicionado: ")

    if not nome.strip():
        print("O nome do produto nao pode ser vazio")

    else:
        preco = obter_float("Preço: ")

        if preco <= 0:
            print("O valor do produto não pode ser =< 0")

        else:
            cardapio.add_produto(Produto(nome, preco))
            salvar_cardapio(cardapio)         
            print(f"Produto {nome} cadastrada com sucesso")    

def fluxo_listar_comandas_ativas(service, cardapio):
    service.listar_comandas_ativas()