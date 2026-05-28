from models.cardapio import Cardapio
from models.produto import Produto
from services.pedido_service import PedidoService
from utils.menu import exibir_menu
from services.persistencia import salvar_cardapio, carregar_cardapio, carregar_pedidos
from utils.menu import (
    fluxo_listar_comandas_ativas,
    fluxo_cadastrar_produto,
    fluxo_listar_cardapio,
    fluxo_fechar_comanda,
    fluxo_ver_extrato,
    fluxo_adicionar_item,
    fluxo_abrir_comanda
)

def main():
    # Instanciamos os gerenciadores globais (Serviços e Cardápio da loja)
    service = PedidoService()
    cardapio = Cardapio()

    # Carrega o cardápio do arquivo JSON
    carregar_cardapio(cardapio)

    # Carga inicial do Cardápio (produtos de demonstração caso esteja vazio na primeira execução)
        # Carga inicial do Cardápio com IDs e Categorias
    if not cardapio.produtos:
        cardapio.add_produto(Produto(1, "Cafe", 4.50, "Bebidas Quentes"))
        cardapio.add_produto(Produto(2, "Pao de Queijo", 6.00, "Salgados"))
        cardapio.add_produto(Produto(3, "Coca-Cola", 5.50, "Bebidas Frias"))
        cardapio.add_produto(Produto(4, "Suco de Laranja", 7.00, "Bebidas Frias"))
        cardapio.add_produto(Produto(5, "Salgado Assado", 8.50, "Salgados"))
        cardapio.add_produto(Produto(6, "Bolo de Cenoura", 6.50, "Sobremesas"))
        cardapio.add_produto(Produto(7, "Torta de Frango", 9.00, "Salgados"))
        cardapio.add_produto(Produto(8, "Agua Mineral", 3.00, "Bebidas Frias"))
        salvar_cardapio(cardapio)


    carregar_pedidos(service, cardapio)
    

    acoes = {
        "1": fluxo_abrir_comanda,
        "2": fluxo_adicionar_item,
        "3": fluxo_ver_extrato,
        "4": fluxo_fechar_comanda,
        "5": fluxo_listar_cardapio,
        "6": fluxo_cadastrar_produto,
        "7": fluxo_listar_comandas_ativas
    }

    while True:
        opcao = exibir_menu()

        if opcao == '0':
            print("Encerrando Sistema...")
            break

        elif opcao in acoes:
            acoes[opcao](service, cardapio)

        else:
            print("Opção invalida, tente novamente")

if __name__ == "__main__":
    main()