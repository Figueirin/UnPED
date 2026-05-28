import json
import os
from models.produto import Produto
from models.pedido import Pedido

# Definição dos caminhos dos arquivos JSON salvos na pasta data/
CAMINHO_CARDAPIO = "data/cardapio.json"
CAMINHO_PEDIDOS = "data/pedidos.json"

def salvar_cardapio(cardapio):
    """
    Grava de forma persistente todos os produtos atuais do cardápio em um arquivo JSON.
    Recria o arquivo a cada salvamento para manter os dados sincronizados.
    """
    dados = [produto.to_dict() for produto in cardapio.produtos]
    with open(CAMINHO_CARDAPIO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_cardapio(cardapio):
    """
    Lê os produtos gravados no arquivo JSON e os cadastra na memória ao iniciar o sistema.
    Possui fallbacks (tratamentos) de segurança para manter a compatibilidade com arquivos JSON antigos.
    """
    if not os.path.exists(CAMINHO_CARDAPIO):
        return
    
    try:
        with open(CAMINHO_CARDAPIO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for item in dados:
                # O método .get garante compatibilidade caso falte alguma propriedade no arquivo antigo
                id_prod = item.get("id", len(cardapio.produtos) + 1)
                categoria = item.get("categoria", "Geral")
                
                # Instancia e registra o produto na memória
                produto = Produto(id_prod, item["nome"], item["preco"], categoria)
                cardapio.add_produto(produto)
    except (json.JSONDecodeError, FileNotFoundError):
        # Ignora erros de leitura ou arquivo vazio para não quebrar a inicialização do programa
        pass

def salvar_pedidos(pedidos_ativos):
    """
    Salva a lista de comandas abertas ativas na memória no arquivo de pedidos JSON.
    """
    dados = [pedido.to_dict() for pedido in pedidos_ativos.values()]
    with open(CAMINHO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_pedidos(service, cardapio):
    """
    Carrega as comandas ativas salvas no arquivo JSON de volta para a memória RAM.
    Reconstrói os relacionamentos (Objetos Clientes, Pedidos e seus respectivos PedidosItens associados).
    """
    if not os.path.exists(CAMINHO_PEDIDOS):
        return

    try:
        with open(CAMINHO_PEDIDOS, "r", encoding="utf-8") as f:
            dados = json.load(f)

            for item_pedido in dados:
                num = item_pedido["Comanda"]
                nome_cliente = item_pedido["Cliente"]

                # 1. Abre novamente a comanda na memória RAM
                service.abrir_comanda(num, nome_cliente)
                pedido = service.buscar_comandas(num)

                # 2. Se a comanda abriu com sucesso, reconstrói seus itens de consumo
                if pedido:
                    for item in item_pedido["Items"]:
                        nome_prod = item["produto"]["nome"]
                        qtd = item["quantidade"]
                        # Busca o produto correspondente no cardápio carregado
                        produto = cardapio.buscar_produto(nome_prod)

                        if produto:
                            # Re-vincula o produto e quantidade à comanda
                            pedido.adicionar_item(produto, qtd)
    except (json.JSONDecodeError, FileNotFoundError):
        # Passa reto em caso de arquivo vazio ou corrompido
        pass
