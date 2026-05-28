from models.cardapio import Cardapio
from models.produto import Produto
from services.pedido_service import PedidoService
from utils.menu import exibir_menu, obter_float, obter_inteiro, lancar_item
from services.persistencia import salvar_cardapio, carregar_cardapio, salvar_pedidos, carregar_pedidos
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
    if not cardapio.produtos:
        cardapio.add_produto(Produto("Cafe", 4.50))
        cardapio.add_produto(Produto("Pao de Queijo", 6.00))
        cardapio.add_produto(Produto("Coca-Cola", 5.50))
        cardapio.add_produto(Produto("Suco de Laranja", 7.00))
        cardapio.add_produto(Produto("Salgado Assado", 8.50))
        cardapio.add_produto(Produto("Bolo de Cenoura", 6.50))
        cardapio.add_produto(Produto("Torta de Frango", 9.00))
        cardapio.add_produto(Produto("Agua Mineral", 3.00))
        # Salva o arquivo cardapio.json inicial
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