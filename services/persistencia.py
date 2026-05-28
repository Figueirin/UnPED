import json
import os
from models.produto import Produto
from models.pedido import Pedido

# Caminhos padrão para salvar os arquivos de dados na pasta data/
CAMINHO_CARDAPIO = "data/cardapio.json"
CAMINHO_PEDIDOS = "data/pedidos.json"

def salvar_cardapio(cardapio):
    """
    Grava os produtos cadastrados no cardápio no arquivo JSON.
    """
    dados = [produto.to_dict() for produto in cardapio.produtos]
    with open(CAMINHO_CARDAPIO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_cardapio(cardapio):
    """
    Lê os produtos salvos no arquivo JSON e os cadastra no cardápio ao iniciar.
    """
    if not os.path.exists(CAMINHO_CARDAPIO):
        return
    
    try:
        with open(CAMINHO_CARDAPIO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for item in dados:
                id_prod = item.get("id", len(cardapio.produtos) + 1)
                categoria = item.get("categoria", "Geral")
                produto = Produto(id_prod, item["nome"], item["preco"], categoria)
                cardapio.add_produto(produto)
    except (json.JSONDecodeError, FileNotFoundError):
        pass

def salvar_pedidos(pedidos_ativos):
    """
    Grava todas as comandas ativas na memória no arquivo JSON.
    """
    dados = [pedido.to_dict() for pedido in pedidos_ativos.values()]
    with open(CAMINHO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_pedidos(service, cardapio):
    """
    Recupera todas as comandas salvas no arquivo JSON, recria os objetos Cliente e Pedido,
    e reconstrói a associação dos itens do cardápio nas respectivas comandas.
    """
    if not os.path.exists(CAMINHO_PEDIDOS):
        return

    try:
        with open(CAMINHO_PEDIDOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

            for item_pedido in dados:
                num = item_pedido["Comanda"]
                nome_cliente = item_pedido["Cliente"]

                # 1. Abre a comanda na memória de forma controlada
                service.abrir_comanda(num, nome_cliente)
                pedido = service.buscar_comandas(num)

                # 2. Se a comanda foi instanciada, reconstrói os itens dela
                if pedido:
                    for item in item_pedido["Items"]:
                        nome_prod = item["produto"]["nome"]
                        qtd = item["quantidade"]
                        produto = cardapio.buscar_produto(nome_prod)

                        if produto:
                            pedido.adicionar_item(produto, qtd)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
